from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

class AnalysisSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    summary: str
    main_claim: Optional[str] = None
    why_viral: List[str] = Field(default_factory=list)
    hook_type: Optional[str] = "announcement"
    content_type: Optional[str] = "news"
    key_facts: List[str] = Field(default_factory=list)
    important_entities: List[str] = Field(default_factory=list)
    audience: Optional[str] = "AI Engineers"
    recommended_angle: Optional[str] = None
    risk_flags: List[str] = Field(default_factory=list)
    confirmed_facts: List[str] = Field(default_factory=list)
    uncertain_claims: List[str] = Field(default_factory=list)
    viral_potential: float = 75.0

class GeneratedVariantSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[str] = None
    variant_type: str  # news, hot_take, educational, builder, thread, question
    tone: str = "professional"
    length: str = "medium"
    content: str
    thread_items: List[str] = Field(default_factory=list)
    similarity_score: float = 0.0
    is_safe: bool = True
    attribution_included: bool = True

class ContentItemBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    source: str
    source_type: str
    source_quality: str = "Tier 1"
    title: Optional[str] = None
    content: str
    url: str
    primary_source_url: Optional[str] = None
    source_count: int = 1
    author: Optional[str] = None
    author_handle: Optional[str] = None
    author_url: Optional[str] = None
    published_at: datetime
    collected_at: datetime
    last_seen_at: Optional[datetime] = None

    # Nullable social metrics
    views: Optional[int] = None
    likes: Optional[int] = None
    reposts: Optional[int] = None
    replies: Optional[int] = None
    quotes: Optional[int] = None
    media: List[str] = Field(default_factory=list)
    hashtags: List[str] = Field(default_factory=list)
    language: str = "en"

    # Dual Virality
    viral_score: Optional[float] = None
    viral_potential: float = 75.0
    engagement_rate: Optional[float] = None
    engagement_velocity: float = 0.0
    trend_score: float = 0.0

    topic: str = "General AI"
    entities: List[str] = Field(default_factory=list)
    sentiment: str = "neutral"
    content_type: str = "news"
    hook_type: str = "announcement"

    # Fact-checking
    confirmed_facts: List[str] = Field(default_factory=list)
    uncertain_claims: List[str] = Field(default_factory=list)

    source_urls: List[str] = Field(default_factory=list)
    original_content_id: Optional[str] = None
    attribution_required: bool = True
    analysis: Optional[AnalysisSchema] = None
    generated_variants: List[GeneratedVariantSchema] = Field(default_factory=list)

class FeedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[ContentItemBase]

class TrendObservationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    trend_id: str
    timestamp: datetime
    mention_count: int
    source_count: int
    source_diversity: int
    social_mentions: Optional[int] = None
    engagement: Optional[float] = None
    new_items: int = 0
    momentum_score: float
    competition_score: float
    opportunity_score: float

class TopicResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    category: str
    momentum: float
    momentum_change_pct: float = 0.0
    momentum_direction: str = "STABLE"
    status: str
    lifecycle_stage: str = "RISING"
    opportunity_score: float = 70.0
    opportunity_type: str = "RISING_OPPORTUNITY"
    competition_score: float = 40.0
    novelty_score: float = 80.0
    audience_fit_score: float = 85.0
    recommended_action: str = "POST_SOON"
    action_reason: Optional[str] = None
    recommended_angle: Optional[str] = None
    alternative_angles: List[str] = Field(default_factory=list)
    saturated_angles: List[str] = Field(default_factory=list)
    under_served_angles: List[str] = Field(default_factory=list)
    recommended_hook_type: str = "contrarian"
    hook_strategy: Optional[str] = None
    recommended_format: str = "single_post"
    format_scores: Dict[str, int] = Field(default_factory=dict)
    primary_audience: str = "AI Engineers"
    secondary_audiences: List[str] = Field(default_factory=list)
    item_count: int
    sources_summary: List[str]
    primary_source: Optional[str] = None
    updated_at: datetime

class OpportunityCardResponse(BaseModel):
    rank: int
    id: str
    topic: str
    category: str
    opportunity_score: float
    opportunity_type: str
    lifecycle: str
    lifecycle_badge: str
    momentum: float
    momentum_change_pct: float
    momentum_direction: str
    competition: float
    novelty: float
    audience_fit: float
    primary_audience: str
    recommended_action: str
    action_reason: str
    recommended_angle: str
    alternative_angles: List[str] = Field(default_factory=list)
    recommended_hook: str
    hook_strategy: str
    recommended_format: str
    format_scores: Dict[str, int] = Field(default_factory=dict)
    item_count: int
    primary_source: Optional[str] = None
    sources_summary: List[str] = Field(default_factory=list)

class TopOpportunitiesResponse(BaseModel):
    total_trends_analyzed: int
    top_opportunities: List[OpportunityCardResponse]
    generated_at: datetime

class SourceEvidenceItem(BaseModel):
    title: str
    url: str
    source: str
    source_quality: str
    published_at: Optional[datetime] = None
    role: str = "Supporting Source"

class TrendDetailResponse(BaseModel):
    id: str
    name: str
    category: str
    lifecycle_stage: str
    status: str
    opportunity_score: float
    opportunity_type: str
    competition_score: float
    novelty_score: float
    audience_fit_score: float
    momentum: float
    momentum_change_pct: float
    momentum_direction: str
    what_happened: str
    why_trending: str
    what_changed: Optional[str] = None
    what_is_saturated: Optional[str] = None
    what_is_missing: Optional[str] = None
    who_cares: Optional[str] = None
    best_angle: str
    alternative_angles: List[str] = Field(default_factory=list)
    saturated_angles: List[str] = Field(default_factory=list)
    under_served_angles: List[str] = Field(default_factory=list)
    best_hook_type: str
    hook_strategy: str
    best_format: str
    format_scores: Dict[str, int] = Field(default_factory=dict)
    timing_verdict: str
    timing_reason: str
    claims_to_avoid: List[str] = Field(default_factory=list)
    source_evidence: List[SourceEvidenceItem] = Field(default_factory=list)
    observations: List[TrendObservationSchema] = Field(default_factory=list)

class ContentPerformanceSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    post_id: Optional[str] = None
    topic: str
    angle: Optional[str] = None
    hook: Optional[str] = None
    format: str = "single_post"
    published_at: datetime
    views: Optional[int] = None
    likes: Optional[int] = None
    reposts: Optional[int] = None
    replies: Optional[int] = None
    engagement_rate: Optional[float] = None

class GenerateRequest(BaseModel):
    tones: List[str] = Field(default_factory=lambda: ["professional"])
    variants: List[str] = Field(default_factory=lambda: ["news", "hot_take", "educational", "builder", "thread", "question"])
    length: str = "medium"  # short, medium, long
    custom_instructions: Optional[str] = None
    include_voice_profile: bool = True
    angle: Optional[str] = None
    hook_type: Optional[str] = None
    target_format: Optional[str] = None

class SaveStoryRequest(BaseModel):
    status: str = "Idea"  # Idea, Draft, Posted, Ignored
    notes: Optional[str] = None

class SavedItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    content_item_id: str
    status: str
    notes: Optional[str] = None
    saved_at: datetime
    content_item: Optional[ContentItemBase] = None

class VoiceProfileRequest(BaseModel):
    name: str = "Default Voice"
    tone_preference: str = "Technical & Authoritative"
    voice_examples: List[str] = Field(default_factory=list)
    guidelines: Optional[str] = None

class VoiceProfileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    tone_preference: str
    voice_examples: List[str]
    guidelines: Optional[str] = None
    updated_at: datetime
