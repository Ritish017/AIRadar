"""
Fast Discovery RSS Engine.
Implements RSSFeed, RSSItem, RSSSource, RSSPoller, and RSSNormalizer
with conditional request support (ETag, If-Modified-Since) and source health telemetry.
"""

import time
import logging
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from email.utils import parsedate_to_datetime
import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

from backend.providers.source_registry import source_registry

logger = logging.getLogger(__name__)

class RSSItem(BaseModel):
    title: str
    link: str
    description: str
    published_at: datetime
    source_name: str
    source_id: str
    source_type: str = "rss"
    quality_tier: str = "Tier 1"
    topic: str = "General AI"
    guid: Optional[str] = None
    author: Optional[str] = None

class RSSFeed(BaseModel):
    source_id: str
    name: str
    url: str
    topic: str = "General AI"
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    last_polled_at: Optional[datetime] = None

class RSSNormalizer:
    """Sanitizes raw feed XML elements into clean RSSItem domain models."""

    @staticmethod
    def clean_html(raw_html: str) -> str:
        if not raw_html:
            return ""
        soup = BeautifulSoup(raw_html, "html.parser")
        # Remove script and style elements
        for s in soup(["script", "style", "nav", "footer"]):
            s.decompose()
        return soup.get_text(separator=" ").strip()

    @staticmethod
    def parse_datetime(date_str: Optional[str]) -> datetime:
        if not date_str:
            return datetime.now(timezone.utc)
        try:
            # Try RFC 822 / 2822
            return parsedate_to_datetime(date_str).astimezone(timezone.utc)
        except Exception:
            pass
        try:
            # Try ISO 8601 (Atom)
            return datetime.fromisoformat(date_str.replace("Z", "+00:00")).astimezone(timezone.utc)
        except Exception:
            return datetime.now(timezone.utc)

    @classmethod
    def normalize_entry(cls, entry: ET.Element, feed: RSSFeed, quality_tier: str) -> Optional[RSSItem]:
        try:
            # Title
            title_elem = entry.find("title")
            if title_elem is None:
                title_elem = entry.find("{http://www.w3.org/2005/Atom}title")
            title = title_elem.text.strip() if title_elem is not None and title_elem.text else "AI Update"

            # Link
            link = ""
            link_elem = entry.find("link")
            if link_elem is None:
                link_elem = entry.find("{http://www.w3.org/2005/Atom}link")
            if link_elem is not None:
                link = link_elem.text or link_elem.get("href") or ""
            link = link.strip()
            if not link:
                return None

            # Description / Content
            desc_elem = entry.find("description")
            if desc_elem is None:
                desc_elem = entry.find("{http://www.w3.org/2005/Atom}summary")
            if desc_elem is None:
                desc_elem = entry.find("{http://www.w3.org/2005/Atom}content")
            raw_desc = desc_elem.text if desc_elem is not None and desc_elem.text else title
            clean_content = cls.clean_html(raw_desc)[:1200]

            # Date
            date_elem = entry.find("pubDate")
            if date_elem is None:
                date_elem = entry.find("{http://www.w3.org/2005/Atom}updated")
            if date_elem is None:
                date_elem = entry.find("{http://www.w3.org/2005/Atom}published")
            pub_date_str = date_elem.text if date_elem is not None else None
            pub_date = cls.parse_datetime(pub_date_str)

            # Author
            author_elem = entry.find("author")
            if author_elem is None:
                author_elem = entry.find("{http://www.w3.org/2005/Atom}author")
            author_name = feed.name
            if author_elem is not None:
                name_sub = author_elem.find("{http://www.w3.org/2005/Atom}name")
                if name_sub is not None and name_sub.text:
                    author_name = name_sub.text.strip()
                elif author_elem.text:
                    author_name = author_elem.text.strip()

            guid_elem = entry.find("guid")
            if guid_elem is None:
                guid_elem = entry.find("{http://www.w3.org/2005/Atom}id")
            guid = guid_elem.text.strip() if guid_elem is not None and guid_elem.text else link

            return RSSItem(
                title=title,
                link=link,
                description=clean_content or title,
                published_at=pub_date,
                source_name=feed.name,
                source_id=feed.source_id,
                source_type="rss",
                quality_tier=quality_tier,
                topic=feed.topic,
                guid=guid,
                author=author_name
            )
        except Exception as e:
            logger.debug(f"Failed to normalize entry from {feed.name}: {e}")
            return None

