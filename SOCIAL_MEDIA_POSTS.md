# TravelPurpose v0.1.0 - Sosyal Medya Paylaşımları

## 📱 WhatsApp Mesajı (Kısa & Samimi)

```
🚀 Yeni proje yayında!

TravelPurpose - Şehir Seyahat Amacı Sınıflandırma Kütüphanesi

✨ Özellikler:
• 9 veri kaynağından şehir etiketleri
• 12 ana kategori (İş, Tatil, Kültür, Plaj, Macera...)
• 70+ alt kategori
• Ülke bilgileri ve ISO kodları
• Python API + CLI

📦 PyPI'den kurulum:
pip install travelpurpose

🔗 GitHub: github.com/teyfikoz/Travel_Purpose-City_Tags

Örnek kullanım:
from travelpurpose import predict_purpose
result = predict_purpose("Istanbul")
# {'main': ['Culture_Heritage', 'Transit_Gateway'], ...}

MIT lisanslı, açık kaynak! 🎉
```

---

## 💼 LinkedIn Paylaşımı (Profesyonel)

```
🎉 Announcing TravelPurpose v0.1.0 - Open Source City Travel Purpose Classification Library

I'm excited to share my latest project: a production-ready Python library that classifies world cities by travel purpose using multi-source public data.

🔍 What is TravelPurpose?
TravelPurpose aggregates data from 9 public sources to automatically classify cities across 12 main categories and 70+ subcategories, helping developers, researchers, and travel tech companies understand travel patterns.

📊 Key Features:
✅ Multi-source data aggregation (Wikidata, Booking.com, Agoda, GeoNames, OpenTripMap, RestCountries, and more)
✅ 12 main categories: Business, Leisure, Culture & Heritage, Beach Resort, Adventure & Nature, Family, Medical Health, Religious Pilgrimage, Winter Sports, Nightlife, Transit Gateway, Seaman Crew
✅ 70+ specialized subcategories
✅ Country enrichment with ISO codes and regional data
✅ Multi-label classification with confidence scoring
✅ Both Python API and CLI interface
✅ Ethical data collection (ToS compliant, rate-limited, robots.txt compliant)

🛠️ Tech Stack:
• Python 3.10+
• Pandas, PyArrow for data processing
• BeautifulSoup, Requests for web scraping
• SPARQL for Wikidata integration
• Typer for CLI

📦 Installation:
```pip install travelpurpose```

💻 Quick Example:
```python
from travelpurpose import predict_purpose

result = predict_purpose("Paris")
print(result)
# {
#     'main': ['Culture_Heritage', 'Leisure', 'Business'],
#     'sub': ['UNESCO_Site', 'Museums', 'Gastronomy'],
#     'confidence': 0.89
# }
```

🔗 Links:
• PyPI: https://pypi.org/project/travelpurpose/
• GitHub: https://github.com/teyfikoz/Travel_Purpose-City_Tags
• Documentation: Full README with examples

🎯 Use Cases:
- Travel recommendation systems
- Tourism market analysis
- Destination planning tools
- Route optimization
- Business intelligence for travel industry

🌍 This project aims to democratize access to structured travel data for developers and researchers worldwide. All data is collected ethically from public sources with full transparency.

💡 Special thanks to the open data communities: Wikidata, OpenStreetMap, GeoNames, and all the travel platforms that make their data publicly accessible.

⭐ If you find this useful, please star the repo and share with your network!

#OpenSource #Python #DataScience #TravelTech #MachineLearning #API #PyPI #DataEngineering #TourismTechnology #SoftwareDevelopment

---

🤝 Contributions welcome! Check out the repository for contribution guidelines.

License: MIT
```

---

## 📧 Email Duyurusu (Profesyonel & Detaylı)

**Konu:** Announcing TravelPurpose v0.1.0 - Open Source City Classification Library

```
Hi [Name/Team],

I'm excited to announce the release of TravelPurpose v0.1.0, an open-source Python library for classifying world cities by travel purpose.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📦 WHAT IS TRAVELPURPOSE?

TravelPurpose is a production-grade Python library that automatically classifies cities across multiple travel-related categories by aggregating data from 9 public sources including Wikidata, travel platforms, and geographic databases.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ KEY FEATURES

Data Sources (9):
• Wikidata - Canonical city data & UNESCO sites
• Booking.com - Accommodation tags
• Agoda - Travel preferences
• Trivago - City districts
• Kayak - Travel guides
• Trip.com - Attractions
• GeoNames - Geographic features
• OpenTripMap - Tourist POIs
• RestCountries - Country metadata

Classification System:
• 12 main categories (Business, Leisure, Culture & Heritage, Beach Resort, etc.)
• 70+ subcategories (Finance Hub, UNESCO Site, Ski Resort, etc.)
• Multi-label predictions
• Confidence scoring (0.0-1.0)

Data Model:
• City name, country, population
• Coordinates (latitude, longitude)
• Country ISO codes (alpha-2, alpha-3)
• Regional classification
• Travel purpose classification
• Source attribution for all tags

Ethics & Compliance:
✓ All data from public sources
✓ ToS-compliant collection
✓ Rate limiting (configurable)
✓ Robots.txt compliance
✓ Full transparency & attribution
✓ No personal data collection

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 INSTALLATION & USAGE

Installation:
```bash
pip install travelpurpose
```

Python API:
```python
from travelpurpose import predict_purpose, tags, search

