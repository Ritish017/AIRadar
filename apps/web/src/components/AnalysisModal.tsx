import React, { useState, useEffect } from "react";
import { ContentItem, Analysis } from "../types";
import { analyzeContentItem } from "../lib/api";
import {
  X,
  Sparkles,
  AlertTriangle,
  CheckCircle,
  ArrowRight,
  Share2,
  Lightbulb,
  Compass,
  ShieldCheck,
  HelpCircle,
  ExternalLink
} from "lucide-react";

interface AnalysisModalProps {
  item: ContentItem | null;
  onClose: () => void;
  onOpenStudio: (item: ContentItem, analysis?: Analysis) => void;
}

export const AnalysisModal: React.FC<AnalysisModalProps> = ({
  item,
  onClose,
  onOpenStudio,
}) => {
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!item) return;

    if (item.analysis) {
      setAnalysis(item.analysis);
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);
    analyzeContentItem(item.id)
      .then((res) => {
        setAnalysis(res);
        setLoading(false);
      })
      .catch((err) => {
        setError(err.message || "Analysis failed");
        setLoading(false);
      });
  }, [item]);

  if (!item) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md animate-fade-in">
      <div className="glass-panel w-full max-w-2xl max-h-[90vh] rounded-2xl overflow-hidden flex flex-col shadow-2xl border border-slate-700/80">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/60">
          <div className="flex items-center space-x-2">
            <div className="p-2 rounded-lg bg-brand-500/20 text-brand-300">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white tracking-tight">AI Virality & Fact-Check Breakdown</h2>
              <p className="text-xs text-slate-400">Gemini multi-source verification and hook psychology</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content Body */}
        <div className="p-6 overflow-y-auto space-y-6 text-sm text-slate-200">
          {loading && (
            <div className="py-16 text-center space-y-3">
              <div className="inline-block animate-spin text-brand-400">
                <Sparkles className="w-8 h-8" />
              </div>
              <p className="text-sm font-medium text-slate-300">Cross-referencing claims and deconstructing virality hooks...</p>
            </div>
          )}

          {error && (
            <div className="p-4 rounded-xl bg-rose-500/15 border border-rose-500/30 text-rose-300 flex items-center space-x-2">
              <AlertTriangle className="w-5 h-5 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {!loading && analysis && (
            <>
              {/* 1. What Happened */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-brand-400 mb-2 flex items-center space-x-1.5">
                  <Compass className="w-4 h-4" />
                  <span>What Happened?</span>
                </h4>
                <div className="p-4 rounded-xl bg-slate-900/70 border border-slate-800/80 text-slate-200 leading-relaxed">
                  {analysis.summary}
                </div>
              </div>

              {/* 2. Verified Facts (✓ Confirmed) */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-2 flex items-center space-x-1.5">
                  <CheckCircle className="w-4 h-4" />
                  <span>Verified Facts (✓ Confirmed)</span>
                </h4>
                <div className="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 space-y-2">
                  {(analysis.confirmed_facts && analysis.confirmed_facts.length > 0 ? analysis.confirmed_facts : analysis.key_facts).map((fact, idx) => (
                    <div key={idx} className="flex items-start space-x-2 text-xs text-emerald-200">
                      <span className="text-emerald-400 font-bold">✓</span>
                      <span>{fact}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* 3. What is Uncertain / Speculative (⚠ Unverified) */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400 mb-2 flex items-center space-x-1.5">
                  <HelpCircle className="w-4 h-4" />
                  <span>What Is Uncertain / Speculation (⚠ Unverified)</span>
                </h4>
                <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/20 space-y-2">
                  {(analysis.uncertain_claims && analysis.uncertain_claims.length > 0 ? analysis.uncertain_claims : [
                    "Real-world enterprise latency and token costs under unquantized loads require independent empirical verification."
                  ]).map((claim, idx) => (
                    <div key={idx} className="flex items-start space-x-2 text-xs text-amber-200">
                      <span className="text-amber-400 font-bold">⚠</span>
                      <span>{claim}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* 4. Why it's going viral */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-rose-400 mb-2 flex items-center space-x-1.5">
                  <Sparkles className="w-4 h-4" />
                  <span>Why It Could Go Viral</span>
                </h4>
                <ul className="space-y-2">
                  {analysis.why_viral.map((reason, idx) => (
                    <li
                      key={idx}
                      className="p-3 rounded-lg bg-slate-900/50 border border-slate-800 flex items-start space-x-2.5"
                    >
                      <span className="flex-shrink-0 w-5 h-5 rounded-full bg-rose-500/20 text-rose-400 text-xs font-bold flex items-center justify-center">
                        {idx + 1}
                      </span>
                      <span className="text-slate-300 leading-snug">{reason}</span>
                    </li>
                  ))}
                </ul>
              </div>

              {/* 5. Content Pattern Matrix */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2">
                  Content Pattern Matrix
                </h4>
                <div className="grid grid-cols-3 gap-3">
                  <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                    <span className="text-[11px] text-slate-400 uppercase font-semibold">Hook Type</span>
                    <p className="text-sm font-bold text-white capitalize mt-0.5">{analysis.hook_type || "Curiosity"}</p>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                    <span className="text-[11px] text-slate-400 uppercase font-semibold">Format</span>
                    <p className="text-sm font-bold text-white capitalize mt-0.5">{analysis.content_type || "News"}</p>
                  </div>
                  <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
                    <span className="text-[11px] text-slate-400 uppercase font-semibold">Quality Tier</span>
                    <p className="text-sm font-bold text-emerald-400 mt-0.5">{item.source_quality || "Tier 1 Official"}</p>
                  </div>
                </div>
              </div>

              {/* 6. Recommended Angle */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-indigo-400 mb-2 flex items-center space-x-1.5">
                  <Lightbulb className="w-4 h-4" />
                  <span>Best Creator Angle</span>
                </h4>
                <div className="p-4 rounded-xl bg-indigo-500/10 border border-indigo-500/25 text-indigo-200/90 leading-relaxed text-xs">
                  {analysis.recommended_angle || "Focus on practical architectural implications: how this reduces latency or unlocks new agentic workflows."}
                </div>
              </div>

              {/* 7. Sources */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 mb-2 flex items-center space-x-1.5">
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  <span>Source Verification & Attribution</span>
                </h4>
                <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 flex items-center justify-between">
                  <div>
                    <div className="text-xs font-bold text-white">{item.author || item.source}</div>
                    <div className="text-[11px] text-slate-400 truncate max-w-md">{item.url}</div>
                  </div>
                  <a
                    href={item.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center space-x-1 text-xs text-brand-400 hover:text-brand-300 font-semibold"
                  >
                    <span>View</span>
                    <ExternalLink className="w-3.5 h-3.5" />
                  </a>
                </div>
              </div>
            </>
          )}
        </div>

        {/* Footer Actions */}
        <div className="p-4 border-t border-slate-800 flex items-center justify-between bg-slate-900/70">
          <div className="text-xs text-slate-400">
            Source: <span className="text-slate-300 font-medium">{item.author || item.source}</span>
          </div>
          <button
            onClick={() => {
              onClose();
              onOpenStudio(item, analysis || undefined);
            }}
            className="flex items-center space-x-2 px-5 py-2.5 rounded-xl text-xs font-bold bg-brand-600 hover:bg-brand-500 text-white transition shadow-lg shadow-brand-500/25"
          >
            <Share2 className="w-4 h-4" />
            <span>Open in Post Studio</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
};
