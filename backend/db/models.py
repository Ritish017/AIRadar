import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Integer, Float, Boolean, DateTime, ForeignKey, JSON, Index
)
from sqlalchemy.orm import relationship
from backend.db.session import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    saved_items = relationship("SavedItem", back_populates="user", cascade="all, delete-orphan")
    voice_profile = relationship("VoiceProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")


class Source(Base):
    __tablename__ = "sources"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    source_type = Column(String(50), nullable=False)  # firecrawl, x, github, reddit, news
    quality_tier = Column(String(20), default="Tier 1")  # Tier 1, Tier 2, Tier 3
    url = Column(String(512), nullable=False)
    icon_url = Column(String(512), nullable=True)
    is_active = Column(Boolean, default=True)
    last_fetched_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ContentItem(Base):
    __tablename__ = "content_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    source = Column(String(100), nullable=False, index=True)
    source_type = Column(String(50), nullable=False, index=True)  # firecrawl, x, github, reddit, demo
    source_quality = Column(String(20), default="Tier 1")  # Tier 1: Official, Tier 2: Tech Press, Tier 3: Community
    title = Column(String(512), nullable=True)
    content = Column(Text, nullable=False)
    url = Column(String(1024), unique=True, nullable=False, index=True)
    primary_source_url = Column(String(1024), nullable=True)
    source_count = Column(Integer, default=1)
    author = Column(String(255), nullable=True, index=True)
    author_handle = Column(String(255), nullable=True)
    author_url = Column(String(512), nullable=True)

    # Timestamps
    published_at = Column(DateTime, nullable=False, index=True)
    collected_at = Column(DateTime, default=datetime.utcnow)
    last_seen_at = Column(DateTime, default=datetime.utcnow)

    # Social metrics (Nullable: do not fabricate when legitimately unavailable)
    views = Column(Integer, nullable=True)
    likes = Column(Integer, nullable=True)
    reposts = Column(Integer, nullable=True)
    replies = Column(Integer, nullable=True)
    quotes = Column(Integer, nullable=True)

    # Media & Metadata
    media = Column(JSON, default=list)
    hashtags = Column(JSON, default=list)
    language = Column(String(10), default="en")

    # Dual Virality Scores
    viral_score = Column(Float, nullable=True, index=True)  # Measurable actual score (when metrics exist)
    viral_potential = Column(Float, default=75.0, index=True)  # Deterministic predicted potential (0-100)
    engagement_rate = Column(Float, nullable=True)
    engagement_velocity = Column(Float, default=0.0)  # e.g., +340%
    trend_score = Column(Float, default=0.0)

    # Categorization
    topic = Column(String(100), default="General AI", index=True)
    entities = Column(JSON, default=list)
    sentiment = Column(String(50), default="neutral")
    content_type = Column(String(50), default="news")  # news, research, benchmark, tool, release
    hook_type = Column(String(50), default="announcement")

    # Multi-Source Fact Checking
    confirmed_facts = Column(JSON, default=list)  # Verified facts (✓)
    uncertain_claims = Column(JSON, default=list)  # Speculation / unverified (⚠)

    # Attribution
    source_urls = Column(JSON, default=list)
    original_content_id = Column(String(255), nullable=True)
    attribution_required = Column(Boolean, default=True)

    # Relationships
    metrics_history = relationship("ContentMetrics", back_populates="content_item", cascade="all, delete-orphan")
    analysis = relationship("Analysis", back_populates="content_item", uselist=False, cascade="all, delete-orphan")
    generated_variants = relationship("GeneratedPost", back_populates="content_item", cascade="all, delete-orphan")
    saved_instances = relationship("SavedItem", back_populates="content_item", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_viral_potential", "viral_potential", "published_at"),
        Index("idx_source_topic", "source", "topic"),
    )


