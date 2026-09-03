import logging
from typing import List, Dict, Any
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from backend.providers.firecrawl_provider import firecrawl_provider
from backend.providers.mock_provider import mock_provider
from backend.providers.x_provider import x_provider
from backend.services.virality.scorer import virality_scorer
from backend.services.trends.trend_detector import trend_detector
from backend.services.trends.trend_momentum import trend_momentum_engine
from backend.services.trends.trend_lifecycle import trend_lifecycle_engine
from backend.services.trends.trend_competition import trend_competition_engine
from backend.services.trends.trend_audience import trend_audience_engine
from backend.services.trends.trend_opportunity import trend_opportunity_engine
from backend.services.trends.trend_strategy import trend_strategy_engine
from backend.db.models import ContentItem, Topic, TopicMention, TrendObservation

logger = logging.getLogger(__name__)

class ProviderManager:
    """
    Orchestrates data acquisition across Firecrawl and supplementary providers,
    performs SHA-256 deduplication, executes dual virality scoring, and feeds
    the comprehensive Trend Intelligence & Content Opportunity Engine.
    """

    def __init__(self):
        self.providers = [
            firecrawl_provider,
            mock_provider,
            x_provider
        ]

    async def ingest_all(self, db: AsyncSession) -> Dict[str, Any]:
        raw_items: List[Dict[str, Any]] = []

        # 1. Fetch items from active providers
        for provider in self.providers:
            try:
                items = await provider.fetch_items()
                logger.info(f"Provider {provider.name} yielded {len(items)} items")
                raw_items.extend(items)
            except Exception as e:
                logger.error(f"Error fetching from {provider.name}: {e}")

        # 2. Normalize and deduplicate by URL
        seen_urls = set()
        deduped_items = []
        for item in raw_items:
            url = item.get("url")
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            deduped_items.append(item)

        logger.info(f"Deduplicated down to {len(deduped_items)} unique items")

        # 3. Score virality & potential
        scored_items = []
        for item in deduped_items:
            pub_date = item.get("published_at") or datetime.now(timezone.utc)

            scores = virality_scorer.score_item(
                published_at=pub_date,
                title=item.get("title", ""),
                content=item.get("content", ""),
                views=item.get("views"),
                likes=item.get("likes"),
                reposts=item.get("reposts"),
                replies=item.get("replies"),
                quotes=item.get("quotes"),
                source_quality=item.get("source_quality", "Tier 1")
            )

            item.update(scores)
            scored_items.append(item)

        # 4. Persist ContentItems to DB
        saved_count = 0
        updated_count = 0
        saved_item_map = {}

        for item in scored_items:
            existing = await db.execute(
                select(ContentItem).where(ContentItem.url == item["url"])
            )
            record = existing.scalar_one_or_none()

            if record:
                if item.get("views") is not None:
                    record.views = item.get("views")
                if item.get("likes") is not None:
                    record.likes = item.get("likes")
                if item.get("reposts") is not None:
                    record.reposts = item.get("reposts")

                record.viral_potential = item.get("viral_potential", record.viral_potential)
                if item.get("viral_score") is not None:
                    record.viral_score = item.get("viral_score")

                record.last_seen_at = datetime.utcnow()
                saved_item_map[item["url"]] = record
                updated_count += 1
            else:
                pub_dt = item["published_at"]
                if hasattr(pub_dt, "tzinfo") and pub_dt.tzinfo:
                    pub_dt = pub_dt.replace(tzinfo=None)

                new_item = ContentItem(
                    source=item["source"],
                    source_type=item["source_type"],
                    source_quality=item.get("source_quality", "Tier 1"),
                    title=item.get("title"),
                    content=item["content"],
                    url=item["url"],
                    primary_source_url=item.get("primary_source_url", item["url"]),
                    source_count=item.get("source_count", 1),
                    author=item.get("author"),
                    author_handle=item.get("author_handle"),
                    author_url=item.get("author_url"),
                    published_at=pub_dt,
                    views=item.get("views"),
                    likes=item.get("likes"),
                    reposts=item.get("reposts"),
                    replies=item.get("replies"),
                    quotes=item.get("quotes"),
                    viral_score=item.get("viral_score"),
                    viral_potential=item.get("viral_potential", 75.0),
                    engagement_velocity=item.get("engagement_velocity", 0.0),
                    engagement_rate=item.get("engagement_rate"),
                    topic=item.get("topic", "AI Models"),
                    content_type=item.get("content_type", "news"),
                    hook_type=item.get("hook_type", "curiosity"),
                    hashtags=item.get("hashtags", []),
                    confirmed_facts=item.get("confirmed_facts", []),
                    uncertain_claims=item.get("uncertain_claims", []),
                    source_urls=[item["url"]]
                )
                db.add(new_item)
                saved_item_map[item["url"]] = new_item
                saved_count += 1

        await db.flush()

        # 5. Execute Comprehensive Trend Intelligence & Content Opportunity Pipeline
        trend_clusters = trend_detector.cluster_items(scored_items)

        for cluster in trend_clusters:
            cluster_name = cluster["name"]
            cluster_items = cluster["items"]
            item_count = len(cluster_items)
            sources = cluster["sources_summary"]
            source_count = len(sources)
            source_diversity = len(sources)

            avg_potential = sum(it.get("viral_potential", 75.0) for it in cluster_items) / max(1, item_count)
            novelty_score = min(98.0, max(50.0, 70.0 + (10.0 if "Tier 1" in cluster["source_qualities"] else 0.0)))
            importance_score = min(95.0, max(60.0, avg_potential * 0.95))
            discussion_score = min(92.0, max(45.0, item_count * 15.0 + source_count * 10.0))
            freshness_score = 90.0
            source_quality_score = 95.0 if "Tier 1" in cluster["source_qualities"] else 75.0

            # Retrieve existing topic and historical observations
            existing_t = await db.execute(
                select(Topic).where(Topic.name == cluster_name).options(selectinload(Topic.observations))
            )
            t_record = existing_t.scalar_one_or_none()

            history_list = []
            if t_record and t_record.observations:
                history_list = [
                    {
                        "timestamp": o.timestamp,
                        "mention_count": o.mention_count,
                        "momentum_score": o.momentum_score
                    }
                    for o in t_record.observations
                ]

            # A. Historical Momentum Engine
            momentum_data = trend_momentum_engine.evaluate_momentum(
                current_mentions=item_count,
                current_sources=source_count,
                current_diversity=source_diversity,
                avg_potential=avg_potential,
                history=history_list
            )

            # B. Competition Engine & Angle Decomposition
            comp_data = trend_competition_engine.analyze_competition(cluster_items)

            # C. Audience Intelligence
            combined_text = " ".join(it.get("title", "") for it in cluster_items)
            aud_data = trend_audience_engine.evaluate_audience(
                title=cluster_name,
                content=combined_text,
                category=cluster["category"]
            )

            # D. Lifecycle Engine
            lifecycle_data = trend_lifecycle_engine.determine_lifecycle(
                momentum_score=momentum_data["momentum_score"],
                momentum_change_pct=momentum_data["momentum_change_pct"],
                momentum_direction=momentum_data["momentum_direction"],
                competition_score=comp_data["competition_score"],
                novelty_score=novelty_score,
                item_count=item_count,
                source_count=source_count
            )

            # E. Opportunity Engine
            opp_score = trend_opportunity_engine.calculate_opportunity_score(
                momentum_score=momentum_data["momentum_score"],
                freshness_score=freshness_score,
                novelty_score=novelty_score,
                audience_fit_score=aud_data["audience_fit_score"],
                discussion_score=discussion_score,
                importance_score=importance_score,
                source_quality_score=source_quality_score,
                competition_score=comp_data["competition_score"]
            )

            opp_type, rec_action, action_reason = trend_opportunity_engine.classify_opportunity(
                opportunity_score=opp_score,
                lifecycle_stage=lifecycle_data["stage"],
                momentum_change_pct=momentum_data["momentum_change_pct"],
                competition_score=comp_data["competition_score"],
                novelty_score=novelty_score,
                audience_fit_score=aud_data["audience_fit_score"]
            )

            # F. Strategy Engine (Angles, 10 Hooks, Formats)
            has_benchmarks = any("benchmark" in (it.get("title", "") + it.get("content", "")).lower() for it in cluster_items)
            strat_data = trend_strategy_engine.synthesize_strategy(
                trend_name=cluster_name,
                category=cluster["category"],
                under_served_angles=comp_data["under_served_angles"],
                primary_audience=aud_data["primary_audience"],
                lifecycle_stage=lifecycle_data["stage"],
                has_benchmarks=has_benchmarks
            )

            # G. Persist or Update Topic
            if t_record:
                t_record.category = cluster["category"]
                t_record.momentum = momentum_data["momentum_score"]
                t_record.momentum_change_pct = momentum_data["momentum_change_pct"]
                t_record.momentum_direction = momentum_data["momentum_direction"]
                t_record.status = lifecycle_data["badge"]
                t_record.lifecycle_stage = lifecycle_data["stage"]
                t_record.opportunity_score = opp_score
                t_record.opportunity_type = opp_type
                t_record.competition_score = comp_data["competition_score"]
                t_record.novelty_score = novelty_score
                t_record.audience_fit_score = aud_data["audience_fit_score"]
                t_record.primary_audience = aud_data["primary_audience"]
                t_record.secondary_audiences = aud_data["secondary_audiences"]
                t_record.saturated_angles = comp_data["saturated_angles"]
                t_record.under_served_angles = comp_data["under_served_angles"]
                t_record.recommended_action = rec_action
                t_record.action_reason = action_reason
                t_record.recommended_angle = strat_data["recommended_angle"]
                t_record.alternative_angles = strat_data["alternative_angles"]
                t_record.recommended_hook_type = strat_data["recommended_hook_type"]
                t_record.hook_strategy = strat_data["hook_strategy"]
                t_record.recommended_format = strat_data["recommended_format"]
                t_record.format_scores = strat_data["format_scores"]
                t_record.item_count = item_count
                t_record.sources_summary = sources
                t_record.primary_source = cluster.get("primary_url")
                t_record.updated_at = datetime.utcnow()
                topic_entity = t_record
            else:
                topic_entity = Topic(
                    name=cluster_name,
                    category=cluster["category"],
                    momentum=momentum_data["momentum_score"],
                    momentum_change_pct=momentum_data["momentum_change_pct"],
                    momentum_direction=momentum_data["momentum_direction"],
                    status=lifecycle_data["badge"],
                    lifecycle_stage=lifecycle_data["stage"],
                    opportunity_score=opp_score,
                    opportunity_type=opp_type,
                    competition_score=comp_data["competition_score"],
                    novelty_score=novelty_score,
                    audience_fit_score=aud_data["audience_fit_score"],
                    primary_audience=aud_data["primary_audience"],
                    secondary_audiences=aud_data["secondary_audiences"],
                    saturated_angles=comp_data["saturated_angles"],
                    under_served_angles=comp_data["under_served_angles"],
                    recommended_action=rec_action,
                    action_reason=action_reason,
                    recommended_angle=strat_data["recommended_angle"],
                    alternative_angles=strat_data["alternative_angles"],
                    recommended_hook_type=strat_data["recommended_hook_type"],
                    hook_strategy=strat_data["hook_strategy"],
                    recommended_format=strat_data["recommended_format"],
                    format_scores=strat_data["format_scores"],
                    item_count=item_count,
                    sources_summary=sources,
                    primary_source=cluster.get("primary_url")
                )
                db.add(topic_entity)
                await db.flush()

            # Record Time-Series Trend Observation
            observation = TrendObservation(
                trend_id=topic_entity.id,
                timestamp=datetime.utcnow(),
                mention_count=item_count,
                source_count=source_count,
                source_diversity=source_diversity,
                momentum_score=momentum_data["momentum_score"],
                competition_score=comp_data["competition_score"],
                opportunity_score=opp_score
            )
            db.add(observation)

            # Link Content Items via TopicMention
            for it in cluster_items:
                c_item = saved_item_map.get(it["url"])
                if c_item:
                    existing_m = await db.execute(
                        select(TopicMention).where(
                            TopicMention.topic_id == topic_entity.id,
                            TopicMention.content_item_id == c_item.id
                        )
                    )
                    if not existing_m.scalar_one_or_none():
                        mention = TopicMention(
                            topic_id=topic_entity.id,
                            content_item_id=c_item.id
                        )
                        db.add(mention)

        await db.commit()

        return {
            "total_fetched": len(raw_items),
            "deduplicated": len(deduped_items),
            "new_saved": saved_count,
            "updated": updated_count,
            "trends_detected": len(trend_clusters)
        }

provider_manager = ProviderManager()
