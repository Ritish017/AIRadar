"""
Global Intelligence Search Service:
Performs unified multi-entity search across Events, News, Trends, Sources, and Opportunities.
"""

import logging
from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, desc

from backend.db.models import Event, Topic, ContentItem

logger = logging.getLogger(__name__)

class GlobalSearchService:
    """Multi-entity intelligence search across live events, news, and trends."""

    async def search(self, query_str: str, db: AsyncSession, limit: int = 20) -> Dict[str, Any]:
        q = query_str.strip().lower()
        if not q:
            return {"query": query_str, "total_results": 0, "events": [], "news": [], "trends": []}

        # Search Events
        event_stmt = select(Event).where(
            or_(
                Event.canonical_title.ilike(f"%{q}%"),
                Event.summary.ilike(f"%{q}%"),
                Event.category.ilike(f"%{q}%")
            )
        ).order_by(desc(Event.momentum_score)).limit(limit)
        event_res = await db.execute(event_stmt)
        events = event_res.scalars().all()

        # Search Trends (Topics)
        topic_stmt = select(Topic).where(
            or_(
                Topic.name.ilike(f"%{q}%"),
                Topic.category.ilike(f"%{q}%")
            )
        ).order_by(desc(Topic.momentum)).limit(limit)
        topic_res = await db.execute(topic_stmt)
        topics = topic_res.scalars().all()

        # Search News (ContentItems)
        news_stmt = select(ContentItem).where(
            or_(
                ContentItem.title.ilike(f"%{q}%"),
                ContentItem.content.ilike(f"%{q}%"),
                ContentItem.source.ilike(f"%{q}%")
            )
        ).order_by(desc(ContentItem.published_at)).limit(limit)
        news_res = await db.execute(news_stmt)
        news = news_res.scalars().all()

        total = len(events) + len(topics) + len(news)

        return {
            "query": query_str,
            "total_results": total,
            "events": [
                {
                    "id": e.id,
                    "title": e.canonical_title,
                    "category": e.category,
                    "status": e.status,
                    "confidence": e.confidence_score,
                    "momentum": e.momentum_score,
                    "published_at": e.event_timestamp.isoformat() if e.event_timestamp else None
                }
                for e in events
            ],
            "trends": [
                {
                    "id": t.id,
                    "name": t.name,
                    "category": t.category,
                    "momentum": t.momentum,
                    "lifecycle": t.lifecycle_stage,
                    "opportunity": t.opportunity_score
                }
                for t in topics
            ],
            "news": [
                {
                    "id": n.id,
                    "title": n.title,
                    "source": n.source,
                    "url": n.url,
                    "published_at": n.published_at.isoformat() if n.published_at else None
                }
                for n in news
            ]
        }

global_search_service = GlobalSearchService()
