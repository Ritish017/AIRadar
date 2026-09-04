"""
Source Registry & Health Monitoring Service.
Maintains the centralized catalogue of AI intelligence sources, priorities,
freshness targets, and live operational health.
"""

import logging
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class SourceDefinition(BaseModel):
    id: str
    name: str
    domain: str
    source_type: str  # official, news, research, community, github
    quality_tier: str = "Tier 1"  # Tier 1: Official, Tier 2: Tech Press, Tier 3: Community
    priority: int = 80  # 0 to 100
    topics: List[str] = Field(default_factory=list)
    freshness_target: str = "15m"  # 5m, 15m, 30m, 1h
    homepage_url: str
    rss_url: Optional[str] = None
    is_active: bool = True
    health_status: str = "healthy"  # healthy, degraded, offline
    last_checked_at: Optional[datetime] = None
    last_success_at: Optional[datetime] = None
    latency_ms: Optional[int] = None
    consecutive_failures: int = 0
    error_message: Optional[str] = None

# Primary Source Registry seeding
PRIMARY_SOURCES: List[Dict[str, Any]] = [
    # Official Frontier Labs
    {
        "id": "openai",
        "name": "OpenAI",
        "domain": "openai.com",
        "source_type": "official",
        "quality_tier": "Tier 1",
        "priority": 100,
        "topics": ["models", "agents", "research", "safety"],
        "freshness_target": "5m",
        "homepage_url": "https://openai.com",
        "rss_url": "https://openai.com/news/rss.xml"
    },
    {
        "id": "google-deepmind",
        "name": "Google DeepMind",
        "domain": "deepmind.google",
        "source_type": "official",
        "quality_tier": "Tier 1",
        "priority": 100,
        "topics": ["models", "research", "robotics", "multimodal"],
        "freshness_target": "5m",
        "homepage_url": "https://deepmind.google",
        "rss_url": "https://blog.google/technology/ai/rss/"
    },
    {
        "id": "anthropic",
        "name": "Anthropic",
        "domain": "anthropic.com",
        "source_type": "official",
        "quality_tier": "Tier 1",
        "priority": 98,
        "topics": ["models", "agents", "research", "safety"],
        "freshness_target": "5m",
        "homepage_url": "https://anthropic.com",
        "rss_url": "https://anthropic.com/news/rss.xml"
    },
    {
        "id": "meta-ai",
        "name": "Meta AI",
        "domain": "ai.meta.com",
        "source_type": "official",
        "quality_tier": "Tier 1",
        "priority": 95,
        "topics": ["models", "open_source", "research"],
        "freshness_target": "10m",
        "homepage_url": "https://ai.meta.com",
        "rss_url": "https://ai.meta.com/blog/rss/"
    },
    {
        "id": "nvidia",
        "name": "NVIDIA AI",
        "domain": "blogs.nvidia.com",
        "source_type": "official",
        "quality_tier": "Tier 1",
        "priority": 92,
        "topics": ["hardware", "robotics", "models", "infrastructure"],
        "freshness_target": "15m",
        "homepage_url": "https://blogs.nvidia.com/blog/category/deep-learning/",
        "rss_url": "https://blogs.nvidia.com/feed/"
    },
    {
        "id": "huggingface",
        "name": "Hugging Face",
        "domain": "huggingface.co",
        "source_type": "official",
        "quality_tier": "Tier 1",
        "priority": 95,
        "topics": ["open_source", "models", "datasets", "research"],
        "freshness_target": "5m",
        "homepage_url": "https://huggingface.co",
        "rss_url": "https://huggingface.co/blog/feed.xml"
    },
    {
        "id": "mistral",
        "name": "Mistral AI",
        "domain": "mistral.ai",
        "source_type": "official",
        "quality_tier": "Tier 1",
        "priority": 90,
        "topics": ["models", "open_source", "agents"],
        "freshness_target": "15m",
        "homepage_url": "https://mistral.ai",
        "rss_url": "https://mistral.ai/news/rss.xml"
    },
    {
        "id": "deepseek",
        "name": "DeepSeek",
        "domain": "deepseek.com",
        "source_type": "official",
        "quality_tier": "Tier 1",
        "priority": 96,
        "topics": ["models", "reasoning", "open_source", "coding"],
        "freshness_target": "5m",
        "homepage_url": "https://deepseek.com",
        "rss_url": None
    },
    # Research & Developer
    {
        "id": "arxiv-ai",
        "name": "arXiv (cs.AI & cs.CL)",
        "domain": "arxiv.org",
        "source_type": "research",
        "quality_tier": "Tier 1",
        "priority": 94,
        "topics": ["research", "papers", "benchmarks", "architectures"],
        "freshness_target": "30m",
        "homepage_url": "https://arxiv.org",
        "rss_url": "http://export.arxiv.org/rss/cs.AI"
    },
    {
        "id": "github-trending",
        "name": "GitHub Trending AI",
        "domain": "github.com",
        "source_type": "github",
        "quality_tier": "Tier 1",
        "priority": 90,
        "topics": ["open_source", "agents", "coding", "tools"],
        "freshness_target": "15m",
        "homepage_url": "https://github.com/trending?since=daily",
        "rss_url": None
    },
    # Tier 2 Tech Media
    {
        "id": "techcrunch",
        "name": "TechCrunch AI",
        "domain": "techcrunch.com",
        "source_type": "news",
        "quality_tier": "Tier 2",
        "priority": 85,
        "topics": ["startups", "business", "models", "funding"],
        "freshness_target": "10m",
        "homepage_url": "https://techcrunch.com/category/artificial-intelligence/",
        "rss_url": "https://techcrunch.com/category/artificial-intelligence/feed/"
    },
    {
        "id": "theverge",
        "name": "The Verge AI",
        "domain": "theverge.com",
        "source_type": "news",
        "quality_tier": "Tier 2",
        "priority": 82,
        "topics": ["tools", "policy", "consumer_ai", "products"],
        "freshness_target": "15m",
        "homepage_url": "https://www.theverge.com/ai-artificial-intelligence",
        "rss_url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"
    },
    {
        "id": "arstechnica",
        "name": "Ars Technica",
        "domain": "arstechnica.com",
        "source_type": "news",
        "quality_tier": "Tier 2",
        "priority": 84,
        "topics": ["research", "hardware", "models", "policy"],
        "freshness_target": "20m",
        "homepage_url": "https://arstechnica.com/information-technology/",
        "rss_url": "https://feeds.arstechnica.com/arstechnica/technology-lab"
    },
    {
        "id": "mit-tech-review",
        "name": "MIT Technology Review",
        "domain": "technologyreview.com",
        "source_type": "news",
        "quality_tier": "Tier 2",
        "priority": 88,
        "topics": ["research", "policy", "robotics", "ethics"],
        "freshness_target": "30m",
        "homepage_url": "https://www.technologyreview.com/topic/artificial-intelligence/",
        "rss_url": "https://www.technologyreview.com/topic/artificial-intelligence/feed"
    },
    {
        "id": "reuters-tech",
        "name": "Reuters Technology",
        "domain": "reuters.com",
        "source_type": "news",
        "quality_tier": "Tier 2",
        "priority": 89,
        "topics": ["business", "policy", "chips", "companies"],
        "freshness_target": "15m",
        "homepage_url": "https://www.reuters.com/technology/artificial-intelligence/",
        "rss_url": None
    },
    # Community & Signals (Tier 3)
    {
        "id": "hackernews",
        "name": "Hacker News AI",
        "domain": "news.ycombinator.com",
        "source_type": "community",
        "quality_tier": "Tier 3",
        "priority": 75,
        "topics": ["open_source", "developer_discussion", "startups"],
        "freshness_target": "15m",
        "homepage_url": "https://news.ycombinator.com",
        "rss_url": "https://news.ycombinator.com/rss"
    },
    {
        "id": "x-signals",
        "name": "X Signals (Curated)",
        "domain": "x.com",
        "source_type": "community",
        "quality_tier": "Tier 3",
        "priority": 78,
        "topics": ["trending", "hot_takes", "breakthroughs"],
        "freshness_target": "5m",
        "homepage_url": "https://x.com",
        "rss_url": None
    }
]