class RSSPoller:
    """
    Asynchronous poller using conditional HTTP headers (ETag, If-Modified-Since)
    for bandwidth and latency optimization.
    """

    def __init__(self):
        self.feed_cache: Dict[str, RSSFeed] = {}
        self._init_feeds()

    def _init_feeds(self):
        sources = source_registry.get_rss_sources()
        for s in sources:
            primary_topic = s.topics[0] if s.topics else "General AI"
            self.feed_cache[s.id] = RSSFeed(
                source_id=s.id,
                name=s.name,
                url=s.rss_url,
                topic=primary_topic
            )

    async def _poll_single_feed(self, client: httpx.AsyncClient, source_id: str, feed: RSSFeed) -> List[Dict[str, Any]]:
        source_def = source_registry.get_source(source_id)
        quality_tier = source_def.quality_tier if source_def else "Tier 1"

        headers = {}
        if feed.etag:
            headers["If-None-Match"] = feed.etag
        if feed.last_modified:
            headers["If-Modified-Since"] = feed.last_modified

        items_out = []
        start_time = time.time()
        try:
            resp = await client.get(feed.url, headers=headers, timeout=4.0)
            latency = int((time.time() - start_time) * 1000)

            if resp.status_code == 304:
                source_registry.record_health(source_id, success=True, latency_ms=latency)
                return []

            if resp.status_code == 200:
                feed.etag = resp.headers.get("ETag")
                feed.last_modified = resp.headers.get("Last-Modified")
                feed.last_polled_at = datetime.now(timezone.utc)

                items = self._parse_feed_xml(resp.text, feed, quality_tier)
                for item in items:
                    items_out.append({
                        "title": item.title,
                        "content": item.description,
                        "url": item.link,
                        "source": item.source_name,
                        "source_type": "rss",
                        "source_quality": item.quality_tier,
                        "author": item.author or item.source_name,
                        "author_handle": (item.author or item.source_name).replace(" ", ""),
                        "author_url": item.link,
                        "published_at": item.published_at,
                        "views": None,  # No fabricated metrics
                        "likes": None,
                        "reposts": None,
                        "replies": None,
                        "quotes": None,
                        "topic": item.topic,
                        "content_type": "news",
                        "hook_type": "breaking_news",
                        "hashtags": ["#AI", f"#{item.topic.replace(' ', '')}"]
                    })
                source_registry.record_health(source_id, success=True, latency_ms=latency)
            else:
                source_registry.record_health(source_id, success=False, latency_ms=latency, error=f"HTTP {resp.status_code}")
        except Exception as e:
            latency = int((time.time() - start_time) * 1000)
            source_registry.record_health(source_id, success=False, latency_ms=latency, error=str(e))
            logger.debug(f"RSS polling notice for {feed.name}: {e}")

        return items_out

    async def poll_all(self) -> List[Dict[str, Any]]:
        """Polls all active RSS feeds concurrently in parallel for low latency."""
        import asyncio
        discovered_items: List[Dict[str, Any]] = []

        async with httpx.AsyncClient(
            follow_redirects=True,
            headers={"User-Agent": "AIViralRadar/3.0 (Global AI Intelligence)"}
        ) as client:
            tasks = [
                self._poll_single_feed(client, s_id, feed)
                for s_id, feed in self.feed_cache.items()
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for res in results:
                if isinstance(res, list):
                    discovered_items.extend(res)

        logger.info(f"RSS Poller harvested {len(discovered_items)} fast discovery signals")
        return discovered_items

    def _parse_feed_xml(self, xml_text: str, feed: RSSFeed, quality_tier: str) -> List[RSSItem]:
        items = []
        try:
            root = ET.fromstring(xml_text)
            # RSS 2.0 vs Atom
            entries = root.findall(".//item")
            if not entries:
                entries = root.findall(".//{http://www.w3.org/2005/Atom}entry")

            for entry in entries[:8]:
                normalized = RSSNormalizer.normalize_entry(entry, feed, quality_tier)
                if normalized:
                    items.append(normalized)
        except Exception as e:
            logger.debug(f"XML parse error for {feed.name}: {e}")
        return items

rss_poller = RSSPoller()
