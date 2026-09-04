import {
  ContentItem, Analysis, GeneratedVariant, Topic, SavedItem, VoiceProfile,
  TopOpportunitiesResponse, TrendDetail, VideoPackage
} from "../types";

const API_BASE = (import.meta.env.VITE_API_BASE as string) || "/api";

export async function fetchHealth(): Promise<{ status: string; providers_active: number }> {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error("API health check failed");
  return res.json();
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

  const res = await fetch(`${API_BASE}/feed?${query.toString()}`);
  if (!res.ok) throw new Error("Failed to fetch feed");
  return res.json();
}

export async function fetchTrending(): Promise<{
  trending_items: ContentItem[];
  count: number;
}> {
  const res = await fetch(`${API_BASE}/trending`);
  if (!res.ok) throw new Error("Failed to fetch trending data");
  return res.json();
}

export async function fetchTopOpportunities(limit: number = 5): Promise<TopOpportunitiesResponse> {
  const res = await fetch(`${API_BASE}/opportunities?limit=${limit}`);
  if (!res.ok) throw new Error("Failed to fetch top opportunities");
  return res.json();
}

export async function fetchTrends(sortBy: string = "opportunity"): Promise<Topic[]> {
  const res = await fetch(`${API_BASE}/trends?sort_by=${sortBy}`);
  if (!res.ok) throw new Error("Failed to fetch trends");
  return res.json();
}

export async function fetchTrendDetail(topicId: string): Promise<TrendDetail> {
  const res = await fetch(`${API_BASE}/trends/${topicId}`);
  if (!res.ok) throw new Error("Failed to fetch trend detail");
  return res.json();
}

export async function triggerTrendStrategy(topicId: string): Promise<any> {
  const res = await fetch(`${API_BASE}/trends/${topicId}/strategy`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to analyze trend strategy with AI");
  return res.json();
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
  const res = await fetch(`${API_BASE}/generate-from-opportunity`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to generate posts from opportunity");
  return res.json();
}

export async function fetchTopics(): Promise<Topic[]> {
  const res = await fetch(`${API_BASE}/topics`);
  if (!res.ok) throw new Error("Failed to fetch topics");
  return res.json();
}

export async function fetchContentItem(id: string): Promise<ContentItem> {
  const res = await fetch(`${API_BASE}/content/${id}`);
  if (!res.ok) throw new Error("Failed to fetch content item");
  return res.json();
}

export async function analyzeContentItem(id: string): Promise<Analysis> {
  const res = await fetch(`${API_BASE}/content/${id}/analyze`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to analyze content");
  return res.json();
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
  const res = await fetch(`${API_BASE}/content/${id}/generate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(options),
  });
  if (!res.ok) throw new Error("Failed to generate posts");
  return res.json();
}

export async function saveStory(
  id: string,
  status: "Idea" | "Draft" | "Posted" | "Ignored" = "Idea",
  notes?: string
): Promise<SavedItem> {
  const res = await fetch(`${API_BASE}/content/${id}/save`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status, notes }),
  });
  if (!res.ok) throw new Error("Failed to save story");
  return res.json();
}

export async function fetchSavedItems(): Promise<SavedItem[]> {
  const res = await fetch(`${API_BASE}/saved`);
  if (!res.ok) throw new Error("Failed to fetch saved stories");
  return res.json();
}

export async function deleteSavedItem(id: string): Promise<void> {
  const res = await fetch(`${API_BASE}/saved/${id}`, { method: "DELETE" });
  if (!res.ok) throw new Error("Failed to delete saved story");
}

export async function fetchVoiceProfile(): Promise<VoiceProfile> {
  const res = await fetch(`${API_BASE}/voice-profile`);
  if (!res.ok) throw new Error("Failed to fetch voice profile");
  return res.json();
}

export async function updateVoiceProfile(profile: Partial<VoiceProfile>): Promise<VoiceProfile> {
  const res = await fetch(`${API_BASE}/voice-profile`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(profile),
  });
  if (!res.ok) throw new Error("Failed to update voice profile");
  return res.json();
}

export async function triggerCollection(): Promise<{ stats: any }> {
  const res = await fetch(`${API_BASE}/collect`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to trigger collection");
  return res.json();
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
  const res = await fetch(`${API_BASE}/video/generate-package`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to generate video package");
  return res.json();
}

export async function fetchVideoTemplates(): Promise<{ templates: any[]; count: number }> {
  const res = await fetch(`${API_BASE}/video/templates`);
  if (!res.ok) throw new Error("Failed to fetch video templates");
  return res.json();
}

export async function fetchVideoCapabilities(): Promise<{ models: any[]; count: number }> {
  const res = await fetch(`${API_BASE}/video/capabilities`);
  if (!res.ok) throw new Error("Failed to fetch video capabilities");
  return res.json();
}

export async function rateVideoPrompt(payload: {
  prompt_id: string;
  rating: number;
  feedback?: string;
  failure_mode?: string;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/video/rate-prompt`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to rate video prompt");
  return res.json();
}

export async function exportVideoPackage(payload: {
  package: any;
  format: string;
}): Promise<{ format: string; content: string }> {
  const res = await fetch(`${API_BASE}/video/export`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to export video package");
  return res.json();
}

export async function fetchVisualConcepts(payload: {
  claim: string;
  topic?: string;
  platform?: string;
  metrics?: Record<string, any>;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/video/visual-concepts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to fetch visual concepts");
  return res.json();
}

export async function analyzeShotComplexity(payload: {
  shot_id?: string;
  visual_objective: string;
  subject_action: string;
  camera_movement: string;
  duration_sec?: number;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/video/shots/analyze`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to analyze shot complexity");
  return res.json();
}

export async function analyzeVideoForensics(payload: {
  video_path_or_id: string;
  prompt_spec?: any;
  storyboard?: any;
  synthetic_properties?: any;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/video/forensics`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to analyze video forensics");
  return res.json();
}

export async function classifyVideoFailures(payload: {
  failures: any[];
}): Promise<any> {
  const res = await fetch(`${API_BASE}/video/failures`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to classify video failures");
  return res.json();
}

export async function evolveVideoPrompt(payload: {
  current_version?: string;
  prompt_text: string;
  failures: any[];
  target_model?: string;
  human_critique?: string;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/video/evolve`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to evolve video prompt");
  return res.json();
}

export async function fetchFailurePatterns(): Promise<any> {
  const res = await fetch(`${API_BASE}/video/failure-patterns`);
  if (!res.ok) throw new Error("Failed to fetch failure patterns");
  return res.json();
}

export async function fetchLearnedHeuristics(): Promise<any> {
  const res = await fetch(`${API_BASE}/video/learning`);
  if (!res.ok) throw new Error("Failed to fetch learned heuristics");
  return res.json();
}

export async function submitVideoFeedback(payload: {
  prompt_id: string;
  rating_stars: number;
  failure_tags: string[];
  critique?: string;
  what_to_change?: string;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/video/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) throw new Error("Failed to submit video feedback");
  return res.json();
}