class SourceRegistry:
    """
    Centralized In-Memory & Database-backed Source Registry.
    Tracks live health, latency, error recovery, and query prioritization.
    """

    def __init__(self):
        self._sources: Dict[str, SourceDefinition] = {}
        for s in PRIMARY_SOURCES:
            self._sources[s["id"]] = SourceDefinition(**s)

    def list_sources(self, source_type: Optional[str] = None) -> List[SourceDefinition]:
        sources = list(self._sources.values())
        if source_type:
            sources = [s for s in sources if s.source_type.lower() == source_type.lower()]
        return sorted(sources, key=lambda x: x.priority, reverse=True)

    def get_source(self, source_id: str) -> Optional[SourceDefinition]:
        return self._sources.get(source_id)

    def get_rss_sources(self) -> List[SourceDefinition]:
        return [s for s in self._sources.values() if s.rss_url and s.is_active]

    def record_health(self, source_id: str, success: bool, latency_ms: Optional[int] = None, error: Optional[str] = None):
        source = self._sources.get(source_id)
        if not source:
            return

        now = datetime.now(timezone.utc)
        source.last_checked_at = now
        if latency_ms is not None:
            source.latency_ms = latency_ms

        if success:
            source.last_success_at = now
            source.consecutive_failures = 0
            source.health_status = "healthy"
            source.error_message = None
        else:
            source.consecutive_failures += 1
            source.error_message = error
            if source.consecutive_failures >= 3:
                source.health_status = "degraded"
            if source.consecutive_failures >= 6:
                source.health_status = "offline"

    def get_health_summary(self) -> Dict[str, Any]:
        total = len(self._sources)
        healthy = sum(1 for s in self._sources.values() if s.health_status == "healthy")
        degraded = sum(1 for s in self._sources.values() if s.health_status == "degraded")
        offline = sum(1 for s in self._sources.values() if s.health_status == "offline")

        return {
            "total_sources": total,
            "healthy_count": healthy,
            "degraded_count": degraded,
            "offline_count": offline,
            "sources": [
                {
                    "id": s.id,
                    "name": s.name,
                    "source_type": s.source_type,
                    "quality_tier": s.quality_tier,
                    "health_status": s.health_status,
                    "latency_ms": s.latency_ms,
                    "last_checked_at": s.last_checked_at.isoformat() if s.last_checked_at else None,
                    "error": s.error_message
                }
                for s in sorted(self._sources.values(), key=lambda x: x.priority, reverse=True)
            ]
        }

source_registry = SourceRegistry()
