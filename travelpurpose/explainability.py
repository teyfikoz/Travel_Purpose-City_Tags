"""
TravelPurpose Explainability Layer v2.0
"""
import math
from typing import Dict, List, Any

class ExplainabilityEngine:
    @staticmethod
    def decompose_confidence(
        source_agreement: float = 0.0,
        ontology_strength: float = 0.0,
        tag_density: float = 0.0,
        authority_weight: float = 0.0,
        ambiguity_penalty: float = 0.0
    ) -> Dict[str, float]:
        components = {
            "source_agreement": source_agreement,
            "ontology_strength": ontology_strength,
            "tag_density": tag_density,
            "authority_weight": authority_weight,
            "ambiguity_penalty": -ambiguity_penalty
        }

        total_positive = sum(v for v in components.values() if v > 0)
        if total_positive > 0:
            for key in components:
                if components[key] > 0:
                    components[key] = components[key] / total_positive

        return components

    @staticmethod
    def calculate_ambiguity(probabilities: List[float]) -> float:
        if not probabilities or len(probabilities) == 1:
            return 0.0

        total = sum(probabilities)
        if total <= 0:
            return 1.0

        probs = [p / total for p in probabilities]
        entropy = -sum(p * math.log2(p) for p in probs if p > 0)
        max_entropy = math.log2(len(probs))

        return entropy / max_entropy if max_entropy > 0 else 0.0

    @staticmethod
    def generate_explanation(
        city: str,
        prediction: Dict,
        confidence_breakdown: Dict[str, float],
        ambiguity_score: float,
        supporting_tags: List[str] = None
    ) -> Dict[str, Any]:
        reasons = []

        if confidence_breakdown.get('source_agreement', 0) > 0.2:
            reasons.append(f"High cross-source agreement")

        if confidence_breakdown.get('authority_weight', 0) > 0.15:
            reasons.append(f"UNESCO/Heritage site boost")

        if supporting_tags:
            reasons.append(f"Supported by tags: {', '.join(supporting_tags[:5])}")

        if ambiguity_score > 0.6:
            reasons.append(f"⚠️ High ambiguity - city serves multiple purposes")

        return {
            "city": city,
            "explanation": {
                "reasons": reasons,
                "confidence_breakdown": confidence_breakdown,
                "ambiguity_score": round(ambiguity_score, 4),
                "supporting_tags": supporting_tags or []
            }
        }
