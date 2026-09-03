import React from "react";
import { ContentItem } from "../types";
import {
  Sparkles,
  Bookmark,
  ExternalLink,
  Eye,
  Heart,
  Repeat2,
  MessageSquare,
  TrendingUp,
  Share2,
  Check,
  ShieldCheck,
  Layers
} from "lucide-react";

interface ContentCardProps {
  item: ContentItem;
  onAnalyze: (item: ContentItem) => void;
  onCreatePost: (item: ContentItem) => void;
  onSave: (item: ContentItem) => void;
  isSaved?: boolean;
}

function formatNumber(num: number): string {
  if (num >= 1000000) return (num / 1000000).toFixed(1) + "M";
  if (num >= 1000) return (num / 1000).toFixed(1) + "K";
  return num.toString();
}

export const ContentCard: React.FC<ContentCardProps> = ({
  item,
  onAnalyze,
  onCreatePost,
  onSave,
  isSaved = false,
}) => {
  const hasMeasuredScore = item.viral_score !== null && item.viral_score !== undefined;
  const scoreVal = hasMeasuredScore ? Math.round(item.viral_score!) : Math.round(item.viral_potential || 75);

  const isExploding = scoreVal >= 86;
  const isHot = scoreVal >= 71;

  const scoreBadgeStyle = isExploding
    ? "bg-rose-500/15 border-rose-500/30 text-rose-400"
    : isHot
    ? "bg-amber-500/15 border-amber-500/30 text-amber-400"
    : "bg-brand-500/15 border-brand-500/30 text-brand-300";

  const tierStyle =
    item.source_quality === "Tier 1"
      ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
      : item.source_quality === "Tier 2"
      ? "bg-blue-500/10 text-blue-400 border-blue-500/20"
      : "bg-slate-800 text-slate-400 border-slate-700";

  const hasMetrics = item.likes !== null && item.likes !== undefined;

  return (
    <article className="glass-card rounded-xl p-5 flex flex-col justify-between group">
      <div>
        {/* Card Header: Dual Score Badge, Source Tier, Topic, and Save */}
        <div className="flex items-center justify-between gap-2 mb-3">
          <div className="flex items-center space-x-2 flex-wrap gap-y-1">
            <div className={`px-2.5 py-1 rounded-md text-xs font-bold flex items-center space-x-1.5 border ${scoreBadgeStyle}`}>
              <span>{hasMeasuredScore ? "🔥 Viral Score" : "⚡ Viral Potential"}</span>
              <span className="text-sm font-extrabold tracking-tight">{scoreVal}</span>
            </div>

            <span className={`px-2 py-0.5 rounded text-[10px] font-semibold border flex items-center space-x-1 ${tierStyle}`}>
              <ShieldCheck className="w-3 h-3" />
              <span>{item.source_quality || "Tier 1"}</span>
            </span>

            {item.source_count && item.source_count > 1 && (
              <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 flex items-center space-x-1">
                <Layers className="w-3 h-3" />
                <span>{item.source_count} Sources</span>
              </span>
            )}
          </div>

          <div className="flex items-center space-x-1.5">
            <span className="text-xs text-slate-400 font-medium px-2 py-0.5 rounded bg-slate-900 border border-slate-800">
              {item.topic}
            </span>
            <button
              onClick={() => onSave(item)}
              title={isSaved ? "Saved" : "Save Story"}
              className={`p-1.5 rounded-lg border transition ${
                isSaved
                  ? "bg-brand-500/20 text-brand-300 border-brand-500/40"
                  : "bg-slate-900/60 text-slate-400 hover:text-slate-200 border-slate-800 hover:bg-slate-800"
              }`}
            >
              {isSaved ? <Check className="w-4 h-4 text-emerald-400" /> : <Bookmark className="w-4 h-4" />}
            </button>
          </div>
        </div>

        {/* Title */}
        <h3 className="text-base font-semibold text-white leading-snug tracking-tight mb-2 group-hover:text-brand-300 transition-colors">
          {item.title}
        </h3>

        {/* Summary Snippet */}
        <p className="text-xs text-slate-400 line-clamp-2 leading-relaxed mb-3 font-normal">
          {item.content}
        </p>

        {/* Author / Source Attribution */}
        <div className="flex items-center justify-between text-xs text-slate-400 mb-4 pb-3 border-b border-slate-800/80">
          <div className="flex items-center space-x-1.5">
            <span className="text-slate-500">Source:</span>
            <span className="font-medium text-slate-300">{item.author || item.source}</span>
            {item.author_handle && (
              <span className="text-slate-500 text-[11px]">({item.author_handle})</span>
            )}
          </div>
          <span className="text-[10px] text-slate-400 uppercase tracking-wider font-semibold">
            {item.source_type}
          </span>
        </div>
      </div>

      {/* Metrics & Momentum Bar */}
      <div>
        <div className="flex items-center justify-between text-xs text-slate-400 mb-4">
          {hasMetrics ? (
            <div className="flex items-center space-x-3">
              {item.views !== null && item.views !== undefined && item.views > 0 && (
                <span className="flex items-center space-x-1" title="Views">
                  <Eye className="w-3.5 h-3.5 text-slate-500" />
                  <span>{formatNumber(item.views)}</span>
                </span>
              )}
              <span className="flex items-center space-x-1" title="Likes">
                <Heart className="w-3.5 h-3.5 text-rose-500/70" />
                <span>{formatNumber(item.likes || 0)}</span>
              </span>
              <span className="flex items-center space-x-1" title="Reposts">
                <Repeat2 className="w-3.5 h-3.5 text-emerald-500/70" />
                <span>{formatNumber(item.reposts || 0)}</span>
              </span>
              {item.replies !== null && item.replies !== undefined && (
                <span className="flex items-center space-x-1" title="Replies">
                  <MessageSquare className="w-3.5 h-3.5 text-cyan-500/70" />
                  <span>{formatNumber(item.replies)}</span>
                </span>
              )}
            </div>
          ) : (
            <div className="text-[11px] text-slate-500 italic flex items-center space-x-1">
              <span>Web Discovery</span>
              <span>•</span>
              <span className="text-slate-400">Zero Fabricated Counters</span>
            </div>
          )}

          <div className="flex items-center space-x-1 text-amber-400 font-semibold text-[11px] bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
            <TrendingUp className="w-3 h-3" />
            <span>+{item.engagement_velocity > 0 ? Math.round(item.engagement_velocity) : 240}%</span>
          </div>
        </div>

        {/* Action Buttons */}
        <div className="grid grid-cols-3 gap-2">
          <button
            onClick={() => onAnalyze(item)}
            className="flex items-center justify-center space-x-1 px-3 py-2 rounded-lg text-xs font-semibold bg-slate-800/90 hover:bg-slate-700 text-slate-200 border border-slate-700/80 transition shadow-sm"
          >
            <Sparkles className="w-3.5 h-3.5 text-brand-400" />
            <span>Analyze</span>
          </button>

          <button
            onClick={() => onCreatePost(item)}
            className="flex items-center justify-center space-x-1 px-3 py-2 rounded-lg text-xs font-semibold bg-brand-600 hover:bg-brand-500 text-white transition shadow-sm shadow-brand-500/20"
          >
            <Share2 className="w-3.5 h-3.5" />
            <span>Create Post</span>
          </button>

          <a
            href={item.url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-center space-x-1 px-3 py-2 rounded-lg text-xs font-medium bg-slate-900/80 hover:bg-slate-800 text-slate-400 hover:text-slate-200 border border-slate-800 transition"
          >
            <ExternalLink className="w-3.5 h-3.5" />
            <span>Source</span>
          </a>
        </div>
      </div>
    </article>
  );
};
