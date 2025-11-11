# Dataset Card for TravelPurpose Cities Dataset

## Dataset Description

### Summary

The TravelPurpose Cities Dataset provides multi-label travel purpose classifications for world cities with population >100,000. Each city is tagged with main categories and subcategories based on aggregated data from public travel platforms and knowledge bases.

### Supported Tasks

- Multi-label city classification
- Travel purpose prediction
- City similarity search
- Tourism market analysis
- Destination recommendation systems

### Languages

- Primary: English (en)
- City names: Unicode-aware, includes native names and ASCII variants
- Tags normalized to English from multiple source languages

## Dataset Structure

### Data Instances

```json
{
  "name": "Istanbul",
  "country": "Turkey",
  "population": 15462452,
  "latitude": 41.0082,
  "longitude": 28.9784,
  "wikidata_id": "Q406",
  "main_categories": ["Culture_Heritage", "Transit_Gateway", "Business", "Leisure"],
  "subcategories": ["UNESCO_Site", "Old_Town", "Mega_Air_Hub", "MICE_Convention", "Gastronomy"],
  "confidence": 0.86,
  "tags": [
    {"tag": "historic", "source": "wikidata", "evidence_type": "category"},
    {"tag": "business-friendly", "source": "booking", "evidence_type": "jsonld"},
    ...
  ],
  "tag_count": 47,
  "source": "wikidata"
}
```

### Data Fields

- **name** (string): City name in English
- **country** (string): Country name
- **population** (int): City population
- **latitude** (float): Latitude coordinate
- **longitude** (float): Longitude coordinate
- **wikidata_id** (string): Wikidata entity ID (e.g., "Q90" for Paris)
- **main_categories** (list[string]): Main travel purpose categories (0-5 labels)
- **subcategories** (list[string]): Specialized subcategories (0-8 labels)
- **confidence** (float): Classification confidence score (0.0-1.0)
- **tags** (list[dict]): Raw harvested tags with source attribution
- **tag_count** (int): Number of tags harvested
- **source** (string): Primary data source for city record
- **purpose** (string, optional): NBD purpose if available

### Data Splits

The dataset is not split as it serves as a reference database rather than a training set. Users can create their own splits for experimentation.

Typical usage:
- Reference: All cities
- Sample for testing: `--sample N` parameter in pipeline

## Dataset Creation

### Curation Rationale

This dataset was created to provide a standardized, multi-source classification of cities by travel purpose. Existing datasets typically focus on single aspects (e.g., only tourism, only business) or rely on single sources. This dataset combines multiple perspectives to provide comprehensive, validated classifications.

### Source Data

#### Initial Data Collection

**Wikidata (Primary Source)**
- SPARQL queries for cities with population >100,000
- Fields: Name, country, coordinates, population, Wikidata ID
- UNESCO World Heritage site associations
- Collection date: 2025-11-11
- Update frequency: On-demand via pipeline

**NBD.xlsx (Optional Internal Source)**
- Pre-existing city classifications
- Merged with high weight (2.0x) when available
- Not required for pipeline operation

#### Data Collection Process

**Public Travel Platforms**

All data collection is public and ToS-compliant:

1. **Booking.com**
   - Method: Public city pages, JSON-LD structured data
   - Tags: Business-friendly, family-friendly, beachfront, spa, etc.
   - Rate limit: 1.5s between requests
   - robots.txt: Respected

2. **Agoda**
   - Method: Public landing pages, meta tags
   - Tags: Business, wellness, shopping, nightlife
   - Rate limit: 1.5s between requests
   - robots.txt: Respected

3. **Trivago**
   - Method: Public city pages
   - Tags: City center, old town, ski region, conference
   - Rate limit: 1.5s between requests
   - robots.txt: Respected

4. **Kayak**
   - Method: Public city guides
   - Tags: MICE, convention, airport hub, family
   - Rate limit: 1.5s between requests
   - robots.txt: Respected

