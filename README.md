# TravelPurpose

[![PyPI version](https://badge.fury.io/py/travelpurpose.svg)](https://badge.fury.io/py/travelpurpose)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A production-grade Python library for classifying world cities by travel purpose using multi-source data from public travel platforms and knowledge bases.

## 🆕 What's New in v2.0.1 (Aralık 2024)

**Production-Ready Enhancements**:
- ✅ **Enhanced PyPI Description**: Better discoverability with clearer value propositions
- ✅ **Offline-First**: All core features work without network access (uses cached data)
- ✅ **Ethical Harvesting**: 100% ToS-compliant multi-source data collection
- ✅ **Performance Optimized**: Faster predictions with improved caching
- ✅ **Type Safety**: Complete type hints for better IDE support

**What Makes TravelPurpose Production-Grade**:
```python
# Explainable predictions - understand WHY
result = predict_purpose("Istanbul", explain=True)
print(result['explanation'])  # Human-readable reasons

# Seasonal awareness - purposes change with time
summer = predict_purpose("Antalya", season="summer")  # Beach boosted
winter = predict_purpose("St. Moritz", season="winter")  # Ski boosted

# Offline-first - works without network
result = predict_purpose("Paris", use_cache=True)  # Uses local data
```

**Production Benefits**:
- 🚀 **No API Costs**: 100% local ML, no external API dependencies
- 🔒 **Privacy-Safe**: Synthetic data generator for testing
- 📊 **Transparent**: Full explainability with confidence breakdowns
- ⚡ **Fast**: Cached predictions, optimized for production

## 🆕 What's New in v2.0

**Explainable AI** - Understand WHY predictions are made:
- **`explain=True`**: Get ambiguity scores, confidence breakdowns, and human-readable explanations
- **Temporal Awareness**: Purposes change with seasons (`month=7` for summer travel)
- **City Fingerprints**: Unique purpose signatures for each city
- **Confidence Decomposition**: See what contributes to each prediction
- **Synthetic Data Generator**: Privacy-safe data for testing and research

```python
# v2.0 NEW: Explainable predictions
result = predict_purpose("Istanbul", explain=True)
print(result['ambiguity_score'])  # 0.32 - moderate ambiguity
print(result['explanation']['reasons'])
# ['High cross-source agreement', 'UNESCO/Heritage site boost', ...]

# v2.0 NEW: Seasonal awareness
summer_purposes = predict_purpose("Antalya", month=7)  # Beach boosted in summer
winter_purposes = predict_purpose("St. Moritz", season="winter")  # Ski boosted
```

## Features

- **Multi-Label Classification**: Cities can have multiple travel purposes (e.g., Business + Culture + Transit)
- **Rich Ontology**: 12 main categories and 70+ subcategories covering all travel purposes
- **Multi-Source Data**: Integrates data from Wikidata, Booking.com, Agoda, Trivago, Kayak, Trip.com, and Skyscanner
- **Hybrid Classifier**: Combines rule-based and embedding-based approaches with confidence scoring
- **🆕 Explainable AI**: Ambiguity scores, confidence decomposition, human-readable explanations
- **🆕 Temporal Awareness**: Seasonal purpose adjustments (e.g., beach cities in summer)
- **🆕 City Fingerprints**: Unique purpose signatures for similarity analysis
- **🆕 Synthetic Data**: Privacy-safe data generation for testing and research
- **Python API & CLI**: Easy-to-use programmatic and command-line interfaces
- **Ethical Data Collection**: Fully compliant with ToS, respects robots.txt, implements rate limiting
- **Production Ready**: Comprehensive tests, CI/CD, type hints, logging, caching

## Installation

```bash
pip install travelpurpose
```

## Quick Start

### Python API

```python
from travelpurpose import predict_purpose, tags

# Predict travel purposes for a city
result = predict_purpose("Istanbul")
print(result)
# {
#     'main': ['Culture_Heritage', 'Transit_Gateway', 'Leisure'],
#     'sub': ['UNESCO_Site', 'Old_Town', 'Mega_Air_Hub', 'Gastronomy'],
#     'confidence': 0.86
# }

# Get raw tags from all sources
city_tags = tags("Antalya")
print(city_tags[:3])
# [
#     {'tag': 'beachfront', 'source': 'booking', 'url': '...', 'ts': '...'},
#     {'tag': 'resort', 'source': 'agoda', 'url': '...'},
#     {'tag': 'all-inclusive', 'source': 'trivago', 'url': '...'}
# ]
```

### Command Line

```bash
# Predict purposes for a city
tpurpose predict "Paris"

# Show raw tags
tpurpose show-tags "Dubai" --limit 20

# Search for cities
tpurpose find "turkey"

# Rebuild dataset (requires network access)
tpurpose rebuild --sample 100 --verbose
```

## Travel Purpose Ontology

### Main Categories (12)

- **Business**: Finance hubs, tech centers, MICE destinations
- **Leisure**: City breaks, luxury, shopping, gastronomy
- **Culture_Heritage**: UNESCO sites, museums, old towns, architecture
- **Beach_Resort**: Beachfront, islands, diving, all-inclusive
- **Adventure_Nature**: Trekking, safari, desert, extreme sports
- **Family**: Theme parks, zoos, safe cities, kid-friendly
- **Medical_Health**: Medical tourism, wellness, spa, rehabilitation
- **Religious_Pilgrimage**: Islamic, Christian, Buddhist, Hindu pilgrimage sites
- **Winter_Snow**: Ski resorts, winter sports, aurora viewing
- **Nightlife_Entertainment**: Party districts, casinos, music festivals
- **Transit_Gateway**: Major airport hubs, connecting destinations
- **Seaman_Crew**: Crew change ports, maritime facilities

### Subcategories (70+)

Each main category has 4-9 specialized subcategories. See `travelpurpose/ontology/ontology.yaml` for the complete taxonomy.

## Data Sources

All data collection is **public, ToS-compliant, and ethical**:

### Knowledge Bases
- **Wikidata**: Canonical city data, coordinates, population, UNESCO sites
- **Wikipedia**: City categories and cultural information

### Travel Platforms (Public Data Only)
- **Booking.com**: Public structured data (JSON-LD), meta tags, city guides
- **Agoda**: Public landing pages, sitemaps, accommodation types
- **Trivago**: Public city pages, district information
- **Kayak**: Public city guides, travel information
- **Trip.com**: Public destination pages, attractions
- **Skyscanner**: Public autocomplete API for city normalization

### Compliance Features
- Respects robots.txt
- Rate limiting (configurable, default 1.5s between requests)
- HTTP caching (24-hour TTL)
- Exponential backoff for retries
- No authentication, logins, or private APIs
- User-Agent identification
- Graceful degradation when sources are unavailable

## Architecture

### Data Pipeline

```bash
python scripts/pipeline.py --min-population 100000 --sample 50
```

The pipeline:
1. Loads NBD.xlsx (if available) with existing city classifications
2. Fetches canonical city data from Wikidata (cities >100K population)
3. Harvests public tags from all sources
4. Normalizes tags to English, handles Unicode city names
5. Maps tags to ontology using fuzzy matching
6. Merges with NBD purposes (if available)
7. Classifies using hybrid rule-based + embedding approach
8. Calculates confidence scores
9. Exports to `travelpurpose/data/cities.{parquet,json}`

### Classifier Design

**Hybrid Approach:**
1. **Rule-Based** (deterministic): Strong tags directly map to categories
2. **Tag Aggregation**: Weighted voting from multiple sources
3. **Confidence Calibration**: Based on data quality and agreement

**Source Weights:**
- Wikidata/UNESCO: 1.5-2.0x (high authority)
- Booking.com/Agoda: 1.0x (standard)
- Trivago/Kayak/Trip.com: 0.9x
- Evidence type boosts: JSON-LD (1.2x), Meta (1.0x), Headings (0.8x)

## Configuration

### Rate Limiting

```python
from travelpurpose.utils.harvest import HarvestConfig

config = HarvestConfig(
    rate_limit=2.0,  # 2 seconds between requests
    timeout=15,
    max_retries=3,
    cache_ttl=86400,  # 24 hours
)
```

### Extending the Ontology

Edit `travelpurpose/ontology/ontology.yaml`:

```yaml
main_categories:
  - Your_New_Category

subcategories:
  Your_New_Category:
    - Subcategory_One
    - Subcategory_Two

tag_mappings:
  your_mapping:
    main: Your_New_Category
    sub: [Subcategory_One]
    keywords: ["keyword1", "keyword2"]
```

## Development

### Setup

```bash
git clone https://github.com/teyfikoz/Travel_Purpose-City_Tags.git
cd Travel_Purpose-City_Tags
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
pytest --cov=travelpurpose --cov-report=term-missing
```

### Linting

```bash
ruff check travelpurpose/
black travelpurpose/
```

### Building for PyPI

```bash
python -m build
twine check dist/*
twine upload dist/*
```

## Examples

See `examples/` directory for Jupyter notebooks:
- `01_quickstart.ipynb`: Basic usage and API examples
- `02_training_and_rules.ipynb`: Advanced classification and ontology customization

## Data Provenance & Ethics

### Dataset Card

See `DATASET_CARD.md` for:
- Data sources and collection dates
- Sample sizes and coverage
- Limitations and biases
- Update frequency

### Ethics & Privacy

- **No PII**: We collect no personal information
- **Public Data Only**: All sources are publicly accessible
- **ToS Compliance**: Strict adherence to platform terms of service
- **Transparency**: Full source attribution in tag metadata
- **Caching**: Reduces load on source platforms
- **Rate Limiting**: Prevents server overload

## Citation

If you use TravelPurpose in research, please cite:

```bibtex
@software{travelpurpose2025,
  title = {TravelPurpose: City Travel Purpose Classification Library},
  author = {Travel Purpose Contributors},
  year = {2025},
  url = {https://github.com/teyfikoz/Travel_Purpose-City_Tags}
}
```

See `CITATION.cff` for more formats.

## License

MIT License - see `LICENSE` file for details.

## Contributing

We welcome contributions! See `CONTRIBUTING.md` for guidelines.

Key areas for contribution:
- Adding new data sources (must be public and ToS-compliant)
- Expanding the ontology with new categories
- Improving classification accuracy
- Adding support for more languages
- Documentation improvements

## Support

- **Issues**: [GitHub Issues](https://github.com/teyfikoz/Travel_Purpose-City_Tags/issues)
- **Discussions**: [GitHub Discussions](https://github.com/teyfikoz/Travel_Purpose-City_Tags/discussions)

## Changelog

See `CHANGELOG.md` for version history and updates.

## Acknowledgments

- Wikidata and Wikipedia communities for open knowledge bases
- Travel platforms for providing public data
- Open source community for excellent Python libraries

---

**Made with ❤️ for the travel and data science communities**
