import logging
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any
import httpx
from backend.providers.base import BaseProvider

logger = logging.getLogger(__name__)

class GitHubProvider(BaseProvider):
    def __init__(self):
        super().__init__(name="GitHub Trending AI", source_type="github")

    async def fetch_items(self) -> List[Dict[str, Any]]:
        items = []
        # Query top trending AI / LLM repos from past 7 days
        seven_days_ago = (datetime.now(timezone.utc) - timedelta(days=7)).strftime("%Y-%m-%d")
        query_url = f"https://api.github.com/search/repositories?q=topic:llm+created:>{seven_days_ago}&sort=stars&order=desc&per_page=8"

        headers = {
            "User-Agent": "AIViralRadar/1.0",
            "Accept": "application/vnd.github.v3+json"
        }

        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                resp = await client.get(query_url, headers=headers)
                if resp.status_code == 200:
                    data = resp.json()
                    now = datetime.now(timezone.utc)
                    for repo in data.get("items", []):
                        stars = repo.get("stargazers_count", 0)
                        forks = repo.get("forks_count", 0)
                        desc = repo.get("description") or "Open source AI project"

                        items.append({
                            "title": f"GitHub Trending: {repo.get('full_name')} ({stars} stars)",
                            "content": f"{desc}. Topics: {', '.join(repo.get('topics', []))}. Language: {repo.get('language')}",
                            "url": repo.get("html_url"),
                            "source": "GitHub",
                            "source_type": "github",
                            "author": repo.get("owner", {}).get("login", "open-source"),
                            "author_handle": repo.get("owner", {}).get("login", ""),
                            "author_url": repo.get("owner", {}).get("html_url", ""),
                            "published_at": now - timedelta(hours=3),
                            "views": stars * 12,
                            "likes": stars,
                            "reposts": forks,
                            "replies": repo.get("open_issues_count", 0),
                            "quotes": int(forks * 0.3),
                            "topic": "Coding",
                            "content_type": "tool",
                            "hook_type": "curiosity",
                            "hashtags": ["#GitHub", "#OpenSource", "#AI"]
                        })
        except Exception as e:
            logger.debug(f"GitHub API fetch error: {e}")

        return items

github_provider = GitHubProvider()
