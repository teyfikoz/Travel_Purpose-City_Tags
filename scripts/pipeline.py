#!/usr/bin/env python3
"""
Main data pipeline for TravelPurpose.

Orchestrates:
1. Loading and cleaning NBD.xlsx (if available)
2. Fetching canonical city data from Wikidata
3. Harvesting tags from public sources
4. Normalizing and merging data
5. Classification using hybrid approach
6. Exporting to parquet and JSON
"""

import argparse
import logging
import os
import sys
import time
from pathlib import Path
from typing import List, Optional

import pandas as pd
from tqdm import tqdm

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from travelpurpose.utils.agoda import AgodaHarvester
from travelpurpose.utils.booking import BookingHarvester
from travelpurpose.utils.geonames import GeoNamesHarvester
from travelpurpose.utils.harvest import HarvestConfig
from travelpurpose.utils.io import (
    get_package_dir,
    load_nbd_excel,
    load_nbd_mapping,
    load_ontology,
    save_cities_data,
)
from travelpurpose.utils.kayak import KayakHarvester
from travelpurpose.utils.normalize import deduplicate_cities
from travelpurpose.utils.opentripmap import OpenTripMapHarvester
from travelpurpose.utils.restcountries import RestCountriesClient
from travelpurpose.utils.scoring import (
    aggregate_scores_by_category,
    calculate_confidence,
    calculate_tag_weights,
    merge_nbd_purposes,
    normalize_scores,
    select_top_labels,
)
from travelpurpose.utils.skyscanner import SkyscannerHarvester
from travelpurpose.utils.tripdotcom import TripDotComHarvester
from travelpurpose.utils.trivago import TrivagoHarvester
from travelpurpose.utils.wikidata import WikidataClient, fetch_canonical_cities

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def load_nbd_data(nbd_path: Optional[str] = None) -> pd.DataFrame:
    """
    Load and clean NBD.xlsx data.

    Args:
        nbd_path: Path to NBD.xlsx file

    Returns:
        Cleaned DataFrame
    """
    logger.info("Step 1: Loading NBD data...")

    if nbd_path and os.path.exists(nbd_path):
        df = load_nbd_excel(nbd_path)
        if df is not None:
            logger.info(f"Loaded {len(df)} rows from NBD.xlsx")
            # Basic cleaning
            if "CITY" in df.columns:
                df.rename(columns={"CITY": "name"}, inplace=True)
            if "COUNTRY" in df.columns:
                df.rename(columns={"COUNTRY": "country"}, inplace=True)
            if "PURPOSE" in df.columns:
                df.rename(columns={"PURPOSE": "purpose"}, inplace=True)

            df.dropna(subset=["name"], inplace=True)
            logger.info(f"Cleaned to {len(df)} cities with valid names")
            return df
    else:
        logger.warning(f"NBD file not found at: {nbd_path}")

    return pd.DataFrame()


def fetch_wikidata_cities(min_population: int = 100000) -> pd.DataFrame:
    """
    Fetch canonical city data from Wikidata.

    Args:
        min_population: Minimum population threshold

    Returns:
        DataFrame with city data
    """
    logger.info(f"Step 2: Fetching cities from Wikidata (pop >= {min_population})...")

    cache_file = str(get_package_dir() / "data" / "wikidata_cities_cache.json")
    cities = fetch_canonical_cities(min_population=min_population, cache_file=cache_file)

    df = pd.DataFrame(cities)
    logger.info(f"Fetched {len(df)} cities from Wikidata")

    # Fetch UNESCO sites
    logger.info("Fetching UNESCO World Heritage sites...")
    client = WikidataClient(rate_limit=1.5)
    unesco_sites = client.get_unesco_sites()

    if unesco_sites:
        logger.info(f"Found {len(unesco_sites)} UNESCO sites")
        # Add as separate tag source
        # This will be merged in tag harvesting phase

    return df


