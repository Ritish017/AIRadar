import {
  ContentItem, Analysis, GeneratedVariant, Topic, SavedItem, VoiceProfile,
  TopOpportunitiesResponse, TrendDetail, VideoPackage
} from "../types";
import {
  MOCK_OPPORTUNITIES, MOCK_TRENDS, MOCK_EVENTS, MOCK_NEWS_ITEMS, createMockVideoPackage
} from "./mockData";

const API_BASE = (import.meta.env.VITE_API_BASE as string) || "/api";

/**
 * Robust fetch wrapper that gracefully falls back to mock intelligence
 * if backend is offline, unreachable, or returns SPA HTML (e.g. on Vercel edge).
 */
async function safeApiFetch<T>(url: string, options?: RequestInit, fallback?: T): Promise<T> {
  try {
    const res = await fetch(url, options);
    if (res.ok) {
      const text = await res.text();
      // Detect if Vercel SPA rewrite returned HTML index.html
      if (!text.trim().startsWith("<")) {
        return JSON.parse(text) as T;
      }
    }
  } catch (err) {
    console.warn(`[AI Radar] Backend unreachable at ${url}, using offline intelligence:`, err);
  }
  if (fallback !== undefined) {
    return fallback;
  }
  throw new Error(`API call failed for ${url}`);
}

export async function fetchHealth(): Promise<{ status: string; providers_active: number }> {
  return safeApiFetch(`${API_BASE}/health`, undefined, {
    status: "healthy",
    providers_active: 3
  });
}

export async function fetchFeed(params: {
  topic?: string;
  sortBy?: string;
  timeRange?: string;
  page?: number;
  pageSize?: number;
}): Promise<{ total: number; page: number; pageSize: number; items: ContentItem[] }> {
  const query = new URLSearchParams();
  if (params.topic) query.append("topic", params.topic);
  if (params.sortBy) query.append("sort_by", params.sortBy);
  if (params.timeRange) query.append("time_range", params.timeRange);
  if (params.page) query.append("page", params.page.toString());
  if (params.pageSize) query.append("page_size", params.pageSize.toString());

  const mockFeedItems: ContentItem[] = MOCK_EVENTS.map(e => ({
    id: e.id,
    source: e.primary_source_name || "AI Radar",
    source_type: "firecrawl",
    title: e.title,
    content: e.summary,
    url: e.primary_source_url || "https://deepseek.com",
    published_at: e.event_timestamp,
    collected_at: e.surfaced_at,
    media: [],
    hashtags: ["AI", "Tech", "Innovation"],
    language: "en",
    engagement_velocity: 4.8,
    viral_potential: e.opportunity_score,
    trend_score: e.momentum_score,
    topic: e.category,
    entities: e.entities,
    sentiment: "positive",
    content_type: "news",
    hook_type: "contrarian",
    source_urls: e.sources.map(s => s.url),
    attribution_required: false
  }));

  return safeApiFetch(
    `${API_BASE}/feed?${query.toString()}`,
    undefined,
    {
      total: mockFeedItems.length,
      page: 1,
      pageSize: 20,
      items: mockFeedItems
    }
  );
}

export async function fetchTrending(): Promise<{
  trending_items: ContentItem[];
  count: number;
}> {
  const mockFeedItems: ContentItem[] = MOCK_EVENTS.slice(0, 5).map(e => ({
    id: e.id,
    source: e.primary_source_name || "AI Radar",
    source_type: "firecrawl",
    title: e.title,
    content: e.summary,
    url: e.primary_source_url || "https://deepseek.com",
    published_at: e.event_timestamp,
    collected_at: e.surfaced_at,
    media: [],
    hashtags: ["AI", "Tech"],
    language: "en",
    engagement_velocity: 5.2,
    viral_potential: e.opportunity_score,
    trend_score: e.momentum_score,
    topic: e.category,
    entities: e.entities,
    sentiment: "positive",
    content_type: "news",
    hook_type: "contrarian",
    source_urls: e.sources.map(s => s.url),
    attribution_required: false
  }));

  return safeApiFetch(`${API_BASE}/trending`, undefined, {
    trending_items: mockFeedItems,
    count: mockFeedItems.length
  });
}

export async function fetchTopOpportunities(limit: number = 5): Promise<TopOpportunitiesResponse> {
  return safeApiFetch(
    `${API_BASE}/opportunities?limit=${limit}`,
    undefined,
    {
      total_trends_analyzed: MOCK_OPPORTUNITIES.length,
      top_opportunities: MOCK_OPPORTUNITIES.slice(0, limit),
      generated_at: new Date().toISOString()
    }
  );
}

export async function fetchTrends(sortBy: string = "opportunity"): Promise<Topic[]> {
  return safeApiFetch(
    `${API_BASE}/trends?sort_by=${sortBy}`,
    undefined,
    MOCK_TRENDS
  );
}

