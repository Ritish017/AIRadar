import React from "react";
import { Zap, TrendingUp, Radio, Cpu, Sparkles } from "lucide-react";

interface MetricStripProps {
  totalItems: number;
  explodingCount: number;
  avgVelocity: number;
  sourcesCount: number;
}

export const MetricStrip: React.FC<MetricStripProps> = ({
  totalItems,
  explodingCount,
  avgVelocity,
  sourcesCount,
}) => {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
      <div className="glass-panel rounded-xl p-3.5 flex items-center space-x-3">
        <div className="p-2.5 rounded-lg bg-rose-500/15 text-rose-400 border border-rose-500/20">
          <Zap className="w-4 h-4" />
        </div>
        <div>
          <p className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">
            Tracked AI Items
          </p>
          <div className="flex items-baseline space-x-1.5">
            <span className="text-xl font-bold text-white tracking-tight">{totalItems}</span>
            <span className="text-[11px] text-emerald-400 font-medium">Live</span>
          </div>
        </div>
      </div>

      <div className="glass-panel rounded-xl p-3.5 flex items-center space-x-3">
        <div className="p-2.5 rounded-lg bg-brand-500/15 text-brand-400 border border-brand-500/20">
          <TrendingUp className="w-4 h-4" />
        </div>
        <div>
          <p className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">
            Exploding Topics
          </p>
          <div className="flex items-baseline space-x-1.5">
            <span className="text-xl font-bold text-white tracking-tight">{explodingCount}</span>
            <span className="text-[11px] text-brand-400 font-medium">+340% avg</span>
          </div>
        </div>
      </div>

      <div className="glass-panel rounded-xl p-3.5 flex items-center space-x-3">
        <div className="p-2.5 rounded-lg bg-amber-500/15 text-amber-400 border border-amber-500/20">
          <Sparkles className="w-4 h-4" />
        </div>
        <div>
          <p className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">
            Peak Velocity
          </p>
          <div className="flex items-baseline space-x-1.5">
            <span className="text-xl font-bold text-white tracking-tight">+{avgVelocity}%</span>
            <span className="text-[11px] text-amber-400 font-medium">acceleration</span>
          </div>
        </div>
      </div>

      <div className="glass-panel rounded-xl p-3.5 flex items-center space-x-3">
        <div className="p-2.5 rounded-lg bg-cyan-500/15 text-cyan-400 border border-cyan-500/20">
          <Radio className="w-4 h-4" />
        </div>
        <div>
          <p className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">
            Multi-Source Feeds
          </p>
          <div className="flex items-baseline space-x-1.5">
            <span className="text-xl font-bold text-white tracking-tight">{sourcesCount}</span>
            <span className="text-[11px] text-cyan-400 font-medium">Active</span>
          </div>
        </div>
      </div>
    </div>
  );
};
