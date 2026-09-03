import logging
from datetime import datetime, timezone, timedelta
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, desc, func, nulls_last, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from backend.db.session import get_db
from backend.db.models import (
    ContentItem, Topic, Analysis, GeneratedPost, SavedItem, VoiceProfile,
    TrendObservation, TrendStrategy, ContentPerformance, TopicMention
)
from backend.schemas.content import (
    ContentItemBase, FeedResponse, TopicResponse, GenerateRequest,
    AnalysisSchema, GeneratedVariantSchema, SaveStoryRequest,
    SavedItemResponse, VoiceProfileRequest, VoiceProfileResponse,
    OpportunityCardResponse, TopOpportunitiesResponse, SourceEvidenceItem,
    TrendDetailResponse, ContentPerformanceSchema
)
from backend.providers.manager import provider_manager
from backend.services.ai.analysis import ai_analysis_service
from backend.services.ai.generation import ai_post_generator
from backend.services.ai.trend_strategist import trend_strategist
from backend.services.virality.scorer import virality_scorer

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api")

def utc_now() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AI Viral Radar API v2 (Trend Intelligence Engine)",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "providers_active": len(provider_manager.providers)
    }

@router.post("/collect")
async def trigger_collection(db: AsyncSession = Depends(get_db)):
    """Manually triggers content ingestion across all providers."""
    result = await provider_manager.ingest_all(db)
    return {"message": "Ingestion completed successfully", "stats": result}

@router.get("/feed", response_model=FeedResponse)
async def get_feed(
    topic: Optional[str] = Query(None, description="Category filter (e.g. Models, Agents, Research)"),
    sort_by: str = Query("viral", description="viral, rising, newest, engagement, velocity"),
    time_range: str = Query("all", description="15m, 1h, 6h, 24h, 7d, all"),
    source_type: Optional[str] = Query(None),
    min_viral_score: Optional[float] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    query = select(ContentItem).options(
        selectinload(ContentItem.analysis),
        selectinload(ContentItem.generated_variants)
    )

    # Filter topic
    if topic and topic.lower() != "all":
        query = query.where(ContentItem.topic.ilike(f"%{topic}%"))

    # Filter source_type
    if source_type and source_type.lower() != "all":
        query = query.where(ContentItem.source_type == source_type.lower())

    # Filter minimum score
    if min_viral_score is not None:
        effective_score_expr = func.coalesce(ContentItem.viral_score, ContentItem.viral_potential)
        query = query.where(effective_score_expr >= min_viral_score)

    # Filter time range
    now = utc_now()
    if time_range == "15m":
        query = query.where(ContentItem.published_at >= now - timedelta(minutes=15))
    elif time_range == "1h":
        query = query.where(ContentItem.published_at >= now - timedelta(hours=1))
    elif time_range == "6h":
        query = query.where(ContentItem.published_at >= now - timedelta(hours=6))
    elif time_range == "24h":
        query = query.where(ContentItem.published_at >= now - timedelta(hours=24))
    elif time_range == "7d":
        query = query.where(ContentItem.published_at >= now - timedelta(days=7))

    # Dual Virality Sorting Expression
    effective_score = func.coalesce(ContentItem.viral_score, ContentItem.viral_potential)

    if sort_by == "newest":
        query = query.order_by(desc(ContentItem.published_at))
    elif sort_by == "engagement":
        query = query.order_by(nulls_last(desc(ContentItem.engagement_rate)), desc(effective_score))
    elif sort_by == "velocity":
        query = query.order_by(desc(ContentItem.engagement_velocity), desc(effective_score))
    elif sort_by == "rising":
        query = query.where(effective_score.between(50, 88)).order_by(desc(ContentItem.engagement_velocity), desc(effective_score))
    else:  # default viral
        query = query.order_by(desc(effective_score), desc(ContentItem.published_at))

    # Total count
    count_query = select(func.count()).select_from(query.subquery())
    total = (await db.execute(count_query)).scalar_one()

    # Pagination
    items_query = query.offset((page - 1) * page_size).limit(page_size)
    result = await db.execute(items_query)
    items = result.scalars().all()

    # Initial bootstrap if empty
    if total == 0 and page == 1:
        await provider_manager.ingest_all(db)
        result = await db.execute(items_query)
        items = result.scalars().all()
        total = len(items)

    return FeedResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=items
    )

