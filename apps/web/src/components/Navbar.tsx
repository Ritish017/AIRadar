import React from "react";
import { 
  Flame, RefreshCw, Bookmark, Mic, Globe, Radio, 
  Zap, Activity, Share2, Sparkles, SlidersHorizontal, Film
} from "lucide-react";

export type V3NavTab = "radar" | "news" | "graph" | "opportunities" | "video" | "voice" | "saved";

interface NavbarProps {
  activeTab: V3NavTab;
  setActiveTab: (tab: V3NavTab) => void;
  savedCount: number;
  onRefresh: () => void;
  onWhatShouldIPost: () => void;
  isRefreshing: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  savedCount,
  onRefresh,
  onWhatShouldIPost,
  isRefreshing,
}) => {
  return (
    <nav className="border-b border-slate-800 bg-[#090d16]/95 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between gap-2">
        {/* Brand */}
        <div className="flex items-center space-x-3 shrink-0">
          <div className="h-8 w-8 rounded-lg bg-gradient-to-tr from-amber-500 via-rose-500 to-indigo-600 p-0.5 shadow-md flex items-center justify-center">
            <div className="w-full h-full bg-[#090d16] rounded-[6px] flex items-center justify-center">
              <Zap className="w-4 h-4 text-amber-400" />
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <span className="font-black text-sm tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
              AI VIRAL RADAR
            </span>
            <span className="inline-flex items-center px-1.5 py-0.2 rounded text-[10px] font-mono font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">
              V3 OS
            </span>
          </div>
        </div>

        {/* Center Navigation Tabs */}
        <div className="flex items-center space-x-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800 overflow-x-auto text-xs">
          <button
            onClick={() => setActiveTab("radar")}
            className={`px-3 py-1.5 rounded-lg font-mono font-semibold flex items-center space-x-1.5 transition ${
              activeTab === "radar"
                ? "bg-amber-500/20 text-amber-300 border border-amber-500/40"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Zap className="w-3.5 h-3.5 text-amber-400" />
            <span>Live Radar</span>
          </button>

          <button
            onClick={() => setActiveTab("news")}
            className={`px-3 py-1.5 rounded-lg font-mono font-semibold flex items-center space-x-1.5 transition ${
              activeTab === "news"
                ? "bg-sky-500/20 text-sky-300 border border-sky-500/40"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Globe className="w-3.5 h-3.5 text-sky-400" />
            <span>Global News</span>
          </button>

          <button
            onClick={() => setActiveTab("graph")}
            className={`px-3 py-1.5 rounded-lg font-mono font-semibold flex items-center space-x-1.5 transition ${
              activeTab === "graph"
                ? "bg-violet-500/20 text-violet-300 border border-violet-500/40"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Share2 className="w-3.5 h-3.5 text-violet-400" />
            <span>Trend Graph</span>
          </button>

          <button
            onClick={() => setActiveTab("opportunities")}
            className={`px-3 py-1.5 rounded-lg font-mono font-semibold flex items-center space-x-1.5 transition ${
              activeTab === "opportunities"
                ? "bg-rose-500/20 text-rose-300 border border-rose-500/40"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Flame className="w-3.5 h-3.5 text-rose-400" />
            <span>Opportunities</span>
          </button>

          <button
            onClick={() => setActiveTab("video")}
            className={`px-3 py-1.5 rounded-lg font-mono font-semibold flex items-center space-x-1.5 transition ${
              activeTab === "video"
                ? "bg-amber-500/20 text-amber-300 border border-amber-500/40"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Film className="w-3.5 h-3.5 text-amber-400" />
            <span>Video Director</span>
          </button>

          <button
            onClick={() => setActiveTab("voice")}
            className={`px-3 py-1.5 rounded-lg font-mono font-semibold flex items-center space-x-1.5 transition ${
              activeTab === "voice"
                ? "bg-indigo-500/20 text-indigo-300 border border-indigo-500/40"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Mic className="w-3.5 h-3.5 text-indigo-400" />
            <span>My Voice & Learning</span>
          </button>

          <button
            onClick={() => setActiveTab("saved")}
            className={`px-3 py-1.5 rounded-lg font-mono font-semibold flex items-center space-x-1.5 transition relative ${
              activeTab === "saved"
                ? "bg-slate-700 text-white"
                : "text-slate-400 hover:text-slate-200"
            }`}
          >
            <Bookmark className="w-3.5 h-3.5" />
            <span>Saved</span>
            {savedCount > 0 && (
              <span className="ml-1 px-1.5 py-0.2 rounded-full text-[10px] bg-amber-400 text-black font-bold">
                {savedCount}
              </span>
            )}
          </button>
        </div>

        {/* Action Button: WHAT SHOULD I POST? */}
        <div className="flex items-center space-x-2 shrink-0">
          <button
            onClick={onWhatShouldIPost}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-bold text-black bg-gradient-to-r from-amber-400 to-orange-500 hover:from-amber-300 hover:to-orange-400 shadow-md transition cursor-pointer"
          >
            <Sparkles className="w-3.5 h-3.5 text-black" />
            <span>What Should I Post?</span>
          </button>
        </div>
      </div>
    </nav>
  );
};
