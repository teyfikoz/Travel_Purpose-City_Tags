"""
Simple City Tags Module
Provides a lightweight tag system for cities with 7 main categories:
BUSINESS, LEISURE, SEAMAN, CRUISE, SECONDHOME, MEDICAL, RELIGIOUS
"""

import csv
import logging
from pathlib import Path
from typing import Dict, List, Optional, Set

import pandas as pd

logger = logging.getLogger(__name__)

# Define simple tags
SIMPLE_TAGS = [
    "BUSINESS",
    "LEISURE",
    "SEAMAN",
    "CRUISE",
    "SECONDHOME",
    "MEDICAL",
    "RELIGIOUS"
]

# Mapping from complex ontology to simple tags
ONTOLOGY_TO_SIMPLE = {
    "Business": "BUSINESS",
    "Finance_Hub": "BUSINESS",
    "Tech_Hub": "BUSINESS",
    "MICE_Convention": "BUSINESS",
    "HQ_Density": "BUSINESS",
    "Logistics_Hub": "BUSINESS",
    "Trade_Fair_City": "BUSINESS",
    "Startup_Ecosystem": "BUSINESS",
    "Air_Cargo_Hub": "BUSINESS",

    "Leisure": "LEISURE",
    "City_Break": "LEISURE",
    "Luxury": "LEISURE",
    "Backpacker": "LEISURE",
    "Shopping": "LEISURE",
    "Gastronomy": "LEISURE",
    "Wellness_Spa": "LEISURE",
    "Romantic": "LEISURE",
    "Eco_Tourism": "LEISURE",
    "Culture_Heritage": "LEISURE",
    "UNESCO_Site": "LEISURE",
    "Museums": "LEISURE",
    "Old_Town": "LEISURE",
    "Architecture": "LEISURE",
    "Beach_Resort": "LEISURE",
    "Beachfront": "LEISURE",
    "Island": "LEISURE",
    "Diving_Spots": "LEISURE",
    "All_Inclusive": "LEISURE",
    "Marina": "LEISURE",
    "Surf": "LEISURE",
    "Adventure_Nature": "LEISURE",
    "Trekking": "LEISURE",
    "Safari": "LEISURE",
    "Family": "LEISURE",
    "Theme_Park": "LEISURE",
    "Zoo_Aquarium": "LEISURE",
    "Winter_Snow": "LEISURE",
    "Ski_Resort": "LEISURE",
    "Nightlife_Entertainment": "LEISURE",
    "Party_District": "LEISURE",
    "Casinos": "LEISURE",

    "Seaman_Crew": "SEAMAN",
    "Crew_Change_Port": "SEAMAN",
    "Shipyards": "SEAMAN",
    "Port_Access": "SEAMAN",
    "Seamen_Clinics": "SEAMAN",

    "Transit_Gateway": "CRUISE",
    "Mega_Air_Hub": "CRUISE",
    "Regional_Hub": "CRUISE",
    "Crew_Change_Friendly": "CRUISE",

    "Medical_Health": "MEDICAL",
    "Cosmetic_Surgery": "MEDICAL",
    "Dental": "MEDICAL",
    "IVF": "MEDICAL",
    "Orthopedic": "MEDICAL",
    "Cardiology": "MEDICAL",
    "Oncology": "MEDICAL",
    "Ophthalmology": "MEDICAL",
    "Rehabilitation": "MEDICAL",
    "Thermal_Spa": "MEDICAL",

    "Religious_Pilgrimage": "RELIGIOUS",
    "Islamic_Pilgrimage": "RELIGIOUS",
    "Christian_Pilgrimage": "RELIGIOUS",
    "Buddhist_Pilgrimage": "RELIGIOUS",
    "Hindu_Pilgrimage": "RELIGIOUS",
    "Shia_Pilgrimage": "RELIGIOUS",
    "Sufi_Shrines": "RELIGIOUS",
}


