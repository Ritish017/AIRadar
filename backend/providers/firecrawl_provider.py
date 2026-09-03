import os
import re
import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
import httpx

from backend.config import settings
from backend.providers.base import BaseProvider
from backend.services.virality.scorer import virality_scorer

logger = logging.getLogger(__name__)

QUERY_GROUPS = {
    "BREAKING": [
        "latest AI model release today",
        "major AI announcement today",
        "new frontier AI launch"
    ],
    "MODELS": [
        "new open source LLM weights release",
        "AI reasoning model benchmark breakthrough",
        "SOTA AI model outperforms"
    ],
    "AGENTS": [
        "new AI agent framework release",
        "autonomous coding agent benchmark",
        "AI software engineering agent launch"
    ],
    "RESEARCH": [
        "new AI multimodal research paper",
        "breakthrough deep learning architecture arXiv",
        "world model robotics foundation AI"
    ],
    "TOOLS": [
        "new generative AI developer tool launched",
        "LLM inference optimization framework"
    ],
    "OPEN_SOURCE": [
        "trending open source AI repository GitHub",
        "Hugging Face trending models release"
    ]
}

TIER_1_DOMAINS = [
    "openai.com", "anthropic.com", "deepmind.google", "ai.meta.com",
    "blogs.nvidia.com", "huggingface.co", "github.com", "arxiv.org",
    "microsoft.com", "stability.ai", "mistral.ai", "cohere.com"
]

TIER_2_DOMAINS = [
    "techcrunch.com", "theverge.com", "arstechnica.com", "venturebeat.com",
    "wired.com", "reuters.com", "bloomberg.com", "technologyreview.com"
]