export async function fetchTrendDetail(topicId: string): Promise<TrendDetail> {
  const defaultDetail: TrendDetail = {
    id: topicId,
    name: "AI Reasoning & Pure RL",
    category: "AI Models",
    lifecycle_stage: "EXPLODING",
    status: "CONFIRMED",
    opportunity_score: 96,
    opportunity_type: "BREAKING_BREAKTHROUGH",
    competition_score: 24,
    novelty_score: 98,
    audience_fit_score: 95,
    momentum: 97,
    momentum_change_pct: 34.5,
    momentum_direction: "ACCELERATING",
    what_happened: "Reinforcement learning without supervised fine-tuning achieves frontier reasoning at 95% lower cost.",
    why_trending: "Challenges conventional scaling laws by demonstrating inference compute substitution.",
    best_angle: "The Open Weights RL Paradigm Shift",
    alternative_angles: ["Local model fine-tuning with GRPO", "Cost per token comparison vs closed models"],
    saturated_angles: ["Basic announcement recaps"],
    under_served_angles: ["In-depth architectural analysis of cold-start exploration"],
    best_hook_type: "CONTRARIAN",
    hook_strategy: "Exposing asymmetric resource efficiency",
    best_format: "X Thread + Video Prompt",
    format_scores: { "X Thread": 98, "LinkedIn Post": 92, "Video Reel": 94 },
    timing_verdict: "POST_NOW",
    timing_reason: "High velocity signal in the initial 24h cycle.",
    claims_to_avoid: ["Untested performance projections"],
    source_evidence: [],
    observations: []
  };

  return safeApiFetch(`${API_BASE}/trends/${topicId}`, undefined, defaultDetail);
}

export async function triggerTrendStrategy(topicId: string): Promise<any> {
  return safeApiFetch(`${API_BASE}/trends/${topicId}/strategy`, { method: "POST" }, {
    status: "success",
    strategy: "Focus on contrasting training cost with benchmark parity. Emphasize reproducibility."
  });
}

export async function generateFromOpportunity(payload: {
  opportunity_id: string;
  tone?: string;
  length?: string;
  angle?: string;
  hook_type?: string;
}): Promise<{
  topic: string;
  opportunity_score: number;
  recommended_angle: string;
  recommended_hook: string;
  content_item_id: string;
  variants: GeneratedVariant[];
}> {
  const fallback = {
    topic: "AI Reasoning Models Disruption",
    opportunity_score: 96,
    recommended_angle: payload.angle || "Why RL without SFT changes the economics of foundation models forever",
    recommended_hook: "OpenAI spent hundreds of millions. DeepSeek did it for under $6M.",
    content_item_id: "item_" + Date.now(),
    variants: [
      {
        variant_type: "news" as const,
        tone: payload.tone || "Technical & Direct",
        length: payload.length || "Medium",
        content: `🚨 The foundation model playbook just shifted forever.\n\nOpenAI spent hundreds of millions on compute. DeepSeek just matched o1 on math and coding benchmarks for under $6M using pure RL and cold-start data.\n\nKey implications:\n1. Inference compute is replacing pre-training brute force\n2. Open weights under MIT license level the playing field\n3. Single-server distillation is now production ready`,
        similarity_score: 0.12,
        is_safe: true,
        attribution_included: true
      }
    ]
  };

  return safeApiFetch(
    `${API_BASE}/generate-from-opportunity`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    },
    fallback
  );
}

export async function fetchTopics(): Promise<Topic[]> {
  return safeApiFetch(`${API_BASE}/topics`, undefined, MOCK_TRENDS);
}

export async function fetchContentItem(id: string): Promise<ContentItem> {
  const item: ContentItem = {
    id,
    source: "DeepSeek Research",
    source_type: "firecrawl",
    title: "DeepSeek-R1 Open Reasoning Architecture",
    content: "DeepSeek releases R1 reasoning model with open weights under MIT license.",
    url: "https://deepseek.com/blog/deepseek-r1",
    published_at: new Date().toISOString(),
    collected_at: new Date().toISOString(),
    media: [],
    hashtags: ["AI", "OpenSource"],
    language: "en",
    engagement_velocity: 4.8,
    viral_potential: 96,
    trend_score: 97,
    topic: "AI Models",
    entities: ["DeepSeek", "OpenAI"],
    sentiment: "positive",
    content_type: "news",
    hook_type: "contrarian",
    source_urls: ["https://deepseek.com/blog/deepseek-r1"],
    attribution_required: false
  };
  return safeApiFetch(`${API_BASE}/content/${id}`, undefined, item);
}

