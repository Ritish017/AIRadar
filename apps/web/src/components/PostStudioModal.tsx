import React, { useState } from "react";
import { ContentItem, Analysis, GeneratedVariant } from "../types";
import { generatePosts } from "../lib/api";
import {
  X,
  Sparkles,
  Copy,
  Check,
  Edit3,
  RefreshCw,
  ExternalLink,
  ShieldCheck,
  FileText,
  MessageSquare,
  HelpCircle,
  Flame,
  BookOpen
} from "lucide-react";

interface PostStudioModalProps {
  item: ContentItem | null;
  analysis?: Analysis;
  initialAngle?: string;
  initialHook?: string;
  onClose: () => void;
}

const TONES = ["professional", "technical", "bold", "casual", "minimal"];
const LENGTHS = ["short", "medium", "long"];

const VARIANT_ICONS: Record<string, React.ReactNode> = {
  news: <FileText className="w-4 h-4 text-cyan-400" />,
  hot_take: <Flame className="w-4 h-4 text-rose-400" />,
  educational: <BookOpen className="w-4 h-4 text-amber-400" />,
  builder: <Sparkles className="w-4 h-4 text-emerald-400" />,
  thread: <MessageSquare className="w-4 h-4 text-brand-400" />,
  question: <HelpCircle className="w-4 h-4 text-indigo-400" />
};

