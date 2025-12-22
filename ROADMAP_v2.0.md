# TravelPurpose v2.0 Roadmap
**Author**: Teyfik Oz
**License**: MIT
**Status**: Implementation Phase

## 0. Vision & Purpose

TravelPurpose v2.0 transforms city travel classification from static single-label tagging into a **dynamic, explainable, and temporally-aware** multi-label prediction engine.

**Core Philosophy**:
- **Explainable by Design**: Every prediction includes reasoning
- **Temporal Awareness**: Seasons and trends matter
- **Privacy-First**: City-level only, no PII
- **Production-Ready**: Deterministic, reproducible, testable
- **Academic-Grade**: Transparent methodology, citable

---

## 1. Product Principles

### 1.1 Data Ethics
- ✅ 100% Public & ToS-compliant data sources
- ✅ No PII, no user tracking, no behavioral profiling
- ✅ City-level aggregates only
- ✅ Full data provenance (manifest + checksums)

### 1.2 Technical Excellence
- ✅ Offline-first inference (pre-computed dataset)
- ✅ Deterministic outputs (reproducible with seed)
- ✅ Explainable-by-design (no black boxes)
- ✅ Version-controlled datasets
- ✅ Comprehensive test coverage (90%+)

### 1.3 Regulatory Compliance
- ✅ GDPR-safe (aggregate data only)
- ✅ EU AI Act compatible (explainability + transparency)
- ✅ Academic citation support
- ✅ Commercial use allowed (MIT license)

---

## 2. v2.0 Core Features

### 2.1 Purpose Confidence Decomposition

**Problem**: v1.x provides predictions without transparency

**Solution**: Break down confidence into interpretable components

**Components**:
```python
confidence_breakdown = {
    "source_agreement": 0.31,      # Agreement across data sources
    "ontology_strength": 0.27,     # Strength of category mapping
    "tag_density": 0.18,           # Number of supporting tags
    "authority_weight": 0.14,      # UNESCO/Wikidata boost
    "ambiguity_penalty": -0.04     # Reduction for conflicting signals
}
```

**Use Cases**:
- Understand WHY a city is classified as "Culture_Heritage"
- Identify weak predictions (low source_agreement)
- Debug ontology mappings
- Build trust with users

---

### 2.2 Temporal Travel Purpose (Seasonal Intelligence)

**Problem**: Cities have different purposes across seasons

**Examples**:
- **Antalya** (Turkey):
  - Summer → Beach_Resort (0.8), Leisure (0.6)
  - Winter → Medical_Health (0.5), City_Break (0.4)
- **Park City** (USA):
  - Winter → Winter_Sports (0.9), Adventure (0.7)
  - Summer → Nature_Outdoor (0.6), Mountain_Resort (0.5)
- **Rio de Janeiro** (Brazil):
  - February → Event_Festival (0.9) [Carnival]
  - Rest of Year → Beach_Resort (0.7), Culture (0.5)

**API**:
```python
# By month
result = predictor.predict_purpose("Antalya", month=7)

# By season
result = predictor.predict_purpose("Antalya", season="winter")

# Time-series
timeline = predictor.get_purpose_timeline("Rome")
```

**Data Sources**:
- Booking.com seasonal tags
- Wikidata event dates (festivals, Olympics, Expo)
- Public festival calendars
- Historical seasonal patterns

**Implementation**:
- Store purpose × month matrix
- Seasonal weights in ontology
- Event calendar integration

---

### 2.3 City Purpose Fingerprint (CPF)

**Purpose**: Create a unique "signature" for each city's travel function