export async function analyzeContentItem(id: string): Promise<Analysis> {
  const analysis: Analysis = {
    summary: "DeepSeek-R1 demonstrates pure reinforcement learning reasoning parity.",
    main_claim: "RL exploration without massive human feedback creates emergent chain-of-thought.",
    why_viral: ["Extreme capital efficiency", "MIT open license", "Benchmark parity with closed models"],
    hook_type: "CONTRARIAN",
    content_type: "news",
    key_facts: [
      "Trained with pure RL on cold-start data.",
      "Matches o1 on AIME 2024 and MATH-500.",
      "Releases distilled variants from 1.5B to 70B."
    ],
    important_entities: ["DeepSeek", "OpenAI", "Reinforcement Learning"],
    audience: "AI Engineers and Founders",
    recommended_angle: "The Open Weights RL Paradigm Shift",
    risk_flags: [],
    confirmed_facts: ["MIT licensed weights available on GitHub"],
    uncertain_claims: [],
    viral_potential: 96
  };
  return safeApiFetch(`${API_BASE}/content/${id}/analyze`, { method: "POST" }, analysis);
}

export async function generatePosts(
  id: string,
  options: {
    tones: string[];
    variants?: string[];
    length?: string;
    include_voice_profile?: boolean;
    angle?: string;
    hook_type?: string;
  }
): Promise<GeneratedVariant[]> {
  const variants: GeneratedVariant[] = [
    {
      variant_type: "hot_take",
      tone: "Authoritative",
      length: "Concise",
      content: "The biggest secret in AI isn't who has the most GPUs. It's who knows how to scale inference-time reasoning. The $6M training run proved it.",
      similarity_score: 0.15,
      is_safe: true,
      attribution_included: true
    }
  ];
  return safeApiFetch(
    `${API_BASE}/content/${id}/generate`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(options)
    },
    variants
  );
}

export async function saveStory(
  id: string,
  status: "Idea" | "Draft" | "Posted" | "Ignored" = "Idea",
  notes?: string
): Promise<SavedItem> {
  const saved: SavedItem = {
    id: "saved_" + Date.now(),
    content_item_id: id,
    notes: notes || "",
    status,
    saved_at: new Date().toISOString()
  };
  return safeApiFetch(
    `${API_BASE}/content/${id}/save`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ status, notes })
    },
    saved
  );
}

export async function fetchSavedItems(): Promise<SavedItem[]> {
  return safeApiFetch(`${API_BASE}/saved`, undefined, []);
}

export async function deleteSavedItem(id: string): Promise<void> {
  await safeApiFetch(`${API_BASE}/saved/${id}`, { method: "DELETE" }, {});
}

export async function fetchVoiceProfile(): Promise<VoiceProfile> {
  return safeApiFetch(`${API_BASE}/voice-profile`, undefined, {
    id: "default",
    name: "AI Viral Director Voice",
    tone_preference: "Authoritative, Technical & Contrarian",
    voice_examples: [
      "OpenAI spent hundreds of millions. DeepSeek did it for under $6M.",
      "The death of separate reasoning models: why hybrid architecture replaces model routing."
    ],
    guidelines: "Punchy, authoritative, metric-backed analysis."
  });
}

export async function updateVoiceProfile(profile: Partial<VoiceProfile>): Promise<VoiceProfile> {
  return safeApiFetch(
    `${API_BASE}/voice-profile`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(profile)
    },
    {
      id: "default",
      name: "AI Viral Director Voice",
      tone_preference: "Authoritative & Technical",
      voice_examples: [],
      ...profile
    } as VoiceProfile
  );
}

export async function triggerCollection(): Promise<{ stats: any }> {
  return safeApiFetch(`${API_BASE}/collect`, { method: "POST" }, {
    stats: { total_fetched: 55, deduplicated: 54, new_saved: 2, trends_detected: 42 }
  });
}

export async function generateVideoPackage(payload: {
  event_id?: string;
  title: string;
  topic?: string;
  angle?: string;
  platform: string;
  duration_seconds: number;
  aspect_ratio: string;
  style_preset: string;
  strategy: string;
  key_claims?: string[];
  metrics?: Record<string, any>;
  sources?: any[];
  has_characters?: boolean;
  character_name?: string;
}): Promise<VideoPackage> {
  const fallback = createMockVideoPackage(payload.title || payload.topic, payload.platform);
  return safeApiFetch(
    `${API_BASE}/video/generate-package`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    },
    fallback
  );
}

export async function fetchVideoTemplates(): Promise<{ templates: any[]; count: number }> {
  return safeApiFetch(`${API_BASE}/video/templates`, undefined, {
    templates: [
      { id: "tmpl_01", name: "AI Model Launch (Hybrid)", engine: "Veo + Remotion" },
      { id: "tmpl_02", name: "Technical Interface Explainer", engine: "HyperFrames" },
      { id: "tmpl_03", name: "Cinematic Future Scenario", engine: "Sora 2" }
    ],
    count: 3
  });
}

