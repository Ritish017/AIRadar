import re
import logging
from typing import List, Dict, Any, Set, Tuple
from rapidfuzz import fuzz

logger = logging.getLogger(__name__)

STOPWORDS = {
    "the", "a", "an", "in", "on", "at", "to", "for", "with", "by", "from",
    "is", "are", "was", "were", "and", "or", "of", "about", "into", "it",
    "this", "that", "new", "released", "announced", "launch", "ai", "model",
    "models", "just", "now", "today", "here", "why", "how", "what"
}

CANONICAL_TOPIC_PATTERNS = [
    (r"reasoning model|o1|o3|r1|deepseek", "AI Reasoning Models"),
    (r"coding agent|swe-bench|cursor|devin|copilot|software engineering agent", "AI Coding Agents"),
    (r"open source|open weights|llama|mistral|hugging face|apache", "Open-Source AI & Weights"),
    (r"robotics|humanoid|figure|unitree|embodied", "Robotics & Physical AI"),
    (r"multimodal|vision|video generation|sora|flux", "Multimodal AI & Vision"),
    (r"inference|latency|quantization|groq|vllm|tokens/sec", "LLM Inference & Systems"),
    (r"mcp|context protocol|anthropic tools|tool use", "Model Context Protocol & Tools"),
    (r"chip|gpu|nvidia|blackwell|tpu|accelerator", "AI Hardware & Semiconductors")
]

class TrendDetector:
    """
    Groups individual content items into canonical, semantically coherent trend clusters.
    """

    def __init__(self, similarity_threshold: float = 60.0):
        self.similarity_threshold = similarity_threshold

    def canonicalize_trend_name(self, title: str, content: str) -> str:
        """Maps content text to clear, high-signal canonical trend names."""
        combined = f"{title} {content}".lower()
        for pattern, canonical in CANONICAL_TOPIC_PATTERNS:
            if re.search(pattern, combined):
                return canonical
        # Fallback: clean headline
        clean_title = re.sub(r"^[^\w]+", "", title).strip()
        words = clean_title.split()[:7]
        return " ".join(words) if words else "Emerging AI Development"

    def cluster_items(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Clusters raw or scored content items into unified trends.
        """
        if not items:
            return []

        clusters: Dict[str, Dict[str, Any]] = {}

        for item in items:
            title = item.get("title", "")
            content = item.get("content", "")
            canonical_name = self.canonicalize_trend_name(title, content)

            # Match with existing cluster if similar
            matched_key = None
            for key in clusters.keys():
                if fuzz.token_set_ratio(key, canonical_name) >= self.similarity_threshold:
                    matched_key = key
                    break

            cluster_key = matched_key or canonical_name
            if cluster_key not in clusters:
                clusters[cluster_key] = {
                    "name": cluster_key,
                    "category": item.get("topic", "AI Models"),
                    "items": [],
                    "sources": set(),
                    "source_qualities": set(),
                    "primary_url": item.get("url"),
                    "primary_title": title,
                    "entities": set()
                }

            clusters[cluster_key]["items"].append(item)
            clusters[cluster_key]["sources"].add(item.get("source", "Web"))
            clusters[cluster_key]["source_qualities"].add(item.get("source_quality", "Tier 1"))

            # Collect entities
            for ent in item.get("entities", []):
                clusters[cluster_key]["entities"].add(ent)

        # Convert sets to lists
        result = []
        for key, data in clusters.items():
            result.append({
                "name": data["name"],
                "category": data["category"],
                "items": data["items"],
                "item_count": len(data["items"]),
                "sources_summary": sorted(list(data["sources"])),
                "source_qualities": sorted(list(data["source_qualities"])),
                "primary_url": data["primary_url"],
                "primary_title": data["primary_title"],
                "entities": sorted(list(data["entities"]))
            })

        result.sort(key=lambda x: x["item_count"], reverse=True)
        return result

trend_detector = TrendDetector()