# -------------------------------------------------------------------------
# TREND INTELLIGENCE & CONTENT OPPORTUNITY ENGINE ENDPOINTS
# -------------------------------------------------------------------------

@router.get("/opportunities", response_model=TopOpportunitiesResponse)
async def get_top_opportunities(
    limit: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns the TOP CONTENT OPPORTUNITIES ranked by opportunity_score.
    Powers the '⚡ WHAT SHOULD I POST?' Engine and Content Opportunities view.
    """
    topics_query = select(Topic).order_by(desc(Topic.opportunity_score)).limit(limit)
    res = await db.execute(topics_query)
    topics = res.scalars().all()

    # Bootstrap if DB is empty
    if not topics:
        await provider_manager.ingest_all(db)
        res = await db.execute(topics_query)
        topics = res.scalars().all()

    total_count = (await db.execute(select(func.count(Topic.id)))).scalar_one()

    opportunity_cards: List[OpportunityCardResponse] = []
    for idx, t in enumerate(topics, start=1):
        opportunity_cards.append(OpportunityCardResponse(
            rank=idx,
            id=t.id,
            topic=t.name,
            category=t.category or "AI Models",
            opportunity_score=t.opportunity_score or 70.0,
            opportunity_type=t.opportunity_type or "RISING_OPPORTUNITY",
            lifecycle=t.lifecycle_stage or "RISING",
            lifecycle_badge=t.status or "📈 Rising",
            momentum=t.momentum or 75.0,
            momentum_change_pct=t.momentum_change_pct or 0.0,
            momentum_direction=t.momentum_direction or "STABLE",
            competition=t.competition_score or 40.0,
            novelty=t.novelty_score or 80.0,
            audience_fit=t.audience_fit_score or 85.0,
            primary_audience=t.primary_audience or "AI Engineers",
            recommended_action=t.recommended_action or "POST_SOON",
            action_reason=t.action_reason or "Strong momentum with under-served developer angles.",
            recommended_angle=t.recommended_angle or f"Practical developer workflow impact of {t.name}",
            alternative_angles=t.alternative_angles or [],
            recommended_hook=t.recommended_hook_type or "contrarian",
            hook_strategy=t.hook_strategy or "Challenge the prevailing assumption regarding adoption speed.",
            recommended_format=t.recommended_format or "single_post",
            format_scores=t.format_scores or {"single_post": 90, "thread": 85},
            item_count=t.item_count or 1,
            primary_source=t.primary_source,
            sources_summary=t.sources_summary or []
        ))

    return TopOpportunitiesResponse(
        total_trends_analyzed=total_count,
        top_opportunities=opportunity_cards,
        generated_at=datetime.now(timezone.utc)
    )

@router.get("/trending")
async def get_trending(db: AsyncSession = Depends(get_db)):
    """Returns top viral content items for quick trending view."""
    query = select(ContentItem).options(
        selectinload(ContentItem.analysis),
        selectinload(ContentItem.generated_variants)
    ).order_by(desc(func.coalesce(ContentItem.viral_score, ContentItem.viral_potential))).limit(10)
    res = await db.execute(query)
    items = res.scalars().all()
    return {"trending_items": items, "count": len(items)}

@router.get("/trends", response_model=List[TopicResponse])
@router.get("/topics", response_model=List[TopicResponse])
async def get_trends(
    sort_by: str = Query("opportunity", description="opportunity, momentum, newest"),
    limit: int = Query(25, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):
    """
    Returns active tracked trends for the Trend Radar visualization.
    """
    query = select(Topic)
    if sort_by == "momentum":
        query = query.order_by(desc(Topic.momentum))
    elif sort_by == "newest":
        query = query.order_by(desc(Topic.updated_at))
    else:
        query = query.order_by(desc(Topic.opportunity_score), desc(Topic.momentum))

    query = query.limit(limit)
    res = await db.execute(query)
    topics = res.scalars().all()

    if not topics:
        await provider_manager.ingest_all(db)
        res = await db.execute(query)
        topics = res.scalars().all()

    return topics

@router.get("/trends/{topic_id}", response_model=TrendDetailResponse)
async def get_trend_detail(topic_id: str, db: AsyncSession = Depends(get_db)):
    """
    Returns full strategic breakdown of a trend for the Trend Detail View:
    What happened, why trending, what changed, saturated vs under-served angles,
    who cares, hook, format, timing, source evidence, and observation history.
    """
    query = select(Topic).options(
        selectinload(Topic.observations),
        selectinload(Topic.strategy)
    ).where(Topic.id == topic_id)
    res = await db.execute(query)
    topic = res.scalar_one_or_none()
    if not topic:
        raise HTTPException(status_code=404, detail="Trend topic not found")

    # Fetch linked content items for source evidence
    mentions_res = await db.execute(
        select(ContentItem).join(TopicMention).where(TopicMention.topic_id == topic_id)
    )
    items = mentions_res.scalars().all()

    # Build traceable source evidence list
    source_evidence: List[SourceEvidenceItem] = []
    if items:
        for idx, it in enumerate(items):
            role = "Primary Source" if idx == 0 else ("Official Lab Blog" if it.source_quality == "Tier 1" else "Supporting Press")
            source_evidence.append(SourceEvidenceItem(
                title=it.title or "AI Development Release Note",
                url=it.url,
                source=it.source,
                source_quality=it.source_quality or "Tier 1",
                published_at=it.published_at,
                role=role
            ))
    elif topic.primary_source:
        source_evidence.append(SourceEvidenceItem(
            title=topic.name,
            url=topic.primary_source,
            source="Official Source",
            source_quality="Tier 1",
            published_at=topic.updated_at,
            role="Primary Source"
        ))

    strat = topic.strategy

    return TrendDetailResponse(
        id=topic.id,
        name=topic.name,
        category=topic.category or "AI Models",
        lifecycle_stage=topic.lifecycle_stage or "RISING",
        status=topic.status or "📈 Rising",
        opportunity_score=topic.opportunity_score or 70.0,
        opportunity_type=topic.opportunity_type or "RISING_OPPORTUNITY",
        competition_score=topic.competition_score or 40.0,
        novelty_score=topic.novelty_score or 80.0,
        audience_fit_score=topic.audience_fit_score or 85.0,
        momentum=topic.momentum or 75.0,
        momentum_change_pct=topic.momentum_change_pct or 0.0,
        momentum_direction=topic.momentum_direction or "STABLE",
        what_happened=strat.what_happened if strat else f"Major architectural update announced across {topic.name}.",
        why_trending=strat.why_trending if strat else "Rapid adoption and debate across AI engineer and technical founder communities.",
        what_changed=strat.what_changed if strat else "Inference economics and agent reliability benchmarks have shifted significantly.",
        what_is_saturated=strat.what_is_saturated if strat else ", ".join(topic.saturated_angles or ["Generic release headlines"]),
        what_is_missing=strat.what_is_missing if strat else ", ".join(topic.under_served_angles or ["Production latency and cost comparisons"]),
        who_cares=strat.who_cares if strat else f"{topic.primary_audience} optimizing production toolchains.",
        best_angle=strat.best_angle if strat else (topic.recommended_angle or f"Architectural tradeoffs in {topic.name}"),
        alternative_angles=strat.alternative_angles if strat else (topic.alternative_angles or []),
        saturated_angles=topic.saturated_angles or [],
        under_served_angles=topic.under_served_angles or [],
        best_hook_type=strat.best_hook_type if strat else (topic.recommended_hook_type or "contrarian"),
        hook_strategy=strat.hook_strategy if strat else (topic.hook_strategy or "Challenge the prevailing consensus."),
        best_format=strat.best_format if strat else (topic.recommended_format or "single_post"),
        format_scores=strat.format_recommendations if strat else (topic.format_scores or {"single_post": 90, "thread": 85}),
        timing_verdict=strat.timing_verdict if strat else (topic.recommended_action or "POST_NOW"),
        timing_reason=strat.timing_reason if strat else (topic.action_reason or "Accelerating momentum with under-served developer angles."),
        claims_to_avoid=strat.claims_to_avoid if strat else ["Unverified benchmark claims without reproducible evals"],
        source_evidence=source_evidence,
        observations=topic.observations or []
    )

@router.post("/trends/{topic_id}/strategy")
async def generate_trend_strategy(topic_id: str, db: AsyncSession = Depends(get_db)):
    """Runs Gemini AI Content Strategist on the trend and caches results."""
    query = select(Topic).options(
        selectinload(Topic.observations),
        selectinload(Topic.strategy)
    ).where(Topic.id == topic_id)
    res = await db.execute(query)
    topic = res.scalar_one_or_none()
    if not topic:
        raise HTTPException(status_code=404, detail="Trend not found")

    mentions_res = await db.execute(
        select(ContentItem).join(TopicMention).where(TopicMention.topic_id == topic_id)
    )
    items = mentions_res.scalars().all()

    trend_payload = {
        "name": topic.name,
        "category": topic.category,
        "lifecycle_stage": topic.lifecycle_stage,
        "momentum": topic.momentum,
        "momentum_change_pct": topic.momentum_change_pct,
        "competition_score": topic.competition_score,
        "primary_audience": topic.primary_audience,
        "saturated_angles": topic.saturated_angles or [],
        "under_served_angles": topic.under_served_angles or [],
        "recommended_action": topic.recommended_action,
        "action_reason": topic.action_reason,
        "items": [
            {"title": it.title, "source": it.source, "source_quality": it.source_quality, "content": it.content[:200]}
            for it in items
        ]
    }

    ai_strategy = await trend_strategist.analyze_trend_strategy(trend_payload)

    # Persist or update strategy
    if topic.strategy:
        strat = topic.strategy
        strat.what_happened = ai_strategy.what_happened
        strat.why_trending = ai_strategy.why_trending
        strat.what_changed = ai_strategy.what_changed
        strat.what_is_saturated = ai_strategy.what_is_saturated
        strat.what_is_missing = ai_strategy.what_is_missing
        strat.who_cares = ai_strategy.who_cares
        strat.best_angle = ai_strategy.best_angle
        strat.alternative_angles = ai_strategy.alternative_angles
        strat.best_hook_type = ai_strategy.best_hook_type
        strat.hook_strategy = ai_strategy.hook_strategy
        strat.best_format = ai_strategy.best_format
        strat.format_recommendations = ai_strategy.format_recommendations
        strat.timing_verdict = ai_strategy.timing_verdict
        strat.timing_reason = ai_strategy.timing_reason
        strat.claims_to_avoid = ai_strategy.claims_to_avoid
    else:
        new_strat = TrendStrategy(
            trend_id=topic.id,
            what_happened=ai_strategy.what_happened,
            why_trending=ai_strategy.why_trending,
            what_changed=ai_strategy.what_changed,
            what_is_saturated=ai_strategy.what_is_saturated,
            what_is_missing=ai_strategy.what_is_missing,
            who_cares=ai_strategy.who_cares,
            best_angle=ai_strategy.best_angle,
            alternative_angles=ai_strategy.alternative_angles,
            best_hook_type=ai_strategy.best_hook_type,
            hook_strategy=ai_strategy.hook_strategy,
            best_format=ai_strategy.best_format,
            format_recommendations=ai_strategy.format_recommendations,
            timing_verdict=ai_strategy.timing_verdict,
            timing_reason=ai_strategy.timing_reason,
            claims_to_avoid=ai_strategy.claims_to_avoid
        )
        db.add(new_strat)

    await db.commit()
    return ai_strategy

@router.post("/generate-from-opportunity")
async def generate_from_opportunity(payload: dict, db: AsyncSession = Depends(get_db)):
    """
    Creates original post variants conditioned on a specific opportunity strategy.
    Connects 'What Should I Post?' and 'Content Opportunities' directly into Post Studio.
    """
    opportunity_id = payload.get("opportunity_id")
    topic_res = await db.execute(
        select(Topic).where(Topic.id == opportunity_id)
    )
    topic = topic_res.scalar_one_or_none()
    if not topic:
        raise HTTPException(status_code=404, detail="Opportunity trend not found")

    # Find first linked ContentItem or most viral ContentItem in this category
    item_res = await db.execute(
        select(ContentItem).join(TopicMention).where(TopicMention.topic_id == opportunity_id).limit(1)
    )
    content_item = item_res.scalar_one_or_none()

    if not content_item:
        cat_res = await db.execute(
            select(ContentItem).order_by(desc(ContentItem.viral_potential)).limit(1)
        )
        content_item = cat_res.scalar_one_or_none()

    if not content_item:
        raise HTTPException(status_code=404, detail="No source content found for this opportunity")

    # Fetch voice profile
    vp_res = await db.execute(select(VoiceProfile).limit(1))
    vp = vp_res.scalar_one_or_none()
    voice_dict = {
        "tone_preference": vp.tone_preference,
        "voice_examples": vp.voice_examples
    } if vp else None

    # Use opportunity recommended angle & hook
    angle = payload.get("angle") or topic.recommended_angle
    hook_type = payload.get("hook_type") or topic.recommended_hook_type
    hook_strat = topic.hook_strategy

    variants = await ai_post_generator.generate_variants(
        item={
            "title": content_item.title or topic.name,
            "content": content_item.content,
            "url": content_item.url,
            "author": content_item.author or "AI Lab",
            "source": content_item.source
        },
        analysis={
            "summary": f"Key development in {topic.name}.",
            "key_facts": [topic.name, topic.category],
            "recommended_angle": angle
        },
        tone=payload.get("tone", "technical"),
        length=payload.get("length", "medium"),
        voice_profile=voice_dict,
        angle=angle,
        hook_strategy=f"Use a {hook_type} hook. {hook_strat or ''}"
    )

    return {
        "topic": topic.name,
        "opportunity_score": topic.opportunity_score,
        "recommended_angle": angle,
        "recommended_hook": hook_type,
        "content_item_id": content_item.id,
        "variants": variants
    }

# -------------------------------------------------------------------------
# CONTENT ITEM DETAILS, ANALYSIS & GENERATION
# -------------------------------------------------------------------------

@router.get("/content/{content_id}", response_model=ContentItemBase)
async def get_content_item(content_id: str, db: AsyncSession = Depends(get_db)):
    query = select(ContentItem).options(
        selectinload(ContentItem.analysis),
        selectinload(ContentItem.generated_variants)
    ).where(ContentItem.id == content_id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Content item not found")
    return item

@router.post("/content/{content_id}/analyze", response_model=AnalysisSchema)
async def analyze_content(content_id: str, db: AsyncSession = Depends(get_db)):
    """Analyzes a content item with AI virality & hook extraction."""
    query = select(ContentItem).options(
        selectinload(ContentItem.analysis)
    ).where(ContentItem.id == content_id)

    result = await db.execute(query)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Content item not found")

    if item.analysis:
        return AnalysisSchema(
            summary=item.analysis.summary,
            main_claim=item.analysis.main_claim,
            why_viral=item.analysis.why_viral or [],
            hook_type=item.analysis.hook_type,
            content_type=item.analysis.content_type,
            key_facts=item.analysis.key_facts or [],
            important_entities=item.analysis.important_entities or [],
            audience=item.analysis.audience,
            recommended_angle=item.analysis.recommended_angle,
            risk_flags=item.analysis.risk_flags or [],
            confirmed_facts=item.analysis.confirmed_facts or [],
            uncertain_claims=item.analysis.uncertain_claims or [],
            viral_potential=item.analysis.viral_potential or 75.0
        )

    item_dict = {
        "title": item.title,
        "content": item.content,
        "source": item.source,
        "author": item.author,
        "published_at": str(item.published_at),
        "url": item.url,
        "views": item.views,
        "likes": item.likes,
        "topic": item.topic,
        "content_type": item.content_type,
        "viral_potential": item.viral_potential
    }

    analysis_result = await ai_analysis_service.analyze_content_item(item_dict)

    new_analysis = Analysis(
        content_item_id=item.id,
        summary=analysis_result.summary,
        main_claim=analysis_result.main_claim,
        why_viral=analysis_result.why_viral,
        hook_type=analysis_result.hook_type,
        content_type=analysis_result.content_type,
        key_facts=analysis_result.key_facts,
        important_entities=analysis_result.important_entities,
        audience=analysis_result.audience,
        recommended_angle=analysis_result.recommended_angle,
        risk_flags=analysis_result.risk_flags,
        confirmed_facts=analysis_result.confirmed_facts,
        uncertain_claims=analysis_result.uncertain_claims,
        viral_potential=analysis_result.viral_potential
    )
    db.add(new_analysis)
    await db.commit()

    return analysis_result

@router.post("/content/{content_id}/generate", response_model=List[GeneratedVariantSchema])
async def generate_posts(
    content_id: str,
    req: GenerateRequest,
    db: AsyncSession = Depends(get_db)
):
    query = select(ContentItem).options(
        selectinload(ContentItem.analysis),
        selectinload(ContentItem.generated_variants)
    ).where(ContentItem.id == content_id)
    result = await db.execute(query)
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Content item not found")

    analysis_dict = None
    if item.analysis:
        analysis_dict = {
            "summary": item.analysis.summary,
            "main_claim": item.analysis.main_claim,
            "key_facts": item.analysis.key_facts or [],
            "recommended_angle": item.analysis.recommended_angle
        }
    else:
        analyzed = await ai_analysis_service.analyze_content_item({
            "title": item.title,
            "content": item.content,
            "source": item.source,
            "url": item.url,
            "viral_potential": item.viral_potential
        })
        analysis_dict = {
            "summary": analyzed.summary,
            "main_claim": analyzed.main_claim,
            "key_facts": analyzed.key_facts or [],
            "recommended_angle": analyzed.recommended_angle
        }

    voice_dict = None
    if req.include_voice_profile:
        vp_res = await db.execute(select(VoiceProfile).limit(1))
        vp = vp_res.scalar_one_or_none()
        if vp:
            voice_dict = {
                "tone_preference": vp.tone_preference,
                "voice_examples": vp.voice_examples
            }

    item_dict = {
        "title": item.title,
        "content": item.content,
        "author": item.author,
        "url": item.url,
        "source": item.source
    }

    generated_variants = await ai_post_generator.generate_variants(
        item=item_dict,
        analysis=analysis_dict,
        tone=req.tones[0] if req.tones else "technical",
        length=req.length,
        voice_profile=voice_dict,
        angle=req.angle,
        hook_strategy=req.hook_type,
        custom_instructions=req.custom_instructions
    )

    for v in generated_variants:
        db_post = GeneratedPost(
            content_item_id=item.id,
            variant_type=v.variant_type,
            tone=v.tone,
            length=v.length,
            content=v.content,
            thread_items=v.thread_items,
            similarity_score=v.similarity_score,
            is_safe=v.is_safe,
            attribution_included=v.attribution_included
        )
        db.add(db_post)

    await db.commit()
    return generated_variants

@router.post("/content/{content_id}/save", response_model=SavedItemResponse)
async def save_content_item(
    content_id: str,
    req: SaveStoryRequest,
    db: AsyncSession = Depends(get_db)
):
    item_res = await db.execute(select(ContentItem).where(ContentItem.id == content_id))
    if not item_res.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Content item not found")

    existing_save = await db.execute(
        select(SavedItem).where(SavedItem.content_item_id == content_id)
    )
    saved = existing_save.scalar_one_or_none()
    if saved:
        saved.status = req.status
        if req.notes:
            saved.notes = req.notes
    else:
        saved = SavedItem(
            content_item_id=content_id,
            status=req.status,
            notes=req.notes
        )
        db.add(saved)

    await db.commit()

    reloaded = await db.execute(
        select(SavedItem).options(
            selectinload(SavedItem.content_item).selectinload(ContentItem.analysis),
            selectinload(SavedItem.content_item).selectinload(ContentItem.generated_variants)
        ).where(SavedItem.id == saved.id)
    )
    return reloaded.scalar_one()

@router.get("/saved", response_model=List[SavedItemResponse])
async def get_saved_items(db: AsyncSession = Depends(get_db)):
    query = select(SavedItem).options(
        selectinload(SavedItem.content_item).selectinload(ContentItem.analysis),
        selectinload(SavedItem.content_item).selectinload(ContentItem.generated_variants)
    ).order_by(desc(SavedItem.saved_at))
    result = await db.execute(query)
    return result.scalars().all()

@router.delete("/saved/{saved_id}")
async def delete_saved_item(saved_id: str, db: AsyncSession = Depends(get_db)):
    query = select(SavedItem).where(SavedItem.id == saved_id)
    result = await db.execute(query)
    saved = result.scalar_one_or_none()
    if not saved:
        raise HTTPException(status_code=404, detail="Saved item not found")
    await db.delete(saved)
    await db.commit()
    return {"message": "Saved item deleted"}

# -------------------------------------------------------------------------
# VOICE PROFILE & PERFORMANCE TRACKING
# -------------------------------------------------------------------------

@router.get("/voice-profile", response_model=VoiceProfileResponse)
async def get_voice_profile(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(VoiceProfile).limit(1))
    profile = result.scalar_one_or_none()
    if not profile:
        profile = VoiceProfile(
            name="Default Tech Voice",
            tone_preference="Technical & Authoritative",
            voice_examples=[
                "Most teams are evaluating models strictly on synthetic benchmarks. In production, 80% of your failure modes are state management and latency jitter.",
                "The shift from single-prompt generation to autonomous agent loops changes everything about compute economics.",
                "Here's what nobody tells you about fine-tuning: dataset purity beats parameter count every single time."
            ],
            guidelines="Concise, data-backed sentences. Avoid excessive emojis. Emphasize developer architectural tradeoffs."
        )
        db.add(profile)
        await db.commit()
        await db.refresh(profile)
    return profile

@router.post("/voice-profile", response_model=VoiceProfileResponse)
async def update_voice_profile(req: VoiceProfileRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(VoiceProfile).limit(1))
    profile = result.scalar_one_or_none()
    if not profile:
        profile = VoiceProfile()
        db.add(profile)

    profile.name = req.name
    profile.tone_preference = req.tone_preference
    profile.voice_examples = req.voice_examples
    profile.guidelines = req.guidelines
    profile.updated_at = utc_now()

    await db.commit()
    await db.refresh(profile)
    return profile

@router.post("/performance", response_model=ContentPerformanceSchema)
async def record_performance(req: ContentPerformanceSchema, db: AsyncSession = Depends(get_db)):
    """Records real published content performance for personal learning."""
    perf = ContentPerformance(
        post_id=req.post_id,
        topic=req.topic,
        angle=req.angle,
        hook=req.hook,
        format=req.format,
        published_at=req.published_at or utc_now(),
        views=req.views,
        likes=req.likes,
        reposts=req.reposts,
        replies=req.replies,
        engagement_rate=req.engagement_rate
    )
    db.add(perf)
    await db.commit()
    await db.refresh(perf)
    return perf

@router.get("/performance", response_model=List[ContentPerformanceSchema])
async def get_performance(db: AsyncSession = Depends(get_db)):
    res = await db.execute(select(ContentPerformance).order_by(desc(ContentPerformance.published_at)))
    return res.scalars().all()

@router.post("/analyze-custom-tweet")
async def analyze_custom_tweet(
    payload: dict,
    db: AsyncSession = Depends(get_db)
):
    text = payload.get("text", "")
    author = payload.get("author", "X User")
    author_handle = payload.get("author_handle", "@user")
    url = payload.get("url", "https://x.com")
    likes = payload.get("likes")
    reposts = payload.get("reposts")
    replies = payload.get("replies")
    views = payload.get("views")

    score_result = virality_scorer.score_item(
        published_at=utc_now() - timedelta(hours=2),
        title=text[:80],
        content=text,
        views=views,
        likes=likes,
        reposts=reposts,
        replies=replies
    )

    analysis = await ai_analysis_service.analyze_content_item({
        "title": text[:80],
        "content": text,
        "author": author,
        "url": url,
        "views": views,
        "likes": likes,
        "viral_potential": score_result["viral_potential"]
    })

    return {
        "text": text,
        "author": author,
        "author_handle": author_handle,
        "url": url,
        "viral_score": score_result["viral_score"],
        "viral_potential": score_result["viral_potential"],
        "badge": score_result["badge"],
        "classification": score_result["classification"],
        "engagement_velocity": score_result["engagement_velocity"],
        "analysis": analysis
    }
