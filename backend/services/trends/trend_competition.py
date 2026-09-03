import re
import logging
from typing import List, Dict, Any, Tuple
from rapidfuzz import fuzz

logger = logging.getLogger(__name__)

ANGLE_TAXONOMY = [
    {
        "id": "generic_announcement",
        "name": "Headline News & Generic Announcement",
        "keywords": ["announces", "releases", "launches", "unveils", "breaking", "new model", "out now"],
        "description": "Standard headline reposting what happened without deep analysis."
    },
    {
        "id": "benchmark_interpretation",
        "name": "Benchmark & Performance Evaluation",
        "keywords": ["benchmark", "swe-bench", "humaneval", "math", "mmlu", "score", "beats", "outperforms", "accuracy"],
        "description": "Examining whether benchmark claims hold up and comparing against rivals."
    },
    {
        "id": "developer_economics",
        "name": "Developer Economics & Latency Jitter",
        "keywords": ["cost", "tokens/sec", "latency", "pricing", "api", "inference", "throughput", "vllm", "groq"],
        "description": "How inference costs, token pricing, and sub-second latency alter software architecture."
    },
    {
        "id": "architecture_weights",
        "name": "Architecture, MoE & Open Weights",
        "keywords": ["weights", "hugging face", "open source", "moe", "quantization", "gguf", "parameters", "fine-tuning"],
        "description": "Technical dive into model architecture, local deployment, and weights availability."
    },
    {
        "id": "developer_workflow",
        "name": "Practical Developer Workflow & Tooling",
        "keywords": ["ide", "cursor", "vscode", "agent", "workflow", "production", "tool use", "mcp", "integration"],
        "description": "Practical day-to-day tooling impact: how software engineers work with this today."
    },
    {
        "id": "reliability_limitations",
        "name": "Failure Modes, Hallucinations & Limits",
        "keywords": ["limitation", "failure", "hallucination", "flaw", "leak", "contamination", "security", "jailbreak"],
        "description": "Critical counter-perspective examining bugs, test contamination, or security risks."
    },
    {
        "id": "future_implications",
        "name": "Ecosystem Disruption & Industry Shift",
        "keywords": ["future", "paradigm shift", "disruption", "replace", "jobs", "startup", "moat", "enterprise"],
        "description": "Longer-term strategic shifts in how companies build moats and capture value."
    }
]

class TrendCompetitionEngine:
    """
    Analyzes content angles across existing coverage to evaluate market saturation
    and discover under-served content opportunities.
    """

    @classmethod
    def classify_item_angle(cls, text: str) -> str:
        clean = text.lower()
        best_angle = "generic_announcement"
        max_matches = 0

        for angle in ANGLE_TAXONOMY:
            matches = sum(1 for kw in angle["keywords"] if kw in clean)
            if matches > max_matches:
                max_matches = matches
                best_angle = angle["id"]

        return best_angle

    @classmethod
    def analyze_competition(cls, items: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes a cluster of content items and returns:
        - competition_score: 0-100 (density and repetition of angles)
        - saturated_angles: angles with excessive duplicate coverage
        - under_served_angles: high-leverage angles with zero or minimal coverage
        - angle_distribution: count per angle
        """
        if not items:
            return {
                "competition_score": 20.0,
                "saturated_angles": [],
                "under_served_angles": [a["name"] for a in ANGLE_TAXONOMY[:3]],
                "angle_distribution": {},
                "semantic_density": 0.2
            }

        angle_counts: Dict[str, int] = {a["id"]: 0 for a in ANGLE_TAXONOMY}

        # 1. Classify each item into an angle
        for item in items:
            combined = f"{item.get('title', '')} {item.get('content', '')}"
            angle_id = cls.classify_item_angle(combined)
            angle_counts[angle_id] += 1

        total_items = len(items)

        # 2. Identify saturated and under-served angles
        saturated: List[str] = []
        under_served: List[str] = []

        for angle in ANGLE_TAXONOMY:
            cnt = angle_counts[angle["id"]]
            if cnt >= 2 or (cnt >= 1 and total_items <= 3 and angle["id"] == "generic_announcement"):
                saturated.append(angle["name"])
            elif cnt == 0:
                under_served.append(angle["name"])

        # 3. Calculate semantic density via pairwise similarity
        pairwise_sims = []
        sample_items = items[:6]
        for i in range(len(sample_items)):
            for j in range(i + 1, len(sample_items)):
                t1 = sample_items[i].get("title", "")
                t2 = sample_items[j].get("title", "")
                pairwise_sims.append(fuzz.token_set_ratio(t1, t2))

        avg_pairwise = (sum(pairwise_sims) / len(pairwise_sims)) if pairwise_sims else 40.0

        # 4. Composite Competition Score (0-100)
        # Volume (up to 40) + Semantic Overlap (up to 40) + Angle Concentration (up to 20)
        volume_factor = min(40.0, total_items * 5.0)
        overlap_factor = (avg_pairwise / 100.0) * 40.0
        concentration_factor = (angle_counts["generic_announcement"] / max(1, total_items)) * 20.0

        comp_score = round(min(100.0, max(15.0, volume_factor + overlap_factor + concentration_factor)), 1)

        # Guarantee at least 2 under-served angles
        if len(under_served) < 2:
            under_served = [a["name"] for a in ANGLE_TAXONOMY if a["name"] not in saturated][:2]

        return {
            "competition_score": comp_score,
            "saturated_angles": saturated,
            "under_served_angles": under_served,
            "angle_distribution": {
                next(a["name"] for a in ANGLE_TAXONOMY if a["id"] == k): v
                for k, v in angle_counts.items() if v > 0
            },
            "semantic_density": round(avg_pairwise / 100.0, 2)
        }

trend_competition_engine = TrendCompetitionEngine()
