# Changelog

All notable changes to TravelPurpose will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-11-11

### Added
- **🏷️ Simple City Tags Module**: New lightweight classification system with 800 cities
  - 7 core tags: BUSINESS, LEISURE, SEAMAN, CRUISE, MEDICAL, RELIGIOUS, SECONDHOME
  - Max 3 tags per city for optimized classification
  - Direct CSV access via `travelpurpose/data/city_tags.csv`
  - Python API: `SimpleCityTags` class with load, search, and statistics methods
  - Comprehensive documentation in `CITY_TAGS_STATS.md`
- **Expanded City Coverage**: 800 cities across 6 continents (up from 324)
  - Americas: 251 cities (31.4%)
  - Europe: 170 cities (21.2%)
  - Asia: 121 cities (15.1%)
  - Africa: 118 cities (14.8%)
  - Middle East: 81 cities (10.1%)
  - Oceania: 59 cities (7.4%)
- **Enhanced Regional Coverage**:
  - Comprehensive Caribbean cruise destinations
  - African medical tourism hubs (Lagos, Accra, Nairobi, Johannesburg)
  - Latin American medical destinations (Medellin, Bogota, San Jose)
  - Turkish domestic and international destinations
  - Pacific island cruise ports
  - European secondary cities and regional hubs
- **New Data Files**:
  - `city_tags.csv`: Main database with 800 cities
  - `CITY_TAGS_STATS.md`: Comprehensive statistics and analysis
  - `city_tags_seed.csv`: Curated seed data for manual overrides
- **Ontology to Simple Tags Converter**: Map complex ontology to simple tags
- **Build Scripts**: `scripts/build_city_tags.py` for automated database generation

### Enhanced
- README.md updated with Simple City Tags quick start section
- Tag distribution optimized for common use cases
- Regional balance improved across all continents
- Medical tourism coverage expanded to 70 cities
- Religious pilgrimage sites increased to 36 cities
- Seaman/crew change ports expanded to 162 cities
- Cruise destinations coverage: 189 cities

### Data Quality
- Removed duplicates across all sources
- Validated all tags against standard taxonomy
- Alphabetically sorted by region and city
- UTF-8 encoding with clean CSV format
- Max 3 tags per city enforcement

### Statistics (v0.2.0)
- Total Cities: 800 (147% increase from v0.1.0)
- Average Tags per City: 1.70
- Tag Usage:
  - LEISURE: 533 cities (66.6%)
  - BUSINESS: 373 cities (46.6%)
  - CRUISE: 189 cities (23.6%)
  - SEAMAN: 162 cities (20.3%)
  - MEDICAL: 70 cities (8.8%)
  - RELIGIOUS: 36 cities (4.5%)

### Use Cases
- Simplified integration for travel booking platforms
- Quick city purpose lookup without complex ontology
- Maritime crew change and port rotation planning
- Medical tourism destination selection
- Cruise itinerary planning
- Religious pilgrimage routing
- Corporate travel and business hub identification

## [0.1.0] - 2025-11-11

### Added
- Initial release of TravelPurpose library
- Multi-label city classification with 12 main categories and 70+ subcategories
- Integration with Wikidata for canonical city data
- Public data harvesters for Booking.com, Agoda, Trivago, Kayak, Trip.com, Skyscanner
- Hybrid rule-based classifier with confidence scoring
- Python API: `predict_purpose()`, `tags()`, `search()`, `load()`
- Command-line interface with `tpurpose` command
- Comprehensive ontology system with YAML configuration
- NBD purpose mapping support
- Data pipeline for building datasets
- Rate limiting and caching infrastructure
- robots.txt compliance
- Full test suite with pytest
- Documentation: README, API reference, examples
- GitHub Actions CI/CD workflows
- PyPI package configuration

### Data Sources
- Wikidata SPARQL endpoint for cities >100K population
- Wikipedia categories for cultural information
- UNESCO World Heritage sites from Wikidata
- Public structured data (JSON-LD) from travel platforms
- Public meta tags and headings from city pages

### Compliance
- Respects robots.txt on all platforms
- Rate limiting (default 1.5s between requests)
- HTTP caching (24-hour TTL)
- No authentication or private APIs used
- User-Agent identification
- Exponential backoff for retries

### Documentation
- Comprehensive README with quickstart
- API documentation with examples
- CONTRIBUTING guidelines
- CODE_OF_CONDUCT
- DATASET_CARD with provenance
- CITATION.cff for academic use
- Jupyter notebook examples

## [0.0.1] - 2025-11-10

### Added
- Project initialization
- Basic package structure

---

## Release Notes

### Version 0.1.0

This is the first production-ready release of TravelPurpose. The library provides:

**Core Features:**
- Classify cities across 12 main travel purpose categories
- 70+ specialized subcategories
- Multi-source data integration (7 public sources)
- Confidence scoring for all predictions
- Python API and CLI

**Data Quality:**
- Coverage: Cities with population >100K
- Multi-source validation
- Weighted aggregation
- Source attribution

**Production Ready:**
- Comprehensive tests (>80% coverage)
- Type hints throughout
- Logging and error handling
- CI/CD with GitHub Actions
- PyPI distribution

**Ethical Data Collection:**
- Fully compliant with platform ToS
- Respects robots.txt
- Rate limiting and caching
- No PII collection
- Transparent source attribution

### Known Limitations

- Dataset must be built locally via pipeline (not included in package)
- Limited coverage for cities <100K population
- Tag quality varies by source availability
- English language focus (limited multilingual support)
- Requires network access for live harvesting

### Future Roadmap

- [ ] Pre-built dataset for major cities (>1M population)
- [ ] Multilingual tag normalization
- [ ] Embedding-based similarity search
- [ ] Real-time confidence calibration
- [ ] Additional data sources (TripAdvisor, Lonely Planet)
- [ ] API endpoint deployment option
- [ ] Dashboard for dataset exploration

### Upgrade Notes

N/A (first release)
