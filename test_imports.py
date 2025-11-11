#!/usr/bin/env python3
"""Quick import test to validate package structure."""

import sys
from pathlib import Path

# Add package to path
sys.path.insert(0, str(Path(__file__).parent))

print("Testing imports...")

try:
    # Test basic imports
    import travelpurpose
    print(f"✓ travelpurpose imported (version: {travelpurpose.__version__})")

    from travelpurpose import predict_purpose, tags, search, load
    print("✓ Main API functions imported")

    from travelpurpose.classifier import get_ontology
    print("✓ Classifier module imported")

    from travelpurpose.utils.io import load_ontology, load_nbd_mapping
    print("✓ I/O utilities imported")

    from travelpurpose.utils.normalize import normalize_city_name, normalize_tag
    print("✓ Normalization utilities imported")

    from travelpurpose.utils.scoring import calculate_tag_weights
    print("✓ Scoring utilities imported")

    from travelpurpose.utils.wikidata import WikidataClient
    print("✓ Wikidata client imported")

    from travelpurpose.utils.harvest import BaseHarvester
    print("✓ Harvest utilities imported")

    # Test loading ontology
    ontology = load_ontology()
    print(f"✓ Ontology loaded: {len(ontology.get('main_categories', []))} main categories")

    # Test loading NBD mapping
    nbd_mapping = load_nbd_mapping()
    print(f"✓ NBD mapping loaded: {len(nbd_mapping.get('nbd_to_main', {}))} mappings")

    print("\n✅ All imports successful!")
    print(f"\nPackage structure validated:")
    print(f"  - Main categories: {', '.join(ontology.get('main_categories', [])[:3])}...")
    print(f"  - Version: {travelpurpose.__version__}")

except Exception as e:
    print(f"\n❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