class ContentMetrics(Base):
    __tablename__ = "content_metrics"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    content_item_id = Column(String(36), ForeignKey("content_items.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    views = Column(Integer, nullable=True)
    likes = Column(Integer, nullable=True)
    reposts = Column(Integer, nullable=True)
    replies = Column(Integer, nullable=True)
    quotes = Column(Integer, nullable=True)
    viral_score = Column(Float, nullable=True)
    viral_potential = Column(Float, default=75.0)

    content_item = relationship("ContentItem", back_populates="metrics_history")


class Topic(Base):
    __tablename__ = "topics"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), unique=True, nullable=False, index=True)
    category = Column(String(100), default="AI Models")
    momentum = Column(Float, default=100.0)  # Momentum score 0-100 or %
    momentum_change_pct = Column(Float, default=0.0)  # e.g. +284%
    momentum_direction = Column(String(50), default="STABLE")  # ACCELERATING, STABLE, DECELERATING, INSUFFICIENT HISTORY
    status = Column(String(50), default="🔥 Exploding")
    lifecycle_stage = Column(String(50), default="RISING")  # EMERGING, RISING, EXPLODING, PEAK, SATURATED, DECLINING, DEAD

    # Opportunity & Competition Metrics
    opportunity_score = Column(Float, default=70.0)  # 0-100
    opportunity_type = Column(String(50), default="RISING_OPPORTUNITY")  # EARLY_DISCOVERY, RISING_OPPORTUNITY, BREAKING, HIGH_REACH, NICHE_HIGH_VALUE, OVERSATURATED, DECLINING, SKIP
    competition_score = Column(Float, default=40.0)  # 0-100
    novelty_score = Column(Float, default=80.0)  # 0-100
    audience_fit_score = Column(Float, default=85.0)  # 0-100

    # Strategic Action & Content Guidance
    recommended_action = Column(String(50), default="POST_SOON")  # POST_NOW, POST_SOON, WATCH, WAIT, SKIP
    action_reason = Column(Text, nullable=True)
    recommended_angle = Column(Text, nullable=True)
    alternative_angles = Column(JSON, default=list)
    saturated_angles = Column(JSON, default=list)
    under_served_angles = Column(JSON, default=list)
    recommended_hook_type = Column(String(100), default="contrarian")
    hook_strategy = Column(Text, nullable=True)
    recommended_format = Column(String(50), default="single_post")
    format_scores = Column(JSON, default=dict)
    primary_audience = Column(String(100), default="AI Engineers")
    secondary_audiences = Column(JSON, default=list)

    item_count = Column(Integer, default=1)
    sources_summary = Column(JSON, default=list)
    primary_source = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    mentions = relationship("TopicMention", back_populates="topic", cascade="all, delete-orphan")
    observations = relationship("TrendObservation", back_populates="topic", cascade="all, delete-orphan")
    strategy = relationship("TrendStrategy", back_populates="topic", uselist=False, cascade="all, delete-orphan")