def harvest_tags_for_cities(cities_df: pd.DataFrame, sample_size: Optional[int] = None) -> pd.DataFrame:
    """
    Harvest tags for cities from all sources.

    Args:
        cities_df: DataFrame with cities
        sample_size: Optional sample size for testing (None = all cities)

    Returns:
        DataFrame with added tags column
    """
    logger.info("Step 3: Harvesting tags from public sources...")

    if sample_size:
        cities_df = cities_df.head(sample_size).copy()  # Use .copy() to avoid SettingWithCopyWarning
        logger.info(f"Sampling {sample_size} cities for testing")

    config = HarvestConfig(rate_limit=1.5)

    # Initialize harvesters (including new sources)
    harvesters = {
        "booking": BookingHarvester(config),
        "agoda": AgodaHarvester(config),
        "trivago": TrivagoHarvester(config),
        "kayak": KayakHarvester(config),
        "tripdotcom": TripDotComHarvester(config),
        "skyscanner": SkyscannerHarvester(config),
        "geonames": GeoNamesHarvester(config, username="demo"),  # Free tier
        "opentripmap": OpenTripMapHarvester(config),  # Using demo key
    }

    # Initialize country enrichment client
    country_client = RestCountriesClient(config)

    all_tags = []
    country_info_list = []

    for idx, row in tqdm(cities_df.iterrows(), total=len(cities_df), desc="Harvesting tags"):
        city_name = row.get("name", "")
        country = row.get("country", "")

        city_tags = []

        # Get country enrichment data
        country_info = None
        if country:
            try:
                country_info = country_client.get_country_info(country)
                if country_info:
                    # Add country-based tags
                    country_tags = country_client.get_country_tags(country_info)
                    city_tags.extend(country_tags)
            except Exception as e:
                logger.warning(f"Failed to get country info for {country}: {e}")

        country_info_list.append(country_info)

        for source_name, harvester in harvesters.items():
            try:
                if source_name == "skyscanner":
                    tags = harvester.get_city_tags(city_name)
                else:
                    tags = harvester.get_city_tags(city_name, country)

                city_tags.extend(tags)
                time.sleep(0.2)  # Small delay between harvesters

            except Exception as e:
                logger.warning(f"Failed to harvest {source_name} for {city_name}: {e}")
                continue

        all_tags.append(city_tags)

    cities_df["tags"] = all_tags
    cities_df["tag_count"] = cities_df["tags"].apply(len)
    cities_df["country_info"] = country_info_list

    # Enrich country field with ISO codes if available
    for idx, row in cities_df.iterrows():
        country_info = row.get("country_info")
        if country_info:
            cities_df.at[idx, "country_iso_alpha2"] = country_info.get("iso_alpha2", "")
            cities_df.at[idx, "country_region"] = country_info.get("region", "")

    logger.info(f"Harvested tags for {len(cities_df)} cities")
    logger.info(f"Total tags collected: {sum(cities_df['tag_count'])}")

    return cities_df


def classify_cities(cities_df: pd.DataFrame, nbd_df: pd.DataFrame) -> pd.DataFrame:
    """
    Classify cities using hybrid rule-based + tag-based approach.

    Args:
        cities_df: DataFrame with cities and tags
        nbd_df: DataFrame with NBD purposes

    Returns:
        DataFrame with classifications
    """
    logger.info("Step 4: Classifying cities...")

    ontology = load_ontology()
    nbd_mapping = load_nbd_mapping()
    tag_mappings = ontology.get("tag_mappings", {})

    main_categories_list = []
    subcategories_list = []
    confidence_list = []
    travel_purpose_list = []

    for idx, row in tqdm(cities_df.iterrows(), total=len(cities_df), desc="Classifying"):
        city_name = row.get("name", "")
        tags = row.get("tags", [])

        # Get NBD purposes if available
        nbd_purposes = []
        travel_purpose = None  # Original travel purpose from NBD
        if not nbd_df.empty:
            nbd_matches = nbd_df[nbd_df["name"].str.lower() == city_name.lower()]
            if len(nbd_matches) > 0:
                purpose = nbd_matches.iloc[0].get("purpose")
                if pd.notna(purpose):
                    nbd_purposes = [purpose]
                    travel_purpose = purpose

        travel_purpose_list.append(travel_purpose)

        # Calculate tag weights
        tag_weights = calculate_tag_weights(tags)

        # Aggregate into category scores
        main_scores, sub_scores = aggregate_scores_by_category(tag_weights, tag_mappings)

        # Merge NBD purposes
        if nbd_purposes:
            main_scores, sub_scores = merge_nbd_purposes(
                main_scores, sub_scores, nbd_purposes, nbd_mapping
            )

        # Normalize scores
        main_scores = normalize_scores(main_scores)
        sub_scores = normalize_scores(sub_scores)

        # Calculate confidence
        confidence = calculate_confidence(main_scores, sub_scores)

        # Select top labels
        top_main = select_top_labels(main_scores, threshold=0.15, max_labels=5)
        top_sub = select_top_labels(sub_scores, threshold=0.10, max_labels=8)

        main_categories_list.append([label for label, _ in top_main])
        subcategories_list.append([label for label, _ in top_sub])
        confidence_list.append(confidence)

    cities_df["main_categories"] = main_categories_list
    cities_df["subcategories"] = subcategories_list
    cities_df["confidence"] = confidence_list
    cities_df["travel_purpose"] = travel_purpose_list  # Original NBD purpose

    logger.info(f"Classified {len(cities_df)} cities")

    # Statistics
    avg_confidence = cities_df["confidence"].mean()
    classified_count = (cities_df["confidence"] > 0).sum()
    logger.info(f"Average confidence: {avg_confidence:.2f}")
    logger.info(f"Cities with classifications: {classified_count}/{len(cities_df)}")

    return cities_df


