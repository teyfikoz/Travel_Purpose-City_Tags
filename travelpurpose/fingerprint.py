"""
City Purpose Fingerprint (CPF) v2.0
"""
import math
from typing import Dict
import numpy as np

class CityFingerprint:
    @staticmethod
    def create_fingerprint(purposes: Dict[str, float]) -> Dict:
        entropy = CityFingerprint._calculate_entropy(purposes)
        uniqueness = CityFingerprint._calculate_uniqueness(purposes)

        return {
            "main_categories": purposes,
            "entropy": round(entropy, 4),
            "uniqueness": round(uniqueness, 4)
        }

    @staticmethod
    def _calculate_entropy(dist: Dict[str, float]) -> float:
        probs = [p for p in dist.values() if p > 0]
        if not probs:
            return 0.0
        return -sum(p * math.log2(p) for p in probs)

    @staticmethod
    def _calculate_uniqueness(dist: Dict[str, float]) -> float:
        # High uniqueness = more extreme distribution
        max_val = max(dist.values()) if dist else 0
        return max_val

    @staticmethod
    def cosine_similarity(fp1: Dict, fp2: Dict) -> float:
        cats1 = fp1.get('main_categories', {})
        cats2 = fp2.get('main_categories', {})

        all_cats = set(cats1.keys()) | set(cats2.keys())
        v1 = np.array([cats1.get(c, 0) for c in all_cats])
        v2 = np.array([cats2.get(c, 0) for c in all_cats])

        dot = np.dot(v1, v2)
        norm1 = np.linalg.norm(v1)
        norm2 = np.linalg.norm(v2)

        if norm1 == 0 or norm2 == 0:
            return 0.0

        return float(dot / (norm1 * norm2))
