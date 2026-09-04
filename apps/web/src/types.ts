export interface Analysis {
  summary: string;
  main_claim?: string;
  why_viral: string[];
  hook_type?: string;
  content_type?: string;
  key_facts: string[];
  important_entities: string[];
  audience?: string;
  recommended_angle?: string;
  risk_flags: string[];
  confirmed_facts?: string[];
  uncertain_claims?: string[];
  viral_potential?: number;
}

export interface GeneratedVariant {
  id?: string;
  variant_type: "news" | "hot_take" | "educational" | "builder" | "thread" | "question";
  tone: string;
  length: string;
  content: string;
  thread_items?: string[];
  similarity_score: number;
  is_safe: boolean;
  attribution_included: boolean;
}

export interface ContentItem {
  id: string;
  source: string;
  source_type: "firecrawl" | "rss" | "x" | "github" | "reddit" | "news" | "demo";
  source_quality?: string;
  source_count?: number;
  primary_source_url?: string;
  title: string;
  content: string;
  url: string;
  author?: string;
  author_handle?: string;
  author_url?: string;
  published_at: string;
  collected_at: string;
  views?: number | null;
  likes?: number | null;
  reposts?: number | null;
  replies?: number | null;
  quotes?: number | null;
  media: string[];
  hashtags: string[];
  language: string;
  engagement_rate?: number | null;
  engagement_velocity: number;
  viral_score?: number | null;
  viral_potential: number;
  trend_score: number;
  topic: string;
  entities: string[];
  sentiment: string;
  content_type: string;
  hook_type: string;
  source_urls: string[];
  confirmed_facts?: string[];
  uncertain_claims?: string[];
  original_content_id?: string;
  attribution_required: boolean;
  analysis?: Analysis;
  generated_variants?: GeneratedVariant[];
}

export interface OpportunityCard {
  rank: number;
  id: string;
  topic: string;
  category: string;
  opportunity_score: number;
  opportunity_type: string;
  lifecycle: string;
  lifecycle_badge: string;
  momentum: number;
  momentum_change_pct: number;
  momentum_direction: "ACCELERATING" | "STABLE" | "DECELERATING" | "INSUFFICIENT HISTORY";
  competition: number;
  novelty: number;
  audience_fit: number;
  primary_audience: string;
  recommended_action: "POST_NOW" | "POST_SOON" | "WATCH" | "WAIT" | "SKIP";
  action_reason: string;
  recommended_angle: string;
  alternative_angles: string[];
  recommended_hook: string;
  hook_strategy: string;
  recommended_format: string;
  format_scores: Record<string, number>;
  item_count: number;
  primary_source?: string;
  sources_summary: string[];
}

export interface TopOpportunitiesResponse {
  total_trends_analyzed: number;
  top_opportunities: OpportunityCard[];
  generated_at: string;
}

export interface SourceEvidenceItem {
  title: string;
  url: string;
  source: string;
  source_quality: string;
  published_at?: string;
  role: string;
}

export interface TrendObservation {
  id: string;
  trend_id: string;
  timestamp: string;
  mention_count: number;
  source_count: number;
  source_diversity: number;
  social_mentions?: number;
  engagement?: number;
  new_items: number;
  momentum_score: number;
  competition_score: number;
  opportunity_score: number;
}

export interface TrendDetail {
  id: string;
  name: string;
  category: string;
  lifecycle_stage: string;
  status: string;
  opportunity_score: number;
  opportunity_type: string;
  competition_score: number;
  novelty_score: number;
  audience_fit_score: number;
  momentum: number;
  momentum_change_pct: number;
  momentum_direction: string;
  what_happened: string;
  why_trending: string;
  what_changed?: string;
  what_is_saturated?: string;
  what_is_missing?: string;
  who_cares?: string;
  best_angle: string;
  alternative_angles: string[];
  saturated_angles: string[];
  under_served_angles: string[];
  best_hook_type: string;
  hook_strategy: string;
  best_format: string;
  format_scores: Record<string, number>;
  timing_verdict: string;
  timing_reason: string;
  claims_to_avoid: string[];
  primary_audience?: string;
  secondary_audiences?: string[];
  source_evidence: SourceEvidenceItem[];
  observations: TrendObservation[];
}

