import React, { useState } from "react";
import { Topic } from "../types";

interface TrendRadarViewProps {
  trends: Topic[];
  isLoading: boolean;
  onSelectTrend: (trendId: string) => void;
  onRefresh: () => void;
}

export const TrendRadarView: React.FC<TrendRadarViewProps> = ({
  trends,
  isLoading,
  onSelectTrend,
  onRefresh,
}) => {
  const [selectedLifecycle, setSelectedLifecycle] = useState<string>("ALL");
  const [sortBy, setSortBy] = useState<"opportunity" | "momentum" | "competition">("opportunity");

  const filterTrends = trends.filter((t) => {
    if (selectedLifecycle === "ALL") return true;
    return (t.lifecycle_stage || "").toUpperCase() === selectedLifecycle;
  });

  const sortedTrends = [...filterTrends].sort((a, b) => {
    if (sortBy === "momentum") {
      return (b.momentum || 0) - (a.momentum || 0);
    }
    if (sortBy === "competition") {
      return (a.competition_score || 0) - (b.competition_score || 0); // lowest competition first
    }
    return (b.opportunity_score || 0) - (a.opportunity_score || 0);
  });

  return (
    <div className="space-y-6">
      {/* Filter and Control Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-xl bg-zinc-900/60 border border-zinc-800">
        <div className="flex flex-wrap items-center gap-1.5">
          {["ALL", "EXPLODING", "RISING", "EMERGING", "PEAK", "SATURATED"].map((stage) => (
            <button
              key={stage}
              onClick={() => setSelectedLifecycle(stage)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold tracking-wide transition-all cursor-pointer ${
                selectedLifecycle === stage
                  ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 shadow-sm"
                  : "bg-zinc-800/60 text-zinc-400 hover:text-zinc-200 border border-transparent"
              }`}
            >
              {stage}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <label className="text-xs text-zinc-400 font-medium">Sort By:</label>
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as any)}
            className="px-3 py-1.5 rounded-lg text-xs font-medium bg-zinc-800 border border-zinc-700 text-zinc-200 focus:outline-none focus:border-cyan-500 cursor-pointer"
          >
            <option value="opportunity">Opportunity Score</option>
            <option value="momentum">Highest Momentum</option>
            <option value="competition">Lowest Competition</option>
          </select>

          <button
            onClick={onRefresh}
            disabled={isLoading}
            className="p-1.5 rounded-lg bg-zinc-800 hover:bg-zinc-700 text-zinc-300 border border-zinc-700 transition-colors cursor-pointer"
            title="Refresh Trends"
          >
            <svg className={`h-4 w-4 ${isLoading ? "animate-spin" : ""}`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>
        </div>
      </div>

      {/* Trends Grid */}
      {sortedTrends.length === 0 ? (
        <div className="text-center py-16 px-4 rounded-xl border border-zinc-800 bg-zinc-900/40">
          <p className="text-zinc-400">No trends match the selected filter.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {sortedTrends.map((trend) => {
            const oppScore = trend.opportunity_score || 70;
            const compScore = trend.competition_score || 40;
            const momScore = trend.momentum || 60;
            const momChange = trend.momentum_change_pct || 0;

            return (
              <div
                key={trend.id}
                onClick={() => onSelectTrend(trend.id)}
                className="group flex flex-col justify-between p-5 rounded-xl border border-zinc-800 bg-zinc-900/50 hover:bg-zinc-800/40 hover:border-cyan-500/40 transition-all cursor-pointer shadow-lg hover:shadow-cyan-950/20"
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span className="text-[11px] font-semibold px-2 py-0.5 rounded-md bg-zinc-800 text-zinc-400">
                      {trend.category}
                    </span>
                    <span className="text-[11px] font-bold px-2 py-0.5 rounded-md bg-zinc-800/90 text-zinc-300 border border-zinc-700">
                      {trend.status}
                    </span>
                  </div>

                  <h4 className="text-base font-bold text-white group-hover:text-cyan-300 transition-colors line-clamp-2">
                    {trend.name}
                  </h4>

                  <p className="text-xs text-zinc-400 mt-2 line-clamp-2">
                    {trend.recommended_angle || "Strategic angle available in trend deep dive."}
                  </p>
                </div>

                <div className="mt-4 pt-4 border-t border-zinc-800/60 space-y-3">
                  <div className="grid grid-cols-3 gap-2 text-center">
                    <div className="p-2 rounded-lg bg-zinc-950/50 border border-zinc-800/60">
                      <div className="text-[9px] uppercase font-semibold text-zinc-500">Opportunity</div>
                      <div className="text-sm font-bold text-cyan-400">{oppScore}</div>
                    </div>

                    <div className="p-2 rounded-lg bg-zinc-950/50 border border-zinc-800/60">
                      <div className="text-[9px] uppercase font-semibold text-zinc-500">Momentum</div>
                      <div className="text-sm font-bold text-emerald-400">
                        {momChange >= 0 ? `+${momChange}%` : `${momChange}%`}
                      </div>
                    </div>

                    <div className="p-2 rounded-lg bg-zinc-950/50 border border-zinc-800/60">
                      <div className="text-[9px] uppercase font-semibold text-zinc-500">Competition</div>
                      <div className={`text-sm font-bold ${compScore <= 45 ? "text-emerald-400" : "text-amber-400"}`}>
                        {compScore}
                      </div>
                    </div>
                  </div>

                  <div className="flex items-center justify-between text-xs text-zinc-400 pt-1">
                    <span className="truncate max-w-[150px]">{trend.primary_audience || "AI Engineers"}</span>
                    <span className="font-semibold text-cyan-400 group-hover:translate-x-0.5 transition-transform flex items-center gap-1">
                      View Strategy →
                    </span>
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