export const PostStudioModal: React.FC<PostStudioModalProps> = ({
  item,
  analysis,
  initialAngle,
  initialHook,
  onClose,
}) => {
  const [tone, setTone] = useState("technical");
  const [length, setLength] = useState("medium");
  const [selectedAngle, setSelectedAngle] = useState(initialAngle || "");
  const [selectedHook, setSelectedHook] = useState(initialHook || "");
  const [loading, setLoading] = useState(false);
  const [variants, setVariants] = useState<GeneratedVariant[]>(item?.generated_variants || []);
  const [activeVariantTab, setActiveVariantTab] = useState<string>("news");
  const [copiedId, setCopiedId] = useState<string | null>(null);
  const [editingIndex, setEditingIndex] = useState<number | null>(null);
  const [editedContent, setEditedContent] = useState<string>("");

  const handleGenerate = async () => {
    if (!item) return;
    setLoading(true);
    try {
      const res = await generatePosts(item.id, {
        tones: [tone],
        length,
        include_voice_profile: true,
        angle: selectedAngle,
        hook_type: selectedHook,
      });
      setVariants(res);
      if (res.length > 0) {
        setActiveVariantTab(res[0].variant_type);
      }
    } catch (err) {
      console.error("Failed to generate variants:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (text: string, id: string) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleOpenX = (text: string) => {
    const encoded = encodeURIComponent(text);
    window.open(`https://x.com/intent/tweet?text=${encoded}`, "_blank");
  };

  if (!item) return null;

  const currentVariant = variants.find((v) => v.variant_type === activeVariantTab) || variants[0];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/70 backdrop-blur-md animate-fade-in">
      <div className="glass-panel w-full max-w-3xl max-h-[92vh] rounded-2xl overflow-hidden flex flex-col shadow-2xl border border-slate-700/80">
        {/* Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-900/80">
          <div className="flex items-center space-x-2">
            <div className="p-2 rounded-lg bg-brand-600/30 text-brand-300">
              <Sparkles className="w-5 h-5 text-brand-400" />
            </div>
            <div>
              <h2 className="text-base font-bold text-white tracking-tight">Original Post Studio</h2>
              <p className="text-xs text-slate-400">Synthesize authentic high-signal posts with voice persona</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Studio Controls */}
        <div className="px-6 py-3.5 border-b border-slate-800/80 bg-slate-900/40 flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center space-x-4">
            {/* Tone Selector */}
            <div className="flex items-center space-x-1.5">
              <span className="text-xs text-slate-400 font-medium">Tone:</span>
              <div className="flex items-center space-x-1 bg-slate-900 p-0.5 rounded-lg border border-slate-800">
                {TONES.map((t) => (
                  <button
                    key={t}
                    onClick={() => setTone(t)}
                    className={`px-2.5 py-1 rounded-md text-[11px] font-medium capitalize transition ${
                      tone === t
                        ? "bg-brand-600 text-white font-semibold"
                        : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    {t}
                  </button>
                ))}
              </div>
            </div>

            {/* Length Selector */}
            <div className="flex items-center space-x-1.5">
              <span className="text-xs text-slate-400 font-medium">Length:</span>
              <div className="flex items-center space-x-1 bg-slate-900 p-0.5 rounded-lg border border-slate-800">
                {LENGTHS.map((l) => (
                  <button
                    key={l}
                    onClick={() => setLength(l)}
                    className={`px-2.5 py-1 rounded-md text-[11px] font-medium capitalize transition ${
                      length === l
                        ? "bg-slate-800 text-white font-semibold"
                        : "text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    {l}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading}
            className="flex items-center space-x-1.5 px-4 py-1.5 rounded-lg text-xs font-bold bg-brand-600 hover:bg-brand-500 text-white transition shadow-sm"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? "animate-spin" : ""}`} />
            <span>{variants.length > 0 ? "Regenerate All" : "Generate Variants"}</span>
          </button>
        </div>

        {/* Studio Body */}
        <div className="p-6 overflow-y-auto flex-1 space-y-4">
          {loading ? (
            <div className="py-20 text-center space-y-3">
              <div className="inline-block animate-spin text-brand-400">
                <Sparkles className="w-8 h-8" />
              </div>
              <p className="text-sm text-slate-300 font-medium">Generating 5 original variants calibrated to your voice...</p>
              <p className="text-xs text-slate-500">Checking anti-copy similarity against source material</p>
            </div>
          ) : variants.length === 0 ? (
            <div className="py-16 text-center space-y-3">
              <Sparkles className="w-10 h-10 text-slate-600 mx-auto" />
              <h3 className="text-sm font-semibold text-slate-300">Ready to synthesize original content</h3>
              <p className="text-xs text-slate-400 max-w-md mx-auto">
                Select your desired tone and length above, then click <strong>Generate Variants</strong> to create 5 distinct, copyright-safe posts.
              </p>
              <button
                onClick={handleGenerate}
                className="mt-2 px-5 py-2 rounded-xl text-xs font-bold bg-brand-600 hover:bg-brand-500 text-white transition shadow-lg shadow-brand-500/25"
              >
                Generate Now
              </button>
            </div>
          ) : (
            <div>
              {/* Variant Tabs */}
              <div className="flex items-center space-x-2 border-b border-slate-800 pb-2 mb-4 overflow-x-auto">
                {variants.map((v) => {
                  const isActive = activeVariantTab === v.variant_type;
                  return (
                    <button
                      key={v.variant_type}
                      onClick={() => setActiveVariantTab(v.variant_type)}
                      className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold capitalize whitespace-nowrap transition ${
                        isActive
                          ? "bg-slate-800 text-white border border-slate-700 shadow-sm"
                          : "text-slate-400 hover:text-slate-200 hover:bg-slate-900"
                      }`}
                    >
                      {VARIANT_ICONS[v.variant_type]}
                      <span>{v.variant_type.replace("_", " ")}</span>
                    </button>
                  );
                })}
              </div>

              {/* Active Variant Card Preview */}
              {currentVariant && (
                <div className="glass-card rounded-xl p-5 space-y-4 border border-slate-700/80">
                  {/* Card Status & Similarity Safeguard */}
                  <div className="flex items-center justify-between text-xs pb-3 border-b border-slate-800">
                    <div className="flex items-center space-x-2">
                      <span className="flex items-center space-x-1 text-emerald-400 font-semibold bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/20">
                        <ShieldCheck className="w-3.5 h-3.5" />
                        <span>Originality Verified</span>
                      </span>
                      <span className="text-slate-500 text-[11px]">
                        Similarity: {Math.round(currentVariant.similarity_score * 100)}% (Safety Threshold: &lt;60%)
                      </span>
                    </div>

                    <span className="text-slate-400 text-xs">
                      {currentVariant.content.length} chars
                    </span>
                  </div>

                  {/* Thread or Single Post View */}
                  {currentVariant.variant_type === "thread" && currentVariant.thread_items && currentVariant.thread_items.length > 0 ? (
                    <div className="space-y-3">
                      {currentVariant.thread_items.map((postText, i) => (
                        <div key={i} className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 text-sm text-slate-100 whitespace-pre-wrap leading-relaxed relative group">
                          {postText}
                          <button
                            onClick={() => handleCopy(postText, `thread_${i}`)}
                            className="absolute top-2 right-2 p-1 rounded bg-slate-800 text-slate-400 opacity-0 group-hover:opacity-100 hover:text-white transition"
                          >
                            {copiedId === `thread_${i}` ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                          </button>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <div className="p-4 rounded-xl bg-slate-900/90 border border-slate-800/80 text-sm text-slate-100 whitespace-pre-wrap leading-relaxed font-sans">
                      {currentVariant.content}
                    </div>
                  )}

                  {/* Card Actions */}
                  <div className="flex items-center justify-between pt-2">
                    <div className="text-xs text-slate-500 flex items-center space-x-1">
                      <span>Attribution preserved:</span>
                      <span className="text-slate-400 font-mono text-[11px] truncate max-w-xs">{item.url}</span>
                    </div>

                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => handleCopy(currentVariant.content, currentVariant.variant_type)}
                        className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition"
                      >
                        {copiedId === currentVariant.variant_type ? (
                          <>
                            <Check className="w-3.5 h-3.5 text-emerald-400" />
                            <span className="text-emerald-400 font-bold">Copied!</span>
                          </>
                        ) : (
                          <>
                            <Copy className="w-3.5 h-3.5" />
                            <span>Copy</span>
                          </>
                        )}
                      </button>

                      <button
                        onClick={() => handleOpenX(currentVariant.content)}
                        className="flex items-center space-x-1.5 px-4 py-1.5 rounded-lg text-xs font-bold bg-white hover:bg-slate-200 text-slate-900 transition shadow-sm"
                      >
                        <ExternalLink className="w-3.5 h-3.5" />
                        <span>Open in X</span>
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
