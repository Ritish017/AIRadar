import logging
from typing import List, Dict, Any, Tuple

logger = logging.getLogger(__name__)

AUDIENCE_PERSONAS = [
    {
        "id": "ai_engineers",
        "name": "AI Engineers & ML Practitioners",
        "keywords": ["vllm", "weights", "fine-tuning", "rag", "quantization", "latency", "tokens/sec", "cuda", "evals"],
        "reason": "Directly impacts production model serving, framework selection, and engineering tradeoffs."
    },
    {
        "id": "developers",
        "name": "Software Engineers & Builders",
        "keywords": ["cursor", "copilot", "coding", "agent", "ide", "api", "sdk", "github", "swe-bench", "python"],
        "reason": "Alters developer daily workflows, software engineering toolchains, and autonomous agent loops."
    },
    {
        "id": "founders",
        "name": "Technical Founders & CTOs",
        "keywords": ["cost", "startup", "economics", "pricing", "moat", "enterprise", "scale", "infrastructure"],
        "reason": "Alters unit economics and infrastructure roadmap when scaling AI-native applications."
    },
    {
        "id": "researchers",
        "name": "AI Researchers & Academics",
        "keywords": ["arxiv", "paper", "architecture", "reasoning", "benchmark", "loss", "training", "dataset", "ablation"],
        "reason": "Presents novel architecture paradigms, mathematical benchmark proofs, or empirical breakthroughs."
    },
    {
        "id": "business_leaders",
        "name": "Enterprise Leaders & Investors",
        "keywords": ["market", "valuation", "adoption", "nvidia", "cloud", "procurement", "governance", "roi"],
        "reason": "Shifts enterprise vendor evaluation, capital allocation, and competitive positioning."
    },
    {
        "id": "general_tech",
        "name": "General Tech & AI Enthusiasts",
        "keywords": ["unveils", "chatgpt", "gemini", "claude", "superhuman", "future", "robot", "agi", "demo"],
        "reason": "High-interest mainstream milestone capturing broader fascination with autonomous intelligence."
    }
]

class TrendAudienceEngine:
    """
    Identifies target audience personas and scores resonance fit for content opportunities.
    """

    @classmethod
    def evaluate_audience(cls, title: str, content: str, category: str = "AI Models") -> Dict[str, Any]:
        combined = f"{title} {content} {category}".lower()
        scores: List[Tuple[Dict[str, Any], int]] = []

        for persona in AUDIENCE_PERSONAS:
            match_count = sum(1 for kw in persona["keywords"] if kw in combined)
            scores.append((persona, match_count))

        # Sort by matches
        scores.sort(key=lambda x: x[1], reverse=True)

        primary_persona, primary_matches = scores[0]
        # Base primary match
        if primary_matches == 0:
            primary_persona = AUDIENCE_PERSONAS[0]  # Default to AI Engineers

        secondary = [p["name"] for p, m in scores[1:3] if m > 0]
        if not secondary:
            secondary = [AUDIENCE_PERSONAS[1]["name"], AUDIENCE_PERSONAS[2]["name"]]

        # Fit score: base 60 + matches * 8
        fit_score = round(min(98.0, max(55.0, 65.0 + primary_matches * 6.5)), 1)

        return {
            "primary_audience": primary_persona["name"],
            "secondary_audiences": secondary,
            "audience_fit_score": fit_score,
            "audience_fit_reason": primary_persona["reason"]
        }

trend_audience_engine = TrendAudienceEngine()
