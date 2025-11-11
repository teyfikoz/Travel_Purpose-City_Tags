# TravelPurpose Project Summary

## Overview

This repository contains **TravelPurpose**, a production-grade Python library for classifying world cities by travel purpose. The library integrates data from multiple public sources including Wikidata, Booking.com, Agoda, Trivago, Kayak, Trip.com, and Skyscanner to provide multi-label classifications across 12 main categories and 70+ subcategories.

## Project Structure

```
Travel_Purpose-City_Tags/
├── travelpurpose/              # Main package
│   ├── __init__.py            # Package initialization and exports
│   ├── classifier.py          # Core classification API
│   ├── tags.py                # Tag extraction and management
│   ├── cli.py                 # Command-line interface
│   ├── data/                  # Data directory (generated)
│   │   └── .gitkeep
│   ├── ontology/              # Classification ontology
│   │   ├── ontology.yaml     # Main ontology definition
│   │   └── mapping_nbd.yaml  # NBD purpose mappings
│   └── utils/                 # Utility modules
│       ├── __init__.py
│       ├── io.py             # File I/O operations
│       ├── normalize.py      # Text normalization
│       ├── harvest.py        # Base harvesting infrastructure
│       ├── scoring.py        # Classification scoring
│       ├── wikidata.py       # Wikidata integration
│       ├── skyscanner.py     # Skyscanner harvester
│       ├── booking.py        # Booking.com harvester
│       ├── agoda.py          # Agoda harvester
│       ├── trivago.py        # Trivago harvester
│       ├── kayak.py          # Kayak harvester
│       └── tripdotcom.py     # Trip.com harvester
│
├── scripts/                   # Pipeline and build scripts
│   ├── pipeline.py           # Main ETL pipeline
│   └── build_release.py      # Release validation script
│
├── tests/                     # Test suite
│   ├── __init__.py
│   ├── test_api.py           # API function tests
│   ├── test_normalize.py     # Normalization tests
│   └── test_scoring.py       # Scoring logic tests
│
├── examples/                  # Usage examples
│   ├── README.md
│   ├── 01_quickstart.ipynb   # Basic usage
│   └── 02_advanced_usage.ipynb  # Advanced features
│
├── .github/
│   └── workflows/
│       ├── ci.yml            # CI workflow (lint, test, build)
│       └── release.yml       # PyPI release workflow
│
├── pyproject.toml            # Package configuration
├── Makefile                  # Development commands
├── .gitignore               # Git ignore rules
├── README.md                # Main documentation
├── LICENSE                  # MIT License
├── CONTRIBUTING.md          # Contribution guidelines
├── CODE_OF_CONDUCT.md       # Code of conduct
├── CHANGELOG.md             # Version history
├── CITATION.cff             # Citation information
├── DATASET_CARD.md          # Dataset documentation
└── PROJECT_SUMMARY.md       # This file
```

## Key Components

### 1. Classification System

**Ontology (ontology.yaml)**
- 12 main categories: Business, Leisure, Culture_Heritage, Beach_Resort, Adventure_Nature, Family, Medical_Health, Religious_Pilgrimage, Winter_Snow, Nightlife_Entertainment, Transit_Gateway, Seaman_Crew
- 70+ subcategories providing granular classification
- Extensible YAML configuration
- Tag-to-category mapping rules

**Hybrid Classifier (classifier.py)**
- Rule-based deterministic mapping
- Tag aggregation with source weighting
- Confidence score calculation (0.0-1.0)
- Multi-label predictions
- Threshold-based filtering

### 2. Data Collection

**Public Sources (All ToS-Compliant)**
- **Wikidata**: Canonical city data via SPARQL
- **UNESCO**: World Heritage sites
- **Travel Platforms**: Public structured data (JSON-LD, meta tags, headings)

**Compliance Infrastructure (harvest.py)**
- robots.txt checking and respect
- Rate limiting (configurable, default 1.5s)
- HTTP caching (24-hour TTL)
- Exponential backoff for retries
- User-Agent identification
- Graceful error handling

### 3. Data Pipeline (scripts/pipeline.py)

