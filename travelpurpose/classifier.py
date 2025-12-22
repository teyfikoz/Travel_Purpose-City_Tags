"""
Main classifier module for travel purpose prediction.

Provides the public API for city travel purpose classification.

v2.0 NEW FEATURES:
- Explainability (explain=True)
- Temporal/seasonal awareness
- City fingerprints
- Confidence decomposition
"""

import logging

import pandas as pd

from travelpurpose.tags import get_tags_for_city, load_tags_cache
from travelpurpose.utils.io import load_cities_data, load_nbd_mapping, load_ontology
from travelpurpose.utils.normalize import normalize_city_name
from travelpurpose.utils.scoring import (
    aggregate_scores_by_category,
    calculate_confidence,
    calculate_tag_weights,
    merge_nbd_purposes,
    normalize_scores,
    select_top_labels,
)

# v2.0 imports
from travelpurpose.explainability import ExplainabilityEngine
from travelpurpose.temporal import TemporalEngine
from travelpurpose.fingerprint import CityFingerprint

logger = logging.getLogger(__name__)

# Global state
_DATA_LOADED = False
_CITIES_DF: pd.DataFrame | None = None
_ONTOLOGY: dict | None = None
_NBD_MAPPING: dict | None = None


def load():
    """
    Load and initialize the classifier data and configuration.

    This function loads:
    - City dataset with tags and classifications
    - Ontology configuration
    - NBD purpose mappings
    - Tags cache

    Call this once before using predict_purpose or other functions.
    """
    global _DATA_LOADED, _CITIES_DF, _ONTOLOGY, _NBD_MAPPING

    if _DATA_LOADED:
        logger.info("Data already loaded")
        return

    logger.info("Loading travelpurpose data...")

    # Load ontology
    _ONTOLOGY = load_ontology()
    logger.info(
        f"Loaded ontology with {len(_ONTOLOGY.get('main_categories', []))} main categories"
    )

    # Load NBD mapping
    _NBD_MAPPING = load_nbd_mapping()
    logger.info(
        f"Loaded NBD mapping with {len(_NBD_MAPPING.get('nbd_to_main', {}))} purposes"
    )

    # Load cities data
    _CITIES_DF = load_cities_data()
    if _CITIES_DF is not None:
        logger.info(f"Loaded {len(_CITIES_DF)} cities from dataset")
    else:
        logger.warning("No cities dataset found. Will use live harvesting.")
        _CITIES_DF = pd.DataFrame()

    # Load tags cache
    load_tags_cache()

    _DATA_LOADED = True
    logger.info("Data loading complete")