class TopicMention(Base):
    __tablename__ = "topic_mentions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    topic_id = Column(String(36), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False)
    content_item_id = Column(String(36), ForeignKey("content_items.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    topic = relationship("Topic", back_populates="mentions")


class TrendObservation(Base):
    """
    Historical observation snapshots for trends over time.
    Provides data points for momentum acceleration, growth curves, and lifecycle tracking.
    """
    __tablename__ = "trend_observations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    trend_id = Column(String(36), ForeignKey("topics.id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    mention_count = Column(Integer, default=1)
    source_count = Column(Integer, default=1)
    source_diversity = Column(Integer, default=1)
    social_mentions = Column(Integer, nullable=True)
    engagement = Column(Float, nullable=True)
    new_items = Column(Integer, default=0)
    momentum_score = Column(Float, default=50.0)
    competition_score = Column(Float, default=30.0)
    opportunity_score = Column(Float, default=65.0)

    topic = relationship("Topic", back_populates="observations")


class TrendStrategy(Base):
    """
    Detailed strategic AI intelligence record generated by Gemini.
    """
    __tablename__ = "trend_strategies"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    trend_id = Column(String(36), ForeignKey("topics.id", ondelete="CASCADE"), unique=True, nullable=False)
    what_happened = Column(Text, nullable=False)
    why_trending = Column(Text, nullable=False)
    what_changed = Column(Text, nullable=True)
    what_is_saturated = Column(Text, nullable=True)
    what_is_missing = Column(Text, nullable=True)
    who_cares = Column(Text, nullable=True)
    best_angle = Column(Text, nullable=False)
    alternative_angles = Column(JSON, default=list)
    best_hook_type = Column(String(100), default="contrarian")
    hook_strategy = Column(Text, nullable=True)
    best_format = Column(String(50), default="single_post")
    format_recommendations = Column(JSON, default=dict)
    timing_verdict = Column(String(50), default="POST_NOW")
    timing_reason = Column(Text, nullable=True)
    claims_to_avoid = Column(JSON, default=list)
    source_evidence = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)

    topic = relationship("Topic", back_populates="strategy")


class ContentPerformance(Base):
    """
    Historical user content performance tracking for personalized opportunity scoring.
    """
    __tablename__ = "content_performance"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    post_id = Column(String(36), nullable=True)
    topic = Column(String(100), nullable=False)
    angle = Column(String(255), nullable=True)
    hook = Column(String(100), nullable=True)
    format = Column(String(50), default="single_post")
    published_at = Column(DateTime, default=datetime.utcnow)
    views = Column(Integer, nullable=True)
    likes = Column(Integer, nullable=True)
    reposts = Column(Integer, nullable=True)
    replies = Column(Integer, nullable=True)
    engagement_rate = Column(Float, nullable=True)


class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    content_item_id = Column(String(36), ForeignKey("content_items.id", ondelete="CASCADE"), unique=True, nullable=False)
    summary = Column(Text, nullable=False)
    main_claim = Column(Text, nullable=True)
    why_viral = Column(JSON, default=list)
    hook_type = Column(String(100), nullable=True)
    content_type = Column(String(100), nullable=True)
    key_facts = Column(JSON, default=list)
    important_entities = Column(JSON, default=list)
    audience = Column(String(255), nullable=True)
    recommended_angle = Column(Text, nullable=True)
    risk_flags = Column(JSON, default=list)
    confirmed_facts = Column(JSON, default=list)
    uncertain_claims = Column(JSON, default=list)
    viral_potential = Column(Float, default=75.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    content_item = relationship("ContentItem", back_populates="analysis")


class GeneratedPost(Base):
    __tablename__ = "generated_posts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    content_item_id = Column(String(36), ForeignKey("content_items.id", ondelete="CASCADE"), nullable=False)
    variant_type = Column(String(50), nullable=False)  # news, hot_take, educational, builder, thread, question
    tone = Column(String(50), default="professional")
    length = Column(String(50), default="medium")
    content = Column(Text, nullable=False)
    thread_items = Column(JSON, default=list)
    similarity_score = Column(Float, default=0.0)
    is_safe = Column(Boolean, default=True)
    attribution_included = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    content_item = relationship("ContentItem", back_populates="generated_variants")


class SavedItem(Base):
    __tablename__ = "saved_items"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    content_item_id = Column(String(36), ForeignKey("content_items.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="Idea")  # Idea, Draft, Posted, Ignored
    notes = Column(Text, nullable=True)
    saved_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="saved_items")
    content_item = relationship("ContentItem", back_populates="saved_instances")


class VoiceProfile(Base):
    __tablename__ = "voice_profiles"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=True)
    name = Column(String(100), default="Default Voice")
    tone_preference = Column(String(50), default="Technical & Authoritative")
    voice_examples = Column(JSON, default=list)
    guidelines = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="voice_profile")


# =========================================================================
# V3 REAL-TIME GLOBAL AI INTELLIGENCE & CONTENT OPERATING SYSTEM MODELS
# =========================================================================

class Event(Base):
    """
    Canonical Clustered Event.
    Multiple articles, announcements, and tweets covering the same development
    cluster into a single canonical Event entity with confidence and latency telemetry.
    """
    __tablename__ = "events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    canonical_title = Column(String(512), nullable=False, index=True)
    summary = Column(Text, nullable=False)
    category = Column(String(100), default="AI Models", index=True)  # AI Models, Companies, Agents, Coding, Video, Image, Robotics, Research, Business, Hardware, Policy
    status = Column(String(50), default="DEVELOPING", index=True)  # CONFIRMED, LIKELY, DEVELOPING, UNVERIFIED, CONTRADICTED
    confidence_score = Column(Float, default=70.0)  # 0 to 100
    source_count = Column(Integer, default=1)
    independent_source_count = Column(Integer, default=1)
    primary_source_url = Column(String(1024), nullable=True)
    primary_source_name = Column(String(255), nullable=True)
    
    # Intelligence Telemetry
    entities = Column(JSON, default=list)
    key_facts = Column(JSON, default=list)
    contradictions = Column(JSON, default=list)
    
    # Scores
    relevance_score = Column(Float, default=85.0)  # 0 to 100
    freshness_score = Column(Float, default=100.0)  # 0 to 100
    momentum_score = Column(Float, default=80.0)  # 0 to 100
    opportunity_score = Column(Float, default=75.0)  # 0 to 100
    
    # Strategic Guidance
    recommended_action = Column(String(50), default="POST_SOON")  # POST_NOW, POST_SOON, WATCH, WAIT, SKIP
    recommended_angle = Column(Text, nullable=True)
    recommended_platform = Column(String(50), default="X")  # X, LinkedIn, Instagram, YouTube
    
    # Latency & Timing KPI Telemetry
    event_timestamp = Column(DateTime, nullable=False, default=datetime.utcnow, index=True)
    first_seen_at = Column(DateTime, default=datetime.utcnow)
    detected_at = Column(DateTime, default=datetime.utcnow)
    verified_at = Column(DateTime, nullable=True)
    analyzed_at = Column(DateTime, nullable=True)
    surfaced_at = Column(DateTime, default=datetime.utcnow)
    
    detection_latency = Column(Float, default=30.0)  # seconds from event_timestamp to first_seen_at
    verification_latency = Column(Float, default=15.0)  # seconds from first_seen_at to verified_at
    analysis_latency = Column(Float, default=12.0)  # seconds from verified_at to analyzed_at
    total_pipeline_latency = Column(Float, default=57.0)  # "Time to Radar" in seconds
    
    # Relationships
    topic_id = Column(String(36), ForeignKey("topics.id", ondelete="SET NULL"), nullable=True)
    sources = relationship("EventSource", back_populates="event", cascade="all, delete-orphan")
    observations = relationship("EventObservation", back_populates="event", cascade="all, delete-orphan")
    briefs = relationship("ContentBrief", back_populates="event", cascade="all, delete-orphan")
    variants = relationship("ContentVariant", back_populates="event", cascade="all, delete-orphan")
    video_prompts = relationship("VideoPrompt", back_populates="event", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_event_status_time", "status", "event_timestamp"),
        Index("idx_event_category", "category"),
    )


class EventSource(Base):
    """Links individual articles, RSS items, and social signals to canonical Events."""
    __tablename__ = "event_sources"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    content_item_id = Column(String(36), ForeignKey("content_items.id", ondelete="SET NULL"), nullable=True)
    url = Column(String(1024), nullable=False)
    title = Column(String(512), nullable=True)
    source_name = Column(String(100), nullable=False)
    source_type = Column(String(50), default="news")  # official, news, research, community, github
    quality_tier = Column(String(20), default="Tier 1")
    published_at = Column(DateTime, default=datetime.utcnow)
    discovered_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", back_populates="sources")


class EventObservation(Base):
    """Chronological tracking of event evolution, velocity, and multi-source coverage expansion."""
    __tablename__ = "event_observations"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    source_count = Column(Integer, default=1)
    velocity = Column(Float, default=0.0)
    momentum = Column(Float, default=50.0)
    confidence_score = Column(Float, default=70.0)

    event = relationship("Event", back_populates="observations")


class ContentBrief(Base):
    """
    Strategic Pre-Generation Brief.
    Constructed by the AI Content Strategist before generating platform copy
    to ensure intentional angles, counterpoints, and factual grounding.
    """
    __tablename__ = "content_briefs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("events.id", ondelete="CASCADE"), nullable=True, index=True)
    topic = Column(String(255), nullable=False)
    audience = Column(String(255), default="AI Engineers & Builders")
    goal = Column(String(255), default="Drive insightful discussion & developer awareness")
    angle = Column(Text, nullable=False)
    content_format = Column(String(100), default="Single Post + Thread")
    hook_strategy = Column(Text, nullable=False)
    key_claims = Column(JSON, default=list)
    supporting_facts = Column(JSON, default=list)
    counterpoint = Column(Text, nullable=True)
    cta_strategy = Column(Text, nullable=True)
    visual_strategy = Column(Text, nullable=True)
    platform_strategy = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", back_populates="briefs")
    variants = relationship("ContentVariant", back_populates="brief", cascade="all, delete-orphan")


class ContentVariant(Base):
    """
    Platform-Native Content Artifact.
    Dedicated outputs for X, LinkedIn, Instagram, and YouTube.
    """
    __tablename__ = "content_variants"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("events.id", ondelete="CASCADE"), nullable=True, index=True)
    brief_id = Column(String(36), ForeignKey("content_briefs.id", ondelete="CASCADE"), nullable=True, index=True)
    platform = Column(String(50), nullable=False, index=True)  # x, linkedin, instagram, youtube
    variant_type = Column(String(50), nullable=False)  # breaking, hot_take, thread, carousel, reel, short, explainer
    title = Column(String(512), nullable=True)
    hook = Column(Text, nullable=False)
    body = Column(Text, nullable=False)
    cta = Column(Text, nullable=True)
    slides = Column(JSON, default=list)  # for Instagram Carousels & X Threads
    script_data = Column(JSON, default=dict)  # for YouTube / Reels (timestamps, B-roll, on-screen text)
    hashtags = Column(JSON, default=list)
    
    # Quality & Originality Safeguards
    quality_score = Column(Float, default=90.0)  # 0 to 100
    quality_breakdown = Column(JSON, default=dict)  # fact_check, originality, hook, clarity, fit
    similarity_score = Column(Float, default=0.0)
    is_original = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", back_populates="variants")
    brief = relationship("ContentBrief", back_populates="variants")