**Structure**:
```python
{
    "city": "Barcelona",
    "fingerprint": {
        "main_categories": {
            "Culture_Heritage": 0.92,
            "Beach_Resort": 0.78,
            "Urban_City_Break": 0.85,
            "Gastronomy": 0.71,
            "Architecture": 0.88,
            # ... 12 total
        },
        "subcategories": {
            # 70+ sparse vector
            "historic_center": 0.95,
            "modernist_architecture": 0.93,
            "mediterranean_beach": 0.82,
            # ...
        },
        "entropy": 2.34,  # Diversity score (high = multi-purpose)
        "uniqueness": 0.67  # How unique vs other cities
    }
}
```

**Use Cases**:
1. **City Similarity**: Find cities similar to Barcelona
2. **Clustering**: Group cities by purpose profile
3. **Trend Analysis**: Track purpose evolution
4. **Recommendation**: "If you liked X, try Y"

**Metrics**:
- Cosine similarity between fingerprints
- Euclidean distance in 12D space
- Entropy (city diversity)
- Uniqueness (outlier score)

---

### 2.4 Explainable Decision Graph

**Problem**: Users don't know WHY a city was classified

**Solution**: Provide traceable reasoning for each prediction

**Output Example**:
```python
explanation = predictor.explain_city("Rome")

{
    "city": "Rome",
    "top_predictions": [
        {
            "category": "Culture_Heritage",
            "confidence": 0.94,
            "reasons": [
                {
                    "source": "wikidata",
                    "signal": "UNESCO_World_Heritage_Site",
                    "weight": 0.35
                },
                {
                    "source": "booking",
                    "signal": "historic_center tag",
                    "weight": 0.28
                },
                {
                    "source": "ontology",
                    "signal": "museum_density > threshold",
                    "weight": 0.22
                }
            ],
            "ambiguity": 0.12,  # Low ambiguity = high certainty
            "supporting_tags": [
                "colosseum", "vatican", "ancient_rome",
                "archaeological_site", "historic_monuments"
            ]
        },
        {
            "category": "Religious_Pilgrimage",
            "confidence": 0.71,
            "reasons": [
                {
                    "source": "wikidata",
                    "signal": "Vatican_City presence",
                    "weight": 0.45
                },
                {
                    "source": "booking",
                    "signal": "pilgrimage tag",
                    "weight": 0.26
                }
            ]
        }
    ],
    "decision_tree": [
        "Step 1: Matched 47 tags to Culture_Heritage",
        "Step 2: UNESCO boost applied (+0.15)",
        "Step 3: Cross-source agreement: 3/3 sources",
        "Step 4: Ambiguity penalty: -0.12"
    ]
}
```

**Benefits**:
- Full transparency
- Debuggable predictions
- User trust
- Academic validity

---

### 2.5 Multi-Language City Name & Tag Normalization

**Problem**: Same city/tag has different names in different languages

**Solution**: Offline normalization dictionary

**Examples**:

**City Names**:
```
İstanbul / Istanbul / İstambul / Stamboul → istanbul (canonical)
München / Munich / Munchen → munich
Москва / Moscow / Moscou → moscow
```

**Tag Names**:
```
beachfront / plage / strand / playa → beach_resort
musée / museum / museo / muzej → museum
montagne / mountain / montaña / berg → mountain
```

**Implementation**:
- Pre-computed normalization dict (JSON)
- Unicode-aware (unidecode)
- No language detection needed
- Fast lookup (hash map)

**Coverage**:
- 500+ city name variants
- 2000+ tag translations
- 15 languages (EN, FR, DE, ES, IT, TR, RU, AR, ZH, JA, KO, PT, NL, PL, SV)

---

### 2.6 Synthetic City Purpose Generator

**Purpose**: Generate realistic but privacy-safe synthetic city profiles

**Use Cases**:
- Demo datasets
- ML model training
- Ontology stress testing
- Benchmark creation
- Academic research (no real data restrictions)

**Features**:
```python
config = SyntheticCityConfig(
    seed=42,                    # Deterministic
    n_cities=500,              # Number of cities
    region="Europe",           # Regional realism
    seasonal_variance=0.2,     # How much seasons vary
    authority_boost=1.3,       # UNESCO/heritage weight
    output_path="synthetic_cities.jsonl"
)

engine = SyntheticCityPurposeEngine(ontology, rng_seed=42)
cities = engine.generate(base_distribution, n=500)
```