export interface Topic {
  id: string;
  name: string;
  category: string;
  momentum: number;
  momentum_change_pct?: number;
  momentum_direction?: string;
  status: string;
  lifecycle_stage?: string;
  opportunity_score?: number;
  opportunity_type?: string;
  competition_score?: number;
  novelty_score?: number;
  audience_fit_score?: number;
  recommended_action?: string;
  action_reason?: string;
  recommended_angle?: string;
  alternative_angles?: string[];
  saturated_angles?: string[];
  under_served_angles?: string[];
  recommended_hook_type?: string;
  hook_strategy?: string;
  recommended_format?: string;
  format_scores?: Record<string, number>;
  primary_audience?: string;
  secondary_audiences?: string[];
  item_count: number;
  sources_summary: string[];
  primary_source?: string;
  updated_at: string;
}

export interface SavedItem {
  id: string;
  content_item_id: string;
  status: "Idea" | "Draft" | "Posted" | "Ignored";
  notes?: string;
  saved_at: string;
  content_item?: ContentItem;
}

export interface VoiceProfile {
  id?: string;
  name: string;
  tone_preference: string;
  voice_examples: string[];
  guidelines?: string;
  updated_at?: string;
}

// =========================================================================
// V3 REAL-TIME GLOBAL AI INTELLIGENCE & CONTENT OPERATING SYSTEM TYPES
// =========================================================================

export interface TerminalStatus {
  status: "LIVE" | "SYNCING" | "OFFLINE";
  last_ingestion_seconds_ago: number;
  detection_latency_seconds: number;
  events_today_count: number;
  breaking_count: number;
  emerging_count: number;
  exploding_count: number;
  opportunities_count: number;
  services: {
    firecrawl: { status: string; latency_ms: number };
    gemini: { status: string; model: string };
    database: { status: string; type: string };
    sources?: {
      total_sources: number;
      healthy_count: number;
      degraded_count: number;
      offline_count: number;
    };
  };
}

export interface V3EventSource {
  source_name: string;
  url: string;
  quality_tier: string;
  title?: string;
  published_at?: string;
}

export interface V3Event {
  id: string;
  title: string;
  summary: string;
  category: string;
  status: "CONFIRMED" | "LIKELY" | "DEVELOPING" | "UNVERIFIED" | "CONTRADICTED";
  confidence_score: number;
  source_count: number;
  independent_source_count: number;
  primary_source_name?: string;
  primary_source_url?: string;
  entities: string[];
  key_facts: string[];
  relevance_score: number;
  freshness_score: number;
  momentum_score: number;
  opportunity_score: number;
  recommended_action: "POST_NOW" | "POST_SOON" | "WATCH" | "WAIT" | "SKIP";
  recommended_angle?: string;
  recommended_platform: "X" | "LinkedIn" | "Instagram" | "YouTube";
  event_timestamp: string;
  first_seen_at: string;
  surfaced_at: string;
  total_pipeline_latency: number;
  sources: V3EventSource[];
}

export interface HookCandidate {
  category: string;
  text: string;
  hook_score: number;
  curiosity: number;
  specificity: number;
  novelty: number;
  clarity: number;
  scroll_stop_potential: number;
  credibility: number;
  conversation_potential: number;
}

export interface ContentBriefData {
  topic: string;
  audience: string;
  goal: string;
  angle: string;
  content_format: string;
  hook_strategy: string;
  key_claims: string[];
  supporting_facts: string[];
  counterpoint: string;
  cta_strategy: string;
  visual_strategy: string;
  platform_strategy: string;
}

export interface QualityEvaluation {
  total_quality_score: number;
  fact_check_score: number;
  originality_score: number;
  hook_strength_score: number;
  clarity_score: number;
  platform_fit_score: number;
  audience_fit_score: number;
  cta_effectiveness: number;
  spam_score: number;
  clickbait_penalty: number;
  is_approved: boolean;
  feedback: string[];
}

export interface PlatformSuite {
  brief: ContentBriefData;
  quality: QualityEvaluation;
  x_content: {
    platform: string;
    selected_hook: HookCandidate;
    single_post: string;
    thread: string[];
    char_count: number;
    hashtags: string[];
  };
  x_hooks: HookCandidate[];
  linkedin_content: {
    platform: string;
    content: string;
    word_count: number;
    cta: string;
  };
  instagram_carousel: {
    platform: string;
    format: string;
    total_slides: number;
    slides: Array<{
      slide_number: number;
      type: string;
      headline: string;
      subtext: string;
      visual_direction: string;
      asset_prompt: string;
    }>;
    caption: string;
  };
  instagram_reel: {
    platform: string;
    format: string;
    duration_seconds: number;
    beats: Array<{
      timecode: string;
      beat: string;
      narration: string;
      visual: string;
    }>;
  };
  youtube_content: {
    platform: string;
    titles: Array<{ style: string; title: string }>;
    selected_title: string;
    thumbnails: Array<{
      concept: number;
      name: string;
      subject: string;
      foreground_text: string;
      emotion: string;
      prompt: string;
    }>;
    short_script: {
      title: string;
      duration: string;
      sections: Array<{ time: string; type: string; text: string }>;
    };
    description: string;
    seo_tags: string[];
  };
}

