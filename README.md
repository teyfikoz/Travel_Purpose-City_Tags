# TravelPurpose

**City travel purpose classification library** — predict why travelers visit any city (Culture, Business, Beach, Adventure, Transit, etc.) using multi-source tag ontology and NBD purpose mappings. No API key required.

[![PyPI version](https://badge.fury.io/py/travelpurpose.svg)](https://pypi.org/project/travelpurpose/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Installation

```bash
pip install travelpurpose
```

## Quick Start

```python
from travelpurpose import predict_purpose, tags, search, load

# Load data once (auto-called on first use)
load()

# Predict travel purposes for any city
result = predict_purpose("Istanbul")
print(result["main"])        # ['Culture_Heritage', 'Transit_Gateway', 'Leisure']
print(result["sub"])         # ['UNESCO_Site', 'Old_Town', 'Mega_Air_Hub', 'Gastronomy']
print(result["confidence"])  # 0.86
```

---

## Features at a Glance

| Feature | Description |
|---------|-------------|
| **Purpose Prediction** | Main + sub travel purpose categories from city name |
| **Tag Extraction** | Fine-grained travel tags per city |
| **City Search** | Search cities by purpose keyword or tag |
| **Confidence Score** | 0–1 score per prediction |
| **Ontology-Based** | Structured category hierarchy (main → sub) |
| **NBD Mapping** | Network-based destination purpose enrichment |
| **Offline-Ready** | Local dataset — no API key needed |

---

## Purpose Categories

**Main Categories:**
- `Culture_Heritage` — museums, UNESCO sites, historical districts
- `Beach_Sun` — coastal resorts, beaches, water sports
- `Business_MICE` — conference centers, financial hubs
- `Nature_Adventure` — hiking, national parks, eco-tourism
- `Transit_Gateway` — hub airports, layover cities
- `Leisure` — entertainment, gastronomy, nightlife
- `Religious_Pilgrimage` — shrines, temples, sacred sites
- `Winter_Sports` — ski resorts, alpine destinations
- `Health_Wellness` — spa, thermal baths, medical tourism

**Example Sub-Categories:** `UNESCO_Site`, `Old_Town`, `Mega_Air_Hub`, `Gastronomy`, `Beach_Resort`, `Ski_Resort`, `Thermal_Spa`, `Festival_City`, `Cruise_Port`

---

## Predict Travel Purpose

```python
from travelpurpose import predict_purpose

# Major tourist city
result = predict_purpose("Paris")
print(result["main"])   # ['Culture_Heritage', 'Leisure', 'Business_MICE']
print(result["sub"])    # ['UNESCO_Site', 'Gastronomy', 'Fashion', 'City_Break']
print(result["confidence"])  # 0.91

# Beach destination
result = predict_purpose("Maldives")
print(result["main"])   # ['Beach_Sun', 'Leisure']
print(result["sub"])    # ['Beach_Resort', 'Luxury', 'Diving']

# Transit hub
result = predict_purpose("Dubai")
print(result["main"])   # ['Transit_Gateway', 'Leisure', 'Business_MICE']
print(result["sub"])    # ['Mega_Air_Hub', 'Shopping', 'Luxury']

# Winter destination
result = predict_purpose("Zermatt")
print(result["main"])   # ['Winter_Sports', 'Nature_Adventure']
print(result["sub"])    # ['Ski_Resort', 'Alpine', 'Scenic']
```

---

## Get City Tags

```python
from travelpurpose import tags

# Get raw travel tags for a city
city_tags = tags("Barcelona")
for tag in city_tags:
    print(f"  {tag['tag']:30s}  score={tag['score']:.2f}  source={tag['source']}")
# beach                          score=0.72  source=ontology
# architecture                   score=0.88  source=dataset
# gastronomy                     score=0.81  source=nbd
# UNESCO_Site                    score=0.76  source=ontology
# nightlife                      score=0.69  source=dataset
# ...

# Top tags only
top = [t for t in tags("Tokyo") if t["score"] > 0.7]
print([t["tag"] for t in top])
```

---

## Search Cities

```python
from travelpurpose import search

# Find cities by purpose or keyword
results = search("ski resort")
for city in results:
    print(f"{city['name']:20s}  purposes={city['main_purposes']}")
# Zermatt              purposes=['Winter_Sports', 'Nature_Adventure']
# Innsbruck            purposes=['Winter_Sports', 'Culture_Heritage']
# Whistler             purposes=['Winter_Sports', 'Nature_Adventure']

results = search("UNESCO heritage")
for city in results[:5]:
    print(city["name"])

# Search by tag
results = search("beach resort luxury")
```

---

## Batch Classification

```python
import pandas as pd
from travelpurpose import predict_purpose, load

load()

cities = ["Istanbul", "Paris", "Tokyo", "Maldives", "Dubai", "Zermatt", "Bali"]
records = []
for city in cities:
    r = predict_purpose(city)
    records.append({
        "city":       city,
        "purpose_1":  r["main"][0] if r["main"] else "",
        "purpose_2":  r["main"][1] if len(r["main"]) > 1 else "",
        "confidence": r["confidence"],
        "tags":       ", ".join(r["sub"][:4]),
    })

df = pd.DataFrame(records)
print(df.to_string(index=False))
#        city          purpose_1       purpose_2  confidence                       tags
#    Istanbul  Culture_Heritage  Transit_Gateway        0.86    UNESCO_Site, Old_Town, ...
#       Paris  Culture_Heritage          Leisure        0.91  UNESCO_Site, Gastronomy, ...
#       Tokyo  Culture_Heritage          Leisure        0.88       Gastronomy, Tech, ...
#    Maldives        Beach_Sun           Leisure        0.89    Beach_Resort, Luxury, ...
```

---

## Ontology Access

```python
from travelpurpose.classifier import get_ontology

# Inspect the category hierarchy
ontology = get_ontology()
print(ontology["main_categories"])
# ['Culture_Heritage', 'Beach_Sun', 'Business_MICE', 'Nature_Adventure', ...]

print(ontology["tag_mappings"]["UNESCO_Site"])
# {'main': 'Culture_Heritage', 'sub': 'UNESCO_Site', 'weight': 0.9}
```

---

## Available Cities

```python
from travelpurpose.classifier import get_available_cities

cities = get_available_cities()
print(f"Cities in dataset: {len(cities)}")
print(cities[:10])
# ['Amsterdam', 'Athens', 'Bali', 'Bangkok', 'Barcelona', 'Beijing', 'Berlin', ...]
```

---

## Integration Example

```python
from travelpurpose import predict_purpose, load

load()

def classify_itinerary(destinations: list[str]) -> dict:
    """Classify a multi-city trip by dominant purpose."""
    purpose_counts = {}
    for dest in destinations:
        result = predict_purpose(dest)
        for purpose in result["main"]:
            purpose_counts[purpose] = purpose_counts.get(purpose, 0) + 1

    dominant = max(purpose_counts, key=purpose_counts.get)
    return {
        "destinations": destinations,
        "dominant_purpose": dominant,
        "breakdown": purpose_counts,
    }

trip = classify_itinerary(["Istanbul", "Athens", "Rome", "Barcelona"])
print(trip["dominant_purpose"])   # Culture_Heritage
print(trip["breakdown"])
# {'Culture_Heritage': 4, 'Leisure': 3, 'Transit_Gateway': 1}
```

---

## License

MIT — [Teyfik Öz](https://github.com/teyfikoz)
