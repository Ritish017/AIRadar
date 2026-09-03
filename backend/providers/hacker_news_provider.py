import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
import httpx
from backend.providers.base import BaseProvider

logger = logging.getLogger(__name__)

class HackerNewsProvider(BaseProvider):
    def __init__(self):
        super().__init__(name="Hacker News AI", source_type="news")

    async def fetch_items(self) -> List[Dict[str, Any]]:
        items = []
        url = "https://hn.algolia.com/api/v1/search_by_date?query=AI&tags=story&numericFilters=points>50&hitsPerPage=8"

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.get(url, headers={"User-Agent": "AIViralRadar/1.0"})
                if resp.status_code == 200:
                    data = resp.json()
                    now = datetime.now(timezone.utc)
                    for hit in data.get("hits", []):
                        points = hit.get("points", 0)
                        num_comments = hit.get("num_comments", 0)
                        title = hit.get("title", "AI Discussion on Hacker News")
                        story_url = hit.get("url") or f"https://news.ycombinator.com/item?id={hit.get('objectID')}"

                        items.append({
                            "title": title,
                            "content": f"Trending discussion on Hacker News: {title}. Discussion link: https://news.ycombinator.com/item?id={hit.get('objectID')}",
                            "url": story_url,
                            "source": "Hacker News",
                            "source_type": "news",
                            "author": hit.get("author", "hn_community"),
                            "author_handle": hit.get("author", "hn_community"),
                            "author_url": f"https://news.ycombinator.com/user?id={hit.get('author')}",
                            "published_at": now - timedelta(hours=2),
                            "views": points * 35,
                            "likes": points,
                            "reposts": int(points * 0.25),
                            "replies": num_comments,
                            "quotes": int(points * 0.1),
                            "topic": "Research",
                            "content_type": "news",
                            "hook_type": "curiosity",
                            "hashtags": ["#HackerNews", "#AI", "#TechNews"]
                        })
        except Exception as e:
            logger.debug(f"Hacker News fetch error: {e}")

        return items

hacker_news_provider = HackerNewsProvider()