class VideoPrompt(Base):
    """
    Production-Grade Video & Motion Graphics Prompts.
    Compiled configurations for Gemini Omni, Remotion, and HyperFrames.
    """
    __tablename__ = "video_prompts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("events.id", ondelete="CASCADE"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    topic = Column(String(255), default="AI Development")
    recommended_provider = Column(String(50), default="gemini_omni")  # gemini_omni, remotion, hyperframes, hybrid
    routing_reason = Column(Text, nullable=True)
    
    # Model-Specific Compiled Payloads
    gemini_omni_prompt = Column(JSON, default=dict)  # 20-field structured cinematic prompt
    remotion_prompt = Column(JSON, default=dict)  # React composition & timeline specs
    hyperframes_prompt = Column(JSON, default=dict)  # HTML-native markup & paused GSAP timelines
    storyboard_scenes = Column(JSON, default=list)  # 6 structured storyboard scenes
    
    created_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", back_populates="video_prompts")


class UserMonitor(Base):
    """Custom topic, entity, or GitHub repository monitors created by users."""
    __tablename__ = "user_monitors"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    query = Column(String(255), nullable=False)
    sources = Column(JSON, default=list)
    frequency = Column(String(50), default="15m")
    importance_threshold = Column(Float, default=75.0)
    notification_threshold = Column(Float, default=80.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ContentQueueItem(Base):
    """Pipeline orchestration for content lifecycle management."""
    __tablename__ = "content_queue"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("events.id", ondelete="SET NULL"), nullable=True)
    platform = Column(String(50), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String(50), default="IDEA")  # IDEA, DRAFT, REVIEW, APPROVED, READY, SCHEDULED, PUBLISHED, PERFORMING, COMPLETED
    priority = Column(String(20), default="HIGH")  # URGENT, HIGH, MEDIUM, LOW
    scheduled_for = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AlertNotification(Base):
    """Real-time system notification alerts for breaking AI events and exploding trends."""
    __tablename__ = "alert_notifications"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    alert_type = Column(String(50), default="BREAKING")  # BREAKING, EMERGING_TREND, HIGH_OPPORTUNITY, MODEL_RELEASE
    severity = Column(String(20), default="info")  # info, warning, urgent
    event_id = Column(String(36), nullable=True)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


