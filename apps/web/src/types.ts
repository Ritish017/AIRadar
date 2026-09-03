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