def export_data(cities_df: pd.DataFrame, output_dir: Optional[str] = None):
    """
    Export processed data to parquet and JSON.

    Args:
        cities_df: Processed cities DataFrame
        output_dir: Output directory (default: package data dir)
    """
    logger.info("Step 5: Exporting data...")

    if output_dir:
        output_path = Path(output_dir)
    else:
        output_path = get_package_dir() / "data"

    save_cities_data(cities_df, output_path)
    logger.info(f"Data exported to {output_path}")


def run_pipeline(
    nbd_path: Optional[str] = None,
    output_dir: Optional[str] = None,
    min_population: int = 100000,
    sample_size: Optional[int] = None,
):
    """
    Run the complete data pipeline.

    Args:
        nbd_path: Path to NBD.xlsx file
        output_dir: Output directory for results
        min_population: Minimum city population
        sample_size: Optional sample size for testing
    """
    start_time = time.time()
    logger.info("=" * 60)
    logger.info("Starting TravelPurpose Data Pipeline")
    logger.info("=" * 60)

    # Load NBD data
    nbd_df = load_nbd_data(nbd_path)

    # Fetch Wikidata cities
    wikidata_df = fetch_wikidata_cities(min_population)

    # Merge with NBD if available
    if not nbd_df.empty:
        logger.info("Merging NBD data with Wikidata cities...")
        cities_df = pd.merge(
            wikidata_df,
            nbd_df[["name", "country", "purpose"]],
            on=["name", "country"],
            how="outer",
        )
        cities_df = deduplicate_cities(cities_df.to_dict("records"))
        cities_df = pd.DataFrame(cities_df)
    else:
        cities_df = wikidata_df

    logger.info(f"Total cities to process: {len(cities_df)}")

    # Harvest tags
    cities_df = harvest_tags_for_cities(cities_df, sample_size)

    # Classify cities
    cities_df = classify_cities(cities_df, nbd_df)

    # Export data
    export_data(cities_df, output_dir)

    elapsed_time = time.time() - start_time
    logger.info("=" * 60)
    logger.info(f"Pipeline completed in {elapsed_time:.1f} seconds")
    logger.info(f"Processed {len(cities_df)} cities")
    logger.info("=" * 60)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="TravelPurpose Data Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--nbd",
        type=str,
        help="Path to NBD.xlsx file",
        default="NBD.xlsx",
    )

    parser.add_argument(
        "--output",
        "-o",
        type=str,
        help="Output directory for results",
        default=None,
    )

    parser.add_argument(
        "--min-population",
        type=int,
        help="Minimum city population",
        default=100000,
    )

    parser.add_argument(
        "--sample",
        type=int,
        help="Sample size for testing (processes only N cities)",
        default=None,
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging",
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    run_pipeline(
        nbd_path=args.nbd if os.path.exists(args.nbd) else None,
        output_dir=args.output,
        min_population=args.min_population,
        sample_size=args.sample,
    )


if __name__ == "__main__":
    main()
