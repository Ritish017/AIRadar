"""
Unified Web Acquisition Layer.
Provides a clean, centralized WebAcquisitionProvider interface utilizing Firecrawl
for deep search, discovery, and scraping, and RSS for fast discovery signals.
"""

import time
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from backend.providers.firecrawl_provider import firecrawl_provider
from backend.providers.rss_poller import rss_poller
from backend.providers.mock_provider import mock_provider
from backend.providers.source_registry import source_registry

logger = logging.getLogger(__name__)

class WebAcquisitionProvider:
    """
    Central Web Acquisition Layer.
    All external web ingestion and extraction flows through this provider.
    Combines Firecrawl's deep extraction and query rotation with RSS fast-signals.
    """

    def __init__(self):
        self.firecrawl = firecrawl_provider
        self.rss = rss_poller
        self.mock = mock_provider

    async def acquire_all(self, include_rss: bool = True) -> List[Dict[str, Any]]:
        """
        Executes a complete web acquisition cycle:
        1. Fast discovery signals from official RSS feeds
        2. Deep query search & markdown extraction via Firecrawl
        3. Fallback to high-signal demo data if external network yields 0 items
        """
        start_time = time.time()
        acquired_items: List[Dict[str, Any]] = []

        # 1. RSS Fast Discovery Signal
        if include_rss:
            try:
                rss_items = await self.rss.poll_all()
                acquired_items.extend(rss_items)
            except Exception as e:
                logger.warning(f"WebAcquisition RSS polling notice: {e}")

        # 2. Firecrawl Deep Web Search & Scrape
        try:
            fc_items = await self.firecrawl.fetch_items()
            acquired_items.extend(fc_items)
            source_registry.record_health("firecrawl", success=True, latency_ms=int((time.time() - start_time) * 1000))
        except Exception as e:
            source_registry.record_health("firecrawl", success=False, error=str(e))
            logger.warning(f"WebAcquisition Firecrawl acquisition error: {e}")

        # 3. Graceful offline fallback to verified sample dataset
        if not acquired_items:
            logger.info("Web acquisition yielded 0 live items. Using high-signal verification demo provider.")
            mock_items = await self.mock.fetch_items()
            acquired_items.extend(mock_items)

        total_latency = int((time.time() - start_time) * 1000)
        logger.info(f"WebAcquisition completed: {len(acquired_items)} items acquired in {total_latency}ms")
        return acquired_items

    async def search_topic(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Executes targeted Firecrawl search on a specific breaking query."""
        try:
            return await self.firecrawl.search_and_extract(query, limit=limit)
        except Exception as e:
            logger.warning(f"Targeted search failed for query '{query}': {e}")
            return []

    async def search_dynamic(
        self,
        entities: Optional[List[str]] = None,
        accelerating_topics: Optional[List[str]] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Executes dynamic event-driven searches generated from entities and accelerated topics."""
        queries = self.firecrawl.generate_dynamic_queries(entities, accelerating_topics)
        results: List[Dict[str, Any]] = []
        for q in queries[:3]:
            res = await self.search_topic(q, limit=limit)
            results.extend(res)
        return results

    async def verify_primary_source(
        self,
        claim_topic: str,
        suspected_entity: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Primary Source Verification Pipeline:
        When an unverified or community signal is detected (e.g. from X or Reddit),
        proactively queries Tier 1 official domains (OpenAI, Anthropic, Google, Meta, GitHub, arXiv)
        to confirm or refute the claim.
        """
        entity_str = f'"{suspected_entity}"' if suspected_entity else ""
        tier1_query = f"{entity_str} {claim_topic} site:openai.com/index OR site:anthropic.com/news OR site:deepmind.google/discover OR site:github.com OR site:arxiv.org"
        logger.info(f"Triggering Primary Source Verification search: {tier1_query}")
        
        candidates = await self.search_topic(tier1_query, limit=3)
        for cand in candidates:
            cand_url = cand.get("url", "")
            quality = self.firecrawl.get_source_quality(cand_url)
            if quality == "Tier 1":
                logger.info(f"Primary source confirmed at {cand_url}")
                return cand
        return None

    async def scrape_url(self, url: str) -> Optional[str]:
        """Deeply extracts clean markdown from a single URL via Firecrawl."""
        try:
            if self.firecrawl.firecrawl_client:
                doc = self.firecrawl.firecrawl_client.scrape_url(url, params={"formats": ["markdown"]})
                if doc and "markdown" in doc:
                    return doc["markdown"]
        except Exception as e:
            logger.debug(f"Direct scrape_url failed for {url}: {e}")
        return None

web_acquisition_provider = WebAcquisitionProvider()
