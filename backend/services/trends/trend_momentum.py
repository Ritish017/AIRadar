import math
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple

class TrendMomentumEngine:
    """
    Evaluates real temporal momentum and acceleration by comparing historical observation snapshots.
    Never fabricates historical data. Displays 'INSUFFICIENT HISTORY' when baseline snapshots are lacking.
    """

    @staticmethod
    def calculate_base_snapshot_momentum(
        item_count: int,
        source_count: int,
        source_diversity: int,
        avg_viral_potential: float = 75.0
    ) -> float:
        """Computes snapshot point density on a 0-100 scale."""
        volume_pts = min(40.0, item_count * 10.0)
        source_pts = min(30.0, source_count * 10.0 + source_diversity * 5.0)
        potential_pts = (avg_viral_potential / 100.0) * 30.0
        return round(min(100.0, volume_pts + source_pts + potential_pts), 1)

    @classmethod
    def evaluate_momentum(
        cls,
        current_mentions: int,
        current_sources: int,
        current_diversity: int,
        avg_potential: float,
        history: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Calculates:
        - momentum_score: 0-100
        - momentum_change_pct: percentage change from previous window
        - momentum_direction: ACCELERATING | STABLE | DECELERATING | INSUFFICIENT HISTORY
        - acceleration_rate: second-derivative acceleration factor
        """
        base_momentum = cls.calculate_base_snapshot_momentum(
            current_mentions, current_sources, current_diversity, avg_potential
        )

        if not history or len(history) < 1:
            return {
                "momentum_score": base_momentum,
                "momentum_change_pct": 0.0,
                "momentum_direction": "INSUFFICIENT HISTORY",
                "acceleration_rate": 0.0,
                "observation_count": 1
            }

        # Sort history by timestamp ascending
        sorted_history = sorted(
            history,
            key=lambda x: x.get("timestamp") or datetime.min.replace(tzinfo=timezone.utc)
        )
        prev_obs = sorted_history[-1]
        prev_mentions = max(1, prev_obs.get("mention_count", 1))

        # 1. First Derivative: Velocity (% change in mentions)
        mention_delta = current_mentions - prev_mentions
        change_pct = round((mention_delta / prev_mentions) * 100.0, 1)

        # 2. Second Derivative: Acceleration (change in velocity)
        acceleration_rate = 0.0
        if len(sorted_history) >= 2:
            prev_prev_obs = sorted_history[-2]
            prev_prev_mentions = max(1, prev_prev_obs.get("mention_count", 1))
            prev_change_pct = ((prev_mentions - prev_prev_mentions) / prev_prev_mentions) * 100.0
            acceleration_rate = round(change_pct - prev_change_pct, 1)
        else:
            acceleration_rate = change_pct

        # 3. Direction Classification
        if (change_pct >= 30.0 and acceleration_rate >= -15.0) or (change_pct >= 60.0):
            direction = "ACCELERATING"
        elif change_pct <= -20.0 or (change_pct < 0.0 and acceleration_rate < -25.0):
            direction = "DECELERATING"
        else:
            direction = "STABLE"

        # 4. Composite Momentum Score (0-100)
        # Scales based on volume density and positive rate of growth
        growth_bonus = min(30.0, max(-20.0, change_pct * 0.25))
        composite_score = round(min(100.0, max(10.0, base_momentum * 0.70 + (50.0 + growth_bonus) * 0.30)), 1)

        return {
            "momentum_score": composite_score,
            "momentum_change_pct": change_pct,
            "momentum_direction": direction,
            "acceleration_rate": acceleration_rate,
            "observation_count": len(history) + 1
        }

trend_momentum_engine = TrendMomentumEngine()
