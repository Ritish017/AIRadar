import React, { useState } from "react";
import { SavedItem, ContentItem } from "../types";
import { Trash2, Edit3, ExternalLink, Bookmark, Check, Share2, Sparkles } from "lucide-react";

interface SavedBoardProps {
  items: SavedItem[];
  onDelete: (id: string) => void;
  onUpdateStatus: (item: SavedItem, newStatus: "Idea" | "Draft" | "Posted" | "Ignored") => void;
  onOpenStudio: (item: ContentItem) => void;
}

const STATUSES: Array<"Idea" | "Draft" | "Posted" | "Ignored"> = ["Idea", "Draft", "Posted", "Ignored"];

export const SavedBoard: React.FC<SavedBoardProps> = ({
  items,
  onDelete,
  onUpdateStatus,
  onOpenStudio,
}) => {
  const [selectedFilter, setSelectedFilter] = useState<string>("All");

  const filtered = selectedFilter === "All"
    ? items
    : items.filter((it) => it.status === selectedFilter);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-white tracking-tight">Saved Stories & Drafts</h2>
          <p className="text-xs text-slate-400">Track and organize curated AI stories through your editorial workflow</p>
        </div>

        <div className="flex items-center space-x-1 bg-slate-900/90 p-1 rounded-xl border border-slate-800">
          {["All", ...STATUSES].map((st) => (
            <button
              key={st}
              onClick={() => setSelectedFilter(st)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold transition ${
                selectedFilter === st
                  ? "bg-brand-600 text-white"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              {st}
            </button>
          ))}
        </div>
      </div>

      {filtered.length === 0 ? (
        <div className="glass-panel rounded-2xl p-16 text-center space-y-3">
          <Bookmark className="w-10 h-10 text-slate-600 mx-auto" />
          <h3 className="text-sm font-semibold text-slate-300">No stories saved in this status</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto">
            Browse the radar feed and click the bookmark icon on any viral AI announcement to save it here.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map((save) => {
            const content = save.content_item;
            if (!content) return null;

            return (
              <div key={save.id} className="glass-card rounded-xl p-5 flex flex-col justify-between space-y-3 border border-slate-800">
                <div>
                  <div className="flex items-center justify-between text-xs mb-2">
                    <select
                      value={save.status}
                      onChange={(e) => onUpdateStatus(save, e.target.value as any)}
                      className="bg-slate-900 text-xs font-semibold px-2 py-1 rounded border border-slate-700 text-brand-300 focus:outline-none"
                    >
                      {STATUSES.map((st) => (
                        <option key={st} value={st}>
                          {st}
                        </option>
                      ))}
                    </select>

                    <button
                      onClick={() => onDelete(save.id)}
                      className="p-1 rounded text-slate-500 hover:text-rose-400 transition"
                      title="Remove from saved"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>

                  <h3 className="text-sm font-semibold text-white line-clamp-2 mb-1.5">
                    {content.title}
                  </h3>
                  <p className="text-xs text-slate-400 line-clamp-2 mb-3">
                    {content.content}
                  </p>

                  {save.notes && (
                    <div className="p-2.5 rounded-lg bg-slate-900/80 border border-slate-800/80 text-[11px] text-amber-200/90 italic">
                      "{save.notes}"
                    </div>
                  )}
                </div>

                <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between">
                  <span className="text-[11px] text-slate-500">
                    Saved {new Date(save.saved_at).toLocaleDateString()}
                  </span>
                  <button
                    onClick={() => onOpenStudio(content)}
                    className="flex items-center space-x-1 px-3 py-1.5 rounded-lg text-xs font-bold bg-brand-600 hover:bg-brand-500 text-white transition shadow-sm"
                  >
                    <Share2 className="w-3.5 h-3.5" />
                    <span>Create Post</span>
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
