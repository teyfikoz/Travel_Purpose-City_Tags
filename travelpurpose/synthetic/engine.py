"""
Synthetic City Purpose Generator
"""
from dataclasses import dataclass
import random
import math
from typing import Dict, List
import json

@dataclass
class SyntheticCityConfig:
    seed: int = 42
    n_cities: int = 500
    region: str = "Europe"
    seasonal_variance: float = 0.2
    authority_boost: float = 1.3
    output_path: str = "synthetic_cities.jsonl"

class SyntheticCityEngine:
    def __init__(self, rng_seed: int = 42):
        self.rng = random.Random(rng_seed)

    def generate_city(self, base_distribution: Dict[str, float]) -> Dict:
        city_profile = {}
        for category, prob in base_distribution.items():
            noise = self.rng.uniform(-0.1, 0.1)
            city_profile[category] = max(0.0, prob + noise)

        total = sum(city_profile.values())
        if total > 0:
            for k in city_profile:
                city_profile[k] /= total

        return city_profile

    def generate(self, base_distribution: Dict[str, float], n: int) -> List[Dict]:
        return [
            {
                "city_id": f"synthetic_{i}",
                "purpose_profile": self.generate_city(base_distribution),
                "entropy": self._entropy(self.generate_city(base_distribution))
            }
            for i in range(n)
        ]

    def _entropy(self, dist: Dict[str, float]) -> float:
        return -sum(p * math.log(p + 1e-9) for p in dist.values() if p > 0)

    def export(self, cities: List[Dict], output_path: str):
        with open(output_path, 'w') as f:
            for city in cities:
                f.write(json.dumps(city) + '\n')
