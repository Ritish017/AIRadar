"""
Trend Relationship Graph Service.
Constructs multi-dimensional semantic graph networks (nodes, edges, clusters)
connecting Trends, Entities, Categories, and Events for the interactive Live Radar view.
"""

import logging
from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from sqlalchemy.orm import selectinload

from backend.db.models import Topic, Event

logger = logging.getLogger(__name__)

class TrendGraphService:
    """
    Constructs node-link relationship graphs between active AI Trends,
    high-signal Events, and key industry Entities.
    """

    async def build_relationship_graph(
        self,
        db: AsyncSession,
        topic_limit: int = 15,
        event_limit: int = 10
    ) -> Dict[str, Any]:
        # 1. Fetch top topics by momentum & opportunity
        topics_stmt = select(Topic).order_by(desc(Topic.momentum)).limit(topic_limit)
        topics_res = await db.execute(topics_stmt)
        topics = topics_res.scalars().all()

        # 2. Fetch top events
        events_stmt = select(Event).order_by(desc(Event.momentum_score)).limit(event_limit)
        events_res = await db.execute(events_stmt)
        events = events_res.scalars().all()

        nodes = []
        links = []
        node_ids = set()

        # Add Category / Hub Nodes
        categories = {t.category for t in topics if t.category} or {"AI Models", "AI Coding", "Agents", "Research"}
        for cat in categories:
            cat_id = f"cat_{cat.lower().replace(' ', '_')}"
            if cat_id not in node_ids:
                nodes.append({
                    "id": cat_id,
                    "name": cat,
                    "type": "category",
                    "group": 1,
                    "size": 32,
                    "color": "#8b5cf6"  # violet
                })
                node_ids.add(cat_id)

        # Add Trend Nodes
        for t in topics:
            trend_id = f"trend_{t.id}"
            if trend_id not in node_ids:
                lifecycle = t.lifecycle_stage or "RISING"
                color = "#f43f5e" if lifecycle in ("EXPLODING", "RISING") else "#38bdf8"
                nodes.append({
                    "id": trend_id,
                    "name": t.name,
                    "type": "trend",
                    "group": 2,
                    "size": min(36, max(18, int((t.momentum or 50) / 3.0))),
                    "momentum": t.momentum,
                    "opportunity": t.opportunity_score,
                    "lifecycle": lifecycle,
                    "category": t.category,
                    "color": color
                })
                node_ids.add(trend_id)

                # Link trend to its category
                if t.category:
                    cat_id = f"cat_{t.category.lower().replace(' ', '_')}"
                    if cat_id in node_ids:
                        links.append({
                            "source": cat_id,
                            "target": trend_id,
                            "value": 2,
                            "type": "category_link"
                        })

        # Add Event Nodes & Inter-trend Connections
        for ev in events:
            event_id = f"ev_{ev.id}"
            if event_id not in node_ids:
                nodes.append({
                    "id": event_id,
                    "name": ev.canonical_title[:45] + "...",
                    "full_title": ev.canonical_title,
                    "type": "event",
                    "group": 3,
                    "size": 20,
                    "status": ev.status,
                    "confidence": ev.confidence_score,
                    "color": "#10b981" if ev.status == "CONFIRMED" else "#f59e0b"
                })
                node_ids.add(event_id)

                # Connect event to relevant category
                if ev.category:
                    cat_id = f"cat_{ev.category.lower().replace(' ', '_')}"
                    if cat_id in node_ids:
                        links.append({
                            "source": event_id,
                            "target": cat_id,
                            "value": 1,
                            "type": "event_cat_link"
                        })

                # Connect event to matching trends via name overlap
                for t in topics:
                    trend_id = f"trend_{t.id}"
                    if trend_id in node_ids and any(w.lower() in ev.canonical_title.lower() for w in t.name.split()[:2] if len(w) > 3):
                        links.append({
                            "source": event_id,
                            "target": trend_id,
                            "value": 3,
                            "type": "event_trend_link"
                        })

        return {
            "nodes": nodes,
            "links": links,
            "meta": {
                "total_nodes": len(nodes),
                "total_links": len(links),
                "active_categories": list(categories)
            }
        }

trend_graph_service = TrendGraphService()
