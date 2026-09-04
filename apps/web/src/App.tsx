import React, { useState, useEffect } from "react";
import { ContentItem, Topic, SavedItem, Analysis, OpportunityCard, V3Event, TrendDetail } from "./types";
import {
  fetchFeed,
  fetchTrending,
  fetchSavedItems,
  saveStory,
  deleteSavedItem,
  triggerCollection,
  fetchTopOpportunities,
  fetchTrends,
} from "./lib/api";
import { Navbar, V3NavTab } from "./components/Navbar";
import { TerminalStatusBar } from "./components/TerminalStatusBar";
import { LiveRadarView } from "./components/LiveRadarView";
import { GlobalNewsCenter } from "./components/GlobalNewsCenter";
import { TrendNetworkGraph } from "./components/TrendNetworkGraph";
import { ContentOpportunitiesView } from "./components/ContentOpportunitiesView";
import { SavedBoard } from "./components/SavedBoard";
import { VoiceLearningView } from "./components/VoiceLearningView";
import { ContentStudioV3 } from "./components/ContentStudioV3";
import { PromptLabModal } from "./components/PromptLabModal";
import { DailyBriefModal } from "./components/DailyBriefModal";
import { GlobalSearchModal } from "./components/GlobalSearchModal";
import { TrendDetailModal } from "./components/TrendDetailModal";
import { VideoDirectorStudio } from "./components/VideoDirectorStudio";
import { AlertCircle } from "lucide-react";

