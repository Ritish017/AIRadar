import {
  ContentItem, Analysis, GeneratedVariant, Topic, SavedItem, VoiceProfile,
  TopOpportunitiesResponse, TrendDetail
} from "../types";

const API_BASE = "http://127.0.0.1:8000/api";

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
