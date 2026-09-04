import React, { useState, useEffect } from "react";
import { 
  X, Check, Copy, Sparkles, ShieldCheck, RefreshCw, Send,
  Share2, FileText, CheckCircle2,
  AlertTriangle, Layers, BookmarkPlus, ChevronRight, Camera, Video, Globe
} from "lucide-react";
import { V3Event, PlatformSuite, HookCandidate } from "../types";

interface ContentStudioV3Props {
  event: V3Event | null;
  isOpen: boolean;
  onClose: () => void;
  onAddToQueue?: (item: any) => void;
}

export const ContentStudioV3: React.FC<ContentStudioV3Props> = ({
  event,
  isOpen,
  onClose,
  onAddToQueue
}) => {
  const [suite, setSuite] = useState<PlatformSuite | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [activeTab, setActiveTab] = useState<"x" | "linkedin" | "instagram" | "youtube" | "brief">("x");
  const [selectedHook, setSelectedHook] = useState<HookCandidate | null>(null);
  const [copied, setCopied] = useState<boolean>(false);
  const [customAngle, setCustomAngle] = useState<string>("");

  const generateContentSuite = async () => {
    if (!event) return;
    setLoading(true);
    try {
      const res = await fetch("/api/content/all", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          event_id: event.id,
          canonical_title: event.title,
          summary: event.summary,
          key_facts: event.key_facts,
          recommended_angle: customAngle || event.recommended_angle,
          primary_source_url: event.primary_source_url
        })
      });

      if (res.ok) {
        const data = await res.json();
        setSuite(data.suite);
        if (data.suite.x_hooks && data.suite.x_hooks.length > 0) {
          setSelectedHook(data.suite.x_hooks[0]);
        }
      }
    } catch (err) {
      console.error("Failed to generate content suite", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen && event) {
      generateContentSuite();
    }
  }, [isOpen, event]);

  if (!isOpen || !event) return null;

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleQueueAdd = (platform: string, content: string) => {
    if (onAddToQueue) {
      onAddToQueue({
        event_id: event.id,
        platform,
        title: event.title,
        content,
        status: "READY",
        priority: "HIGH"
      });
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/85 backdrop-blur-md overflow-y-auto">
      <div className="bg-[#090d16] border border-slate-700/80 rounded-2xl w-full max-w-5xl max-h-[92vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="p-4 sm:p-5 border-b border-slate-800 flex items-center justify-between bg-[#0e1322]">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-gradient-to-br from-amber-500/20 to-orange-500/20 border border-amber-500/30">
              <Sparkles className="w-5 h-5 text-amber-400" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h2 className="text-base sm:text-lg font-black text-white">
                  Multi-Platform Content Studio
                </h2>
                <span className="bg-emerald-950/80 text-emerald-400 border border-emerald-800/40 text-[10px] font-mono px-2 py-0.5 rounded font-bold">
                  9-DIMENSION VERIFIED
                </span>
              </div>
              <p className="text-xs text-slate-400 line-clamp-1 mt-0.5">
                Target: {event.title}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Quality Score Bar & Navigation Tabs */}
        <div className="bg-[#0b0f19] px-5 py-2.5 border-b border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2 overflow-x-auto">
            <button
              onClick={() => setActiveTab("x")}
              className={`px-3 py-1.5 rounded-lg font-mono font-semibold transition flex items-center gap-1.5 ${
                activeTab === "x" 
                  ? "bg-slate-700 text-white" 
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <span>𝕏 Post & 10 Hooks</span>
            </button>

            <button
              onClick={() => setActiveTab("linkedin")}
              className={`px-3 py-1.5 rounded-lg font-mono font-semibold transition flex items-center gap-1.5 ${
                activeTab === "linkedin" 
                  ? "bg-sky-950 text-sky-300 border border-sky-800" 
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Share2 className="w-3.5 h-3.5 text-sky-400" />
              <span>LinkedIn Analysis</span>
            </button>

            <button
              onClick={() => setActiveTab("instagram")}
              className={`px-3 py-1.5 rounded-lg font-mono font-semibold transition flex items-center gap-1.5 ${
                activeTab === "instagram" 
                  ? "bg-pink-950 text-pink-300 border border-pink-800" 
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Camera className="w-3.5 h-3.5 text-pink-400" />
              <span>Instagram Carousel & Reel</span>
            </button>

            <button
              onClick={() => setActiveTab("youtube")}
              className={`px-3 py-1.5 rounded-lg font-mono font-semibold transition flex items-center gap-1.5 ${
                activeTab === "youtube" 
                  ? "bg-red-950 text-red-300 border border-red-800" 
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Video className="w-3.5 h-3.5 text-red-400" />
              <span>YouTube 10 Titles & Script</span>
            </button>

            <button
              onClick={() => setActiveTab("brief")}
              className={`px-3 py-1.5 rounded-lg font-mono font-semibold transition flex items-center gap-1.5 ${
                activeTab === "brief" 
                  ? "bg-violet-950 text-violet-300 border border-violet-800" 
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <FileText className="w-3.5 h-3.5 text-violet-400" />
              <span>Strategic Brief</span>
            </button>
          </div>

          {suite && (
            <div className="flex items-center gap-3 font-mono">
              <span className="text-slate-500">Quality Score:</span>
              <span className="text-emerald-400 font-bold text-sm">
                {suite.quality.total_quality_score}/100
              </span>
              <span className="text-slate-600">|</span>
              <span className="text-sky-400">Originality: {suite.quality.originality_score}%</span>
            </div>
          )}
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-5 space-y-6">
          {loading ? (
            <div className="py-24 text-center space-y-3">
              <RefreshCw className="w-8 h-8 text-amber-400 animate-spin mx-auto" />
              <p className="text-sm font-mono text-slate-300">
                Compiling Pre-Generation Brief, scoring 10 hook styles, and generating cross-platform suite...
              </p>
            </div>
          ) : !suite ? (
            <div className="text-center py-20 text-slate-400">
              <p>Failed to generate content suite. Please try again.</p>
            </div>
          ) : (
            <>
              {/* TAB 1: X (TWITTER) STUDIO */}
              {activeTab === "x" && (
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
                  {/* Left Column: 10 Scored Hooks */}
                  <div className="lg:col-span-5 space-y-3">
                    <h3 className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider flex items-center justify-between">
                      <span>10 Hook Candidates (Scored)</span>
                      <span className="text-amber-400">Top Selected</span>
                    </h3>

                    <div className="space-y-2.5 max-h-[500px] overflow-y-auto pr-1 scrollbar-thin">
                      {suite.x_hooks.map((hook, idx) => (
                        <div
                          key={idx}
                          onClick={() => setSelectedHook(hook)}
                          className={`p-3 rounded-xl border text-xs cursor-pointer transition ${
                            selectedHook?.text === hook.text
                              ? "bg-amber-950/40 border-amber-500/60 shadow-md"
                              : "bg-[#0d121f] border-slate-800 hover:border-slate-700"
                          }`}
                        >
                          <div className="flex items-center justify-between mb-1.5">
                            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded bg-slate-800 text-slate-300">
                              {hook.category}
                            </span>
                            <span className="font-mono font-black text-amber-400 text-xs">
                              {hook.hook_score}/100
                            </span>
                          </div>
                          <p className="text-slate-200 font-medium leading-relaxed">
                            "{hook.text}"
                          </p>
                          <div className="flex items-center gap-3 text-[10px] font-mono text-slate-500 mt-2">
                            <span>Scroll-Stop: {hook.scroll_stop_potential}%</span>
                            <span>Curiosity: {hook.curiosity}%</span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Right Column: Single Post & 9-Tweet Thread */}
                  <div className="lg:col-span-7 space-y-5">
                    {/* Single Post Card */}
                    <div className="bg-[#0e1322] border border-slate-800 rounded-xl p-4 space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-mono font-bold text-slate-400">SINGLE POST</span>
                        <div className="flex items-center gap-2">
                          <button
                            onClick={() => handleCopy(suite.x_content.single_post)}
                            className="flex items-center gap-1 text-xs font-mono bg-slate-800 hover:bg-slate-700 text-slate-300 px-2.5 py-1 rounded transition"
                          >
                            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                            <span>Copy</span>
                          </button>

                          <button
                            onClick={() => handleQueueAdd("x", suite.x_content.single_post)}
                            className="flex items-center gap-1 text-xs font-mono bg-amber-500 hover:bg-amber-400 text-black font-bold px-2.5 py-1 rounded transition"
                          >
                            <BookmarkPlus className="w-3.5 h-3.5" />
                            <span>Queue</span>
                          </button>
                        </div>
                      </div>

                      <div className="bg-[#070a12] p-4 rounded-lg font-sans text-sm text-slate-200 whitespace-pre-wrap leading-relaxed border border-slate-800/80">
                        {selectedHook ? selectedHook.text : suite.x_content.selected_hook.text}
                        {"\n\n"}
                        {suite.x_content.single_post.split("\n\n").slice(1).join("\n\n")}
                      </div>
                    </div>

                    {/* 9-Tweet Thread Card */}
                    <div className="bg-[#0e1322] border border-slate-800 rounded-xl p-4 space-y-3">
                      <div className="flex items-center justify-between">
                        <span className="text-xs font-mono font-bold text-slate-400">
                          9-TWEET STRUCTURED THREAD
                        </span>
                        <button
                          onClick={() => handleCopy(suite.x_content.thread.join("\n\n---\n\n"))}
                          className="flex items-center gap-1 text-xs font-mono bg-slate-800 hover:bg-slate-700 text-slate-300 px-2.5 py-1 rounded transition"
                        >
                          <Copy className="w-3.5 h-3.5" />
                          <span>Copy All</span>
                        </button>
                      </div>

                      <div className="space-y-2 max-h-[260px] overflow-y-auto pr-1 scrollbar-thin">
                        {suite.x_content.thread.map((tweet, i) => (
                          <div key={i} className="bg-[#070a12] p-3 rounded border border-slate-800/60 text-xs text-slate-300">
                            {tweet}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 2: LINKEDIN */}
              {activeTab === "linkedin" && (
                <div className="bg-[#0e1322] border border-slate-800 rounded-xl p-6 space-y-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-sm font-bold text-white flex items-center gap-2">
                        <Share2 className="w-4 h-4 text-sky-400" />
                        Enterprise Thought Leadership Copy
                      </h3>
                      <p className="text-xs text-slate-400">
                        Crafted for technology founders, engineering executives, and ML practitioners.
                      </p>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handleCopy(suite.linkedin_content.content)}
                        className="flex items-center gap-1.5 text-xs font-mono bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg transition"
                      >
                        <Copy className="w-3.5 h-3.5" />
                        <span>Copy Post</span>
                      </button>

                      <button
                        onClick={() => handleQueueAdd("linkedin", suite.linkedin_content.content)}
                        className="flex items-center gap-1.5 text-xs font-mono bg-sky-600 hover:bg-sky-500 text-white font-bold px-3 py-1.5 rounded-lg transition"
                      >
                        <BookmarkPlus className="w-3.5 h-3.5" />
                        <span>Add to Queue</span>
                      </button>
                    </div>
                  </div>

                  <div className="bg-[#070a12] p-5 rounded-xl border border-slate-800 text-sm text-slate-200 whitespace-pre-wrap leading-relaxed">
                    {suite.linkedin_content.content}
                  </div>
                </div>
              )}

              {/* TAB 3: INSTAGRAM */}
              {activeTab === "instagram" && (
                <div className="space-y-6">
                  {/* Carousel */}
                  <div className="bg-[#0e1322] border border-slate-800 rounded-xl p-5 space-y-4">
                    <div className="flex items-center justify-between">
                      <div>
                        <h3 className="text-sm font-bold text-white flex items-center gap-2">
                          <Camera className="w-4 h-4 text-pink-400" />
                          8-Slide Instagram Carousel Blueprint
                        </h3>
                        <p className="text-xs text-slate-400">Complete with visual direction and image prompts per slide.</p>
                      </div>

                      <button
                        onClick={() => handleCopy(JSON.stringify(suite.instagram_carousel.slides, null, 2))}
                        className="text-xs font-mono bg-slate-800 hover:bg-slate-700 text-slate-200 px-3 py-1.5 rounded-lg transition flex items-center gap-1"
                      >
                        <Copy className="w-3.5 h-3.5" />
                        <span>Copy All Slides</span>
                      </button>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
                      {suite.instagram_carousel.slides.map((slide) => (
                        <div key={slide.slide_number} className="bg-[#070a12] border border-slate-800 rounded-lg p-3.5 space-y-2 text-xs">
                          <div className="flex items-center justify-between">
                            <span className="font-mono text-pink-400 font-bold">Slide {slide.slide_number}</span>
                            <span className="text-[10px] text-slate-500 font-mono">{slide.type.toUpperCase()}</span>
                          </div>
                          <h4 className="font-bold text-white text-sm">{slide.headline}</h4>
                          <p className="text-slate-300 text-[11px] leading-relaxed">{slide.subtext}</p>
                          <div className="bg-slate-900/80 p-2 rounded text-[10px] text-slate-400 border border-slate-800">
                            <strong className="text-slate-300">Prompt: </strong>{slide.asset_prompt}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Reel Script */}
                  <div className="bg-[#0e1322] border border-slate-800 rounded-xl p-5 space-y-3">
                    <h3 className="text-sm font-bold text-white">35-Second High-Retention Reel Script</h3>
                    <div className="space-y-2">
                      {suite.instagram_reel.beats.map((b, idx) => (
                        <div key={idx} className="bg-[#070a12] p-3 rounded-lg border border-slate-800 flex flex-col sm:flex-row gap-3 text-xs">
                          <span className="font-mono text-amber-400 font-bold w-24 shrink-0">{b.timecode}</span>
                          <div className="flex-1 space-y-1">
                            <div className="text-white font-semibold">{b.narration}</div>
                            <div className="text-slate-500 text-[11px] italic">Visual: {b.visual}</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 4: YOUTUBE */}
              {activeTab === "youtube" && (
                <div className="space-y-6">
                  {/* 10 Title Candidates */}
                  <div className="bg-[#0e1322] border border-slate-800 rounded-xl p-5 space-y-3">
                    <h3 className="text-sm font-bold text-white flex items-center gap-2">
                      <Video className="w-4 h-4 text-red-400" />
                      10 Viral Title Candidates
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                      {suite.youtube_content.titles.map((t, idx) => (
                        <div key={idx} className="bg-[#070a12] p-2.5 rounded-lg border border-slate-800 flex items-center justify-between text-xs">
                          <div>
                            <span className="text-[10px] font-mono text-red-400 font-bold block">{t.style}</span>
                            <span className="text-white font-medium">{t.title}</span>
                          </div>
                          <button onClick={() => handleCopy(t.title)} className="text-slate-500 hover:text-white p-1">
                            <Copy className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* 3 Thumbnail Concepts */}
                  <div className="bg-[#0e1322] border border-slate-800 rounded-xl p-5 space-y-3">
                    <h3 className="text-sm font-bold text-white">3 High-CTR Thumbnail Blueprints</h3>
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                      {suite.youtube_content.thumbnails.map((thumb) => (
                        <div key={thumb.concept} className="bg-[#070a12] border border-slate-800 rounded-lg p-3.5 text-xs space-y-2">
                          <span className="font-mono text-red-400 font-bold">Concept {thumb.concept}: {thumb.name}</span>
                          <div className="text-amber-300 font-black text-sm tracking-wider">{thumb.foreground_text}</div>
                          <p className="text-slate-300 text-[11px]">{thumb.subject}</p>
                          <div className="text-[10px] text-slate-500 bg-slate-900 p-2 rounded">
                            <strong>AI Prompt: </strong>{thumb.prompt}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* TAB 5: STRATEGIC BRIEF */}
              {activeTab === "brief" && (
                <div className="bg-[#0e1322] border border-slate-800 rounded-xl p-6 space-y-4 text-xs">
                  <h3 className="text-sm font-bold text-white">Pre-Generation Content Brief</h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="bg-[#070a12] p-4 rounded-lg border border-slate-800 space-y-2">
                      <span className="font-mono text-slate-400 font-bold uppercase">Audience & Goal</span>
                      <p className="text-slate-200"><strong>Audience:</strong> {suite.brief.audience}</p>
                      <p className="text-slate-200"><strong>Goal:</strong> {suite.brief.goal}</p>
                    </div>

                    <div className="bg-[#070a12] p-4 rounded-lg border border-slate-800 space-y-2">
                      <span className="font-mono text-slate-400 font-bold uppercase">Angle & Hook Strategy</span>
                      <p className="text-slate-200"><strong>Angle:</strong> {suite.brief.angle}</p>
                      <p className="text-slate-200"><strong>Hook Strategy:</strong> {suite.brief.hook_strategy}</p>
                    </div>
                  </div>

                  <div className="bg-[#070a12] p-4 rounded-lg border border-slate-800 space-y-2">
                    <span className="font-mono text-slate-400 font-bold uppercase">Critical Counterpoint & Caveats</span>
                    <p className="text-amber-300 font-medium">{suite.brief.counterpoint}</p>
                  </div>
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </div>
  );
};