**Realism Factors**:
- Region-based purpose distributions (Europe ≠ Asia ≠ Americas)
- Seasonal variability injection
- Authority signal simulation (UNESCO-like boost)
- Noise + variance to avoid perfect patterns
- Entropy control (multi-purpose vs single-purpose cities)

**Privacy Guarantees**:
- NO real city copying
- Sampling from aggregate distributions
- Deterministic with seed
- No PII possible

---

### 2.7 Purpose Drift Detection

**Problem**: City purposes change over time

**Examples**:
- **Dubai** (2000 → 2025):
  - 2000: Transit_Hub (0.8), Business (0.4)
  - 2010: Luxury_Shopping (0.9), Business (0.7), Entertainment (0.5)
  - 2025: Entertainment (0.95), Luxury (0.9), Business (0.8)

- **Detroit** (1950 → 2025):
  - 1950: Industrial_Business (0.9)
  - 2000: Urban_Decay (not a category, low scores)
  - 2025: Culture_Arts (0.6), Urban_Renewal (0.5)

**Metrics**:
1. **KL Divergence**: `D_KL(P_old || P_new)`
2. **Cosine Drift**: `1 - cosine_similarity(fingerprint_t1, fingerprint_t2)`
3. **Category Delta Heatmap**: Which categories grew/shrank

**API**:
```python
drift = predictor.detect_purpose_drift(
    city="Dubai",
    year_start=2000,
    year_end=2025,
    granularity="5y"  # 5-year intervals
)

{
    "city": "Dubai",
    "drift_score": 0.68,  # High drift
    "kl_divergence": 1.23,
    "growing_categories": [
        ("Entertainment", +0.45),
        ("Luxury_Shopping", +0.50)
    ],
    "declining_categories": [
        ("Transit_Hub", -0.40)
    ],
    "stability_rank": "Low"  # High/Medium/Low
}
```

---

## 3. API v2.0 Specification

### 3.1 Core Prediction API

```python
from travelpurpose import TravelPurposePredictor

predictor = TravelPurposePredictor()

# Basic prediction (backward compatible)
result = predictor.predict_purpose("Barcelona")

# With temporal awareness (NEW)
result = predictor.predict_purpose("Barcelona", month=7)
result = predictor.predict_purpose("Barcelona", season="summer")

# With explainability (NEW)
result = predictor.predict_purpose(
    city="Rome",
    top_k=5,
    explain=True  # Returns full explanation
)

# Output structure
{
    "city": "Rome",
    "purposes": [
        {
            "category": "Culture_Heritage",
            "confidence": 0.94,
            "subcategories": ["historic_center", "museum", "ancient_ruins"],
        },
        # ... top_k
    ],

    # NEW v2.0 fields (if explain=True)
    "confidence_breakdown": {
        "source_agreement": 0.31,
        "ontology_strength": 0.27,
        "tag_density": 0.18,
        "authority_weight": 0.14,
        "ambiguity_penalty": -0.04
    },
    "explanation": {
        "reasons": [...],
        "decision_tree": [...],
        "supporting_tags": [...]
    },
    "ambiguity_score": 0.12,
    "entropy": 2.34
}
```

### 3.2 Advanced APIs (NEW v2.0)

```python
# City fingerprint
fingerprint = predictor.get_city_fingerprint("Tokyo")

# City comparison
similarity = predictor.compare_cities("Barcelona", "Valencia")
# Returns: cosine_similarity, euclidean_distance, shared_categories

# Regional clustering
clusters = predictor.cluster_cities(region="Europe", n_clusters=10)

# Purpose drift
drift = predictor.detect_purpose_drift("Dubai", year_start=2000, year_end=2025)

# Temporal timeline
timeline = predictor.get_purpose_timeline("Antalya")
# Returns: 12-month purpose profile

# Explainability
explanation = predictor.explain_city("Paris")
```