# =========================================================================
# V3.3 VIDEO REALITY BENCHMARK & CREATIVE INTELLIGENCE MODELS
# =========================================================================

class VideoVisualConceptModel(Base):
    __tablename__ = "video_visual_concepts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    event_id = Column(String(36), ForeignKey("events.id", ondelete="CASCADE"), nullable=True, index=True)
    claim = Column(Text, nullable=False)
    topic = Column(String(255), nullable=False)
    representation_type = Column(String(100), nullable=False)
    headline = Column(String(255), nullable=False)
    core_metaphor = Column(Text, nullable=False)
    what_viewer_sees = Column(Text, nullable=False)
    fit_score = Column(Float, default=90.0)
    is_selected = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class VideoForensicRecordModel(Base):
    __tablename__ = "video_forensic_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    video_prompt_id = Column(String(36), ForeignKey("video_prompts.id", ondelete="CASCADE"), nullable=True, index=True)
    video_path_or_url = Column(String(1024), nullable=False)
    prompt_readiness_score = Column(Float, default=95.0)
    expected_executability_score = Column(Float, default=92.0)
    actual_video_quality_score = Column(Float, default=85.0)
    overall_verdict = Column(String(20), default="PASS")  # EXCELLENT, PASS, WARN, FAIL
    dimension_scores = Column(JSON, default=dict)  # 23 forensic dimensions
    detected_failures = Column(JSON, default=list)
    representative_frames = Column(JSON, default=list)
    metadata_extracted = Column(JSON, default=dict)
    remediation_actions = Column(JSON, default=list)
    created_at = Column(DateTime, default=datetime.utcnow)