# Predict travel purposes
result = predict_purpose("Tokyo")
print(result)
# {
#     'main': ['Business', 'Culture_Heritage', 'Transit_Gateway'],
#     'sub': ['Tech_Hub', 'Mega_Air_Hub', 'Gastronomy'],
#     'confidence': 0.91
# }

# Get raw tags
city_tags = tags("Barcelona")

# Search cities
results = search("spain")
```

Command Line:
```bash
# Predict city purposes
tpurpose predict "Dubai"

# Show tags
tpurpose show-tags "Paris" --limit 20

# Search cities
tpurpose find "italy"

# Rebuild dataset
tpurpose rebuild --sample 100 --verbose
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 USE CASES

• Travel Recommendation Systems
• Tourism Market Analysis
• Destination Planning Tools
• Route Optimization
• Business Intelligence for Travel Industry
• Academic Research
• Data Science Projects

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 TECHNICAL SPECS

• Language: Python 3.10+
• License: MIT
• Package Size: 84 KB
• Dependencies: 17 core libraries
• Test Coverage: Comprehensive unit tests
• CI/CD: GitHub Actions
• Distribution: PyPI

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔗 LINKS

• PyPI Package: https://pypi.org/project/travelpurpose/
• GitHub Repository: https://github.com/teyfikoz/Travel_Purpose-City_Tags
• Documentation: See README.md
• Issues & Discussions: GitHub Issues

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🤝 CONTRIBUTING

Contributions are welcome! Areas for contribution:
• Adding new data sources (must be public & ToS-compliant)
• Expanding the ontology
• Improving classification accuracy
• Adding language support
• Documentation improvements

Please see CONTRIBUTING.md in the repository.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 CITATION

If you use TravelPurpose in your research:

@software{travelpurpose2025,
  title = {TravelPurpose: City Travel Purpose Classification Library},
  author = {Travel Purpose Contributors},
  year = {2025},
  url = {https://github.com/teyfikoz/Travel_Purpose-City_Tags}
}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⭐ If you find this project useful, please:
• Star the GitHub repository
• Share with your network
• Report issues or suggest features
• Consider contributing

Thank you for your interest in TravelPurpose!

Best regards,
Teyfik Öz

---
GitHub: github.com/teyfikoz
Project: github.com/teyfikoz/Travel_Purpose-City_Tags
```

---

## 🐦 Twitter/X Paylaşımı (Kısa)

```
🚀 Just launched TravelPurpose v0.1.0!

Open-source Python library for city travel purpose classification

✨ 9 data sources
📊 12 categories, 70+ subcategories
🌍 Country enrichment
🐍 pip install travelpurpose

GitHub: github.com/teyfikoz/Travel_Purpose-City_Tags
PyPI: pypi.org/project/travelpurpose/

#Python #OpenSource #TravelTech #DataScience
```

---

## 📱 Instagram Story Metni

```
🎉 NEW PROJECT ALERT

TravelPurpose v0.1.0
City Classification Library 🌍

🔹 9 Data Sources
🔹 12 Categories
🔹 70+ Subcategories
🔹 Open Source
🔹 MIT Licensed

pip install travelpurpose

Link in bio 👆
#Python #OpenSource #Travel
```

---

## 📰 Medium/Blog Başlığı ve Giriş

**Başlık:**
"Building TravelPurpose: An Open-Source City Classification Library from 9 Public Data Sources"

**Alt Başlık:**
"How I built a production-ready Python library that aggregates travel data from Wikidata, booking platforms, and geographic APIs"

**Giriş Paragrafı:**
```
Understanding why people travel to specific cities is crucial for travel recommendation systems, tourism analysis, and destination planning. But collecting and structuring this data from multiple sources is time-consuming and complex.

That's why I built TravelPurpose—an open-source Python library that automatically classifies world cities by travel purpose, aggregating data from 9 public sources including Wikidata, major travel platforms, and geographic databases.

In this article, I'll share:
• The architecture and design decisions
• How to ethically collect data from public sources
• Multi-source data aggregation challenges
• The classification system (12 categories, 70+ subcategories)
• How you can use it in your projects

Let's dive in! 🚀
```

---

## 📋 README Badge'ları (GitHub için)

```markdown
[![PyPI version](https://badge.fury.io/py/travelpurpose.svg)](https://badge.fury.io/py/travelpurpose)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/travelpurpose)](https://pepy.tech/project/travelpurpose)
[![GitHub stars](https://img.shields.io/github/stars/teyfikoz/Travel_Purpose-City_Tags.svg)](https://github.com/teyfikoz/Travel_Purpose-City_Tags/stargazers)
```

---

## Kullanım Talimatları:

1. **WhatsApp:** Direkt kopyala-yapıştır
2. **LinkedIn:** Profile yapıştır, hashtag'leri düzenle, görsel ekle
3. **Email:** Alıcı listesine göre özelleştir
4. **Twitter:** 280 karakter limitine dikkat et
5. **Instagram:** Story için görsel hazırla
6. **Medium:** Detaylı makale olarak genişlet

Başarılar! 🚀
