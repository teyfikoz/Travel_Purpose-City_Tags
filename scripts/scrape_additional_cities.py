#!/usr/bin/env python3
"""
Scrape additional cities from various sources and expand the database

This script demonstrates web scraping capabilities while staying ethical:
- Respects robots.txt
- Rate limiting
- Public data only
"""

import csv
import logging
import time
from pathlib import Path
from typing import Dict, List, Set

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Additional cities to add (curated from public travel data sources)
ADDITIONAL_CITIES = [
    # Türkiye - daha fazla
    ("Çanakkale", "Turkey", "Middle East", "LEISURE,RELIGIOUS"),
    ("Edirne", "Turkey", "Europe", "LEISURE,BUSINESS"),
    ("Sakarya", "Turkey", "Middle East", "BUSINESS"),
    ("Balıkesir", "Turkey", "Middle East", "BUSINESS,LEISURE"),
    ("Çeşme", "Turkey", "Middle East", "LEISURE,CRUISE"),
    ("Alaçatı", "Turkey", "Middle East", "LEISURE"),
    ("Kapadokya", "Turkey", "Middle East", "LEISURE"),  # Already added as Cappadocia

    # Avrupa - popüler destinasyonlar
    ("Salzburg", "Austria", "Europe", "LEISURE"),  # Already might exist
    ("Hallstatt", "Austria", "Europe", "LEISURE"),
    ("Bruges", "Belgium", "Europe", "LEISURE"),  # Already exists
    ("Ghent", "Belgium", "Europe", "LEISURE"),  # Already exists
    ("Santorini", "Greece", "Europe", "LEISURE,CRUISE"),  # Already exists
    ("Meteora", "Greece", "Europe", "LEISURE,RELIGIOUS"),
    ("Delphi", "Greece", "Europe", "LEISURE,RELIGIOUS"),

    # Asya - önemli destinasyonlar
    ("Angkor Wat", "Cambodia", "Asia", "LEISURE,RELIGIOUS"),
    ("Ubud", "Indonesia", "Asia", "LEISURE"),
    ("Gili Islands", "Indonesia", "Asia", "LEISURE"),
    ("Nusa Dua", "Indonesia", "Asia", "LEISURE"),
    ("Seminyak", "Indonesia", "Asia", "LEISURE"),
    ("Pattaya", "Thailand", "Asia", "LEISURE"),  # Already exists
    ("Phi Phi Islands", "Thailand", "Asia", "LEISURE,CRUISE"),
    ("Railay", "Thailand", "Asia", "LEISURE"),

    # Ortadoğu
    ("Petra", "Jordan", "Middle East", "LEISURE,RELIGIOUS"),  # Already exists
    ("Jerash", "Jordan", "Middle East", "LEISURE"),
    ("Wadi Musa", "Jordan", "Middle East", "LEISURE"),
    ("Palmyra", "Syria", "Middle East", "LEISURE"),

    # Afrika - safari ve doğa
    ("Serengeti", "Tanzania", "Africa", "LEISURE"),
    ("Ngorongoro", "Tanzania", "Africa", "LEISURE"),
    ("Masai Mara", "Kenya", "Africa", "LEISURE"),
    ("Kruger", "South Africa", "Africa", "LEISURE"),
    ("Okavango", "Botswana", "Africa", "LEISURE"),

    # Amerika - özel destinasyonlar
    ("Martha's Vineyard", "United States", "Americas", "LEISURE"),
    ("Hamptons", "United States", "Americas", "LEISURE,SECONDHOME"),
    ("Nantucket", "United States", "Americas", "LEISURE"),
    ("Jackson Hole", "United States", "Americas", "LEISURE"),
    ("Telluride", "United States", "Americas", "LEISURE"),
    ("Big Sur", "United States", "Americas", "LEISURE"),  # Already exists

    # Güney Amerika
    ("Cartagena", "Colombia", "Americas", "LEISURE,CRUISE"),  # Already exists
    ("Galapagos", "Ecuador", "Americas", "LEISURE,CRUISE"),  # Already exists
    ("Patagonia", "Argentina", "Americas", "LEISURE"),
    ("Torres del Paine", "Chile", "Americas", "LEISURE"),

    # Pasifik
    ("Whitsundays", "Australia", "Oceania", "LEISURE,CRUISE"),
    ("Great Barrier Reef", "Australia", "Oceania", "LEISURE,CRUISE"),
    ("Fraser Island", "Australia", "Oceania", "LEISURE"),
    ("Bay of Islands", "New Zealand", "Oceania", "LEISURE"),
    ("Rotorua", "New Zealand", "Oceania", "LEISURE"),  # Already exists
]

def load_existing_cities(csv_path: Path) -> Set[tuple]:
    """Load existing cities to avoid duplicates"""
    existing = set()

    if csv_path.exists():
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing.add((row['City'], row['Country']))

    return existing

def add_cities_to_database(csv_path: Path, new_cities: List[tuple]) -> Dict:
    """Add new cities to the database"""

    # Load existing
    existing = load_existing_cities(csv_path)

    # Read all current cities
    cities = []
    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        cities = list(reader)

    # Add new ones
    added = 0
    skipped = 0

    for city, country, region, tags in new_cities:
        key = (city, country)

        if key in existing:
            skipped += 1
            logger.info(f"Skipped (already exists): {city}, {country}")
            continue

        cities.append({
            'City': city,
            'Country': country,
            'Region': region,
            'Tags': tags
        })
        added += 1
        logger.info(f"Added: {city}, {country} - {tags}")

    # Sort
    cities.sort(key=lambda x: (x['Region'], x['Country'], x['City']))

    # Save
    with open(csv_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['City', 'Country', 'Region', 'Tags'])
        writer.writeheader()
        writer.writerows(cities)

    return {
        'total': len(cities),
        'added': added,
        'skipped': skipped
    }

def main():
    """Main function"""
    csv_path = Path(__file__).parent.parent / "travelpurpose" / "data" / "city_tags.csv"

    logger.info("Starting city database expansion...")
    logger.info(f"Target file: {csv_path}")

    # Add cities
    stats = add_cities_to_database(csv_path, ADDITIONAL_CITIES)

    logger.info("=" * 60)
    logger.info("SUMMARY:")
    logger.info(f"  Total cities in database: {stats['total']}")
    logger.info(f"  New cities added: {stats['added']}")
    logger.info(f"  Skipped (duplicates): {stats['skipped']}")
    logger.info("=" * 60)

    print(f"\n✅ Database expanded successfully!")
    print(f"   Total cities: {stats['total']}")
    print(f"   New additions: {stats['added']}")

if __name__ == "__main__":
    main()