---

## 4. Data Layer Architecture

### 4.1 Dataset Schema (Parquet Format)

**Main Table**: `city_purposes.parquet`

| Column | Type | Description |
|--------|------|-------------|
| city_id | string | Unique identifier |
| city_name | string | Canonical name (normalized) |
| country | string | ISO 3166-1 alpha-3 |
| lat | float | Latitude |
| lon | float | Longitude |
| tag | string | Raw tag from source |
| mapped_main | string | Main purpose category (12 categories) |
| mapped_sub | string | Subcategory (70+) |
| source | string | Data source (wikidata/booking/etc) |
| authority_weight | float | Authority boost (1.0-2.0) |
| ts | datetime | Data fetch timestamp |
| season | string | summer/winter/spring/fall/all |
| month | int | 1-12 or NULL for year-round |

**Seasonal Table**: `seasonal_weights.parquet`

| Column | Type | Description |
|--------|------|-------------|
| city_id | string | City identifier |
| category | string | Purpose category |
| month | int | 1-12 |
| weight | float | Seasonal boost (0.0-2.0) |

**Fingerprint Table**: `city_fingerprints.parquet` (Pre-computed)

| Column | Type | Description |
|--------|------|-------------|
| city_id | string | City identifier |
| category | string | Purpose category |
| score | float | Normalized score (0-1) |
| entropy | float | City diversity |
| uniqueness | float | Outlier score |

### 4.2 Data Provenance

**Manifest File**: `data_manifest.json`

```json
{
    "version": "2.0.0",
    "created": "2025-12-20T00:00:00Z",
    "sources": [
        {
            "name": "wikidata",
            "url": "https://query.wikidata.org/",
            "fetch_date": "2025-12-15",
            "license": "CC0",
            "hash_sha256": "abc123...",
            "record_count": 15432
        },
        {
            "name": "booking_public",
            "url": "https://...",
            "fetch_date": "2025-12-16",
            "license": "Public Domain",
            "hash_sha256": "def456...",
            "record_count": 8921
        }
    ],
    "ontology_version": "2.0",
    "total_cities": 5000,
    "total_tags": 125000,
    "categories": 12,
    "subcategories": 73
}
```

---

## 5. Testing Strategy (90%+ Coverage)

### 5.1 Unit Tests

**Ontology Mapping**:
```python
def test_ontology_mapping():
    assert map_tag("historic center") == ("Culture_Heritage", "historic_center")
    assert map_tag("plage") == ("Beach_Resort", "beach")
    assert map_tag("unknown_tag_xyz") == (None, None)
```

**Normalization**:
```python
def test_city_normalization():
    assert normalize_city("İstanbul") == "istanbul"
    assert normalize_city("München") == "munich"
    assert normalize_city("Москва") == "moscow"
```

**Confidence Breakdown**:
```python
def test_confidence_sum():
    breakdown = decompose_confidence(...)
    total = sum(v for v in breakdown.values() if v > 0)
    assert 0.95 <= total <= 1.05  # Allow small float errors
```

### 5.2 Golden City Benchmark

**300 Expert-Curated Cities**:
```python
GOLDEN_CITIES = [
    {
        "city": "Paris",
        "expected_top3": [
            "Culture_Heritage",
            "Urban_City_Break",
            "Gastronomy"
        ],
        "min_confidence": 0.7
    },
    # ... 299 more
]

def test_golden_set():
    for city in GOLDEN_CITIES:
        result = predictor.predict_purpose(city["city"])
        top3 = [p["category"] for p in result["purposes"][:3]]
        assert set(top3) == set(city["expected_top3"])
```

### 5.3 Property-Based Tests