class SimpleCityTags:
    """Manages simple city tags system"""

    def __init__(self, data_path: Optional[Path] = None):
        """
        Initialize SimpleCityTags

        Args:
            data_path: Path to city_tags.csv file
        """
        if data_path is None:
            data_path = Path(__file__).parent / "data" / "city_tags.csv"

        self.data_path = Path(data_path)
        self._data: Optional[pd.DataFrame] = None

    def load(self) -> pd.DataFrame:
        """Load city tags from CSV"""
        if self.data_path.exists():
            self._data = pd.read_csv(self.data_path)
            logger.info(f"Loaded {len(self._data)} cities from {self.data_path}")
        else:
            self._data = pd.DataFrame(columns=["City", "Country", "Region", "Tags"])
            logger.warning(f"City tags file not found: {self.data_path}")

        return self._data

    def save(self, df: pd.DataFrame):
        """Save city tags to CSV"""
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(self.data_path, index=False)
        logger.info(f"Saved {len(df)} cities to {self.data_path}")

    def get_city_tags(self, city: str, country: Optional[str] = None) -> List[str]:
        """
        Get tags for a specific city

        Args:
            city: City name
            country: Optional country name for disambiguation

        Returns:
            List of tags for the city
        """
        if self._data is None:
            self.load()

        # Search for city
        mask = self._data["City"].str.lower() == city.lower()
        if country:
            mask &= self._data["Country"].str.lower() == country.lower()

        matches = self._data[mask]
        if len(matches) == 0:
            logger.warning(f"City not found: {city}")
            return []

        tags_str = matches.iloc[0]["Tags"]
        return [tag.strip() for tag in tags_str.split(",")]

    def add_city(self, city: str, country: str, region: str, tags: List[str]):
        """
        Add or update a city with tags

        Args:
            city: City name
            country: Country name
            region: Region (Europe, Asia, Africa, Americas, Middle East, Oceania)
            tags: List of tags (max 3)
        """
        if self._data is None:
            self.load()

        # Validate tags
        tags = tags[:3]  # Max 3 tags
        for tag in tags:
            if tag not in SIMPLE_TAGS:
                raise ValueError(f"Invalid tag: {tag}. Must be one of {SIMPLE_TAGS}")

        # Check if city exists
        mask = (self._data["City"].str.lower() == city.lower()) & \
               (self._data["Country"].str.lower() == country.lower())

        tags_str = ",".join(tags)

        if mask.any():
            # Update existing city
            self._data.loc[mask, "Tags"] = tags_str
            logger.info(f"Updated {city}, {country}: {tags_str}")
        else:
            # Add new city
            new_row = pd.DataFrame([{
                "City": city,
                "Country": country,
                "Region": region,
                "Tags": tags_str
            }])
            self._data = pd.concat([self._data, new_row], ignore_index=True)
            logger.info(f"Added {city}, {country}: {tags_str}")

    def get_statistics(self) -> Dict:
        """
        Get statistics about the city tags dataset

        Returns:
            Dictionary with statistics
        """
        if self._data is None:
            self.load()

        # Count by region
        region_counts = self._data["Region"].value_counts().to_dict()

        # Count tag usage
        tag_counts = {}
        for tag in SIMPLE_TAGS:
            tag_counts[tag] = self._data["Tags"].str.contains(tag, case=False, na=False).sum()

        # Tags per city distribution
        self._data["tag_count"] = self._data["Tags"].str.split(",").str.len()

        return {
            "total_cities": len(self._data),
            "regions": region_counts,
            "tag_usage": tag_counts,
            "avg_tags_per_city": self._data["tag_count"].mean(),
            "max_tags_per_city": self._data["tag_count"].max(),
        }

    def search_by_tag(self, tag: str) -> pd.DataFrame:
        """
        Search cities by tag

        Args:
            tag: Tag to search for

        Returns:
            DataFrame of cities with the tag
        """
        if self._data is None:
            self.load()

        if tag not in SIMPLE_TAGS:
            raise ValueError(f"Invalid tag: {tag}. Must be one of {SIMPLE_TAGS}")

        mask = self._data["Tags"].str.contains(tag, case=False, na=False)
        return self._data[mask]

    def export_by_region(self, output_dir: Path):
        """
        Export separate CSV files for each region

        Args:
            output_dir: Directory to save region files
        """
        if self._data is None:
            self.load()

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        for region in self._data["Region"].unique():
            region_df = self._data[self._data["Region"] == region]
            output_path = output_dir / f"{region.lower()}_cities.csv"
            region_df.to_csv(output_path, index=False)
            logger.info(f"Exported {len(region_df)} cities to {output_path}")


def convert_ontology_to_simple(main_categories: List[str]) -> Set[str]:
    """
    Convert complex ontology categories to simple tags

    Args:
        main_categories: List of main category names from ontology

    Returns:
        Set of simple tags
    """
    simple_tags = set()

    for category in main_categories:
        if category in ONTOLOGY_TO_SIMPLE:
            simple_tags.add(ONTOLOGY_TO_SIMPLE[category])

    # Limit to max 3 tags
    if len(simple_tags) > 3:
        # Prioritize: BUSINESS > MEDICAL > RELIGIOUS > SEAMAN > CRUISE > LEISURE > SECONDHOME
        priority = ["BUSINESS", "MEDICAL", "RELIGIOUS", "SEAMAN", "CRUISE", "LEISURE", "SECONDHOME"]
        sorted_tags = sorted(simple_tags, key=lambda x: priority.index(x) if x in priority else 999)
        simple_tags = set(sorted_tags[:3])

    return simple_tags