export function App() {
  const [activeTab, setActiveTab] = useState<V3NavTab>("radar");

  // V2/V3 Data states
  const [opportunities, setOpportunities] = useState<OpportunityCard[]>([]);
  const [trends, setTrends] = useState<Topic[]>([]);
  const [savedItems, setSavedItems] = useState<SavedItem[]>([]);

  // UI state
  const [loading, setLoading] = useState<boolean>(false);
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  // V3 Modals state
  const [studioEvent, setStudioEvent] = useState<V3Event | null>(null);
  const [promptLabEvent, setPromptLabEvent] = useState<V3Event | null>(null);
  const [videoDirectorEvent, setVideoDirectorEvent] = useState<V3Event | null>(null);
  const [isDailyBriefOpen, setIsDailyBriefOpen] = useState<boolean>(false);
  const [isSearchOpen, setIsSearchOpen] = useState<boolean>(false);
  const [selectedTrendDetailId, setSelectedTrendDetailId] = useState<string | null>(null);

  // Load Opportunities & Saved Items
  const loadInitialData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [oppData, trendsList, savedList] = await Promise.all([
        fetchTopOpportunities(5),
        fetchTrends("opportunity"),
        fetchSavedItems()
      ]);
      setOpportunities(oppData.top_opportunities || []);
      setTrends(trendsList || []);
      setSavedItems(savedList || []);
    } catch (err: any) {
      console.error("Initial load error:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadInitialData();

    // Keyboard shortcut '/' or 'Ctrl+K' to open global search
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "/" && !(e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement)) {
        e.preventDefault();
        setIsSearchOpen(true);
      }
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setIsSearchOpen(true);
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);

  const handleRefresh = async () => {
    setIsRefreshing(true);
    try {
      await triggerCollection();
      await loadInitialData();
    } catch (err) {
      console.error("Manual sync failed:", err);
    } finally {
      setIsRefreshing(false);
    }
  };

  const handleWhatShouldIPost = () => {
    setActiveTab("opportunities");
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

  // Convert news or opportunity surrogate to V3Event for Content Studio
  const handleOpenStudioForNews = (news: any) => {
    const ev: V3Event = {
      id: news.id,
      title: news.title,
      summary: news.content,
      category: news.category || "General AI",
      status: "CONFIRMED",
      confidence_score: 90.0,
      source_count: 1,
      independent_source_count: 1,
      primary_source_name: news.source,
      primary_source_url: news.url,
      entities: [],
      key_facts: news.confirmed_facts || [news.title],
      relevance_score: 85.0,
      freshness_score: 95.0,
      momentum_score: news.viral_potential || 80.0,
      opportunity_score: 75.0,
      recommended_action: "POST_NOW",
      recommended_angle: `Practical engineer takeaways from ${news.title}`,
      recommended_platform: "X",
      event_timestamp: news.published_at || new Date().toISOString(),
      first_seen_at: new Date().toISOString(),
      surfaced_at: new Date().toISOString(),
      total_pipeline_latency: 24.0,
      sources: [
        {
          source_name: news.source,
          url: news.url,
          quality_tier: news.source_quality || "Tier 1"
        }
      ]
    };
    setStudioEvent(ev);
  };

  const handleSelectOpportunity = (opp: OpportunityCard) => {
    const ev: V3Event = {
      id: opp.id,
      title: opp.topic,
      summary: `Trend opportunity in ${opp.category}: ${opp.recommended_angle}`,
      category: opp.category,
      status: "CONFIRMED",
      confidence_score: 88.0,
      source_count: opp.item_count || 3,
      independent_source_count: opp.sources_summary.length || 2,
      entities: [opp.topic],
      key_facts: [opp.recommended_angle, `Hook strategy: ${opp.hook_strategy}`],
      relevance_score: opp.audience_fit,
      freshness_score: opp.novelty,
      momentum_score: opp.momentum,
      opportunity_score: opp.opportunity_score,
      recommended_action: opp.recommended_action,
      recommended_angle: opp.recommended_angle,
      recommended_platform: "X",
      event_timestamp: new Date().toISOString(),
      first_seen_at: new Date().toISOString(),
      surfaced_at: new Date().toISOString(),
      total_pipeline_latency: 28.0,
      sources: opp.sources_summary.map((src) => ({
        source_name: src,
        url: opp.primary_source || "https://news.ycombinator.com",
        quality_tier: "Tier 1"
      }))
    };
    setStudioEvent(ev);
  };

  return (
    <div className="min-h-screen bg-[#06090f] text-slate-100 flex flex-col font-sans selection:bg-amber-500/30 selection:text-amber-200">
      {/* 1. Terminal Real-Time Top Status Bar */}
      <TerminalStatusBar
        onRefresh={handleRefresh}
        onOpenDailyBrief={() => setIsDailyBriefOpen(true)}
        onOpenSearch={() => setIsSearchOpen(true)}
      />

      {/* 2. Global Navigation Bar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        savedCount={savedItems.length}
        onRefresh={handleRefresh}
        onWhatShouldIPost={handleWhatShouldIPost}
        isRefreshing={isRefreshing}
      />

      {/* 3. Main Workspace Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {error && (
          <div className="mb-6 p-4 rounded-xl bg-rose-950/60 border border-rose-800 text-rose-300 text-xs flex items-center justify-between">
            <div className="flex items-center gap-2">
              <AlertCircle className="w-4 h-4 text-rose-400" />
              <span>{error}</span>
            </div>
            <button onClick={loadInitialData} className="underline hover:text-white font-mono">
              Retry Sync
            </button>
          </div>
        )}

        {/* TAB 1: LIVE RADAR (PRIMARY COMMAND CENTER) */}
        {activeTab === "radar" && (
          <LiveRadarView
            onOpenContentStudio={(ev) => setStudioEvent(ev)}
            onOpenPromptLab={(ev) => setPromptLabEvent(ev)}
            onOpenVideoDirector={(ev) => {
              setVideoDirectorEvent(ev);
              setActiveTab("video");
            }}
            onOpenEventDetail={(ev) => setSelectedTrendDetailId(ev.id)}
          />
        )}

        {/* TAB 2: GLOBAL AI NEWS (11 DOMAIN CATEGORIES) */}
        {activeTab === "news" && (
          <GlobalNewsCenter
            onOpenContentStudioForNews={handleOpenStudioForNews}
          />
        )}

        {/* TAB 3: TREND RELATIONSHIP GRAPH */}
        {activeTab === "graph" && (
          <TrendNetworkGraph
            onSelectTrendNode={(name) => {
              setActiveTab("opportunities");
            }}
          />
        )}

        {/* TAB 4: WHAT SHOULD I POST? / OPPORTUNITIES */}
        {activeTab === "opportunities" && (
          <ContentOpportunitiesView
            opportunities={opportunities}
            isLoading={loading}
            onRefresh={handleWhatShouldIPost}
            onSelectOpportunity={handleSelectOpportunity}
            onViewTrendDetail={(id) => setSelectedTrendDetailId(id)}
          />
        )}

        {/* TAB 5: VIDEO DIRECTOR (AI CREATIVE DIRECTOR V3.2) */}
        {activeTab === "video" && (
          <VideoDirectorStudio
            initialEvent={videoDirectorEvent}
          />
        )}

        {/* TAB 6: MY VOICE & LEARNING LOOP */}
        {activeTab === "voice" && <VoiceLearningView />}

        {/* TAB 7: SAVED STORIES */}
        {activeTab === "saved" && (
          <SavedBoard
            items={savedItems}
            onDelete={handleDeleteSaved}
            onUpdateStatus={handleUpdateSavedStatus}
            onOpenStudio={(it) => handleOpenStudioForNews(it)}
          />
        )}
      </main>

      {/* 4. MODALS & STUDIO DRAWERS */}
      {studioEvent && (
        <ContentStudioV3
          event={studioEvent}
          isOpen={!!studioEvent}
          onClose={() => setStudioEvent(null)}
          onAddToQueue={(qItem) => {
            fetch("/api/queue", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(qItem)
            });
            setStudioEvent(null);
          }}
        />
      )}

      {promptLabEvent && (
        <PromptLabModal
          event={promptLabEvent}
          isOpen={!!promptLabEvent}
          onClose={() => setPromptLabEvent(null)}
        />
      )}

      {isDailyBriefOpen && (
        <DailyBriefModal
          isOpen={isDailyBriefOpen}
          onClose={() => setIsDailyBriefOpen(false)}
          onOpenOpportunity={(id) => {
            setIsDailyBriefOpen(false);
            setSelectedTrendDetailId(id);
          }}
        />
      )}

      {isSearchOpen && (
        <GlobalSearchModal
          isOpen={isSearchOpen}
          onClose={() => setIsSearchOpen(false)}
          onSelectResult={(type, item) => {
            if (type === "event" || type === "news") {
              handleOpenStudioForNews(item);
            } else if (type === "trend") {
              setSelectedTrendDetailId(item.id);
            }
          }}
        />
      )}

      {selectedTrendDetailId && (
        <TrendDetailModal
          trendId={selectedTrendDetailId}
          onClose={() => setSelectedTrendDetailId(null)}
          onCreatePostFromTrend={(trend: TrendDetail) => {
            const ev: V3Event = {
              id: trend.id,
              title: trend.name,
              summary: trend.what_happened,
              category: trend.category || "AI Models",
              status: "CONFIRMED",
              confidence_score: 92.0,
              source_count: 4,
              independent_source_count: 3,
              entities: [trend.name],
              key_facts: [trend.best_angle, trend.timing_reason],
              relevance_score: trend.audience_fit_score || 85.0,
              freshness_score: trend.novelty_score || 80.0,
              momentum_score: trend.momentum || 80.0,
              opportunity_score: trend.opportunity_score || 85.0,
              recommended_action: "POST_NOW",
              recommended_angle: trend.best_angle,
              recommended_platform: "X",
              event_timestamp: new Date().toISOString(),
              first_seen_at: new Date().toISOString(),
              surfaced_at: new Date().toISOString(),
              total_pipeline_latency: 30.0,
              sources: []
            };
            setSelectedTrendDetailId(null);
            setStudioEvent(ev);
          }}
        />
      )}
    </div>
  );
}

export default App;