class VideoFailureRecordModel(Base):
    __tablename__ = "video_failure_records"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    forensic_id = Column(String(36), ForeignKey("video_forensic_records.id", ondelete="CASCADE"), nullable=True, index=True)
    failure_code = Column(String(100), nullable=False, index=True)
    category = Column(String(50), nullable=False)  # Generation, Continuity, Story, Technical, Creative
    title = Column(String(255), nullable=False)
    severity = Column(String(20), default="Medium")  # Critical, High, Medium, Low
    diagnostic_evidence = Column(Text, nullable=False)
    mutation_operator = Column(String(100), nullable=False)
    resolved_in_version = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class VideoPromptVersionModel(Base):
    __tablename__ = "video_prompt_versions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    video_prompt_id = Column(String(36), ForeignKey("video_prompts.id", ondelete="CASCADE"), nullable=True, index=True)
    version_label = Column(String(20), nullable=False)  # V1, V2, V3
    parent_version = Column(String(20), nullable=True)
    model = Column(String(50), default="AUTO")
    primary_failure_addressed = Column(String(255), nullable=True)
    prompt_text = Column(Text, nullable=False)
    mutations_applied = Column(JSON, default=list)
    predicted_quality_score = Column(Float, default=90.0)
    actual_quality_score = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class VideoBenchmarkCaseModel(Base):
    __tablename__ = "video_benchmark_cases"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    case_number = Column(Integer, nullable=False, index=True)
    category = Column(String(100), nullable=False)  # News, Technical, Educational, Cinematic, etc.
    title = Column(String(255), nullable=False)
    expected_concept = Column(String(255), nullable=False)
    expected_routing = Column(String(50), nullable=False)
    expected_complexity = Column(Float, default=50.0)
    prompt_readiness = Column(Float, default=95.0)
    actual_quality_score = Column(Float, default=88.0)
    status = Column(String(50), default="ACTIVE")
    case_data = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)


class VideoHumanFeedbackModel(Base):
    __tablename__ = "video_human_feedback"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    video_prompt_id = Column(String(36), nullable=True, index=True)
    rating_stars = Column(Integer, default=5)  # 1 to 5 stars
    failure_tags = Column(JSON, default=list)  # boring, confusing, bad pacing, bad visuals, etc.
    user_critique = Column(Text, nullable=True)
    what_to_change = Column(Text, nullable=True)
    applied_to_mutation = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


