import math
import re
from datetime import datetime, timezone
from typing import Dict, Any, Optional, Tuple
from backend.services.virality.engagement import calculate_base_engagement_score, calculate_engagement_rate
from backend.services.virality.velocity import calculate_velocity_multiplier

class ViralityScorer:
    """
    Dual Virality Engine:
    1. Measurable Viral Score (0-100): Calculated from verified social metrics (views, likes, reposts).
    2. Predicted Viral Potential (0-100): Deterministic qualitative prediction for web/Firecrawl
       discoveries where social counters are unavailable or newly published.
    """

    @staticmethod
    def calculate_freshness_multiplier(published_at: datetime, half_life_hours: float = 28.0) -> float:
        now = datetime.now(timezone.utc)
        if published_at.tzinfo is None:
            pub_utc = published_at.replace(tzinfo=timezone.utc)
        else:
            pub_utc = published_at

        age_seconds = max(0.0, (now - pub_utc).total_seconds())
        age_hours = age_seconds / 3600.0

        decay_constant = 0.693147 / half_life_hours
        freshness = math.exp(-decay_constant * age_hours)
        return max(0.20, min(1.20, freshness))

    @classmethod
    def calculate_viral_potential(
        cls,
        title: str,
        content: str,
        source_quality: str = "Tier 1",
        published_at: Optional[datetime] = None
    ) -> float:
        """
        Deterministic Framework for Viral Potential (0-100):
        - Novelty (0-25): breakthrough, sota, first, release, announce, unveil
        - Technical Importance (0-20): benchmark, reasoning, weights, architecture, swe-bench, model
        - Discussion & Controversy (0-15): outperforms, beats, rivals, debate, paradigm shift
        - Developer Relevance (0-15): open source, repo, agent, api, framework, tooling
        - Source Quality Tier (0-15): Tier 1 (15), Tier 2 (10), Tier 3 (5)
        - Timeliness Decay (0-10): recency multiplier
        """
        text = f"{title or ''} {content or ''}".lower()
        score = 0.0

        # 1. Novelty (Max 25)
        novelty_signals = [
            ("first", 6), ("unveil", 7), ("release", 7), ("breakthrough", 8),
            ("state of the art", 8), ("sota", 7), ("novel", 6), ("announce", 6),
            ("introducing", 6), ("launch", 6)
        ]
        novelty_score = sum(weight for kw, weight in novelty_signals if kw in text)
        score += min(25.0, max(8.0, novelty_score))

        # 2. Technical Importance (Max 20)
        tech_signals = [
            ("benchmark", 7), ("reasoning", 7), ("weights", 7), ("architecture", 6),
            ("swe-bench", 8), ("model", 5), ("human_eval", 6), ("tokens/sec", 5),
            ("quantization", 5), ("multimodal", 6)
        ]
        tech_score = sum(weight for kw, weight in tech_signals if kw in text)
        score += min(20.0, max(6.0, tech_score))

        # 3. Discussion & Controversy (Max 15)
        discussion_signals = [
            ("outperforms", 7), ("beats", 7), ("rivals", 6), ("debate", 5),
            ("leak", 6), ("game changer", 5), ("replacement", 5)
        ]
        discussion_score = sum(weight for kw, weight in discussion_signals if kw in text)
        score += min(15.0, max(4.0, discussion_score))

        # 4. Developer Relevance (Max 15)
        dev_signals = [
            ("open source", 7), ("open-weights", 7), ("github", 6), ("agent", 7),
            ("api", 5), ("framework", 5), ("sdk", 5), ("code", 5)
        ]
        dev_score = sum(weight for kw, weight in dev_signals if kw in text)
        score += min(15.0, max(5.0, dev_score))

        # 5. Source Quality (Max 15)
        if source_quality == "Tier 1":
            score += 15.0
        elif source_quality == "Tier 2":
            score += 10.0
        else:
            score += 5.0

        # 6. Timeliness (Max 10)
        if published_at:
            freshness = cls.calculate_freshness_multiplier(published_at, half_life_hours=36.0)
            score += min(10.0, round(freshness * 10.0, 1))
        else:
            score += 9.0

        return round(min(100.0, max(30.0, score)), 1)

    @classmethod
    def score_item(
        cls,
        published_at: datetime,
        title: Optional[str] = "",
        content: Optional[str] = "",
        views: Optional[int] = None,
        likes: Optional[int] = None,
        reposts: Optional[int] = None,
        replies: Optional[int] = None,
        quotes: Optional[int] = None,
        source_quality: str = "Tier 1",
        trend_multiplier: float = 1.0
    ) -> Dict[str, Any]:
        viral_potential = cls.calculate_viral_potential(
            title=title or "",
            content=content or "",
            source_quality=source_quality,
            published_at=published_at
        )

        has_social_metrics = (
            views is not None or
            likes is not None or
            reposts is not None
        )

        if not has_social_metrics:
            if viral_potential >= 86.0:
                badge = f"⚡ Viral Potential {Math_round(viral_potential)}"
                classification = "Exploding Potential"
            elif viral_potential >= 71.0:
                badge = f"⚡ Viral Potential {Math_round(viral_potential)}"
                classification = "High Potential"
            elif viral_potential >= 51.0:
                badge = f"⚡ Viral Potential {Math_round(viral_potential)}"
                classification = "Rising Potential"
            else:
                badge = f"⚡ Viral Potential {Math_round(viral_potential)}"
                classification = "Moderate"

            return {
                "viral_score": None,
                "viral_potential": viral_potential,
                "classification": classification,
                "badge": badge,
                "engagement_rate": None,
                "engagement_velocity": 0.0,
                "velocity_multiplier": 1.0,
                "freshness_multiplier": round(cls.calculate_freshness_multiplier(published_at), 2),
                "trend_multiplier": round(trend_multiplier, 2)
            }

        safe_views = views or 0
        safe_likes = likes or 0
        safe_reposts = reposts or 0
        safe_replies = replies or 0
        safe_quotes = quotes or 0

        base_eng = calculate_base_engagement_score(safe_views, safe_likes, safe_reposts, safe_replies, safe_quotes)
        vel_mult, vel_pct = calculate_velocity_multiplier(published_at, safe_likes, safe_reposts, safe_replies, safe_views)
        freshness_mult = cls.calculate_freshness_multiplier(published_at, half_life_hours=28.0)
        eng_rate = calculate_engagement_rate(safe_views, safe_likes, safe_reposts, safe_replies, safe_quotes)

        raw_score = base_eng * vel_mult * freshness_mult * max(0.9, trend_multiplier)
        normalized_score = round(min(100.0, max(5.0, (raw_score / 120.0) * 100.0)), 1)

        if normalized_score >= 86.0:
            classification = "Viral"
            badge = f"🚀 Exploding {Math_round(normalized_score)}"
        elif normalized_score >= 71.0:
            classification = "Hot"
            badge = f"🔥 Hot {Math_round(normalized_score)}"
        elif normalized_score >= 51.0:
            classification = "Rising"
            badge = f"⚡ Rising {Math_round(normalized_score)}"
        elif normalized_score >= 31.0:
            classification = "Normal"
            badge = f"📈 Normal {Math_round(normalized_score)}"
        else:
            classification = "Low"
            badge = f"💤 Low {Math_round(normalized_score)}"

        return {
            "viral_score": normalized_score,
            "viral_potential": viral_potential,
            "classification": classification,
            "badge": badge,
            "engagement_rate": eng_rate,
            "engagement_velocity": vel_pct,
            "velocity_multiplier": round(vel_mult, 2),
            "freshness_multiplier": round(freshness_mult, 2),
            "trend_multiplier": round(trend_multiplier, 2)
        }

def Math_round(val: float) -> int:
    return int(round(val))

virality_scorer = ViralityScorer()
