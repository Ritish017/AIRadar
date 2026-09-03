import React from "react";
import { ContentItem, Topic } from "../types";
import { TrendingUp, Flame, Award, Building2, Cpu, Wrench, ArrowUpRight } from "lucide-react";

interface OverviewViewProps {
  trendingItems: ContentItem[];
  topics: Topic[];
  onSelectContent: (item: ContentItem) => void;
}

const TOP_CREATORS = [
  { name: "Sam Altman", handle: "@sama", topic: "Frontier Models", impact: "High" },
  { name: "Andrej Karpathy", handle: "@karpathy", topic: "LLM Mechanics", impact: "Viral" },
  { name: "Jim Fan", handle: "@DrJimFan", topic: "Embodied AI & Robotics", impact: "High" },
  { name: "Yann LeCun", handle: "@ylecun", topic: "World Models", impact: "High" },
  { name: "Demis Hassabis", handle: "@demishassabis", topic: "AlphaFold & Gemini", impact: "Frontier" },
];

const TRENDING_ENTITIES = [
  { name: "OpenAI", type: "Company", metric: "3.8M weekly views", growth: "+310%" },
  { name: "DeepSeek", type: "Model/Lab", metric: "2.4M weekly views", growth: "+490%" },
  { name: "Anthropic", type: "Company", metric: "1.9M weekly views", growth: "+240%" },
  { name: "Figure AI", type: "Robotics", metric: "1.2M weekly views", growth: "+380%" },
  { name: "NVIDIA", type: "Hardware", metric: "4.1M weekly views", growth: "+180%" },
];

export const OverviewView: React.FC<OverviewViewProps> = ({
  trendingItems,
  topics,
  onSelectContent,
}) => {
  return (
    <div className="space-y-8">
      {/* Top Section: Exploding Topics & Viral Radar Leaders */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Exploding Topics Matrix */}
        <div className="lg:col-span-2 glass-panel rounded-2xl p-6 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
              <TrendingUp className="w-4 h-4 text-brand-400" />
              <span>Exploding AI Topics</span>
            </h3>
            <span className="text-xs text-slate-500">Cross-source momentum</span>
          </div>

          <div className="space-y-3">
            {topics.slice(0, 5).map((t) => (
              <div
                key={t.name}
                className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between hover:border-brand-500/30 transition"
              >
                <div>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm font-semibold text-white">{t.name}</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/15 text-rose-400 border border-rose-500/20">
                      {t.status}
                    </span>
                  </div>
                  <div className="flex items-center space-x-2 mt-1 text-[11px] text-slate-400">
                    <span>Category: {t.category}</span>
                    <span>•</span>
                    <span>Sources: {t.sources_summary.join(", ")}</span>
                  </div>
                </div>

                <div className="text-right">
                  <span className="text-sm font-extrabold text-amber-400">+{t.momentum}%</span>
                  <p className="text-[10px] text-slate-500">velocity growth</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top AI Creators */}
        <div className="glass-panel rounded-2xl p-6 border border-slate-800">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center space-x-2">
              <Award className="w-4 h-4 text-amber-400" />
              <span>Top AI Voices on X</span>
            </h3>
          </div>

          <div className="space-y-3">
            {TOP_CREATORS.map((c) => (
              <div
                key={c.handle}
                className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between"
              >
                <div>
                  <h4 className="text-xs font-bold text-white">{c.name}</h4>
                  <p className="text-[11px] text-slate-400">{c.handle} • {c.topic}</p>
                </div>
                <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-brand-500/20 text-brand-300">
                  {c.impact}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Trending Companies & Models */}
      <div className="glass-panel rounded-2xl p-6 border border-slate-800">
        <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-4 flex items-center space-x-2">
          <Building2 className="w-4 h-4 text-cyan-400" />
          <span>Trending Ecosystem Entities</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-5 gap-3">
          {TRENDING_ENTITIES.map((ent) => (
            <div
              key={ent.name}
              className="p-4 rounded-xl bg-slate-900/70 border border-slate-800 hover:border-slate-700 transition"
            >
              <span className="text-[11px] text-slate-500 uppercase font-semibold">{ent.type}</span>
              <h4 className="text-sm font-bold text-white mt-0.5">{ent.name}</h4>
              <div className="flex items-center justify-between mt-2 pt-2 border-t border-slate-800/80">
                <span className="text-[11px] text-slate-400">{ent.metric}</span>
                <span className="text-xs font-bold text-emerald-400">{ent.growth}</span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Top Viral Stories Leaderboard */}
      <div>
        <h3 className="text-sm font-bold text-white uppercase tracking-wider mb-4 flex items-center space-x-2">
          <Flame className="w-4 h-4 text-rose-500" />
          <span>Viral Radar Leaderboard</span>
        </h3>

        <div className="space-y-2.5">
          {trendingItems.slice(0, 5).map((item, idx) => (
            <div
              key={item.id}
              onClick={() => onSelectContent(item)}
              className="glass-card rounded-xl p-4 flex items-center justify-between cursor-pointer group border border-slate-800 hover:border-brand-500/40"
            >
              <div className="flex items-center space-x-4">
                <span className="w-6 text-center font-extrabold text-sm text-slate-500 group-hover:text-brand-400">
                  #{idx + 1}
                </span>
                <div>
                  <h4 className="text-sm font-semibold text-white group-hover:text-brand-300 transition-colors">
                    {item.title}
                  </h4>
                  <p className="text-xs text-slate-400 mt-0.5">
                    {item.source} • {item.author || item.source_type}
                  </p>
                </div>
              </div>

              <div className="flex items-center space-x-4">
                <div className="text-right">
                  <span className="text-xs font-extrabold text-rose-400 bg-rose-500/10 px-2 py-0.5 rounded border border-rose-500/20">
                    Score {Math.round(item.viral_score)}
                  </span>
                </div>
                <ArrowUpRight className="w-4 h-4 text-slate-500 group-hover:text-brand-400 transition" />
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
