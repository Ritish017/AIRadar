import re
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
from collections import defaultdict
from rapidfuzz import fuzz

STOPWORDS = {
    "the", "a", "an", "in", "on", "at", "to", "for", "with", "by", "from",
    "is", "are", "was", "were", "and", "or", "of", "about", "into", "it",
    "this", "that", "new", "released", "announced", "launch", "ai", "model"
}

def extract_key_phrases(text: str) -> List[str]:
    """Extract clean 2-3 word candidate topic phrases from text."""
    clean = re.sub(r"[^\w\s-]", " ", text.lower())
    tokens = [w for w in clean.split() if len(w) > 2 and w not in STOPWORDS]
    phrases = []
    for i in range(len(tokens) - 1):
        phrases.append(f"{tokens[i]} {tokens[i+1]}")
    return phrases

class TrendDetector:
    def __init__(self, similarity_threshold: float = 65.0):
        self.similarity_threshold = similarity_threshold

    def cluster_topics(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Groups items into topic clusters, tracks multi-source momentum,
        and assigns status: 🔥 Exploding, ⚡ Surging, 📈 Rising, or 💤 Steady.
        """
        if not items:
            return []

        clusters: List[Dict[str, Any]] = []

        for item in items:
            title_or_content = item.get("title") or item.get("content", "")[:120]
            matched = False

            for cluster in clusters:
                sim = fuzz.token_set_ratio(cluster["name"], title_or_content)
                if sim >= self.similarity_threshold:
                    cluster["items"].append(item)
                    cluster["sources"].add(item.get("source_type", "web"))
                    matched = True
                    break

            if not matched:
                # Derive representative name from title
                short_name = (item.get("title") or title_or_content[:60]).strip()
                clusters.append({
                    "id": f"topic_{len(clusters)+1}",
                    "name": short_name,
                    "category": item.get("topic", "AI Models"),
                    "items": [item],
                    "sources": {item.get("source_type", "web")},
                })

        # Calculate momentum and status
        results = []
        for c in clusters:
            count = len(c["items"])
            source_count = len(c["sources"])
            avg_viral = sum(it.get("viral_score", 50) for it in c["items"]) / count

            # Momentum calculation (+120% to +600%)
            raw_momentum = (count * 45.0) + (source_count * 60.0) + (avg_viral * 1.5)
            momentum_pct = round(min(850.0, raw_momentum), 1)

            if momentum_pct > 300 or (source_count >= 3 and count >= 2):
                status = "🔥 Exploding"
            elif momentum_pct > 180 or source_count >= 2:
                status = "⚡ Surging"
            elif momentum_pct > 90:
                status = "📈 Rising"
            else:
                status = "💤 Steady"

            results.append({
                "name": c["name"],
                "category": c["category"],
                "momentum": momentum_pct,
                "status": status,
                "item_count": count,
                "sources_summary": sorted(list(c["sources"])),
                "updated_at": datetime.now(timezone.utc)
            })

        # Sort by momentum descending
        results.sort(key=lambda x: x["momentum"], reverse=True)
        return results

trend_detector = TrendDetector()
