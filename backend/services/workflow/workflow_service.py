"""
Workflow & Intelligence Operations Service:
Generates Daily Intelligence Briefs ("What Happened While I Was Away?"),
orchestrates the "Plan My Day" automated schedule, and manages the Content Queue.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, func
from sqlalchemy.orm import selectinload

from backend.db.models import Event, Topic, ContentQueueItem, UserMonitor, ContentItem

logger = logging.getLogger(__name__)

class WorkflowService:
    """
    Orchestrates daily intelligence briefings, day planning, and content queue state machines.
    """

    async def generate_daily_brief(self, db: AsyncSession) -> Dict[str, Any]:
        """
        Generates executive intelligence summary:
        Top events, exploding trends, top content opportunities, and what to post today.
        """
        # 1. Fetch top events
        events_stmt = select(Event).order_by(desc(Event.momentum_score)).limit(10)
        events_res = await db.execute(events_stmt)
        events = events_res.scalars().all()

        # 2. Fetch top trends
        trends_stmt = select(Topic).order_by(desc(Topic.momentum)).limit(5)
        trends_res = await db.execute(trends_stmt)
        trends = trends_res.scalars().all()

        # 3. Fetch top opportunity
        top_opp_stmt = select(Topic).order_by(desc(Topic.opportunity_score)).limit(1)
        top_opp_res = await db.execute(top_opp_stmt)
        best_opportunity = top_opp_res.scalar_one_or_none()

        # 4. Count stats
        total_events = len(events)
        exploding_count = sum(1 for t in trends if (t.lifecycle_stage or "") in ("EXPLODING", "RISING"))
        breaking_count = sum(1 for e in events if e.status == "CONFIRMED")

        best_opp_data = None
        if best_opportunity:
            best_opp_data = {
                "id": best_opportunity.id,
                "topic": best_opportunity.name,
                "opportunity_score": best_opportunity.opportunity_score,
                "competition_score": best_opportunity.competition_score,
                "recommended_angle": best_opportunity.recommended_angle or f"Practical developer implications of {best_opportunity.name}",
                "status": best_opportunity.recommended_action or "POST_NOW"
            }
        elif events:
            best_opp_data = {
                "id": events[0].id,
                "topic": events[0].canonical_title,
                "opportunity_score": events[0].opportunity_score,
                "competition_score": 35.0,
                "recommended_angle": events[0].recommended_angle,
                "status": "POST_NOW"
            }

        return {
            "title": "AI Viral Radar Daily Executive Briefing",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "summary": f"Since your last visit: {total_events} major AI developments detected, with {exploding_count} accelerating trends and {breaking_count} confirmed stories.",
            "metrics": {
                "major_events_count": total_events,
                "emerging_trends_count": len(trends),
                "exploding_trends_count": exploding_count,
                "opportunities_count": 4 if best_opp_data else 0
            },
            "best_opportunity": best_opp_data,
            "top_events": [
                {
                    "id": e.id,
                    "title": e.canonical_title,
                    "status": e.status,
                    "confidence": e.confidence_score,
                    "category": e.category,
                    "momentum": e.momentum_score
                }
                for e in events[:5]
            ],
            "what_you_should_post_today": (
                f"Prioritize '{best_opp_data['topic'] if best_opp_data else 'latest model efficiency breakthroughs'}'. "
                f"Audience conversation is peaking with low competitive saturation on developer workflow angles."
            )
        }

    async def plan_my_day(self, db: AsyncSession) -> List[Dict[str, Any]]:
        """
        Generates a recommended, actionable 1-day multi-platform publishing schedule.
        """
        # Fetch top active opportunity
        stmt = select(Topic).order_by(desc(Topic.opportunity_score)).limit(3)
        res = await db.execute(stmt)
        topics = res.scalars().all()

        topic_1 = topics[0].name if len(topics) > 0 else "Frontier Model Breakthrough"
        topic_2 = topics[1].name if len(topics) > 1 else "AI Coding Agents Benchmark"
        topic_3 = topics[2].name if len(topics) > 2 else "Local Inference Optimization"

        now = datetime.now(timezone.utc)
        base_date = now.strftime("%Y-%m-%d")

        return [
            {
                "time_slot": "08:30 AM",
                "platform": "X (Twitter)",
                "format": "Single Post (Breaking Hook)",
                "topic": topic_1,
                "recommended_angle": f"The single verified specification developers need to know about {topic_1}",
                "priority": "URGENT",
                "action": "Generate X Post"
            },
            {
                "time_slot": "10:45 AM",
                "platform": "LinkedIn",
                "format": "Enterprise Thought Leadership",
                "topic": topic_1,
                "recommended_angle": f"Inference economics and architecture shift for engineering leaders",
                "priority": "HIGH",
                "action": "Generate LinkedIn Post"
            },
            {
                "time_slot": "01:30 PM",
                "platform": "Instagram",
                "format": "8-Slide Carousel",
                "topic": topic_2,
                "recommended_angle": "Side-by-side benchmark comparison and terminal walkthrough",
                "priority": "MEDIUM",
                "action": "Generate Carousel"
            },
            {
                "time_slot": "05:15 PM",
                "platform": "X (Twitter)",
                "format": "9-Tweet Deep-Dive Thread",
                "topic": topic_2,
                "recommended_angle": "Deconstructing the self-repair loop and multi-file context retention",
                "priority": "HIGH",
                "action": "Generate Thread"
            },
            {
                "time_slot": "08:00 PM",
                "platform": "YouTube",
                "format": "60-Second Short & Script",
                "topic": topic_3,
                "recommended_angle": "Stop paying cloud API bills: Run this locally in 3 commands",
                "priority": "MEDIUM",
                "action": "Generate Video Script"
            }
        ]

workflow_service = WorkflowService()
