import React, { useState, useEffect } from "react";
import { 
  ShieldCheck, CheckCircle2, Clock, AlertCircle, ExternalLink, 
  Sparkles, Video, Share2, Filter, Layers, Zap, ArrowUpRight, 
  Flame, RefreshCw, Eye, Film
} from "lucide-react";
import { V3Event } from "../types";

interface LiveRadarViewProps {
  onOpenContentStudio: (event: V3Event) => void;
  onOpenPromptLab: (event: V3Event) => void;
  onOpenEventDetail?: (event: V3Event) => void;
  onOpenVideoDirector?: (event: V3Event) => void;
}

export const LiveRadarView: React.FC<LiveRadarViewProps> = ({
  onOpenContentStudio,
  onOpenPromptLab,
  onOpenEventDetail,
  onOpenVideoDirector
}) => {
  const [events, setEvents] = useState<V3Event[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [statusFilter, setStatusFilter] = useState<string>("ALL");
  const [categoryFilter, setCategoryFilter] = useState<string>("ALL");
  const [searchQuery, setSearchQuery] = useState<string>("");

  const fetchEvents = async () => {
    setLoading(true);
    try {
      const params = new URLSearchParams();
      if (statusFilter !== "ALL") params.append("status", statusFilter);
      if (categoryFilter !== "ALL") params.append("category", categoryFilter);
      if (searchQuery) params.append("search", searchQuery);

      const res = await fetch(`/api/events?${params.toString()}`);
      if (res.ok) {
        const data = await res.json();
        setEvents(data.events || []);
      }
    } catch (err) {
      console.error("Failed to load events", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEvents();
    const interval = setInterval(fetchEvents, 20000); // Polling every 20s
    return () => clearInterval(interval);
  }, [statusFilter, categoryFilter, searchQuery]);

  const getStatusBadge = (status: string, confidence: number) => {
    switch (status) {
      case "CONFIRMED":
        return (
          <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-950/80 text-emerald-400 border border-emerald-500/40 font-mono">
            <ShieldCheck className="w-3.5 h-3.5" />
            CONFIRMED ({confidence}%)
          </span>
        );
      case "LIKELY":
        return (
          <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-sky-950/80 text-sky-400 border border-sky-500/40 font-mono">
            <CheckCircle2 className="w-3.5 h-3.5" />
            LIKELY ({confidence}%)
          </span>
        );
      case "DEVELOPING":
        return (
          <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-amber-950/80 text-amber-400 border border-amber-500/40 font-mono">
            <Clock className="w-3.5 h-3.5" />
            DEVELOPING
          </span>
        );
      default:
        return (
          <span className="flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-slate-800 text-slate-400 border border-slate-700 font-mono">
            <Eye className="w-3.5 h-3.5" />
            UNVERIFIED
          </span>
        );
    }
  };

  const getActionBadge = (action: string) => {
    switch (action) {
      case "POST_NOW":
        return <span className="bg-rose-500/20 text-rose-300 border border-rose-500/40 px-2 py-0.5 rounded text-[11px] font-bold font-mono">🔥 POST NOW</span>;
      case "POST_SOON":
        return <span className="bg-amber-500/20 text-amber-300 border border-amber-500/40 px-2 py-0.5 rounded text-[11px] font-bold font-mono">⚡ POST SOON</span>;
      default:
        return <span className="bg-slate-800 text-slate-400 px-2 py-0.5 rounded text-[11px] font-mono">WATCH</span>;
    }
  };

  return (
    <div className="space-y-5 pb-12">
      {/* Control Header & Filters */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 bg-[#0d121f] border border-slate-800/80 p-4 rounded-xl">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-black text-white tracking-tight flex items-center gap-2">
              <Zap className="w-5 h-5 text-amber-400" />
              Real-Time Global AI Radar
            </h1>
            <span className="bg-amber-500/20 text-amber-400 border border-amber-500/30 text-[10px] px-2 py-0.5 rounded font-mono font-bold">
              ZERO-COPY CANONICAL CLUSTERS
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Corroborated AI developments clustered across official labs, tech press, ArXiv, and community signals.
          </p>
        </div>

        {/* Filter Controls */}
        <div className="flex items-center gap-2.5 flex-wrap">
          <div className="flex items-center bg-slate-900 border border-slate-700/80 rounded-lg p-0.5 text-xs">
            {["ALL", "CONFIRMED", "DEVELOPING"].map((st) => (
              <button
                key={st}
                onClick={() => setStatusFilter(st)}
                className={`px-3 py-1 rounded-md font-mono transition ${
                  statusFilter === st 
                    ? "bg-slate-700 text-white font-bold" 
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {st}
              </button>
            ))}
          </div>

          <button
            onClick={fetchEvents}
            className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition"
            title="Refresh Live Radar"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? "animate-spin text-amber-400" : ""}`} />
          </button>
        </div>
      </div>

      {/* Events Grid */}
      {loading && events.length === 0 ? (
        <div className="flex flex-col items-center justify-center p-16 bg-[#0d121f]/50 border border-slate-800 rounded-xl">
          <RefreshCw className="w-8 h-8 text-amber-400 animate-spin mb-3" />
          <p className="text-sm text-slate-300 font-mono">Synthesizing live canonical intelligence from web acquisition layers...</p>
        </div>
      ) : events.length === 0 ? (
        <div className="text-center p-16 bg-[#0d121f]/50 border border-slate-800 rounded-xl">
          <p className="text-slate-400">No events matching the active filter criteria.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-4">
          {events.map((ev) => (
            <div
              key={ev.id}
              className="bg-[#0e1322] border border-slate-800 hover:border-slate-700/80 rounded-xl p-5 transition hover:shadow-xl hover:shadow-sky-950/20 relative group"
            >
              {/* Card Header: Category + Status + Latency Badge */}
              <div className="flex flex-wrap items-center justify-between gap-2 mb-3">
                <div className="flex items-center gap-2">
                  <span className="bg-violet-950/80 text-violet-300 border border-violet-700/40 text-[11px] font-mono px-2.5 py-0.5 rounded font-semibold">
                    {ev.category}
                  </span>
                  {getStatusBadge(ev.status, ev.confidence_score)}
                  {getActionBadge(ev.recommended_action)}
                </div>

                <div className="flex items-center gap-3 text-xs font-mono text-slate-400">
                  <span className="flex items-center gap-1" title="Time to Radar: pipeline latency">
                    <Zap className="w-3.5 h-3.5 text-amber-400" />
                    <span className="text-slate-500">Radar Latency:</span>
                    <span className="text-amber-300 font-bold">{ev.total_pipeline_latency || 28}s</span>
                  </span>
                  <span className="text-slate-600">|</span>
                  <span>{new Date(ev.event_timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                </div>
              </div>

              {/* Title & Summary */}
              <h2 
                onClick={() => onOpenEventDetail && onOpenEventDetail(ev)}
                className="text-lg font-bold text-white group-hover:text-amber-300 transition cursor-pointer leading-snug mb-2"
              >
                {ev.title}
              </h2>
              <p className="text-sm text-slate-300 leading-relaxed mb-4">
                {ev.summary}
              </p>

              {/* Verified Sources Pill Row */}
              <div className="flex flex-wrap items-center gap-2 mb-4">
                <span className="text-xs text-slate-500 font-mono font-medium flex items-center gap-1">
                  <Layers className="w-3.5 h-3.5" />
                  Corroborating Sources ({ev.source_count}):
                </span>
                {ev.sources && ev.sources.map((src, i) => (
                  <a
                    key={i}
                    href={src.url}
                    target="_blank"
                    rel="noreferrer"
                    className="flex items-center gap-1 bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-2 py-0.5 rounded text-[11px] font-mono transition"
                  >
                    <span>{src.source_name}</span>
                    <span className="text-[9px] text-slate-500">({src.quality_tier})</span>
                    <ArrowUpRight className="w-2.5 h-2.5 text-slate-500" />
                  </a>
                ))}
              </div>

              {/* Key Claims & Opportunity Guidance */}
              {ev.recommended_angle && (
                <div className="bg-[#121829] border border-slate-800/80 rounded-lg p-3 mb-4 flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-xs">
                  <div>
                    <span className="text-slate-400 font-mono">Recommended Angle: </span>
                    <span className="text-slate-200 font-semibold">{ev.recommended_angle}</span>
                  </div>
                  <span className="text-violet-400 font-mono text-[11px] self-start sm:self-auto">
                    Platform Fit: {ev.recommended_platform || "X"}
                  </span>
                </div>
              )}

              {/* Action Bar */}
              <div className="flex items-center justify-between pt-3 border-t border-slate-800/60 flex-wrap gap-2">
                <div className="flex items-center gap-4 text-xs font-mono text-slate-400">
                  <span>Viral Potential: <strong className="text-white">{ev.momentum_score}/100</strong></span>
                  <span>Opportunity: <strong className="text-emerald-400">{ev.opportunity_score}/100</strong></span>
                </div>

                <div className="flex items-center gap-2.5">
                  <button
                    onClick={() => onOpenVideoDirector ? onOpenVideoDirector(ev) : onOpenPromptLab(ev)}
                    className="flex items-center gap-1.5 bg-indigo-950/80 hover:bg-indigo-900 text-indigo-300 border border-indigo-700/60 px-3 py-1.5 rounded-lg text-xs font-semibold transition"
                    title="Open V3.2 AI Video Creative Director & Prompt Compiler"
                  >
                    <Film className="w-3.5 h-3.5 text-amber-400" />
                    <span>Video Director</span>
                  </button>

                  <button
                    onClick={() => onOpenPromptLab(ev)}
                    className="flex items-center gap-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-3 py-1.5 rounded-lg text-xs font-semibold transition"
                    title="Generate Omni, Remotion, or HyperFrames video prompt"
                  >
                    <Video className="w-3.5 h-3.5 text-rose-400" />
                    <span>Prompt Lab</span>
                  </button>

                  <button
                    onClick={() => onOpenContentStudio(ev)}
                    className="flex items-center gap-1.5 bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-400 hover:to-orange-500 text-black font-bold px-3.5 py-1.5 rounded-lg text-xs transition shadow-md shadow-amber-500/10"
                    title="Open Content Factory: Pre-Generation Brief, 10 Hooks, X, LinkedIn, Instagram, YouTube"
                  >
                    <Sparkles className="w-3.5 h-3.5 text-black" />
                    <span>Content Factory</span>
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
