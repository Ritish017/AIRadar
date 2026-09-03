import React, { useState, useEffect } from "react";
import { TrendDetail } from "../types";
import { fetchTrendDetail, triggerTrendStrategy } from "../lib/api";

interface TrendDetailModalProps {
  trendId: string | null;
  onClose: () => void;
  onCreatePostFromTrend: (trend: TrendDetail) => void;
}

export const TrendDetailModal: React.FC<TrendDetailModalProps> = ({
  trendId,
  onClose,
  onCreatePostFromTrend,
}) => {
  const [detail, setDetail] = useState<TrendDetail | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [runningAI, setRunningAI] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!trendId) return;
    loadDetail();
  }, [trendId]);

  const loadDetail = async () => {
    if (!trendId) return;
    try {
      setLoading(true);
      setError(null);
      const data = await fetchTrendDetail(trendId);
      setDetail(data);
    } catch (err: any) {
      setError(err.message || "Failed to load trend detail");
    } finally {
      setLoading(false);
    }
  };

  const handleRunAIStrategist = async () => {
    if (!trendId) return;
    try {
      setRunningAI(true);
      await triggerTrendStrategy(trendId);
      await loadDetail();
    } catch (err: any) {
      alert("AI Strategy run notice: " + (err.message || "Request timed out"));
    } finally {
      setRunningAI(false);
    }
  };

  if (!trendId) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm overflow-y-auto">
      <div className="relative w-full max-w-4xl rounded-2xl border border-zinc-700 bg-zinc-900 shadow-2xl p-6 sm:p-8 max-h-[90vh] overflow-y-auto space-y-6">
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 p-2 rounded-lg text-zinc-400 hover:text-white hover:bg-zinc-800 transition-colors cursor-pointer"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>

        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 space-y-4">
            <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-cyan-400"></div>
            <p className="text-zinc-400 text-sm">Loading comprehensive trend intelligence...</p>
          </div>
        ) : error || !detail ? (
          <div className="text-center py-16 text-rose-400">
            <p>{error || "Trend data not found."}</p>
          </div>
        ) : (
          <>
            {/* Header / Title Banner */}
            <div>
              <div className="flex flex-wrap items-center gap-2 mb-2">
                <span className="px-2.5 py-0.5 text-xs font-semibold rounded-md bg-zinc-800 text-cyan-300 border border-zinc-700">
                  {detail.category}
                </span>
                <span className="px-2.5 py-0.5 text-xs font-bold rounded-md bg-zinc-800 text-zinc-200 border border-zinc-700">
                  {detail.status}
                </span>
                <span className="px-2.5 py-0.5 text-xs font-semibold rounded-md bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
                  {detail.timing_verdict.replace("_", " ")}
                </span>
              </div>

              <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
                {detail.name}
              </h2>

              {/* Key Metrics Bar */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4">
                <div className="p-3 rounded-xl bg-zinc-950/70 border border-zinc-800 text-center">
                  <div className="text-[10px] uppercase font-semibold text-zinc-500">Opportunity Score</div>
                  <div className="text-xl font-bold text-cyan-400">{detail.opportunity_score}/100</div>
                </div>
                <div className="p-3 rounded-xl bg-zinc-950/70 border border-zinc-800 text-center">
                  <div className="text-[10px] uppercase font-semibold text-zinc-500">Momentum</div>
                  <div className="text-xl font-bold text-emerald-400">
                    {detail.momentum_change_pct >= 0 ? `+${detail.momentum_change_pct}%` : `${detail.momentum_change_pct}%`}
                  </div>
                </div>
                <div className="p-3 rounded-xl bg-zinc-950/70 border border-zinc-800 text-center">
                  <div className="text-[10px] uppercase font-semibold text-zinc-500">Competition</div>
                  <div className={`text-xl font-bold ${detail.competition_score <= 45 ? "text-emerald-400" : "text-amber-400"}`}>
                    {detail.competition_score}/100
                  </div>
                </div>
                <div className="p-3 rounded-xl bg-zinc-950/70 border border-zinc-800 text-center">
                  <div className="text-[10px] uppercase font-semibold text-zinc-500">Audience Fit</div>
                  <div className="text-xl font-bold text-indigo-400">{detail.audience_fit_score}/100</div>
                </div>
              </div>
            </div>

            {/* Strategic Intelligence Sections (Prompt Section 19) */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* 1. What is Happening */}
              <div className="p-4 rounded-xl bg-zinc-950/40 border border-zinc-800/80 space-y-1">
                <h4 className="text-xs font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-1.5">
                  <span>📰 What Is Happening?</span>
                </h4>
                <p className="text-sm text-zinc-200">{detail.what_happened}</p>
              </div>

              {/* 2. Why is it Trending */}
              <div className="p-4 rounded-xl bg-zinc-950/40 border border-zinc-800/80 space-y-1">
                <h4 className="text-xs font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-1.5">
                  <span>🔥 Why Is It Trending?</span>
                </h4>
                <p className="text-sm text-zinc-200">{detail.why_trending}</p>
              </div>

              {/* 3. What Changed */}
              <div className="p-4 rounded-xl bg-zinc-950/40 border border-zinc-800/80 space-y-1">
                <h4 className="text-xs font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-1.5">
                  <span>⚡ What Changed Recently?</span>
                </h4>
                <p className="text-sm text-zinc-200">{detail.what_changed || "Inference economics and developer tooling support have accelerated."}</p>
              </div>

              {/* 4. Who Cares */}
              <div className="p-4 rounded-xl bg-zinc-950/40 border border-zinc-800/80 space-y-1">
                <h4 className="text-xs font-bold text-zinc-400 uppercase tracking-wider flex items-center gap-1.5">
                  <span>🎯 Who Cares? (Audience)</span>
                </h4>
                <p className="text-sm text-zinc-200">{detail.who_cares || detail.primary_audience || "AI Engineers and autonomous agent builders."}</p>
              </div>
            </div>

            {/* Angle & Saturation Analysis */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* What is Saturated */}
              <div className="p-4 rounded-xl bg-rose-950/10 border border-rose-500/20 space-y-2">
                <h4 className="text-xs font-bold text-rose-300 uppercase tracking-wider flex items-center gap-1.5">
                  <span>🛑 What Is Saturated (Avoid Posting This)</span>
                </h4>
                <p className="text-xs text-zinc-300">
                  {detail.what_is_saturated || "Generic press release reposts, marketing claims, and standard high-level summaries."}
                </p>
                {detail.saturated_angles && detail.saturated_angles.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    {detail.saturated_angles.map((ang, i) => (
                      <span key={i} className="text-[10px] px-2 py-0.5 rounded bg-rose-900/30 text-rose-300 border border-rose-800/40">
                        {ang}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* What is Missing */}
              <div className="p-4 rounded-xl bg-emerald-950/10 border border-emerald-500/20 space-y-2">
                <h4 className="text-xs font-bold text-emerald-300 uppercase tracking-wider flex items-center gap-1.5">
                  <span>✨ Under-Served White Space (Take This Angle)</span>
                </h4>
                <p className="text-xs text-zinc-300">
                  {detail.what_is_missing || "Real-world production failure modes, latency jitter benchmarks, and architectural cost comparisons."}
                </p>
                {detail.under_served_angles && detail.under_served_angles.length > 0 && (
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    {detail.under_served_angles.map((ang, i) => (
                      <span key={i} className="text-[10px] px-2 py-0.5 rounded bg-emerald-900/30 text-emerald-300 border border-emerald-800/40">
                        {ang}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Tactical Recommendations (Best Angle, Hook, Format) */}
            <div className="p-5 rounded-xl bg-gradient-to-br from-cyan-950/30 via-zinc-900 to-indigo-950/30 border border-cyan-500/30 space-y-4">
              <div>
                <span className="text-xs font-bold text-cyan-300 uppercase tracking-wider">
                  🏆 Recommended High-Leverage Angle
                </span>
                <p className="text-sm font-semibold text-white mt-1">
                  "{detail.best_angle}"
                </p>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2 border-t border-cyan-500/20 text-xs">
                <div>
                  <span className="text-zinc-400 font-semibold uppercase tracking-wider text-[10px]">
                    Hook Strategy ({detail.best_hook_type})
                  </span>
                  <p className="text-zinc-200 mt-0.5">{detail.hook_strategy}</p>
                </div>

                <div>
                  <span className="text-zinc-400 font-semibold uppercase tracking-wider text-[10px]">
                    Post Timing & Reason ({detail.timing_verdict})
                  </span>
                  <p className="text-zinc-200 mt-0.5">{detail.timing_reason}</p>
                </div>
              </div>
            </div>

            {/* Traceable Source Evidence (Section 20) */}
            <div className="p-4 rounded-xl bg-zinc-950/60 border border-zinc-800 space-y-3">
              <h4 className="text-xs font-bold text-zinc-400 uppercase tracking-wider">
                🔗 Traceable Source Evidence
              </h4>
              {detail.source_evidence && detail.source_evidence.length > 0 ? (
                <div className="space-y-2">
                  {detail.source_evidence.map((src, i) => (
                    <div key={i} className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 p-2.5 rounded-lg bg-zinc-900/80 border border-zinc-800 text-xs">
                      <div className="truncate max-w-lg">
                        <span className="font-semibold text-zinc-200">{src.title}</span>
                        <div className="text-zinc-500 text-[11px] truncate">{src.url}</div>
                      </div>
                      <div className="flex items-center gap-2 shrink-0">
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-cyan-950 text-cyan-300 border border-cyan-800">
                          {src.source_quality}
                        </span>
                        <a
                          href={src.url}
                          target="_blank"
                          rel="noreferrer"
                          className="text-cyan-400 hover:underline text-[11px] font-medium"
                        >
                          Visit Source ↗
                        </a>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-zinc-500 italic">No secondary sources registered yet.</p>
              )}
            </div>

            {/* Bottom Actions */}
            <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-4 border-t border-zinc-800">
              <button
                onClick={handleRunAIStrategist}
                disabled={runningAI}
                className="w-full sm:w-auto px-4 py-2.5 rounded-xl text-xs font-semibold text-zinc-300 bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 transition-colors flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
              >
                {runningAI ? "Gemini Strategist Running..." : "⚡ Run Gemini AI Strategist"}
              </button>

              <button
                onClick={() => {
                  onClose();
                  onCreatePostFromTrend(detail);
                }}
                className="w-full sm:w-auto px-6 py-2.5 rounded-xl text-xs font-bold text-white bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 shadow-lg shadow-cyan-500/25 transition-all flex items-center justify-center gap-2 cursor-pointer"
              >
                <span>🚀 Create Post in Post Studio</span>
              </button>
            </div>
          </>
        )}
      </div>
    </div>
  );
};