export interface OmniPromptPayload {
  subject: string;
  action: string;
  environment: string;
  time_of_day: string;
  lighting: string;
  camera: Record<string, string>;
  composition: string;
  depth: string;
  materials: string;
  physics: string;
  motion: string;
  audio: string;
  dialogue: string;
  style: string;
  color_tone: string;
  continuity: string;
  negative_constraints: string[];
  output_format: string;
  compiled_master_prompt: string;
}

export interface StoryboardScene {
  scene_number: number;
  timecode: string;
  duration_sec: number;
  beat_type: string;
  narration: string;
  visual_direction: string;
  camera_instruction: string;
  on_screen_text: string;
  recommended_engine: string;
  asset_prompt: string;
}

export interface DailyBrief {
  title: string;
  generated_at: string;
  summary: string;
  metrics: {
    major_events_count: number;
    emerging_trends_count: number;
    exploding_trends_count: number;
    opportunities_count: number;
  };
  best_opportunity?: {
    id: string;
    topic: string;
    opportunity_score: number;
    competition_score: number;
    recommended_angle: string;
    status: string;
  };
  top_events: Array<{
    id: string;
    title: string;
    status: string;
    confidence: number;
    category: string;
    momentum: number;
  }>;
  what_you_should_post_today: string;
}

export interface DayPlanSlot {
  time_slot: string;
  platform: string;
  format: string;
  topic: string;
  recommended_angle: string;
  priority: string;
  action: string;
}

export interface ContentQueueItem {
  id: string;
  event_id?: string;
  platform: string;
  title: string;
  content: string;
  status: "IDEA" | "DRAFT" | "REVIEW" | "APPROVED" | "READY" | "SCHEDULED" | "PUBLISHED" | "PERFORMING" | "COMPLETED";
  priority: "URGENT" | "HIGH" | "MEDIUM" | "LOW";
  scheduled_for?: string;
  created_at: string;
}

export interface TrendGraphData {
  nodes: Array<{
    id: string;
    name: string;
    type: "category" | "trend" | "event";
    size: number;
    color: string;
    momentum?: number;
    opportunity?: number;
    lifecycle?: string;
    status?: string;
  }>;
  links: Array<{
    source: string;
    target: string;
    value: number;
    type: string;
  }>;
  meta: {
    total_nodes: number;
    total_links: number;
    active_categories: string[];
  };
}

export interface VideoHookVisualizer {
  hook_id: string;
  first_spoken_line: string;
  first_visual: string;
  first_camera_movement: string;
  first_on_screen_text: string;
  first_sfx: string;
  curiosity_mechanism: string;
  retention_score: number;
}

export interface VideoStoryboardScene {
  scene_number: number;
  start_time_sec: number;
  end_time_sec: number;
  duration_sec: number;
  narrative_purpose: string;
  visual_objective: string;
  voiceover_text: string;
  on_screen_text: string;
  recommended_engine: "REMOTION" | "OMNI" | "VEO" | "HYPERFRAMES" | "HYBRID";
  transition_out: string;
  sound_design: string;
}

export interface VideoShotDirection {
  shot_id: string;
  scene_number: number;
  start_sec: number;
  duration_sec: number;
  engine: "REMOTION" | "OMNI" | "VEO" | "HYPERFRAMES";
  visual_objective: string;
  camera_position: string;
  camera_movement: string;
  subject_action: string;
  environment_lighting: string;
  shot_complexity: number;
  exact_model_prompt: string;
  negative_constraints: string;
  continuity_requirements: string;
  copyable_prompt: string;
}

export interface VideoAssetRequirement {
  asset_id: string;
  asset_type: string;
  description: string;
  source: string;
  aspect_ratio: string;
  used_by_shot: string;
}

