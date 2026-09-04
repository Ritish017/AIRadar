import React, { useState, useEffect } from "react";
import { 
  X, Clock, Calendar, CheckCircle2, Flame, Sparkles, 
  ArrowRight, Copy, RefreshCw, ListFilter, Send
} from "lucide-react";
import { DailyBrief, DayPlanSlot, ContentQueueItem } from "../types";

interface DailyBriefModalProps {
  isOpen: boolean;
  onClose: () => void;
  onOpenOpportunity?: (trendId: string) => void;
}

export const DailyBriefModal: React.FC<DailyBriefModalProps> = ({
  isOpen,
  onClose,
  onOpenOpportunity
}) => {
  const [brief, setBrief] = useState<DailyBrief | null>(null);
  const [plan, setPlan] = useState<DayPlanSlot[]>([]);
  const [queue, setQueue] = useState<ContentQueueItem[]>([]);
  const [activeTab, setActiveTab] = useState<"brief" | "plan" | "queue">("brief");
  const [loading, setLoading] = useState<boolean>(true);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [bRes, pRes, qRes] = await Promise.all([
        fetch("/api/brief/daily"),
        fetch("/api/plan-day"),
        fetch("/api/queue")
      ]);

      if (bRes.ok) setBrief(await bRes.json());
      if (pRes.ok) {
        const pd = await pRes.json();
        setPlan(pd.schedule || []);
      }
      if (qRes.ok) {
        const qd = await qRes.json();
        setQueue(qd.items || []);
      }
    } catch (err) {
      console.error("Failed to fetch workflow data", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen) fetchData();
  }, [isOpen]);

  if (!isOpen) return null;

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/85 backdrop-blur-md overflow-y-auto">
      <div className="bg-[#090d16] border border-slate-700 rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="p-4 sm:p-5 border-b border-slate-800 flex items-center justify-between bg-[#0e1322]">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-indigo-500/20 border border-indigo-500/30">
              <Clock className="w-5 h-5 text-indigo-400" />
            </div>
            <div>
              <h2 className="text-base sm:text-lg font-black text-white flex items-center gap-2">
                Executive Daily Briefing & Day Planner
              </h2>
              <p className="text-xs text-slate-400">
                Automated synthesis: "What happened while I was away?" & scheduled 5-slot calendar.
              </p>
            </div>
          </div>

          <button onClick={onClose} className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab Selector */}
        <div className="bg-[#0b0f19] px-5 py-2 border-b border-slate-800 flex items-center gap-2 text-xs">
          <button
            onClick={() => setActiveTab("brief")}
            className={`px-3 py-1.5 rounded-lg font-mono font-semibold transition ${
              activeTab === "brief" ? "bg-indigo-950 text-indigo-300 border border-indigo-800" : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Daily Briefing
          </button>

          <button
            onClick={() => setActiveTab("plan")}
            className={`px-3 py-1.5 rounded-lg font-mono font-semibold transition ${
              activeTab === "plan" ? "bg-indigo-950 text-indigo-300 border border-indigo-800" : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Plan My Day (5 Slots)
          </button>

          <button
            onClick={() => setActiveTab("queue")}
            className={`px-3 py-1.5 rounded-lg font-mono font-semibold transition ${
              activeTab === "queue" ? "bg-indigo-950 text-indigo-300 border border-indigo-800" : "text-slate-400 hover:text-slate-200"
            }`}
          >
            Content Queue ({queue.length})
          </button>
        </div>

        {/* Body */}
        <div className="flex-1 overflow-y-auto p-5 space-y-5">
          {loading ? (
            <div className="py-20 text-center space-y-3">
              <RefreshCw className="w-8 h-8 text-indigo-400 animate-spin mx-auto" />
              <p className="text-xs font-mono text-slate-400">Synthesizing executive briefing from global intelligence feed...</p>
            </div>
          ) : (
            <>
              {/* TAB 1: EXECUTIVE BRIEF */}
              {activeTab === "brief" && brief && (
                <div className="space-y-5">
                  <div className="bg-[#0e1322] border border-slate-800 rounded-xl p-5 space-y-3">
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-mono text-indigo-400 font-bold uppercase">
                        EXECUTIVE SUMMARY: WHAT HAPPENED WHILE I WAS AWAY?
                      </span>
                      <span className="text-[11px] font-mono text-slate-500">
                        {new Date(brief.generated_at).toLocaleDateString()}
                      </span>
                    </div>
                    <p className="text-sm text-slate-200 leading-relaxed">{brief.summary}</p>
                  </div>

                  {/* Directive */}
                  <div className="bg-gradient-to-r from-indigo-950/60 to-purple-950/60 border border-indigo-500/40 rounded-xl p-4 flex items-start gap-3">
                    <Sparkles className="w-5 h-5 text-indigo-400 shrink-0 mt-0.5" />
                    <div>
                      <span className="text-xs font-mono font-bold text-indigo-300 block mb-1">
                        TODAY'S POSTING DIRECTIVE
                      </span>
                      <p className="text-xs text-slate-200 leading-relaxed font-medium">
                        {brief.what_you_should_post_today}
                      </p>
                    </div>
                  </div>

                  {/* Top Opportunity */}
                  {brief.best_opportunity && (
                    <div className="bg-[#0d121f] border border-slate-800 rounded-xl p-4 flex items-center justify-between gap-4">
                      <div>
                        <div className="flex items-center gap-2 mb-1">
                          <Flame className="w-4 h-4 text-rose-400" />
                          <span className="text-xs font-mono text-slate-400">Top Opportunity:</span>
                          <span className="text-xs font-bold text-white">{brief.best_opportunity.topic}</span>
                        </div>
                        <p className="text-xs text-slate-300">Angle: {brief.best_opportunity.recommended_angle}</p>
                      </div>

                      <div className="flex items-center gap-3">
                        <span className="font-mono text-emerald-400 font-bold text-sm">
                          {brief.best_opportunity.opportunity_score}/100
                        </span>
                        {onOpenOpportunity && (
                          <button
                            onClick={() => onOpenOpportunity(brief.best_opportunity!.id)}
                            className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs px-3 py-1.5 rounded font-semibold transition"
                          >
                            Explore
                          </button>
                        )}
                      </div>
                    </div>
                  )}
                </div>
              )}

              {/* TAB 2: PLAN MY DAY */}
              {activeTab === "plan" && (
                <div className="space-y-3">
                  <h3 className="text-xs font-mono font-bold text-slate-400 uppercase">
                    5-Slot High-Signal Publishing Schedule
                  </h3>

                  <div className="space-y-2.5">
                    {plan.map((slot, idx) => (
                      <div
                        key={idx}
                        className="bg-[#0e1322] border border-slate-800 rounded-xl p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs"
                      >
                        <div className="flex items-center gap-3">
                          <span className="font-mono text-amber-400 font-bold text-sm w-16 shrink-0">
                            {slot.time_slot}
                          </span>
                          <div>
                            <div className="flex items-center gap-2">
                              <span className="font-mono text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded font-semibold">
                                {slot.platform.toUpperCase()} - {slot.format}
                              </span>
                              <span className="font-bold text-white text-sm">{slot.topic}</span>
                            </div>
                            <p className="text-slate-400 text-xs mt-1">Angle: {slot.recommended_angle}</p>
                          </div>
                        </div>

                        <span className="font-mono text-xs px-2.5 py-1 rounded bg-indigo-950/60 text-indigo-300 border border-indigo-800/40 self-start sm:self-auto">
                          {slot.action}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* TAB 3: CONTENT QUEUE */}
              {activeTab === "queue" && (
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <h3 className="text-xs font-mono font-bold text-slate-400 uppercase">
                      Active Queue Pipeline
                    </h3>
                    <span className="text-xs text-slate-500 font-mono">{queue.length} Scheduled Items</span>
                  </div>

                  {queue.length === 0 ? (
                    <div className="text-center py-16 bg-[#0e1322] rounded-xl border border-slate-800">
                      <p className="text-slate-400 text-xs">Content queue is currently empty. Generate content from Live Radar or News Center to queue.</p>
                    </div>
                  ) : (
                    <div className="space-y-3">
                      {queue.map((item) => (
                        <div key={item.id} className="bg-[#0e1322] border border-slate-800 rounded-xl p-4 text-xs space-y-2">
                          <div className="flex items-center justify-between">
                            <div className="flex items-center gap-2">
                              <span className="font-mono font-bold text-[10px] bg-indigo-950 text-indigo-300 px-2 py-0.5 rounded">
                                {item.platform.toUpperCase()}
                              </span>
                              <span className="font-bold text-white">{item.title}</span>
                            </div>

                            <span className="font-mono text-[10px] bg-emerald-950 text-emerald-400 px-2 py-0.5 rounded border border-emerald-800/40">
                              {item.status}
                            </span>
                          </div>

                          <p className="text-slate-300 whitespace-pre-wrap line-clamp-3 bg-[#070a12] p-2.5 rounded border border-slate-800 font-sans text-xs">
                            {item.content}
                          </p>

                          <div className="flex items-center justify-between pt-1">
                            <span className="text-[10px] font-mono text-slate-500">Priority: {item.priority}</span>
                            <button
                              onClick={() => handleCopy(item.id, item.content)}
                              className="flex items-center gap-1 font-mono text-xs text-slate-400 hover:text-white"
                            >
                              <Copy className="w-3 h-3" />
                              <span>{copiedId === item.id ? "Copied" : "Copy Content"}</span>
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};