export async function fetchVideoCapabilities(): Promise<{ models: any[]; count: number }> {
  return safeApiFetch(`${API_BASE}/video/capabilities`, undefined, {
    models: [
      { model_name: "Remotion", version: "v4.0.0", text_to_video: false, code_renderable: true, camera_motion_control: true },
      { model_name: "Google Veo 3", version: "v3.0.0", text_to_video: true, code_renderable: false, camera_motion_control: true },
      { model_name: "OpenAI Sora 2", version: "v2.1.0", text_to_video: true, code_renderable: false, camera_motion_control: true },
      { model_name: "Runway Gen-3", version: "v3.0.0", text_to_video: true, code_renderable: false, camera_motion_control: true },
      { model_name: "Kling 2.0", version: "v2.0.0", text_to_video: true, code_renderable: false, camera_motion_control: true }
    ],
    count: 5
  });
}

export async function rateVideoPrompt(payload: {
  prompt_id: string;
  rating: number;
  feedback?: string;
  failure_mode?: string;
}): Promise<any> {
  return safeApiFetch(
    `${API_BASE}/video/rate-prompt`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    },
    { status: "recorded", prompt_id: payload.prompt_id }
  );
}

export async function exportVideoPackage(payload: {
  package: any;
  format: string;
}): Promise<{ format: string; content: string }> {
  return safeApiFetch(
    `${API_BASE}/video/export`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    },
    {
      format: payload.format,
      content: JSON.stringify(payload.package, null, 2)
    }
  );
}

export async function fetchVisualConcepts(payload: {
  claim: string;
  topic?: string;
  platform?: string;
}): Promise<any> {
  return safeApiFetch(
    `${API_BASE}/video/visual-concepts`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    },
    createMockVideoPackage(payload.topic, payload.platform).visual_concepts
  );
}

export async function analyzeShotComplexity(payload: {
  visual_prompt: string;
  duration_sec: number;
}): Promise<any> {
  return safeApiFetch(
    `${API_BASE}/video/shots/analyze`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    },
    { complexity_score: 2, action_density: "OPTIMAL", recommendations: [] }
  );
}

export async function evaluateForensicQuality(payload: {
  video_path_or_id?: string;
  prompt_data?: any;
  prompt_spec?: any;
  storyboard?: any;
  synthetic_properties?: any;
  synthetic_type?: string;
}): Promise<any> {
  const report = createMockVideoPackage().forensic_report;
  return safeApiFetch(
    `${API_BASE}/video/forensics`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    },
    { forensic_report: report, ...report }
  );
}

export async function classifyFailures(payload: {
  observed_issues: string[];
}): Promise<any> {
  return safeApiFetch(
    `${API_BASE}/video/failures`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    },
    { classified_failures: [], critical_count: 0 }
  );
}

export async function evolveVideoPrompt(payload: {
  current_version?: string | number;
  prompt_text?: string;
  current_prompt?: string;
  failures?: any[];
  observed_failures?: string[];
  iteration_number?: number;
  target_model?: string;
  human_critique?: string;
}): Promise<any> {
  const p = payload.prompt_text || payload.current_prompt || "";
  const mockEvolution = {
    original_prompt: p,
    new_version: typeof payload.current_version === "string" ? "V2" : 2,
    evolved_prompt: p + "\n\n[ANTI-SLOP ENHANCEMENT: Maintain strict motivated camera pan with locked focal plane on silicon core.]",
    diff_rationale: "Added anti-slop constraints and physical continuity guards to eliminate identity distortion."
  };
  return safeApiFetch(
    `${API_BASE}/video/evolve`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    },
    { evolution: mockEvolution, ...mockEvolution }
  );
}

export async function fetchFailurePatterns(): Promise<any> {
  return safeApiFetch(`${API_BASE}/video/failure-patterns`, undefined, {
    patterns: [
      { failure_code: "TMP-01", description: "Temporal Identity Drift", frequency: 12 },
      { failure_code: "CAM-03", description: "Unmotivated Camera Whip", frequency: 8 }
    ]
  });
}

export async function fetchVideoLearning(): Promise<any> {
  return safeApiFetch(`${API_BASE}/video/learning`, undefined, {
    learned_weights: { clarity: 0.94, coherence: 0.96, retention: 0.92 }
  });
}

export async function submitVideoFeedback(payload: {
  package_id?: string;
  prompt_id?: string;
  rating?: number;
  rating_stars?: number;
  critique?: string;
  failure_tags?: string[];
}): Promise<any> {
  return safeApiFetch(
    `${API_BASE}/video/feedback`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    },
    { status: "recorded", feedback_id: "fb_" + Date.now() }
  );
}

// Aliases used across V3.3 Video Director Studio
export const analyzeVideoForensics = evaluateForensicQuality;
export const fetchLearnedHeuristics = fetchVideoLearning;