5. **Trip.com**
   - Method: Public destination pages
   - Tags: Cultural, historical, beach, adventure
   - Rate limit: 1.5s between requests
   - robots.txt: Respected

6. **Skyscanner**
   - Method: Public autosuggest API
   - Data: City names, IATA codes, normalization
   - Rate limit: 1.5s between requests

#### Who are the source data producers?

- **Wikidata**: Community-curated knowledge base
- **Travel Platforms**: Commercial platforms with public data
- **UNESCO**: Official World Heritage site designations
- **NBD.xlsx**: Internal business intelligence (optional)

### Annotations

#### Annotation Process

The dataset uses automated classification rather than manual annotation:

1. **Tag Aggregation**: Collect tags from all sources with source attribution
2. **Weight Calculation**: Apply source-specific weights (Wikidata 1.5x, Booking 1.0x, etc.)
3. **Evidence Boost**: JSON-LD (1.2x), Meta tags (1.0x), Headings (0.8x)
4. **Category Mapping**: Fuzzy match tags to ontology categories
5. **Score Normalization**: Softmax-like normalization
6. **Confidence Calculation**: Weighted average of main (0.7) and sub (0.3) scores
7. **Threshold Filtering**: Main >0.15, Sub >0.10

#### Who are the annotators?

N/A - Automated classification system

### Personal and Sensitive Information

**No personal information is collected.** The dataset contains only:
- Geographic data (city names, coordinates, populations)
- Public travel characteristics
- Publicly available tags from travel platforms

## Considerations for Using the Data

### Social Impact

**Intended Use:**
- Tourism analysis and planning
- Destination recommendation systems
- Market research
- Travel route optimization
- Business intelligence

**Potential Misuse:**
- Stereotyping cities or regions
- Ignoring within-city diversity
- Using classifications to justify discrimination
- Tourism overtourism if not used responsibly

### Discussion of Biases

**Known Biases:**

1. **Geographic Bias**: Cities >100K population only; under-represents smaller destinations
2. **Language Bias**: English-centric tag normalization may miss nuances
3. **Source Bias**: Western travel platforms over-represented
4. **Temporal Bias**: Snapshot in time; cities evolve
5. **Commercial Bias**: Focus on commercial travel aspects
6. **Digital Divide**: Cities with less online presence under-represented

**Mitigation Efforts:**
- Multi-source aggregation reduces single-source bias
- Confidence scores reflect data quality
- Source attribution enables bias analysis
- Wikidata provides geographic balance
- Extensible ontology allows bias correction

### Limitations

- **Coverage**: Limited to cities >100K population
- **Freshness**: Data becomes stale; requires periodic refresh
- **Depth**: Surface-level categorization; lacks fine-grained detail
- **Validation**: Limited ground truth validation
- **Multilingual**: Primarily English tags
- **Seasonality**: No seasonal variation capture
- **Events**: No special event or festival capture

### Recommendations

**Users should:**
- Check confidence scores before using classifications
- Validate results for critical applications
- Consider multiple sources for ground truth
- Update data regularly via pipeline
- Be aware of biases when interpreting results
- Not use as sole basis for major decisions

**Users should not:**
- Assume completeness or accuracy
- Use for real-time applications without fresh data
- Ignore low confidence scores
- Apply classifications to individuals
- Use for discriminatory purposes

## Additional Information

### Dataset Curators

Travel Purpose Contributors

### Licensing Information

- **Code**: MIT License
- **Data**: Aggregated from public sources under their respective terms
- **Wikidata**: CC0 (Public Domain)
- **Travel Platform Data**: Fair use for research and analysis

### Citation Information

```bibtex
@dataset{travelpurpose_cities_2025,
  title={TravelPurpose Cities Dataset},
  author={Travel Purpose Contributors},
  year={2025},
  url={https://github.com/teyfikoz/Travel_Purpose-City_Tags}
}
```

### Contributions

Contributions are welcome! See CONTRIBUTING.md for guidelines on:
- Adding new data sources
- Improving tag mappings
- Extending geographic coverage
- Enhancing multilingual support
