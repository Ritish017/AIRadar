import React from "react";
import { Filter, ArrowUpDown, Clock } from "lucide-react";

interface FilterBarProps {
  selectedTopic: string;
  onSelectTopic: (topic: string) => void;
  selectedSort: string;
  onSelectSort: (sort: string) => void;
  selectedTime: string;
  onSelectTime: (time: string) => void;
}

const TOPICS = [
  "All",
  "Models",
  "Agents",
  "Research",
  "Startups",
  "Robotics",
  "Coding",
  "Open Source",
  "AI Tools",
  "Companies"
];

const SORTS = [
  { id: "viral", label: "🔥 Viral Score" },
  { id: "rising", label: "⚡ Rising Velocity" },
  { id: "newest", label: "⏱ Newest" },
  { id: "engagement", label: "📈 Engagement Rate" },
  { id: "velocity", label: "🚀 Acceleration" },
];

const TIMES = [
  { id: "15m", label: "15m" },
  { id: "1h", label: "1h" },
  { id: "6h", label: "6h" },
  { id: "24h", label: "24h" },
  { id: "7d", label: "7d" },
  { id: "all", label: "All time" },
];

export const FilterBar: React.FC<FilterBarProps> = ({
  selectedTopic,
  onSelectTopic,
  selectedSort,
  onSelectSort,
  selectedTime,
  onSelectTime,
}) => {
  return (
    <div className="space-y-3 mb-6">
      {/* Category Pills */}
      <div className="flex items-center space-x-1.5 overflow-x-auto pb-1 scrollbar-none">
        {TOPICS.map((topic) => {
          const isSelected = selectedTopic.toLowerCase() === topic.toLowerCase();
          return (
            <button
              key={topic}
              onClick={() => onSelectTopic(topic)}
              className={`px-3 py-1.5 rounded-full text-xs font-medium whitespace-nowrap transition-all ${
                isSelected
                  ? "bg-brand-500/20 text-brand-300 border border-brand-500/40 shadow-sm"
                  : "bg-slate-900/60 text-slate-400 hover:text-slate-200 hover:bg-slate-800/80 border border-slate-800/60"
              }`}
            >
              {topic}
            </button>
          );
        })}
      </div>

      {/* Sort & Time Controls */}
      <div className="flex flex-wrap items-center justify-between gap-3 pt-1 border-t border-slate-800/60">
        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-1.5 text-xs text-slate-400 font-medium">
            <ArrowUpDown className="w-3.5 h-3.5 text-slate-500" />
            <span>Sort:</span>
          </div>
          <div className="flex items-center space-x-1 bg-slate-900/80 p-0.5 rounded-lg border border-slate-800">
            {SORTS.map((s) => (
              <button
                key={s.id}
                onClick={() => onSelectSort(s.id)}
                className={`px-2.5 py-1 rounded-md text-[11px] font-medium transition ${
                  selectedSort === s.id
                    ? "bg-slate-800 text-white font-semibold"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {s.label}
              </button>
            ))}
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-1.5 text-xs text-slate-400 font-medium">
            <Clock className="w-3.5 h-3.5 text-slate-500" />
            <span>Time:</span>
          </div>
          <div className="flex items-center space-x-1 bg-slate-900/80 p-0.5 rounded-lg border border-slate-800">
            {TIMES.map((t) => (
              <button
                key={t.id}
                onClick={() => onSelectTime(t.id)}
                className={`px-2 py-1 rounded-md text-[11px] font-medium transition ${
                  selectedTime === t.id
                    ? "bg-brand-600/30 text-brand-300 font-semibold border border-brand-500/30"
                    : "text-slate-400 hover:text-slate-200"
                }`}
              >
                {t.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
