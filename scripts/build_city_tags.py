#!/usr/bin/env python3
"""
Build comprehensive city_tags.csv from multiple sources

This script:
1. Fetches major cities from Wikidata (population > 100K)
2. Harvests tags from travel platforms
3. Converts to simple tag system
4. Generates city_tags.csv with full coverage
"""

import argparse
import logging
from pathlib import Path
import time
from typing import Dict, List, Set

import pandas as pd
from tqdm import tqdm

from travelpurpose.simple_tags import SimpleCityTags, SIMPLE_TAGS, convert_ontology_to_simple
from travelpurpose.utils.wikidata import WikidataClient
from travelpurpose.utils.booking import BookingHarvester
from travelpurpose.utils.agoda import AgodaHarvester
from travelpurpose.utils.harvest import HarvestConfig

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Region mapping
REGION_MAP = {
    "Europe": ["France", "Germany", "Italy", "Spain", "United Kingdom", "Netherlands", "Belgium",
               "Switzerland", "Austria", "Poland", "Czech Republic", "Portugal", "Greece", "Sweden",
               "Denmark", "Norway", "Finland", "Ireland", "Croatia", "Romania", "Hungary", "Bulgaria",
               "Serbia", "Slovakia", "Slovenia", "Estonia", "Latvia", "Lithuania", "Iceland", "Luxembourg"],

    "Asia": ["China", "Japan", "South Korea", "India", "Thailand", "Singapore", "Malaysia", "Indonesia",
             "Philippines", "Vietnam", "Taiwan", "Hong Kong", "Cambodia", "Laos", "Myanmar", "Bangladesh",
             "Sri Lanka", "Nepal", "Mongolia", "Brunei", "Macao", "Bhutan", "Maldives"],

    "Middle East": ["United Arab Emirates", "Saudi Arabia", "Qatar", "Kuwait", "Bahrain", "Oman",
                    "Turkey", "Israel", "Jordan", "Lebanon", "Iraq", "Iran", "Yemen", "Syria", "Palestine"],

    "Africa": ["South Africa", "Egypt", "Morocco", "Kenya", "Nigeria", "Ghana", "Tanzania", "Ethiopia",
               "Tunisia", "Algeria", "Uganda", "Senegal", "Rwanda", "Botswana", "Namibia", "Mauritius",
               "Seychelles", "Zambia", "Zimbabwe", "Madagascar", "Mozambique", "Cameroon", "Ivory Coast"],

    "Americas": ["United States", "Canada", "Mexico", "Brazil", "Argentina", "Chile", "Colombia",
                 "Peru", "Ecuador", "Venezuela", "Uruguay", "Paraguay", "Bolivia", "Costa Rica",
                 "Panama", "Guatemala", "Dominican Republic", "Cuba", "Jamaica", "Bahamas", "Trinidad and Tobago"],

    "Oceania": ["Australia", "New Zealand", "Fiji", "Papua New Guinea", "Samoa", "Tonga", "Vanuatu",
                "Solomon Islands", "French Polynesia", "New Caledonia", "Guam"]
}


def get_region_for_country(country: str) -> str:
    """Get region for a country"""
    for region, countries in REGION_MAP.items():
        if country in countries:
            return region
    return "Other"