export interface VideoPackage {
  package_id: string;
  event_id?: string;
  title: string;
  platform: string;
  duration_seconds: number;
  aspect_ratio: string;
  style_preset: string;
  generation_strategy: string;
  creative_concept: string;
  why_this_video: string;
  ranked_hooks: VideoHookVisualizer[];
  storyboard: VideoStoryboardScene[];
  shot_list: VideoShotDirection[];
  asset_manifest: VideoAssetRequirement[];
  audio_plan: {
    voiceover_script: string;
    music_genre: string;
    bpm_range: string;
    emotional_role: string;
    sfx_cues: Array<{ timestamp_sec: number; sound_event: string; intensity: string }>;
  };
  engines: {
    remotion?: {
      standalone_agent_prompt: string;
      video_props_interface: string;
      render_command: string;
    };
    omni?: Array<{
      shot_id: string;
      purpose: string;
      visual_prompt: string;
      audio_direction: string;
      continuity: string;
      avoid: string;
    }>;
    veo?: Array<{
      shot_id: string;
      workflow_type: string;
      prompt: string;
      start_frame_prompt?: string;
      end_frame_prompt?: string;
      motion_prompt?: string;
    }>;
    hyperframes?: {
      composition_id: string;
      html_markup: string;
      css_styles: string;
      gsap_timeline_code: string;
      standalone_agent_prompt: string;
    };
  };
  hybrid_assembly?: {
    layer_order: string[];
    compositing_instructions: string;
  };
  quality_report: {
    overall_readiness_score: number;
    passes_quality_gate: boolean;
    dimension_scores: Record<string, number>;
    self_critique: string[];
    prohibited_phrases_detected: string[];
  };
  visual_concepts?: VisualConceptSuite;
  production_shots?: ProductionShotSpec[];
  forensic_report?: VideoForensicReport;
  prompt_evolution?: PromptEvolutionLineage;
  created_at: string;
}

export interface VisualConcept {
  concept_id: string;
  representation_type: string;
  headline: string;
  core_visual_metaphor: string;
  description: string;
  what_viewer_sees: string;
  what_viewer_understands: string;
  information_density: number;
  conceptual_clarity: number;
  emotional_impact: number;
  novelty_score: number;
  production_feasibility: number;
  recommended_engine: string;
  asset_requirements?: string[];
  anti_slop_safeguards?: string[];
  overall_fit_score: number;
  is_recommended?: boolean;
  selection_rationale?: string;
}

export interface VisualConceptSuite {
  suite_id: string;
  claim_or_narration: string;
  topic?: string;
  platform?: string;
  candidates: VisualConcept[];
  selected_concept: VisualConcept;
}

export interface ProductionShotSpec {
  shot_id: string;
  scene_number: number;
  duration_sec: number;
  purpose: string;
  narration: string;
  visual_representation_type: string;
  primary_engine: string;
  model_selection_reason: string;
  subject: string;
  action: string;
  environment: string;
  composition_and_framing: string;
  camera_movement: string;
  lighting: string;
  color_palette: string;
  complexity_score: number;
  is_decomposed: boolean;
  decomposed_micro_shots?: Array<any>;
}

export interface ForensicDimensionEvaluation {
  dimension_name: string;
  score: number;
  status: "PASS" | "WARN" | "FAIL";
  evidence: string[];
}

export interface VideoForensicReport {
  analysis_id: string;
  video_identifier: string;
  prompt_readiness_score: number;
  expected_executability_score: number;
  actual_video_quality_score: number;
  overall_verdict: "EXCELLENT" | "PASS" | "WARN" | "FAIL";
  dimension_scores: Record<string, number>;
  dimension_evaluations: ForensicDimensionEvaluation[];
  detected_failures: Array<{
    id: string;
    category: string;
    dimension?: string;
    severity: string;
    description: string;
    recommended_fix: string;
  }>;
  representative_frames: Array<{
    frame_index: number;
    timestamp_sec: number;
    percentage: number;
    timecode: string;
    description: string;
  }>;
  extracted_metadata?: {
    duration_sec: number;
    width: number;
    height: number;
    aspect_ratio: string;
    fps: number;
    frame_count: number;
    has_audio: boolean;
    bitrate_kbps: number;
    scene_cut_count: number;
  };
  remediation_actions: string[];
}

export interface PromptEvolutionLineage {
  evolution_id: string;
  parent_version: string;
  new_version: string;
  primary_failure_addressed: string;
  mutations_applied: Array<{
    operator: string;
    target_shot_or_section: string;
    rationale: string;
    original_snippet?: string;
    mutated_snippet?: string;
    expected_quality_delta: number;
  }>;
  evolved_prompt_text: string;
  expected_executability_score: number;
  predicted_quality_score: number;
  lineage_notes: string;
}

export interface FailurePatternDashboard {
  most_common_failures: Array<{
    failure_name: string;
    frequency_percentage: number;
    impact: string;
    failure_code?: string;
  }>;
  best_improvement_mutations: Array<{
    mutation: string;
    quality_gain_percentage: string;
    confidence: number;
  }>;
  learned_heuristics: Array<{
    heuristic_id: string;
    context_condition: string;
    recommendation: string;
    confidence: number;
    sample_count: number;
    validation_status: string;
  }>;
  total_evaluations_monitored: number;
}

