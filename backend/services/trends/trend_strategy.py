import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

HOOK_DEFINITIONS = {
    "contrarian": {
        "type": "CONTRARIAN",
        "strategy": "Challenge the common consensus or assumption that everyone is currently taking for granted."
    },
    "data_driven": {
        "type": "DATA_DRIVEN",
        "strategy": "Anchor the hook with exact benchmark numbers, latency drops, or parameter ratios."
    },
    "curiosity": {
        "type": "CURIOSITY",
        "strategy": "Open an information gap highlighting a surprising, non-obvious consequence."
    },
    "breaking_news": {
        "type": "BREAKING_NEWS",
        "strategy": "Fast, high-impact milestone announcement focusing strictly on verified facts."
    },
    "educational": {
        "type": "EDUCATIONAL",
        "strategy": "Break down the architectural mechanism so builders understand what just changed under the hood."
    },
    "prediction": {
        "type": "PREDICTION",
        "strategy": "Project where this trajectory leads 6 months out for production toolchains."
    },
    "comparison": {
        "type": "COMPARISON",
        "strategy": "Direct architectural side-by-side contrasting frontier closed APIs vs open-weights alternatives."
    },
    "question": {
        "type": "QUESTION",
        "strategy": "Frame an authentic technical dilemma presenting two opposing architectural philosophies."
    },
    "story": {
        "type": "STORY",
        "strategy": "Narrative arc tracing how the team solved an intractable engineering bottleneck."
    },
    "surprise": {
        "type": "SURPRISE",
        "strategy": "Lead with the counter-intuitive metric that defies standard industry expectations."
    }
}

class TrendStrategyEngine:
    """
    Deterministic rule-based strategy synthesizer for angles, hooks, and formats.
    Provides immediate zero-latency strategic guidance and serves as the baseline for Gemini.
    """

    @classmethod
    def synthesize_strategy(
        cls,
        trend_name: str,
        category: str,
        under_served_angles: List[str],
        primary_audience: str,
        lifecycle_stage: str,
        has_benchmarks: bool = False
    ) -> Dict[str, Any]:
        """
        Generates recommended angle, hook strategy, and format suitability scores.
        """
        # 1. Recommended Angle (Prioritize under-served white space)
        if under_served_angles:
            chosen_angle_name = under_served_angles[0]
            recommended_angle = f"Focus on {chosen_angle_name}: Explain how this development shifts developer unit economics and daily production workflows."
            alternative_angles = [
                f"Angle: {a} — highlight practical implications for {primary_audience}."
                for a in under_served_angles[1:4]
            ]
        else:
            recommended_angle = f"Analyze developer architectural tradeoffs: How {trend_name} impacts real-world latency jitter and token economics."
            alternative_angles = [
                "Challenge prevailing benchmark interpretations with empirical caveats.",
                "Ecosystem analysis: Who gains defensive leverage and who loses their moat."
            ]

        # 2. Hook Intelligence
        if has_benchmarks or "benchmark" in trend_name.lower():
            hook_info = HOOK_DEFINITIONS["data_driven"]
        elif lifecycle_stage in ("EXPLODING", "PEAK"):
            hook_info = HOOK_DEFINITIONS["contrarian"]
        elif lifecycle_stage == "EMERGING":
            hook_info = HOOK_DEFINITIONS["curiosity"]
        else:
            hook_info = HOOK_DEFINITIONS["educational"]

        # 3. Format Intelligence
        # Calculate suitability scores for each format (0-100)
        format_scores = {
            "single_post": 92 if lifecycle_stage in ("EXPLODING", "BREAKING") else 82,
            "thread": 94 if has_benchmarks or lifecycle_stage in ("RISING", "PEAK") else 78,
            "chart": 88 if has_benchmarks else 65,
            "question": 84 if lifecycle_stage in ("SATURATED", "PEAK") else 70,
            "short_video": 72,
            "poll": 68 if lifecycle_stage in ("SATURATED", "PEAK") else 50
        }

        # Pick best format
        best_format = max(format_scores.items(), key=lambda x: x[1])[0]

        return {
            "recommended_angle": recommended_angle,
            "alternative_angles": alternative_angles,
            "recommended_hook_type": hook_info["type"],
            "hook_strategy": hook_info["strategy"],
            "recommended_format": best_format,
            "format_scores": format_scores
        }

trend_strategy_engine = TrendStrategyEngine()
