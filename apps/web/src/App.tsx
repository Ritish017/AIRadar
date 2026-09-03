import React, { useState, useEffect } from "react";
import { ContentItem, Topic, SavedItem, Analysis, OpportunityCard, TrendDetail } from "./types";
import {
  fetchFeed,
  fetchTrending,
  fetchTopics,
  fetchSavedItems,
  saveStory,
  deleteSavedItem,
  triggerCollection,
  fetchTopOpportunities,
  fetchTrends,
} from "./lib/api";
import { Navbar } from "./components/Navbar";
import { MetricStrip } from "./components/MetricStrip";
import { FilterBar } from "./components/FilterBar";
import { ContentCard } from "./components/ContentCard";
import { AnalysisModal } from "./components/AnalysisModal";
import { PostStudioModal } from "./components/PostStudioModal";
import { SavedBoard } from "./components/SavedBoard";
import { VoiceProfileView } from "./components/VoiceProfileModal";
import { ContentOpportunitiesView } from "./components/ContentOpportunitiesView";
import { TrendRadarView } from "./components/TrendRadarView";
import { TrendDetailModal } from "./components/TrendDetailModal";
import { AlertCircle, Zap, Flame } from "lucide-react";

export function App() {
  const [activeTab, setActiveTab] = useState<"opportunities" | "radar" | "feed" | "overview" | "saved" | "voice">("opportunities");

  // Data states
  const [opportunities, setOpportunities] = useState<OpportunityCard[]>([]);
  const [trends, setTrends] = useState<Topic[]>([]);
  const [items, setItems] = useState<ContentItem[]>([]);
  const [totalItems, setTotalItems] = useState<number>(0);
  const [trendingItems, setTrendingItems] = useState<ContentItem[]>([]);
  const [savedItems, setSavedItems] = useState<SavedItem[]>([]);

  // Filter states
  const [selectedTopic, setSelectedTopic] = useState<string>("All");
  const [selectedSort, setSelectedSort] = useState<string>("viral");
  const [selectedTime, setSelectedTime] = useState<string>("all");

  // UI state
  const [loading, setLoading] = useState<boolean>(true);
  const [opportunitiesLoading, setOpportunitiesLoading] = useState<boolean>(false);
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // Modals state
  const [analyzingItem, setAnalyzingItem] = useState<ContentItem | null>(null);
  const [studioItem, setStudioItem] = useState<ContentItem | null>(null);
  const [studioAnalysis, setStudioAnalysis] = useState<Analysis | undefined>(undefined);
  const [studioInitialAngle, setStudioInitialAngle] = useState<string | undefined>(undefined);
  const [studioInitialHook, setStudioInitialHook] = useState<string | undefined>(undefined);
  const [selectedTrendDetailId, setSelectedTrendDetailId] = useState<string | null>(null);

  // Initial load
  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      const [oppData, trendsList, feedData, trendData, savedList] = await Promise.all([
        fetchTopOpportunities(5),
        fetchTrends("opportunity"),
        fetchFeed({
          topic: selectedTopic === "All" ? undefined : selectedTopic,
          sortBy: selectedSort,
          timeRange: selectedTime,
          page: 1,
          pageSize: 24,
        }),
        fetchTrending(),
        fetchSavedItems(),
      ]);

      setOpportunities(oppData.top_opportunities || []);
      setTrends(trendsList || []);
      setItems(feedData.items);
      setTotalItems(feedData.total);
      setTrendingItems(trendData.trending_items);
      setSavedItems(savedList);
    } catch (err: any) {
      console.error("Error loading dashboard data:", err);
      setError(err.message || "Failed to connect to AI Viral Radar backend");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [selectedTopic, selectedSort, selectedTime]);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    try {
      await triggerCollection();
      await loadData();
    } catch (err) {
      console.error("Manual sync failed:", err);
    } finally {
      setIsRefreshing(false);
    }
  };

  const handleWhatShouldIPost = async () => {
    setActiveTab("opportunities");
    setOpportunitiesLoading(true);
    try {
      const oppData = await fetchTopOpportunities(5);
      setOpportunities(oppData.top_opportunities || []);
    } catch (err) {
      console.error("Failed to re-fetch opportunities:", err);
    } finally {
      setOpportunitiesLoading(false);
    }
  };

  const handleSaveItem = async (item: ContentItem) => {
    try {
      const saved = await saveStory(item.id, "Idea");
      setSavedItems((prev) => [saved, ...prev.filter((s) => s.content_item_id !== item.id)]);
    } catch (err) {
      console.error("Failed to save story:", err);
    }
  };

  const handleDeleteSaved = async (id: string) => {
    try {
      await deleteSavedItem(id);
      setSavedItems((prev) => prev.filter((s) => s.id !== id));
    } catch (err) {
      console.error("Failed to delete saved story:", err);
    }
  };

  const handleUpdateSavedStatus = async (item: SavedItem, newStatus: "Idea" | "Draft" | "Posted" | "Ignored") => {
    try {
      const updated = await saveStory(item.content_item_id, newStatus, item.notes);
      setSavedItems((prev) => prev.map((s) => (s.id === item.id ? updated : s)));
    } catch (err) {
      console.error("Failed to update status:", err);
    }
  };

  // Bridge from Opportunity Card to Post Studio
  const handleSelectOpportunity = (opp: OpportunityCard) => {
    // Find matching content item or create surrogate item for Post Studio
    const matchingItem = items.find((it) => it.topic.toLowerCase() === opp.topic.toLowerCase()) || items[0] || {
      id: opp.id,
      title: opp.topic,
      content: opp.recommended_angle,
      url: opp.primary_source || "https://news.ycombinator.com",
      source: "AI Viral Radar",
      source_type: "firecrawl",
      published_at: new Date().toISOString(),
      collected_at: new Date().toISOString(),
      viral_score: opp.opportunity_score,
      viral_potential: opp.opportunity_score,
      trend_score: opp.momentum,
      topic: opp.topic,
      entities: [],
      sentiment: "positive",
      content_type: "release",
      hook_type: opp.recommended_hook,
      media: [],
      hashtags: [],
      language: "en",
      engagement_velocity: opp.momentum,
      source_urls: [],
      attribution_required: true,
    };

    setStudioItem(matchingItem);
    setStudioInitialAngle(opp.recommended_angle);
    setStudioInitialHook(opp.recommended_hook);
  };

  // Bridge from Trend Detail to Post Studio
  const handleCreatePostFromTrend = (trend: TrendDetail) => {
    const matchingItem = items.find((it) => it.topic.toLowerCase() === trend.name.toLowerCase()) || items[0] || {
      id: trend.id,
      title: trend.name,
      content: trend.best_angle,
      url: trend.source_evidence?.[0]?.url || "https://news.ycombinator.com",
      source: "AI Viral Radar",
      source_type: "firecrawl",
      published_at: new Date().toISOString(),
      collected_at: new Date().toISOString(),
      viral_score: trend.opportunity_score,
      viral_potential: trend.opportunity_score,
      trend_score: trend.momentum,
      topic: trend.name,
      entities: [],
      sentiment: "positive",
      content_type: "release",
      hook_type: trend.best_hook_type,
      media: [],
      hashtags: [],
      language: "en",
      engagement_velocity: trend.momentum,
      source_urls: [],
      attribution_required: true,
    };

    setStudioItem(matchingItem);
    setStudioInitialAngle(trend.best_angle);
    setStudioInitialHook(trend.best_hook_type);
  };

  const savedIds = new Set(savedItems.map((s) => s.content_item_id));

  return (
    <div className="min-h-screen bg-[#070a12] text-slate-100 flex flex-col font-sans selection:bg-cyan-500/30 selection:text-cyan-200">
      {/* Top Navigation Bar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        savedCount={savedItems.length}
        onRefresh={handleRefresh}
        onWhatShouldIPost={handleWhatShouldIPost}
        isRefreshing={isRefreshing}
        isDemoMode={true}
      />

      {/* Main Workspace Canvas */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {/* Metric Strip */}
        <MetricStrip
          totalItems={totalItems || items.length}
          explodingCount={trends.filter((t) => t.momentum > 200).length || 3}
          avgVelocity={340}
          sourcesCount={7}
        />

        {/* Global Error Banner */}
        {error && (
          <div className="p-4 rounded-xl bg-rose-500/15 border border-rose-500/30 text-rose-200 mb-6 flex items-center justify-between">
            <div className="flex items-center space-x-2.5">
              <AlertCircle className="w-5 h-5 text-rose-400 flex-shrink-0" />
              <span className="text-xs">{error}</span>
            </div>
            <button
              onClick={loadData}
              className="px-3 py-1 bg-rose-500/20 hover:bg-rose-500/30 rounded-lg text-xs font-semibold cursor-pointer"
            >
              Retry
            </button>
          </div>
        )}

        {/* TAB 1: CONTENT OPPORTUNITIES (WHAT SHOULD I POST?) */}
        {activeTab === "opportunities" && (
          <ContentOpportunitiesView
            opportunities={opportunities}
            isLoading={opportunitiesLoading || loading}
            onRefresh={handleWhatShouldIPost}
            onSelectOpportunity={handleSelectOpportunity}
            onViewTrendDetail={(id) => setSelectedTrendDetailId(id)}
          />
        )}

        {/* TAB 2: TREND RADAR */}
        {activeTab === "radar" && (
          <TrendRadarView
            trends={trends}
            isLoading={loading}
            onSelectTrend={(id) => setSelectedTrendDetailId(id)}
            onRefresh={loadData}
          />
        )}

        {/* TAB 3: RADAR FEED */}
        {activeTab === "feed" && (
          <div>
            <FilterBar
              selectedTopic={selectedTopic}
              onSelectTopic={setSelectedTopic}
              selectedSort={selectedSort}
              onSelectSort={setSelectedSort}
              selectedTime={selectedTime}
              onSelectTime={setSelectedTime}
            />

            {loading ? (
              <div className="py-24 text-center space-y-3">
                <div className="inline-block animate-spin text-cyan-400">
                  <Flame className="w-8 h-8" />
                </div>
                <p className="text-sm font-semibold text-slate-300">Scanning multi-source viral AI feeds...</p>
                <p className="text-xs text-slate-500">Calculating engagement velocity and freshness decay</p>
              </div>
            ) : items.length === 0 ? (
              <div className="glass-panel rounded-2xl p-16 text-center space-y-3 border border-slate-800">
                <Flame className="w-10 h-10 text-slate-600 mx-auto" />
                <h3 className="text-sm font-semibold text-slate-300">No stories found matching filters</h3>
                <p className="text-xs text-slate-400 max-w-sm mx-auto">
                  Try adjusting the category or time range filters above to view more items.
                </p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                {items.map((item) => (
                  <ContentCard
                    key={item.id}
                    item={item}
                    onAnalyze={(it) => setAnalyzingItem(it)}
                    onCreatePost={(it) => {
                      setStudioItem(it);
                      setStudioAnalysis(it.analysis);
                      setStudioInitialAngle(undefined);
                      setStudioInitialHook(undefined);
                    }}
                    onSave={handleSaveItem}
                    isSaved={savedIds.has(item.id)}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {/* TAB 4: SAVED STORIES */}
        {activeTab === "saved" && (
          <SavedBoard
            items={savedItems}
            onDelete={handleDeleteSaved}
            onUpdateStatus={handleUpdateSavedStatus}
            onOpenStudio={(it) => {
              setStudioItem(it);
              setStudioAnalysis(it.analysis);
              setStudioInitialAngle(undefined);
              setStudioInitialHook(undefined);
            }}
          />
        )}

        {/* TAB 5: VOICE PROFILE */}
        {activeTab === "voice" && <VoiceProfileView />}
      </main>

      {/* Modals & Strategic Drawers */}
      {analyzingItem && (
        <AnalysisModal
          item={analyzingItem}
          onClose={() => setAnalyzingItem(null)}
          onOpenStudio={(it, analysis) => {
            setAnalyzingItem(null);
            setStudioItem(it);
            setStudioAnalysis(analysis);
            setStudioInitialAngle(undefined);
            setStudioInitialHook(undefined);
          }}
        />
      )}

      {studioItem && (
        <PostStudioModal
          item={studioItem}
          analysis={studioAnalysis}
          initialAngle={studioInitialAngle}
          initialHook={studioInitialHook}
          onClose={() => {
            setStudioItem(null);
            setStudioAnalysis(undefined);
            setStudioInitialAngle(undefined);
            setStudioInitialHook(undefined);
          }}
        />
      )}

      {selectedTrendDetailId && (
        <TrendDetailModal
          trendId={selectedTrendDetailId}
          onClose={() => setSelectedTrendDetailId(null)}
          onCreatePostFromTrend={handleCreatePostFromTrend}
        />
      )}
    </div>
  );
}
export default App;