class FirecrawlProvider(BaseProvider):
    """
    Centralized Web Research & Scraping Provider powered by Firecrawl.
    Discovers, crawls, and extracts clean markdown from live AI web sources.
    """

    def __init__(self):
        super().__init__(name="Firecrawl Web Discovery", source_type="firecrawl")
        self.api_key = settings.FIRECRAWL_API_KEY or os.environ.get("FIRECRAWL_API_KEY")
        self.current_group_idx = 0
        self.group_keys = list(QUERY_GROUPS.keys())
        self.firecrawl_client = None

        if self.api_key:
            try:
                from firecrawl import FirecrawlApp
                self.firecrawl_client = FirecrawlApp(api_key=self.api_key)
                logger.info("FirecrawlApp SDK client initialized successfully")
            except Exception as e:
                logger.warning(f"FirecrawlApp SDK init notice: {e}. Will use direct HTTP API.")

    def get_source_quality(self, url: str) -> str:
        """Assigns source tier quality based on domain authority."""
        try:
            domain = urlparse(url).netloc.lower()
            if any(t1 in domain for t1 in TIER_1_DOMAINS):
                return "Tier 1"
            if any(t2 in domain for t2 in TIER_2_DOMAINS):
                return "Tier 2"
            return "Tier 3"
        except Exception:
            return "Tier 2"

    def get_source_name(self, url: str) -> str:
        """Extracts clean source name from URL."""
        try:
            domain = urlparse(url).netloc.lower()
            if domain.startswith("www."):
                domain = domain[4:]
            parts = domain.split(".")
            if len(parts) >= 2:
                return parts[0].capitalize()
            return domain
        except Exception:
            return "Web Source"

    def get_next_query(self) -> Tuple[str, str]:
        """Rotates through dynamic query groups."""
        group = self.group_keys[self.current_group_idx % len(self.group_keys)]
        queries = QUERY_GROUPS[group]
        # Pick first query in current rotation
        query = queries[(self.current_group_idx // len(self.group_keys)) % len(queries)]
        self.current_group_idx += 1
        return group, query

    async def search_and_extract(
        self,
        query: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Executes Firecrawl search and returns extracted markdown content.
        Uses SDK or direct REST API v1.
        """
        if not self.api_key:
            logger.info("FIRECRAWL_API_KEY not configured. Operating in Demo Mode.")
            return []

        results = []

        # 1. Try SDK if available
        if self.firecrawl_client:
            try:
                # FirecrawlApp.search(query, params)
                res = self.firecrawl_client.search(query, {
                    "limit": limit,
                    "scrapeOptions": {"formats": ["markdown"]}
                })
                if isinstance(res, dict) and "data" in res:
                    return res["data"]
                elif isinstance(res, list):
                    return res
            except Exception as e:
                logger.warning(f"Firecrawl SDK search failed: {e}. Falling back to REST API.")

        # 2. Fallback to official REST API v1
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            payload = {
                "query": query,
                "limit": limit,
                "scrapeOptions": {"formats": ["markdown"]}
            }
            async with httpx.AsyncClient(timeout=20.0) as client:
                resp = await client.post("https://api.firecrawl.dev/v1/search", headers=headers, json=payload)
                if resp.status_code == 200:
                    data = resp.json()
                    results = data.get("data", [])
                else:
                    logger.warning(f"Firecrawl REST search returned {resp.status_code}: {resp.text[:200]}")
        except Exception as e:
            logger.warning(f"Firecrawl REST search error: {e}")

        return results

    async def fetch_items(self) -> List[Dict[str, Any]]:
        """
        Main provider interface: rotates queries, executes Firecrawl search,
        normalizes results, filters relevance, and attaches quality tiers.
        """
        if not self.api_key:
            return []

        group_name, query = self.get_next_query()
        logger.info(f"Firecrawl discovery starting for group [{group_name}] with query: '{query}'")

        raw_results = await self.search_and_extract(query, limit=settings.MAX_SEARCH_RESULTS)
        items: List[Dict[str, Any]] = []
        now = datetime.now(timezone.utc)

        for res in raw_results:
            url = res.get("url") or res.get("link")
            if not url:
                continue

            title = res.get("title") or res.get("metadata", {}).get("title") or "AI Development"
            content = res.get("markdown") or res.get("content") or res.get("description") or ""

            # Cheap deterministic AI relevance filter
            combined_text = f"{title} {content}".lower()
            ai_keywords = ["ai", "model", "llm", "agent", "benchmark", "weights", "robot", "reasoning", "neural", "deep learning"]
            if not any(k in combined_text for k in ai_keywords):
                continue

            quality = self.get_source_quality(url)
            source_name = self.get_source_name(url)

            # Category mapping from query group
            category_map = {
                "BREAKING": "Models",
                "MODELS": "Models",
                "AGENTS": "Agents",
                "RESEARCH": "Research",
                "TOOLS": "AI Tools",
                "OPEN_SOURCE": "Open Source"
            }
            topic = category_map.get(group_name, "AI Models")

            # Determine published_at if available
            pub_date = now - timedelta(hours=2)

            # Calculate deterministic viral potential
            potential = virality_scorer.calculate_viral_potential(
                title=title,
                content=content[:1000],
                source_quality=quality,
                published_at=pub_date
            )

            items.append({
                "title": title.strip(),
                "content": content.strip()[:2000] if content else title,
                "url": url.strip(),
                "primary_source_url": url.strip(),
                "source": source_name,
                "source_type": "firecrawl",
                "source_quality": quality,
                "source_count": 1,
                "author": res.get("metadata", {}).get("author") or source_name,
                "author_handle": f"@{source_name.lower()}",
                "author_url": url,
                "published_at": pub_date,
                "views": None,  # Do not fabricate metrics when unavailable
                "likes": None,
                "reposts": None,
                "replies": None,
                "quotes": None,
                "viral_score": None,  # Social score is None; viral_potential is used
                "viral_potential": potential,
                "topic": topic,
                "content_type": "news",
                "hook_type": "breaking_news" if group_name == "BREAKING" else "milestone",
                "hashtags": [f"#{topic.replace(' ', '')}", "#ArtificialIntelligence"],
                "confirmed_facts": [],
                "uncertain_claims": []
            })

        logger.info(f"Firecrawl discovery extracted {len(items)} relevant AI items")
        return items

firecrawl_provider = FirecrawlProvider()
