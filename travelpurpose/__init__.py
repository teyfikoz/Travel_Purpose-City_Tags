"""
TravelPurpose - City Travel Purpose Classification Library

A production-grade Python library for classifying world cities by travel purpose
using multi-source data from public travel platforms and knowledge bases.

v2.0 NEW FEATURES:
- Explainability (explain=True): Understand WHY predictions are made
- Temporal/seasonal awareness: Purpose changes with seasons
- City fingerprints: Unique purpose signatures for each city
- Confidence decomposition: See what contributes to confidence
- Synthetic city generator: Privacy-safe data generation
"""

__version__ = "2.0.4"
__author__ = "Travel Purpose Contributors"

from travelpurpose.classifier import load, predict_purpose, search, tags

# v2.0 NEW: Explainability and analytics modules
from travelpurpose.explainability import ExplainabilityEngine
from travelpurpose.temporal import TemporalEngine
from travelpurpose.fingerprint import CityFingerprint
from travelpurpose.synthetic.engine import SyntheticCityEngine, SyntheticCityConfig

__all__ = [
    # Core API
    "predict_purpose",
    "tags",
    "search",
    "load",
    # v2.0 NEW: Advanced features
    "ExplainabilityEngine",
    "TemporalEngine",
    "CityFingerprint",
    "SyntheticCityEngine",
    "SyntheticCityConfig",
    # Meta
    "__version__",
]