def predict_purpose(
    city_name: str,
    use_cache: bool = True,
    month: int = None,
    season: str = None,
    explain: bool = False,
    offline_mode: bool = None
) -> dict:
    """
    Predict travel purposes for a city - ENHANCED v2.0

    Args:
        city_name: Name of the city
        use_cache: Whether to use cached data (default: True)
        month: Month (1-12) for seasonal adjustment (v2.0 NEW)
        season: Season name ('winter'/'spring'/'summer'/'fall') (v2.0 NEW)
        explain: Include explainability details (v2.0 NEW)
        offline_mode: If True, work WITHOUT network access (v2.0.1 NEW).
                     If None, auto-detect from environment (CI, PYTEST, TRAVELPURPOSE_OFFLINE)

    Returns:
        Dictionary with:
        - main: List of main category labels
        - sub: List of subcategory labels
        - confidence: Overall confidence score (0-1)
        - scores: Detailed scores for debugging (optional)

        v2.0 NEW (if explain=True):
        - ambiguity_score: Uncertainty measure (0-1)
        - confidence_breakdown: Component analysis
        - explanation: Human-readable reasons
        - fingerprint: City purpose fingerprint

    Example:
        >>> predict_purpose("Istanbul", explain=True)
        {
            'main': ['Culture_Heritage', 'Transit_Gateway', 'Leisure'],
            'sub': ['UNESCO_Site', 'Old_Town', 'Mega_Air_Hub', 'Gastronomy'],
            'confidence': 0.86,
            'ambiguity_score': 0.32,
            'explanation': {...}
        }
    """
    if not _DATA_LOADED:
        load()

    city_norm = normalize_city_name(city_name)

    # Try to find city in dataset first
    nbd_purposes = []
    if use_cache and _CITIES_DF is not None and len(_CITIES_DF) > 0:
        matches = _CITIES_DF[
            _CITIES_DF["name"].str.lower().apply(normalize_city_name) == city_norm
        ]
        if len(matches) > 0:
            city_row = matches.iloc[0]
            # Extract NBD purposes if available
            purpose_val = city_row.get("purpose")
            if purpose_val is not None and not (
                isinstance(purpose_val, float) and pd.isna(purpose_val)
            ):
                nbd_purposes = [purpose_val]
            # Check if already classified
            main_cats = city_row.get("main_categories")
            if main_cats is not None and not (
                isinstance(main_cats, float) and pd.isna(main_cats)
            ):
                return {
                    "main": (
                        city_row["main_categories"]
                        if isinstance(city_row["main_categories"], list)
                        else [city_row["main_categories"]]
                    ),
                    "sub": (
                        city_row.get("subcategories", [])
                        if isinstance(city_row.get("subcategories"), list)
                        else []
                    ),
                    "confidence": city_row.get("confidence", 0.8),
                }

    # Harvest tags with improved timeout handling and offline mode support
    tags = get_tags_for_city(city_name, use_cache=use_cache, offline_mode=offline_mode)

    # Use fallback knowledge base if no tags found
    if not tags and not nbd_purposes:
        logger.info(f"No tags found, trying fallback knowledge base for: {city_name}")
        from travelpurpose.utils.normalize import get_fallback_data

        fallback_result = get_fallback_data(city_name)
        if fallback_result:
            logger.info(f"Using fallback data for {city_name}")
            return fallback_result

    if not tags and not nbd_purposes:
        logger.warning(f"No data found for city: {city_name}")
        return {
            "main": [],
            "sub": [],
            "confidence": 0.0,
        }

    # Calculate tag weights
    tag_weights = calculate_tag_weights(tags)

    # Aggregate into category scores
    tag_mappings = _ONTOLOGY.get("tag_mappings", {})
    main_scores, sub_scores = aggregate_scores_by_category(tag_weights, tag_mappings)

    # Merge NBD purposes if available
    if nbd_purposes:
        main_scores, sub_scores = merge_nbd_purposes(
            main_scores, sub_scores, nbd_purposes, _NBD_MAPPING
        )

    # Normalize scores
    main_scores = normalize_scores(main_scores)
    sub_scores = normalize_scores(sub_scores)

    # v2.0 NEW: Apply temporal/seasonal boost if provided
    if month or season:
        main_scores = TemporalEngine.apply_seasonal_boost(
            main_scores, season=season, month=month
        )
        logger.info(f"Applied seasonal boost for {'month ' + str(month) if month else season}")

    # Calculate confidence
    confidence = calculate_confidence(main_scores, sub_scores)

    # Select top labels
    top_main = select_top_labels(main_scores, threshold=0.15, max_labels=5)
    top_sub = select_top_labels(sub_scores, threshold=0.10, max_labels=8)

    result = {
        "main": [label for label, _ in top_main],
        "sub": [label for label, _ in top_sub],
        "confidence": round(confidence, 2),
    }

    # v2.0 NEW: Add explainability if requested
    if explain:
        # Calculate ambiguity score
        top_scores = [score for _, score in top_main]
        ambiguity_score = ExplainabilityEngine.calculate_ambiguity(top_scores)

        # Decompose confidence into components
        # Calculate component values
        num_sources = len(set(tag.get('source', 'unknown') for tag in tags))
        source_agreement = min(num_sources / 5.0, 1.0) if tags else 0.0
        ontology_strength = max(top_scores) if top_scores else 0.0
        tag_density = min(len(tags) / 50.0, 1.0) if tags else 0.0
        authority_weight = 0.15 if any('unesco' in label.lower() or 'heritage' in label.lower()
                                      for label in result['main']) else 0.0

        confidence_breakdown = ExplainabilityEngine.decompose_confidence(
            source_agreement=source_agreement,
            ontology_strength=ontology_strength,
            tag_density=tag_density,
            authority_weight=authority_weight,
            ambiguity_penalty=ambiguity_score * 0.2
        )

        # Generate explanation
        supporting_tags = [tag.get('tag', '') for tag in tags[:10]] if tags else []
        explanation = ExplainabilityEngine.generate_explanation(
            city=city_name,
            prediction=result,
            confidence_breakdown=confidence_breakdown,
            ambiguity_score=ambiguity_score,
            supporting_tags=supporting_tags
        )

        # Create city fingerprint
        fingerprint = CityFingerprint.create_fingerprint(main_scores)

        # Add to result
        result['ambiguity_score'] = round(ambiguity_score, 4)
        result['confidence_breakdown'] = confidence_breakdown
        result['explanation'] = explanation['explanation']
        result['fingerprint'] = fingerprint

        logger.info(f"Generated explainability for {city_name}: ambiguity={ambiguity_score:.4f}")

    logger.info(f"Predicted purposes for {city_name}: {result['main']}")
    return result


def tags(city_name: str, use_cache: bool = True) -> list[dict]:
    """
    Get raw harvested tags for a city.

    Args:
        city_name: Name of the city
        use_cache: Whether to use cached data

    Returns:
        List of tag dictionaries with source information

    Example:
        >>> tags("Antalya")[:2]
        [
            {'tag': 'beachfront', 'source': 'booking', 'url': '...', 'ts': '...'},
            {'tag': 'resort', 'source': 'agoda', 'url': '...', 'ts': '...'}
        ]
    """
    if not _DATA_LOADED:
        load()

    return get_tags_for_city(city_name, use_cache=use_cache)


def search(query: str) -> list[dict]:
    """
    Search for cities matching a query.

    Args:
        query: Search query (city name, country, etc.)

    Returns:
        List of matching city dictionaries

    Example:
        >>> search("paris")
        [{'name': 'Paris', 'country': 'France', 'population': 2148000, ...}]
    """
    if not _DATA_LOADED:
        load()

    if _CITIES_DF is None or len(_CITIES_DF) == 0:
        logger.warning("No cities dataset available for search")
        return []

    query_norm = normalize_city_name(query)

    # Search in name and country
    matches = _CITIES_DF[
        _CITIES_DF["name"]
        .str.lower()
        .apply(normalize_city_name)
        .str.contains(query_norm)
        | _CITIES_DF.get("country", pd.Series(dtype=str))
        .str.lower()
        .str.contains(query_norm, na=False)
    ]

    results = matches.head(20).to_dict("records")
    logger.info(f"Found {len(results)} matches for query: {query}")
    return results


def get_ontology() -> dict:
    """
    Get the current ontology configuration.

    Returns:
        Ontology dictionary with main_categories, subcategories, and tag_mappings
    """
    if not _DATA_LOADED:
        load()

    return _ONTOLOGY


def get_available_cities() -> list[str]:
    """
    Get list of available cities in the dataset.

    Returns:
        List of city names
    """
    if not _DATA_LOADED:
        load()

    if _CITIES_DF is None or len(_CITIES_DF) == 0:
        return []

    return _CITIES_DF["name"].tolist()
