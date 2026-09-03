import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
import httpx
from backend.providers.base import BaseProvider

logger = logging.getLogger(__name__)

SUBREDDITS = ["LocalLLaMA", "MachineLearning", "Artificial"]

class RedditProvider(BaseProvider):
    def __init__(self):
        super().__init__(name="Reddit AI Communities", source_type="reddit")

    async def fetch_items(self) -> List[Dict[str, Any]]:
        items = []
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AIViralRadar/1.0"}

        async with httpx.AsyncClient(timeout=8.0) as client:
            for sub in SUBREDDITS:
                url = f"https://www.reddit.com/r/{sub}/hot.json?limit=5"
                try:
                    resp = await client.get(url, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        now = datetime.now(timezone.utc)
                        for post_data in data.get("data", {}).get("children", []):
                            post = post_data.get("data", {})
                            if post.get("stickied"):
                                continue

                            score = post.get("score", 0)
                            num_comments = post.get("num_comments", 0)
                            title = post.get("title", "")
                            selftext = post.get("selftext", "")[:500]

                            items.append({
                                "title": title,
                                "content": selftext if selftext else title,
                                "url": f"https://reddit.com{post.get('permalink')}",
                                "source": f"r/{sub}",
                                "source_type": "reddit",
                                "author": post.get("author", "redditor"),
                                "author_handle": f"u/{post.get('author')}",
                                "author_url": f"https://reddit.com/user/{post.get('author')}",
                                "published_at": now - timedelta(hours=3),
                                "views": score * 40,
                                "likes": score,
                                "reposts": int(score * 0.15),
                                "replies": num_comments,
                                "quotes": int(score * 0.05),
                                "topic": "Open Source" if sub == "LocalLLaMA" else "Research",
                                "content_type": "discussion",
                                "hook_type": "curiosity",
                                "hashtags": [f"#{sub}", "#AICommunity"]
                            })
                except Exception as e:
                    logger.debug(f"Reddit error for r/{sub}: {e}")

        return items

reddit_provider = RedditProvider()
