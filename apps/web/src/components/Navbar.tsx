import React from "react";
import { Flame, RefreshCw, Bookmark, Mic, LayoutGrid, Radio, Zap, Activity } from "lucide-react";

interface NavbarProps {
  activeTab: "opportunities" | "radar" | "feed" | "overview" | "saved" | "voice";
  setActiveTab: (tab: "opportunities" | "radar" | "feed" | "overview" | "saved" | "voice") => void;
  savedCount: number;
  onRefresh: () => void;
  onWhatShouldIPost: () => void;
  isRefreshing: boolean;
  isDemoMode?: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  savedCount,
  onRefresh,
  onWhatShouldIPost,
  isRefreshing,
  isDemoMode = true,
}) => {
  return (
    <header className="sticky top-0 z-40 border-b border-slate-800/80 glass-panel">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-2">
        {/* Brand & Tagline */}
        <div className="flex items-center space-x-3 shrink-0">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-indigo-600 p-0.5 shadow-lg shadow-cyan-500/20 flex items-center justify-center">
            <div className="w-full h-full bg-[#090d16] rounded-[10px] flex items-center justify-center">
              <Zap className="w-5 h-5 text-cyan-400" />
            </div>
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-white via-slate-100 to-slate-400 bg-clip-text text-transparent">
                AI VIRAL RADAR
              </span>
              <span className="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-semibold bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                V2 ENGINE
              </span>
            </div>
            <p className="text-xs text-slate-400 hidden sm:block">
              Trend Intelligence & Content Opportunity Engine
            </p>
          </div>
        </div>

        {/* Center Navigation Tabs */}
        <nav className="flex items-center space-x-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800 overflow-x-auto">
          <button
            onClick={() => setActiveTab("opportunities")}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center space-x-1.5 transition-all cursor-pointer ${
              activeTab === "opportunities"
                ? "bg-gradient-to-r from-cyan-500 to-blue-600 text-white shadow-sm"
                : "text-slate-300 hover:text-white hover:bg-slate-800/60"
            }`}
          >
            <Zap className="w-3.5 h-3.5 text-amber-300" />
            <span>⚡ Opportunities</span>
          </button>

          <button
            onClick={() => setActiveTab("radar")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition-all cursor-pointer ${
              activeTab === "radar"
                ? "bg-cyan-600 text-white shadow-sm"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
            }`}
          >
            <Activity className="w-3.5 h-3.5" />
            <span>Trend Radar</span>
          </button>

          <button
            onClick={() => setActiveTab("feed")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition-all cursor-pointer ${
              activeTab === "feed"
                ? "bg-cyan-600 text-white shadow-sm"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
            }`}
          >
            <Radio className="w-3.5 h-3.5" />
            <span>Feed</span>
          </button>

          <button
            onClick={() => setActiveTab("saved")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition-all relative cursor-pointer ${
              activeTab === "saved"
                ? "bg-cyan-600 text-white shadow-sm"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
            }`}
          >
            <Bookmark className="w-3.5 h-3.5" />
            <span>Saved</span>
            {savedCount > 0 && (
              <span className="ml-1 px-1.5 py-0.2 rounded-full text-[10px] bg-cyan-400 text-dark-900 font-bold">
                {savedCount}
              </span>
            )}
          </button>

          <button
            onClick={() => setActiveTab("voice")}
            className={`px-3 py-1.5 rounded-lg text-xs font-medium flex items-center space-x-1.5 transition-all cursor-pointer ${
              activeTab === "voice"
                ? "bg-cyan-600 text-white shadow-sm"
                : "text-slate-400 hover:text-slate-200 hover:bg-slate-800/60"
            }`}
          >
            <Mic className="w-3.5 h-3.5" />
            <span>My Voice</span>
          </button>
        </nav>

        {/* Right Prominent Action Button: WHAT SHOULD I POST? */}
        <div className="flex items-center space-x-2 shrink-0">
          <button
            onClick={onWhatShouldIPost}
            className="flex items-center space-x-1.5 px-3.5 py-1.5 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-amber-500 via-rose-500 to-indigo-600 hover:from-amber-400 hover:to-indigo-500 shadow-md shadow-rose-500/20 transition-all cursor-pointer animate-pulse"
          >
            <Zap className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">⚡ WHAT SHOULD I POST?</span>
            <span className="sm:hidden">⚡ POST?</span>
          </button>

          <button
            onClick={onRefresh}
            disabled={isRefreshing}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-xl text-xs font-semibold bg-slate-800/80 hover:bg-slate-700/80 text-slate-300 border border-slate-700/60 transition shadow-sm cursor-pointer"
            title="Sync Sources"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? "animate-spin text-cyan-400" : ""}`} />
            <span className="hidden md:inline">Sync</span>
          </button>
        </div>
      </div>
    </header>
  );
};
