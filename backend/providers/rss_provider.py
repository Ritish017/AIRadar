import logging
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
import httpx
from bs4 import BeautifulSoup
from backend.providers.base import BaseProvider

logger = logging.getLogger(__name__)

RSS_FEEDS = [
    {"name": "TechCrunch AI", "url": "https://techcrunch.com/category/artificial-intelligence/feed/", "source_type": "news", "topic": "Startups"},
    {"name": "The Verge AI", "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", "source_type": "news", "topic": "AI Tools"},
    {"name": "Ars Technica AI", "url": "https://feeds.arstechnica.com/arstechnica/technology-lab", "source_type": "news", "topic": "Research"},
    {"name": "VentureBeat AI", "url": "https://venturebeat.com/category/ai/feed/", "source_type": "news", "topic": "Companies"},
    {"name": "OpenAI Blog", "url": "https://openai.com/news/rss.xml", "source_type": "rss", "topic": "Models"},
    {"name": "Anthropic News", "url": "https://anthropic.com/news/rss.xml", "source_type": "rss", "topic": "Research"},
    {"name": "Google AI Blog", "url": "https://blog.google/technology/ai/rss/", "source_type": "rss", "topic": "Research"},
    {"name": "Hugging Face Blog", "url": "https://huggingface.co/blog/feed.xml", "source_type": "rss", "topic": "Open Source"},
]

class RSSProvider(BaseProvider):
    def __init__(self):
        super().__init__(name="AI RSS & News Feeds", source_type="rss")

    async def fetch_items(self) -> List[Dict[str, Any]]:
        items: List[Dict[str, Any]] = []

        async with httpx.AsyncClient(timeout=10.0, follow_redirects=True, headers={"User-Agent": "AIViralRadar/1.0"}) as client:
            for feed in RSS_FEEDS:
                try:
                    resp = await client.get(feed["url"])
                    if resp.status_code == 200:
                        feed_items = self._parse_feed_xml(resp.text, feed)
                        items.extend(feed_items)
                except Exception as e:
                    logger.debug(f"Could not fetch RSS feed {feed['name']}: {e}")

        return items

    def _parse_feed_xml(self, xml_text: str, feed_meta: Dict[str, Any]) -> List[Dict[str, Any]]:
        parsed = []
        try:
            root = ET.fromstring(xml_text)
            # Support RSS 2.0 <item> and Atom <entry>
            channel_items = root.findall(".//item")
            if not channel_items:
                channel_items = root.findall(".//{http://www.w3.org/2005/Atom}entry")

            now = datetime.now(timezone.utc)

            for entry in channel_items[:6]:
                # Extract title
                title_elem = entry.find("title") or entry.find("{http://www.w3.org/2005/Atom}title")
                title = title_elem.text.strip() if title_elem is not None and title_elem.text else "AI Update"

                # Extract link
                link = ""
                link_elem = entry.find("link") or entry.find("{http://www.w3.org/2005/Atom}link")
                if link_elem is not None:
                    link = link_elem.text or link_elem.get("href") or ""

                # Extract description/content
                desc_elem = entry.find("description") or entry.find("{http://www.w3.org/2005/Atom}summary") or entry.find("{http://www.w3.org/2005/Atom}content")
                raw_desc = desc_elem.text if desc_elem is not None and desc_elem.text else title
                # Strip HTML tags
                soup = BeautifulSoup(raw_desc, "html.parser")
                clean_content = soup.get_text(separator=" ").strip()[:600]

                # Estimated initial metrics for discovered news
                parsed.append({
                    "title": title,
                    "content": clean_content if clean_content else title,
                    "url": link,
                    "source": feed_meta["name"],
                    "source_type": feed_meta["source_type"],
                    "author": feed_meta["name"],
                    "author_handle": feed_meta["name"].replace(" ", ""),
                    "author_url": link,
                    "published_at": now - timedelta(hours=1),
                    "views": 45000,
                    "likes": 850,
                    "reposts": 140,
                    "replies": 35,
                    "quotes": 20,
                    "topic": feed_meta.get("topic", "AI Tools"),
                    "content_type": "news",
                    "hook_type": "breaking_news",
                    "hashtags": ["#AI", f"#{feed_meta['topic'].replace(' ', '')}"]
                })
        except Exception as e:
            logger.debug(f"Error parsing XML for {feed_meta['name']}: {e}")

        return parsed

rss_provider = RSSProvider()
