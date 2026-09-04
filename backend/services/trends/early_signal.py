"""
V3 Early Signal Engine:
Detects nascent AI breakthroughs before mainstream saturation.
Calculates EarlySignalScore, Explosion Probability, and Trajectory Forecasts.
"""

import math
import logging
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class EarlySignalTelemetry(BaseModel):
    is_early_signal: bool = False
    early_signal_score: float = 0.0  # 0 to 100
    explosion_probability: float = 0.0  # 0 to 100%
    probability_label: str = "MODEL ESTIMATE (High probability of continued growth)"
    probability_disclaimer: str = "Probabilistic estimation based on mention acceleration, low competition, and source authority. Never a guarantee of viral reach."
    trajectory: str = "STEADY"  # EXPLODING, ACCELERATING, STEADY, NICHE
    catalyst_type: str = "Technical Breakthrough"
    underserved_ratio: float = 0.0
    rationale: str = ""

class EarlySignalEngine:
    """
    Identifies high-conviction early signals before they hit mainstream saturation.
    Evaluates growth velocity, source authority, low competitive crowding, and novelty.
    """

    def evaluate_early_signal(
        self,
        mention_count: int,
        acceleration_pct: float,
        momentum_score: float,
        competition_score: float,
        novelty_score: float,
        source_diversity: int,
        has_tier1_source: bool = True
    ) -> EarlySignalTelemetry:
        """
        Computes early signal score and explosion probability.
        
        Conditions for High Early Signal:
        - Small current signal (<= 30 mentions)
        - High growth / acceleration (> +50%)
        - Low competition (< 45)
        - High novelty (> 75)
        - Authoritative sources (>= 2 sources with Tier 1/2 presence)
        """
        # 1. Base Early Signal Score
        # Novelty component (30%)
        novelty_comp = (novelty_score / 100.0) * 30.0
        
        # Acceleration component (30%)
        norm_accel = min(150.0, max(0.0, acceleration_pct)) / 150.0
        accel_comp = norm_accel * 30.0
        
        # Low competition advantage (25%)
        comp_advantage = max(0.0, 100.0 - competition_score) / 100.0
        comp_comp = comp_advantage * 25.0
        
        # Source authority boost (15%)
        src_comp = min(1.0, source_diversity / 4.0) * (15.0 if has_tier1_source else 8.0)
        
        signal_score = min(99.0, max(10.0, novelty_comp + accel_comp + comp_comp + src_comp))

        # 2. Explosion Probability Formula
        # Non-linear probability based on low competition + high acceleration + low baseline mentions
        is_nascent = mention_count <= 35
        prob_base = (signal_score * 0.6) + (norm_accel * 30.0) + (10.0 if is_nascent else 0.0)
        
        # Dampen if already crowded
        if competition_score > 65:
            prob_base -= (competition_score - 65) * 0.8

        explosion_prob = round(min(96.0, max(5.0, prob_base)), 1)

        # 3. Trajectory Verdict
        if explosion_prob >= 75.0 and acceleration_pct >= 80.0:
            trajectory = "EXPLODING"
            is_early = True
            rationale = f"High acceleration (+{acceleration_pct:.0f}%) with low competition ({competition_score:.0f}/100) indicates imminent breakout."
        elif explosion_prob >= 60.0 or acceleration_pct >= 40.0:
            trajectory = "ACCELERATING"
            is_early = True
            rationale = "Multi-source interest building steadily; ideal window for first-mover commentary."
        elif competition_score < 30.0 and novelty_score >= 80.0:
            trajectory = "NICHE"
            is_early = False
            rationale = "High novelty technical topic with specialized builder interest."
        else:
            trajectory = "STEADY"
            is_early = False
            rationale = "Standard development pacing without acute viral acceleration."

        return EarlySignalTelemetry(
            is_early_signal=is_early,
            early_signal_score=round(signal_score, 1),
            explosion_probability=explosion_prob,
            trajectory=trajectory,
            catalyst_type="Open Weights Release" if novelty_score > 85 else "Benchmark Leap",
            underserved_ratio=round(comp_advantage, 2),
            rationale=rationale
        )

early_signal_engine = EarlySignalEngine()
