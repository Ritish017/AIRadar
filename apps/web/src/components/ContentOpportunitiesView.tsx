import React from "react";
import { OpportunityCard } from "../types";

interface ContentOpportunitiesViewProps {
  opportunities: OpportunityCard[];
  isLoading: boolean;
  onRefresh: () => void;
  onSelectOpportunity: (opportunity: OpportunityCard) => void;
  onViewTrendDetail: (trendId: string) => void;
}

export const ContentOpportunitiesView: React.FC<ContentOpportunitiesViewProps> = ({
  opportunities,
  isLoading,
  onRefresh,
  onSelectOpportunity,
  onViewTrendDetail,
}) => {
  const getRankBadge = (rank: number) => {
    if (rank === 1) return { label: "🥇 1ST OPPORTUNITY", color: "border-amber-500/40 bg-amber-500/10 text-amber-300" };
    if (rank === 2) return { label: "🥈 2ND OPPORTUNITY", color: "border-slate-400/40 bg-slate-400/10 text-slate-200" };
    if (rank === 3) return { label: "🥉 3RD OPPORTUNITY", color: "border-amber-700/40 bg-amber-700/10 text-amber-400" };
    return { label: `#${rank} OPPORTUNITY`, color: "border-zinc-700 bg-zinc-800/60 text-zinc-400" };
  };

  const getActionColor = (action: string) => {
    switch (action) {
      case "POST_NOW":
        return "bg-emerald-500/20 text-emerald-300 border-emerald-500/50";
      case "POST_SOON":
        return "bg-cyan-500/20 text-cyan-300 border-cyan-500/50";
      case "WATCH":
        return "bg-amber-500/20 text-amber-300 border-amber-500/50";
      case "WAIT":
        return "bg-purple-500/20 text-purple-300 border-purple-500/50";
      default:
        return "bg-zinc-700/40 text-zinc-400 border-zinc-700";
    }
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 p-6 rounded-2xl bg-gradient-to-r from-cyan-950/40 via-zinc-900 to-indigo-950/40 border border-cyan-500/20">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 text-xs font-semibold uppercase tracking-wider rounded-full bg-cyan-500/20 text-cyan-300 border border-cyan-500/40">
              ⚡ Trend Intelligence V2
            </span>
            <span className="text-xs text-zinc-400">Deterministic Opportunity Prioritization</span>
          </div>
          <h2 className="text-2xl font-bold text-white tracking-tight">
            What Should I Post Right Now?
          </h2>
          <p className="text-sm text-zinc-400 mt-1 max-w-2xl">
            Ranked by high momentum, technical novelty, audience fit, and competitive gap analysis. Zero fabricated virality guarantees.
          </p>
        </div>

        <button
          onClick={onRefresh}
          disabled={isLoading}
          className="flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl font-medium text-sm text-white bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 shadow-lg shadow-cyan-500/20 transition-all disabled:opacity-50 cursor-pointer"
        >
          {isLoading ? (
            <>
              <svg className="animate-spin h-4 w-4 text-white" viewBox="0 0 24 24" fill="none">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z" />
              </svg>
              <span>Analyzing Trends...</span>
            </>
          ) : (
            <>
              <span>⚡ Recalculate Opportunities</span>
            </>
          )}
        </button>
      </div>

      {/* Opportunities List */}
      {opportunities.length === 0 ? (
        <div className="text-center py-16 px-4 rounded-2xl border border-zinc-800 bg-zinc-900/40">
          <p className="text-zinc-400 mb-3">No active opportunity trends detected yet.</p>
          <button
            onClick={onRefresh}
            className="px-4 py-2 text-xs font-medium text-cyan-400 bg-cyan-950/40 border border-cyan-800 rounded-lg hover:bg-cyan-900/50"
          >
            Trigger Ingestion & Opportunity Analysis
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          {opportunities.map((opp) => {
            const rankBadge = getRankBadge(opp.rank);
            const actionStyle = getActionColor(opp.recommended_action);

            return (
              <div
                key={opp.id}
                className="relative rounded-2xl border border-zinc-800/80 bg-zinc-900/70 backdrop-blur-md overflow-hidden hover:border-cyan-500/40 transition-all p-6 shadow-xl"
              >
                {/* Top Badge & Metric Bar */}
                <div className="flex flex-wrap items-center justify-between gap-3 mb-4 pb-4 border-b border-zinc-800/60">
                  <div className="flex items-center gap-2.5">
                    <span className={`px-2.5 py-1 text-xs font-bold rounded-lg border ${rankBadge.color}`}>
                      {rankBadge.label}
                    </span>
                    <span className="px-2 py-0.5 text-xs font-medium rounded-md bg-zinc-800 text-zinc-300">
                      {opp.category}
                    </span>
                    <span className="px-2 py-0.5 text-xs font-semibold rounded-md bg-zinc-800/90 text-zinc-200 border border-zinc-700">
                      {opp.lifecycle_badge}
                    </span>
                  </div>

                  {/* Timing Action Badge */}
                  <div className={`px-3 py-1 text-xs font-bold rounded-full border ${actionStyle} flex items-center gap-1.5`}>
                    <span>{opp.recommended_action.replace("_", " ")}</span>
                  </div>
                </div>

                {/* Main Content Area */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* Left Column: Title, Scores & Metrics */}
                  <div className="lg:col-span-2 space-y-4">
                    <div>
                      <h3 className="text-xl font-bold text-white group-hover:text-cyan-300 transition-colors">
                        {opp.topic}
                      </h3>
                      <p className="text-xs text-zinc-400 mt-1 italic">
                        "{opp.action_reason}"
                      </p>
                    </div>

                    {/* Metric Cards Grid */}
                    <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                      <div className="p-3 rounded-xl bg-zinc-950/60 border border-zinc-800">
                        <div className="text-[10px] uppercase font-semibold text-zinc-500 tracking-wider">Opportunity</div>
                        <div className="text-lg font-bold text-cyan-400">{opp.opportunity_score} <span className="text-xs text-zinc-500">/100</span></div>
                        <div className="text-[10px] text-zinc-400">{opp.opportunity_type.replace("_", " ")}</div>
                      </div>

                      <div className="p-3 rounded-xl bg-zinc-950/60 border border-zinc-800">
                        <div className="text-[10px] uppercase font-semibold text-zinc-500 tracking-wider">Momentum</div>
                        <div className="text-lg font-bold text-emerald-400">
                          {opp.momentum_change_pct >= 0 ? `+${opp.momentum_change_pct}%` : `${opp.momentum_change_pct}%`}
                        </div>
                        <div className="text-[10px] text-zinc-400">{opp.momentum_direction}</div>
                      </div>

                      <div className="p-3 rounded-xl bg-zinc-950/60 border border-zinc-800">
                        <div className="text-[10px] uppercase font-semibold text-zinc-500 tracking-wider">Competition</div>
                        <div className={`text-lg font-bold ${opp.competition <= 45 ? "text-emerald-400" : opp.competition <= 70 ? "text-amber-400" : "text-rose-400"}`}>
                          {opp.competition} <span className="text-xs text-zinc-500">/100</span>
                        </div>
                        <div className="text-[10px] text-zinc-400">{opp.competition <= 45 ? "Low White-space" : "Crowded"}</div>
                      </div>

                      <div className="p-3 rounded-xl bg-zinc-950/60 border border-zinc-800">
                        <div className="text-[10px] uppercase font-semibold text-zinc-500 tracking-wider">Audience Fit</div>
                        <div className="text-lg font-bold text-indigo-400">{opp.audience_fit} <span className="text-xs text-zinc-500">/100</span></div>
                        <div className="text-[10px] text-zinc-400 truncate">{opp.primary_audience}</div>
                      </div>
                    </div>

                    {/* Recommended Angle Callout */}
                    <div className="p-4 rounded-xl bg-cyan-950/20 border border-cyan-500/30">
                      <div className="flex items-center justify-between mb-1.5">
                        <span className="text-xs font-semibold text-cyan-300 uppercase tracking-wider flex items-center gap-1.5">
                          <span>🎯 Recommended High-Leverage Angle</span>
                        </span>
                        <span className="text-[10px] text-zinc-400">Gaps in existing coverage</span>
                      </div>
                      <p className="text-sm text-zinc-200 font-medium">
                        "{opp.recommended_angle}"
                      </p>
                      {opp.alternative_angles && opp.alternative_angles.length > 0 && (
                        <div className="mt-2.5 pt-2 border-t border-cyan-500/20">
                          <span className="text-[11px] text-zinc-400 font-medium">Alternative Angle: </span>
                          <span className="text-xs text-zinc-300">{opp.alternative_angles[0]}</span>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Right Column: Tactical Guidance & Actions */}
                  <div className="flex flex-col justify-between p-4 rounded-xl bg-zinc-950/40 border border-zinc-800/80 space-y-4">
                    <div className="space-y-3">
                      <div>
                        <span className="text-[10px] uppercase font-semibold text-zinc-500 tracking-wider">Hook Strategy ({opp.recommended_hook})</span>
                        <p className="text-xs text-zinc-300 mt-0.5">
                          {opp.hook_strategy}
                        </p>
                      </div>

                      <div>
                        <span className="text-[10px] uppercase font-semibold text-zinc-500 tracking-wider">Recommended Format</span>
                        <div className="flex items-center gap-2 mt-1">
                          <span className="px-2.5 py-1 text-xs font-semibold rounded-md bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 capitalize">
                            {opp.recommended_format.replace("_", " ")}
                          </span>
                          <span className="text-xs text-zinc-400">
                            Confidence: {opp.format_scores?.[opp.recommended_format] || 90}%
                          </span>
                        </div>
                      </div>

                      <div>
                        <span className="text-[10px] uppercase font-semibold text-zinc-500 tracking-wider">Target Persona</span>
                        <p className="text-xs text-zinc-300 mt-0.5 font-medium">
                          {opp.primary_audience}
                        </p>
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="space-y-2 pt-2">
                      <button
                        onClick={() => onSelectOpportunity(opp)}
                        className="w-full flex items-center justify-center gap-2 py-2.5 px-4 rounded-xl font-semibold text-xs text-white bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 transition-all shadow-md shadow-cyan-500/20 cursor-pointer"
                      >
                        <span>🚀 Create Post With This Angle</span>
                      </button>

                      <button
                        onClick={() => onViewTrendDetail(opp.id)}
                        className="w-full flex items-center justify-center gap-2 py-2 px-4 rounded-xl font-medium text-xs text-zinc-300 bg-zinc-800/80 hover:bg-zinc-700/80 border border-zinc-700 transition-all cursor-pointer"
                      >
                        <span>🔍 Deep-Dive Trend Strategy</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
