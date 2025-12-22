"""
TravelPurpose Temporal/Seasonal Support v2.0
"""
from typing import Dict, Optional

class TemporalEngine:
    SEASONS = {
        "winter": [12, 1, 2],
        "spring": [3, 4, 5],
        "summer": [6, 7, 8],
        "fall": [9, 10, 11]
    }

    @staticmethod
    def get_season(month: int) -> str:
        for season, months in TemporalEngine.SEASONS.items():
            if month in months:
                return season
        return "all"

    @staticmethod
    def apply_seasonal_boost(
        purposes: Dict[str, float],
        season: Optional[str] = None,
        month: Optional[int] = None
    ) -> Dict[str, float]:
        if month:
            season = TemporalEngine.get_season(month)

        if not season or season == "all":
            return purposes

        # Seasonal boosts
        seasonal_boosts = {
            "winter": {"Winter_Sports": 1.5, "Medical_Health": 1.2},
            "summer": {"Beach_Resort": 1.4, "Nature_Outdoor": 1.3},
            "spring": {"Nature_Outdoor": 1.2, "Event_Festival": 1.1},
            "fall": {"Culture_Heritage": 1.1, "Gastronomy": 1.2}
        }

        boosted = purposes.copy()
        if season in seasonal_boosts:
            for category, boost in seasonal_boosts[season].items():
                if category in boosted:
                    boosted[category] *= boost

        # Renormalize
        total = sum(boosted.values())
        if total > 0:
            boosted = {k: v/total for k, v in boosted.items()}

        return boosted