End-to-end ETL pipeline:
1. Load NBD.xlsx (optional internal data)
2. Fetch cities from Wikidata (SPARQL)
3. Harvest tags from all sources
4. Normalize tags (multilingual → English)
5. Map tags to ontology categories
6. Merge NBD classifications
7. Calculate scores and confidence
8. Export to parquet + JSON

### 4. Python API

**Main Functions:**
```python
from travelpurpose import predict_purpose, tags, search, load

# Predict travel purposes
result = predict_purpose("Istanbul")
# {'main': [...], 'sub': [...], 'confidence': 0.86}

# Get raw tags
city_tags = tags("Antalya")

# Search cities
results = search("paris")

# Load data (called automatically)
load()
```

### 5. Command-Line Interface

```bash
# Predict purposes
tpurpose predict "Dubai"

# Show raw tags
tpurpose show-tags "Barcelona" --limit 20

# Search cities
tpurpose find "france"

# Rebuild dataset
tpurpose rebuild --sample 100 --verbose

# Show version
tpurpose --version
```

### 6. Testing & Quality

**Test Suite (tests/)**
- Unit tests for all major modules
- API endpoint tests
- Normalization tests
- Scoring logic tests
- pytest with coverage reporting

**Code Quality**
- Ruff linting
- Black code formatting
- Type hints throughout
- Comprehensive documentation
- Logging infrastructure

### 7. CI/CD & Distribution

**GitHub Actions**
- **CI Workflow**: Lint, test, build on push/PR
- **Release Workflow**: Auto-publish to PyPI on git tag

**PyPI Configuration**
- Package name: `travelpurpose`
- Version: 0.1.0
- Python 3.10+ support
- Console script entry point: `tpurpose`

## Installation & Usage

### For Users

```bash
pip install travelpurpose
```

### For Developers

```bash
git clone https://github.com/teyfikoz/Travel_Purpose-City_Tags.git
cd Travel_Purpose-City_Tags
make install-dev
make test
```

## Data Provenance

All data is collected ethically and legally:
- **Public Sources Only**: No authentication, logins, or private APIs
- **ToS Compliance**: Strict adherence to platform terms
- **robots.txt**: Checked and respected
- **Rate Limiting**: Conservative request rates
- **Attribution**: Full source tracking in metadata
- **Caching**: Reduces redundant requests

## Licensing

- **Code**: MIT License
- **Data**: Aggregated from public sources under fair use
- **Wikidata**: CC0 (Public Domain)

## Documentation

### Main Documentation
- **README.md**: Installation, quickstart, API reference
- **CONTRIBUTING.md**: Development guidelines
- **DATASET_CARD.md**: Data provenance and ethics
- **CHANGELOG.md**: Version history

### Examples
- **01_quickstart.ipynb**: Basic usage tutorial
- **02_advanced_usage.ipynb**: Advanced features and customization

## Deployment Checklist

Before v0.1.0 release:

- [x] Core package structure
- [x] Ontology system
- [x] Data harvesters for all sources
- [x] Classification system
- [x] Python API
- [x] CLI interface
- [x] Data pipeline
- [x] Test suite
- [x] Documentation
- [x] CI/CD workflows
- [x] Example notebooks
- [x] License and attribution
- [x] PyPI configuration

## Next Steps

### Immediate (Post-Release)
1. Run full pipeline on production data
2. Validate classifications for major cities
3. Publish v0.1.0 to PyPI
4. Announce release

### Short-Term (v0.2.0)
- Pre-built dataset for top 1000 cities
- Multilingual tag support
- Embedding-based similarity search
- Performance optimizations
- Additional data sources (TripAdvisor, Lonely Planet)

### Long-Term (v1.0.0)
- Real-time API deployment
- Dashboard for data exploration
- Active learning for classification improvement
- Temporal analysis (seasonality)
- Event detection (festivals, conferences)

## Contributors

Travel Purpose Contributors - 2025

## Links

- **Repository**: https://github.com/teyfikoz/Travel_Purpose-City_Tags
- **Issues**: https://github.com/teyfikoz/Travel_Purpose-City_Tags/issues
- **PyPI**: https://pypi.org/project/travelpurpose/ (post-release)

---

**Last Updated**: 2025-11-11
**Status**: Ready for v0.1.0 release