def determine_simple_tags(city_name: str, country: str, wikidata_categories: List[str]) -> List[str]:
    """
    Determine simple tags for a city based on various signals

    Args:
        city_name: City name
        country: Country name
        wikidata_categories: Categories from Wikidata

    Returns:
        List of simple tags (max 3)
    """
    tags = set()

    # Convert city name to lower for matching
    city_lower = city_name.lower()

    # Business hubs (capitals, major cities)
    business_keywords = ["capital", "financial", "business", "tech", "silicon", "startup"]
    major_business_cities = [
        "london", "new york", "tokyo", "singapore", "hong kong", "dubai", "shanghai",
        "paris", "frankfurt", "zurich", "milan", "amsterdam", "sydney", "toronto",
        "san francisco", "los angeles", "chicago", "boston", "seattle", "austin",
        "bangalore", "mumbai", "delhi", "beijing", "seoul", "taipei", "kuala lumpur",
        "bangkok", "jakarta", "manila", "istanbul", "moscow", "warsaw", "prague",
        "vienna", "munich", "barcelona", "madrid", "lisbon", "dublin", "copenhagen"
    ]

    if any(city_lower == city for city in major_business_cities):
        tags.add("BUSINESS")
    elif any(keyword in " ".join(wikidata_categories).lower() for keyword in business_keywords):
        tags.add("BUSINESS")

    # Seaman/Port cities
    seaman_keywords = ["port", "harbor", "harbour", "maritime", "naval", "shipyard", "seaport"]
    major_ports = [
        "rotterdam", "hamburg", "antwerp", "singapore", "hong kong", "shanghai", "busan",
        "dubai", "jebel ali", "klaipeda", "gdansk", "piraeus", "istanbul", "izmir",
        "valencia", "barcelona", "marseille", "genoa", "naples", "trieste", "koper",
        "constanta", "odessa", "novorossiysk", "varna", "burgas", "alexandria",
        "port said", "mombasa", "dar es salaam", "durban", "cape town", "lagos",
        "manila", "jakarta", "mumbai", "chennai", "colombo", "karachi", "ho chi minh",
        "vancouver", "seattle", "los angeles", "long beach", "miami", "houston",
        "santos", "buenos aires", "valparaiso", "callao"
    ]

    if any(city_lower == port for port in major_ports):
        tags.add("SEAMAN")
    elif any(keyword in " ".join(wikidata_categories).lower() for keyword in seaman_keywords):
        tags.add("SEAMAN")

    # Medical tourism hubs
    medical_keywords = ["medical", "health", "hospital", "clinic", "surgery", "dental", "ivf"]
    medical_hubs = [
        "bangkok", "singapore", "kuala lumpur", "seoul", "taipei", "dubai", "istanbul",
        "mumbai", "delhi", "chennai", "bangalore", "bangkok", "antalya", "izmir",
        "budapest", "prague", "warsaw", "mexico city", "cancun", "san jose",
        "medellin", "bogota", "buenos aires", "santiago", "sao paulo", "rio de janeiro",
        "nairobi", "johannesburg", "cairo", "tunis", "marrakech", "casablanca",
        "manila", "phuket", "penang", "hanoi", "ho chi minh"
    ]

    if any(city_lower == hub for hub in medical_hubs):
        tags.add("MEDICAL")
    elif any(keyword in " ".join(wikidata_categories).lower() for keyword in medical_keywords):
        tags.add("MEDICAL")

    # Religious pilgrimage sites
    religious_keywords = ["pilgrimage", "religious", "holy", "sacred", "mosque", "church",
                         "temple", "shrine", "cathedral", "hajj", "umrah", "mecca", "medina"]
    religious_cities = [
        "mecca", "medina", "jerusalem", "vatican", "rome", "santiago de compostela",
        "lourdes", "fatima", "varanasi", "amritsar", "bodh gaya", "lumbini", "kathmandu",
        "bangkok", "kyoto", "nara", "istanbul", "konya", "mashhad", "qom", "najaf",
        "karbala", "shiraz", "trabzon", "sivas", "bursa"
    ]

    if any(city_lower == rcity for rcity in religious_cities):
        tags.add("RELIGIOUS")
    elif any(keyword in " ".join(wikidata_categories).lower() for keyword in religious_keywords):
        tags.add("RELIGIOUS")

    # Cruise destinations
    cruise_keywords = ["cruise", "port of call", "cruise terminal", "ferry"]
    cruise_destinations = [
        "miami", "fort lauderdale", "barcelona", "venice", "dubrovnik", "athens",
        "istanbul", "naples", "rome", "marseille", "monaco", "nice", "cannes",
        "split", "kotor", "santorini", "mykonos", "rhodes", "crete", "malta",
        "palma", "ibiza", "funchal", "reykjavik", "bergen", "oslo", "stockholm",
        "helsinki", "tallinn", "st petersburg", "riga", "copenhagen", "tallinn",
        "vancouver", "seattle", "juneau", "ketchikan", "sitka", "anchorage",
        "sydney", "auckland", "fiji", "papeete", "singapore", "phuket", "bali",
        "dubai", "muscat", "doha", "abu dhabi", "mombasa", "zanzibar", "seychelles"
    ]

    if any(city_lower == dest for dest in cruise_destinations):
        tags.add("CRUISE")
    elif any(keyword in " ".join(wikidata_categories).lower() for keyword in cruise_keywords):
        tags.add("CRUISE")

    # Leisure (default for tourist cities)
    leisure_keywords = ["tourism", "tourist", "resort", "beach", "culture", "heritage",
                       "unesco", "museum", "attraction", "vacation", "holiday"]

    if any(keyword in " ".join(wikidata_categories).lower() for keyword in leisure_keywords):
        tags.add("LEISURE")

    # If no specific tags, check if it's a popular tourist destination
    tourist_destinations = [
        "paris", "london", "rome", "barcelona", "amsterdam", "venice", "florence",
        "prague", "vienna", "budapest", "krakow", "lisbon", "porto", "seville",
        "granada", "munich", "berlin", "athens", "santorini", "mykonos", "dubrovnik",
        "new york", "san francisco", "las vegas", "los angeles", "miami", "orlando",
        "cancun", "playa del carmen", "cabo", "punta cana", "cartagena", "rio",
        "buenos aires", "cusco", "machu picchu", "lima", "santiago", "valparaiso",
        "tokyo", "kyoto", "osaka", "bangkok", "phuket", "bali", "singapore",
        "hong kong", "shanghai", "beijing", "dubai", "abu dhabi", "doha", "muscat",
        "marrakech", "cairo", "cape town", "johannesburg", "nairobi", "zanzibar",
        "sydney", "melbourne", "auckland", "queenstown", "fiji"
    ]

    if any(city_lower == dest for dest in tourist_destinations) and len(tags) == 0:
        tags.add("LEISURE")

    # Ensure at least one tag
    if len(tags) == 0:
        tags.add("LEISURE")

    # Prioritize and limit to 3 tags
    priority = ["BUSINESS", "MEDICAL", "RELIGIOUS", "SEAMAN", "CRUISE", "LEISURE", "SECONDHOME"]
    sorted_tags = sorted(tags, key=lambda x: priority.index(x) if x in priority else 999)

    return sorted_tags[:3]


