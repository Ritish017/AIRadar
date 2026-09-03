import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class TrendOpportunityEngine:
    """
    Deterministic Content Opportunity Engine:
    Evaluates where momentum, novelty, audience fit, and competitive white-space align
    to create high-leverage posting opportunities.
    """

    @classmethod
    def calculate_opportunity_score(
        cls,
        momentum_score: float,       # 0-100
        freshness_score: float,      # 0-100
        novelty_score: float,        # 0-100
        audience_fit_score: float,   # 0-100
        discussion_score: float,     # 0-100
        importance_score: float,     # 0-100
        source_quality_score: float, # 0-100
        competition_score: float     # 0-100
    ) -> float:
        """
        Formula:
        opportunity_score =
          momentum * 0.22 +
          freshness * 0.15 +
          novelty * 0.15 +
          audience_fit * 0.15 +
          discussion_potential * 0.10 +
          importance * 0.10 +
          source_quality * 0.05 +
          competition_inverse * 0.08
        """
        comp_inverse = max(0.0, 100.0 - competition_score)

        raw = (
            momentum_score * 0.22 +
            freshness_score * 0.15 +
            novelty_score * 0.15 +
            audience_fit_score * 0.15 +
            discussion_score * 0.10 +
            importance_score * 0.10 +
            source_quality_score * 0.05 +
            comp_inverse * 0.08
        )
        return round(min(100.0, max(15.0, raw)), 1)

    @classmethod
    def classify_opportunity(
        cls,
        opportunity_score: float,
        lifecycle_stage: str,
        momentum_change_pct: float,
        competition_score: float,
        novelty_score: float,
        audience_fit_score: float,
        age_hours: float = 6.0
    ) -> TupleType:
        """
        Returns (opportunity_type, recommended_action, action_reason)
        """
        # 1. SKIP / DECLINING
        if lifecycle_stage in ("DECLINING", "DEAD") or opportunity_score < 40.0:
            return (
                "DECLINING" if lifecycle_stage == "DECLINING" else "SKIP",
                "SKIP",
                "Trend momentum is declining or dead with low audience leverage. Skip."
            )

        # 2. OVERSATURATED
        if lifecycle_stage == "SATURATED" or (competition_score >= 70.0 and novelty_score < 60.0):
            return (
                "OVERSATURATED",
                "WAIT",
                "High public attention but generic angles are severely overcrowded. Wait for a unique angle or new benchmark."
            )

        # 3. BREAKING
        if age_hours <= 3.0 and momentum_change_pct >= 50.0 and opportunity_score >= 80.0:
            return (
                "BREAKING",
                "POST_NOW",
                "Breaking milestone in its initial surge. Post immediately to capture early engagement momentum."
            )

        # 4. EXPLODING / HIGH_REACH
        if lifecycle_stage == "EXPLODING" or (momentum_change_pct >= 40.0 and opportunity_score >= 85.0):
            return (
                "HIGH_REACH",
                "POST_NOW",
                "Momentum is accelerating rapidly with broad multi-source reach and moderate competition. Post now."
            )

        # 5. EARLY_DISCOVERY
        if lifecycle_stage == "EMERGING" and novelty_score >= 80.0 and competition_score <= 45.0:
            return (
                "EARLY_DISCOVERY",
                "POST_SOON",
                "Early technical discovery not yet widely saturated. Publish soon with an educational or builder angle."
            )

        # 6. NICHE_HIGH_VALUE
        if audience_fit_score >= 85.0 and competition_score <= 40.0:
            return (
                "NICHE_HIGH_VALUE",
                "POST_SOON",
                "Highly targeted to technical practitioners with low competitive noise. High conversion value."
            )

        # 7. RISING_OPPORTUNITY (Default strong)
        if opportunity_score >= 70.0:
            return (
                "RISING_OPPORTUNITY",
                "POST_SOON",
                "Solid upward momentum across sources. Good window to share a differentiated technical takeaway."
            )

        return (
            "WATCH",
            "WATCH",
            "Moderate interest developing. Watch for further community traction before publishing."
        )

TupleType = tuple[str, str, str]
trend_opportunity_engine = TrendOpportunityEngine()
