import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class TrendLifecycleEngine:
    """
    Deterministic 7-Stage Trend Lifecycle Engine:
    EMERGING -> RISING -> EXPLODING -> PEAK -> SATURATED -> DECLINING -> DEAD

    Operates on measurable physical signals:
    - momentum_score (0-100)
    - momentum_change_pct (% growth)
    - momentum_direction (ACCELERATING / STABLE / DECELERATING / INSUFFICIENT HISTORY)
    - competition_score (0-100)
    - novelty_score (0-100)
    - item_count (volume)
    - source_count (cross-platform breadth)
    - age_hours (recency)
    """

    @staticmethod
    def determine_lifecycle(
        momentum_score: float,
        momentum_change_pct: float,
        momentum_direction: str,
        competition_score: float,
        novelty_score: float,
        item_count: int,
        source_count: int,
        age_hours: float = 6.0
    ) -> Dict[str, Any]:
        """
        Determines the current lifecycle stage and returns stage description and status badge.
        """
        # 1. DEAD
        if age_hours > 72.0 and momentum_score < 35.0 and item_count <= 2:
            return {
                "stage": "DEAD",
                "badge": "💀 Dead",
                "reason": "Activity has ceased with negligible new discussion over 72 hours."
            }

        # 2. SATURATED
        if (competition_score >= 65.0 and item_count >= 7 and novelty_score <= 65.0) or (item_count >= 12 and momentum_direction == "DECELERATING"):
            return {
                "stage": "SATURATED",
                "badge": "🛑 Saturated",
                "reason": "Market is flooded with repetitive commentary; angle novelty has depleted."
            }

        # 3. DECLINING
        if (momentum_direction == "DECELERATING" and momentum_change_pct <= -20.0) or (momentum_score < 45.0 and age_hours > 24.0 and item_count <= 3):
            return {
                "stage": "DECLINING",
                "badge": "📉 Declining",
                "reason": "Discussion velocity is dropping significantly as public attention shifts elsewhere."
            }

        # 4. EXPLODING
        if (momentum_score >= 75.0 and (momentum_change_pct >= 40.0 or item_count >= 5 and source_count >= 3)) or (momentum_direction == "ACCELERATING" and item_count >= 4):
            return {
                "stage": "EXPLODING",
                "badge": "🔥 Exploding",
                "reason": "Experiencing exponential multi-source growth across developer and news feeds."
            }

        # 5. PEAK
        if item_count >= 8 and (momentum_direction in ("DECELERATING", "STABLE") or momentum_change_pct <= 15.0):
            return {
                "stage": "PEAK",
                "badge": "⚡ Peak",
                "reason": "Reaching maximum attention saturation; velocity is beginning to plateau."
            }

        # 6. EMERGING (Early stage, low absolute volume, young age)
        if item_count <= 2 or (age_hours <= 12.0 and novelty_score >= 75.0 and source_count <= 2):
            return {
                "stage": "EMERGING",
                "badge": "🌱 Emerging",
                "reason": "Early-stage discovery with low absolute volume but high novelty and breakout potential."
            }

        # 7. RISING
        if (momentum_score >= 50.0 and item_count >= 3) or (momentum_change_pct > 15.0 and age_hours <= 48.0):
            return {
                "stage": "RISING",
                "badge": "📈 Rising",
                "reason": "Gaining steady momentum with cross-source validation and expanding interest."
            }

        return {
            "stage": "EMERGING",
            "badge": "🌱 Emerging",
            "reason": "Early-stage discovery with low absolute volume but high novelty and breakout potential."
        }

trend_lifecycle_engine = TrendLifecycleEngine()