def build_city_tags_database(
    min_population: int = 100000,
    max_cities: int = 2000,
    output_path: Path = None
) -> pd.DataFrame:
    """
    Build comprehensive city tags database

    Args:
        min_population: Minimum city population
        max_cities: Maximum number of cities to process
        output_path: Path to save city_tags.csv

    Returns:
        DataFrame with city tags
    """
    logger.info(f"Building city tags database (min_pop={min_population}, max={max_cities})")

    if output_path is None:
        output_path = Path(__file__).parent.parent / "travelpurpose" / "data" / "city_tags.csv"

    # Initialize Wikidata client
    wikidata_client = WikidataClient(rate_limit=1.0)

    # Fetch cities from Wikidata
    logger.info("Fetching cities from Wikidata...")
    cities = wikidata_client.get_cities_by_population(min_population=min_population, limit=max_cities)
    logger.info(f"Fetched {len(cities)} cities from Wikidata")

    # Build city tags
    city_data = []

    for city in tqdm(cities, desc="Processing cities"):
        city_name = city.get("name", "")
        country = city.get("country", "")
        wikidata_id = city.get("wikidata_id", "")

        if not city_name or not country:
            continue

        # Get region
        region = get_region_for_country(country)

        # Get Wikidata categories
        try:
            categories = wikidata_client.get_city_categories(wikidata_id)
        except Exception as e:
            logger.warning(f"Failed to get categories for {city_name}: {e}")
            categories = []

        # Determine tags
        tags = determine_simple_tags(city_name, country, categories)

        city_data.append({
            "City": city_name,
            "Country": country,
            "Region": region,
            "Tags": ",".join(tags)
        })

        # Rate limiting
        time.sleep(0.5)

    # Create DataFrame
    df = pd.DataFrame(city_data)

    # Sort by region and city
    df = df.sort_values(["Region", "Country", "City"]).reset_index(drop=True)

    # Save to CSV
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    logger.info(f"Saved {len(df)} cities to {output_path}")

    # Print statistics
    stats = SimpleCityTags(output_path).get_statistics()
    logger.info(f"\n=== City Tags Statistics ===")
    logger.info(f"Total cities: {stats['total_cities']}")
    logger.info(f"Regions: {stats['regions']}")
    logger.info(f"Tag usage: {stats['tag_usage']}")
    logger.info(f"Avg tags per city: {stats['avg_tags_per_city']:.2f}")

    return df


def main():
    parser = argparse.ArgumentParser(description="Build city tags database")
    parser.add_argument("--min-population", type=int, default=100000,
                       help="Minimum city population (default: 100000)")
    parser.add_argument("--max-cities", type=int, default=2000,
                       help="Maximum number of cities (default: 2000)")
    parser.add_argument("--output", type=Path, default=None,
                       help="Output CSV file path")
    parser.add_argument("--verbose", action="store_true",
                       help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    build_city_tags_database(
        min_population=args.min_population,
        max_cities=args.max_cities,
        output_path=args.output
    )


if __name__ == "__main__":
    main()