**Random Tag Handling**:
```python
@given(st.text())
def test_random_tags_dont_crash(tag):
    result = map_tag(tag)
    assert isinstance(result, tuple)
    assert len(result) == 2
```

**Empty/Conflict Handling**:
```python
def test_empty_sources():
    result = predictor.predict_purpose("NonexistentCity12345")
    assert result["purposes"] == []
    assert "ambiguity_score" in result

def test_conflicting_signals():
    # City with both "beach" and "winter_sports" tags
    # Should have high ambiguity
    result = predictor.predict_purpose("ConflictCity", explain=True)
    assert result["ambiguity_score"] > 0.6
```

---

## 6. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-2)
- ✅ Create project structure
- ✅ Design confidence decomposition
- ✅ Implement explainability engine
- ✅ Add temporal/seasonal support

### Phase 2: Intelligence (Weeks 3-4)
- ✅ City fingerprint calculation
- ✅ Purpose drift detection
- ✅ Multi-language normalization
- ✅ Synthetic city generator

### Phase 3: Integration (Week 5)
- ✅ Update core predictor with v2.0 features
- ✅ Add `explain=True` parameter
- ✅ Backward compatibility testing

### Phase 4: Testing & Polish (Week 6)
- ✅ Golden city benchmark
- ✅ Comprehensive test suite (90%+ coverage)
- ✅ Documentation update
- ✅ PyPI release

---

## 7. Version Plan

- **v1.0.x**: Current stable (tag-based classification)
- **v2.0.0**: Explainability + Temporal + Synthetic (THIS RELEASE)
- **v2.1.0**: Drift detection + Similarity API (Q1 2026)
- **v2.2.0**: Interactive dashboards + Visualization (Q2 2026)
- **v3.0.0**: ML-enhanced hybrid (Q3 2026)

---

## 8. Ethics & Legal Compliance

### What TravelPurpose IS:
- ✅ City-level purpose classification engine
- ✅ Aggregate data from public sources
- ✅ Transparent and explainable
- ✅ Privacy-first design

### What TravelPurpose IS NOT:
- ❌ Individual traveler profiling
- ❌ Real-time tracking
- ❌ Personalization engine
- ❌ Suitable for discriminatory decisions

### Compliance Checklist:
- [x] No PII collection
- [x] City-level aggregates only
- [x] Full data provenance
- [x] Explainability by design
- [x] GDPR-safe (aggregate only)
- [x] Dataset Card included
- [x] MIT license (commercial use OK)

---

## 9. Success Metrics

### Technical:
- ✅ 90%+ test coverage
- ✅ 100% deterministic outputs (with seed)
- ✅ < 100ms inference time per city
- ✅ < 50MB package size
- ✅ Zero runtime dependencies on APIs

### Academic:
- ✅ Publishable methodology
- ✅ Reproducible results
- ✅ Citable dataset
- ✅ Open-source contribution

### Community:
- ✅ 1,000+ PyPI downloads/month
- ✅ 100+ GitHub stars
- ✅ 10+ academic citations
- ✅ Industry adoption (tourism analytics)

---

## 10. Definition of Done

A feature is "done" when:
- [x] Unit tests pass (90%+ coverage)
- [x] Property tests pass
- [x] Golden benchmark passes
- [x] Documentation complete
- [x] Explainability verified
- [x] Deterministic outputs confirmed
- [x] CI/CD green
- [x] Peer review complete

---

## Conclusion

TravelPurpose v2.0 represents a paradigm shift from static city tagging to **dynamic, explainable, and temporally-aware** purpose classification. By combining rigorous data ethics, academic-grade transparency, and production-ready engineering, we create a tool that serves both researchers and practitioners while maintaining the highest standards of responsibility.

**Core Innovation**: Every prediction can answer "WHY?" - making TravelPurpose not just accurate, but trustworthy.

---

**Next Steps**: Begin implementation with Phase 1 (Foundation) → Week 1-2 deliverables.
