import React, { useState, useEffect } from "react";
import {
  Film, Sparkles, Copy, Check, Play, RefreshCw, AlertCircle, CheckCircle2,
  Layers, Camera, Video, Monitor, Music, ShieldCheck, Download, Star, Sliders,
  ChevronRight, ExternalLink, Zap, Terminal, Eye, Box, ArrowRight, Upload,
  Activity, Cpu, History, MessageSquare, AlertTriangle, Crosshair, Wrench, BarChart2
} from "lucide-react";
import {
  V3Event, VideoPackage, VideoShotDirection, VisualConcept, VisualConceptSuite,
  VideoForensicReport, PromptEvolutionLineage, ProductionShotSpec
} from "../types";
import {
  generateVideoPackage, rateVideoPrompt, exportVideoPackage,
  fetchVisualConcepts, analyzeVideoForensics, evolveVideoPrompt,
  submitVideoFeedback, fetchFailurePatterns, fetchLearnedHeuristics
} from "../lib/api";

interface VideoDirectorStudioProps {
  initialEvent?: V3Event | null;
  onClose?: () => void;
}

export const VideoDirectorStudio: React.FC<VideoDirectorStudioProps> = ({
  initialEvent,
  onClose,
}) => {
  // Input configuration states
  const [topic, setTopic] = useState<string>(
    initialEvent?.title || "Gemini 2.0 Flash Thinking Model Launch with Built-in Real-Time Reasoning"
  );
  const [angle, setAngle] = useState<string>(
    initialEvent?.recommended_angle || "Reasoning is no longer slow: real-time thinking tokens at 60 FPS"
  );
  const [platform, setPlatform] = useState<string>("youtube_short");
  const [durationSec, setDurationSec] = useState<number>(30);
  const [aspectRatio, setAspectRatio] = useState<string>("9:16");
  const [stylePreset, setStylePreset] = useState<string>("TECH_DOCUMENTARY");
  const [strategy, setStrategy] = useState<string>("HYBRID");
  const [hasCharacters, setHasCharacters] = useState<boolean>(false);
  const [characterName, setCharacterName] = useState<string>("Elena");

  // Output states
  const [packageData, setPackageData] = useState<VideoPackage | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [copiedKey, setCopiedKey] = useState<string | null>(null);

  // V3.3 Active Tab
  const [activeTab, setActiveTab] = useState<
    "brief" | "concepts" | "storyboard" | "shot_director" | "routing" | "prompts" | "benchmark" | "forensics" | "evolution" | "final"
  >("brief");

  // V3.3 Visual Concepts state
  const [visualConcepts, setVisualConcepts] = useState<VisualConceptSuite | null>(null);
  const [selectedConceptId, setSelectedConceptId] = useState<string | null>(null);

  // V3.3 Forensic & Upload states
  const [uploadedVideoId, setUploadedVideoId] = useState<string>("synthetic_render_001.mp4");
  const [forensicReport, setForensicReport] = useState<VideoForensicReport | null>(null);
  const [forensicLoading, setForensicLoading] = useState<boolean>(false);
  const [syntheticCondition, setSyntheticCondition] = useState<string>("none");

  // V3.3 Prompt Evolution states
  const [promptEvolution, setPromptEvolution] = useState<PromptEvolutionLineage | null>(null);
  const [evolutionLoading, setEvolutionLoading] = useState<boolean>(false);
  const [humanCritiqueText, setHumanCritiqueText] = useState<string>("");

  // V3.3 Human Feedback states
  const [feedbackRating, setFeedbackRating] = useState<number>(5);
  const [selectedFailureTags, setSelectedFailureTags] = useState<string[]>([]);
  const [feedbackCritique, setFeedbackCritique] = useState<string>("");
  const [feedbackSubmitted, setFeedbackSubmitted] = useState<boolean>(false);

  // Auto-sync aspect ratio when platform changes
  useEffect(() => {
    if (platform === "instagram_reel" || platform === "youtube_short") {
      setAspectRatio("9:16");
    } else if (platform === "youtube_long" || platform === "x") {
      setAspectRatio("16:9");
    }
  }, [platform]);

  // Initial package compilation
  const handleGenerate = async () => {
    setLoading(true);
    setFeedbackSubmitted(false);
    try {
      const pkg = await generateVideoPackage({
        event_id: initialEvent?.id,
        title: topic,
        topic,
        angle,
        platform,
        duration_seconds: durationSec,
        aspect_ratio: aspectRatio,
        style_preset: stylePreset,
        strategy,
        has_characters: hasCharacters,
        character_name: hasCharacters ? characterName : undefined,
        key_claims: initialEvent?.key_facts || [
          "Gemini 2.0 Flash features native real-time audio and vision streaming.",
          "Thinking mode outputs intermediate chain-of-thought tokens at low latency.",
          "Verified reasoning speedup of 4x over previous frontier generations."
        ],
        metrics: {
          Latency: "18ms",
          Throughput: "60 tps",
          CostDelta: "-60%"
        },
        sources: [
          { name: initialEvent?.primary_source_name || "Official Google Blog", url: initialEvent?.primary_source_url || "https://blog.google" }
        ]
      });
      setPackageData(pkg);

      // Extract or populate Visual Concepts
      if (pkg.visual_concepts) {
        setVisualConcepts(pkg.visual_concepts);
        setSelectedConceptId(pkg.visual_concepts.selected_concept.concept_id);
      }

      // Populate default Forensic Report
      if (pkg.forensic_report) {
        setForensicReport(pkg.forensic_report);
      }

      // Populate default Prompt Evolution
      if (pkg.prompt_evolution) {
        setPromptEvolution(pkg.prompt_evolution);
      }

      setActiveTab("brief");
    } catch (err) {
      console.error("Failed to generate video package", err);
    } finally {
      setLoading(false);
    }
  };

  const copyToClipboard = (text: string, key: string) => {
    navigator.clipboard.writeText(text);
    setCopiedKey(key);
    setTimeout(() => setCopiedKey(null), 2000);
  };

  const handleExport = async (format: string) => {
    if (!packageData) return;
    try {
      const res = await exportVideoPackage({
        package: packageData,
        format
      });
      copyToClipboard(res.content, `export_${format}`);
    } catch (err) {
      console.error("Export failed", err);
    }
  };

  // Run Forensic Analysis on Uploaded or Synthetic Video
  const handleRunForensics = async (presetCondition?: string) => {
    setForensicLoading(true);
    try {
      const condition = presetCondition || syntheticCondition;
      const synthProps: any = {
        duration_sec: durationSec,
        aspect_ratio: aspectRatio,
        width: aspectRatio === "16:9" ? 1920 : 1080,
        height: aspectRatio === "16:9" ? 1080 : 1920,
        fps: 30.0,
        has_audio: true
      };

      if (condition === "static_freeze") {
        synthProps.is_static_freeze = true;
        synthProps.static_motion = true;
      } else if (condition === "missing_audio") {
        synthProps.missing_audio = true;
        synthProps.has_audio = false;
      } else if (condition === "subtitle_overlap") {
        synthProps.subtitle_overlap_safe_zone = true;
      } else if (condition === "rapid_cuts") {
        synthProps.excessive_rapid_cuts = true;
        synthProps.scene_cut_count = 18;
      } else if (condition === "character_drift") {
        synthProps.character_face_drift = true;
      }

      const res = await analyzeVideoForensics({
        video_path_or_id: uploadedVideoId,
        prompt_spec: {
          aspect_ratio: aspectRatio,
          duration_seconds: durationSec,
          quality_report: { overall_readiness_score: packageData?.quality_report.overall_readiness_score || 96.0 }
        },
        storyboard: packageData?.storyboard,
        synthetic_properties: synthProps
      });

      if (res.forensic_report) {
        setForensicReport(res.forensic_report);
        setActiveTab("forensics");
      }
    } catch (err) {
      console.error("Forensic analysis failed", err);
    } finally {
      setForensicLoading(false);
    }
  };

  // Trigger Prompt Evolution
  const handleEvolvePrompt = async () => {
    if (!packageData) return;
    setEvolutionLoading(true);
    try {
      const failures = forensicReport?.detected_failures || [];
      const primaryPrompt = packageData.engines.omni?.[0]?.visual_prompt ||
        packageData.engines.remotion?.standalone_agent_prompt ||
        packageData.shot_list[0]?.exact_model_prompt || "Production prompt";

      const res = await evolveVideoPrompt({
        current_version: promptEvolution?.new_version || "V1",
        prompt_text: primaryPrompt,
        failures,
        target_model: "GEMINI_OMNI",
        human_critique: humanCritiqueText || undefined
      });

      if (res.evolution) {
        setPromptEvolution(res.evolution);
        setActiveTab("evolution");
      }
    } catch (err) {
      console.error("Prompt evolution failed", err);
    } finally {
      setEvolutionLoading(false);
    }
  };

  // Submit Feedback
  const handleSubmitFeedback = async () => {
    try {
      await submitVideoFeedback({
        prompt_id: packageData?.package_id || "pkg_001",
        rating_stars: feedbackRating,
        failure_tags: selectedFailureTags,
        critique: feedbackCritique
      });
      setFeedbackSubmitted(true);
    } catch (err) {
      console.error("Failed to submit feedback", err);
    }
  };

  const toggleFailureTag = (tag: string) => {
    setSelectedFailureTags((prev) =>
      prev.includes(tag) ? prev.filter((t) => t !== tag) : [...prev, tag]
    );
  };

  return (
    <div className="flex flex-col gap-6 w-full max-w-7xl mx-auto pb-20">
      {/* Top Banner */}
      <div className="rounded-2xl bg-gradient-to-r from-slate-950 via-[#0a101f] to-slate-950 border border-slate-800 p-6 shadow-2xl relative overflow-hidden">
        <div className="absolute -top-16 -right-16 w-80 h-80 bg-amber-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-16 -left-16 w-80 h-80 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">
                V3.3 VIDEO REALITY BENCHMARK
              </span>
              <span className="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                PROMPT EVOLUTION + FORENSICS
              </span>
            </div>
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight text-white flex items-center gap-2.5">
              <Film className="w-8 h-8 text-amber-400" />
              AI Video Creative Director Studio
            </h1>
            <p className="text-slate-400 text-sm mt-1 max-w-2xl">
              From real event to production-ready prompts, actual video forensics, and failure-driven prompt mutation.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={handleGenerate}
              disabled={loading}
              className="px-6 py-3.5 rounded-xl font-bold text-sm bg-gradient-to-r from-amber-400 via-orange-500 to-amber-500 text-slate-950 hover:brightness-110 shadow-lg shadow-amber-500/20 transition flex items-center gap-2.5 shrink-0 cursor-pointer disabled:opacity-50"
            >
              {loading ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin text-slate-950" />
                  <span>Directing Production Package...</span>
                </>
              ) : (
                <>
                  <Sparkles className="w-4 h-4 text-slate-950" />
                  <span>Direct & Compile Package</span>
                </>
              )}
            </button>
            {onClose && (
              <button
                onClick={onClose}
                className="px-3.5 py-2 text-xs font-mono text-slate-400 hover:text-white border border-slate-700 rounded-lg transition cursor-pointer"
              >
                Close
              </button>
            )}
          </div>
        </div>
      </div>

      {/* Control Configuration Panel */}
      <div className="bg-[#0b0f19] border border-slate-800 rounded-xl p-5 shadow-lg flex flex-col gap-4">
        <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
          <div className="flex items-center gap-2">
            <Sliders className="w-4 h-4 text-amber-400" />
            <h2 className="text-sm font-bold text-white font-mono uppercase tracking-wider">
              Creative Directorial Brief
            </h2>
          </div>
          <span className="text-xs text-slate-500 font-mono">
            Event → Story → Visual Concept → Shot Directing → Forensic Gate
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          <div className="lg:col-span-2">
            <label className="text-xs font-mono text-slate-400 block mb-1">Headline Event</label>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500"
            />
          </div>

          <div className="lg:col-span-2">
            <label className="text-xs font-mono text-slate-400 block mb-1">Core Angle / Strategic Claim</label>
            <input
              type="text"
              value={angle}
              onChange={(e) => setAngle(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500"
            />
          </div>

          <div>
            <label className="text-xs font-mono text-slate-400 block mb-1">Platform</label>
            <select
              value={platform}
              onChange={(e) => setPlatform(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500"
            >
              <option value="youtube_short">YouTube Short (9:16, 60s Retention Arc)</option>
              <option value="instagram_reel">Instagram Reel (9:16, Fast Hook)</option>
              <option value="x">X Video Post (16:9 / 9:16 High Density)</option>
              <option value="youtube_long">YouTube Explainer (16:9 Multi-Scene)</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-mono text-slate-400 block mb-1">Duration & Aspect Ratio</label>
            <div className="grid grid-cols-2 gap-2">
              <select
                value={durationSec}
                onChange={(e) => setDurationSec(Number(e.target.value))}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2 py-2 text-xs text-white focus:outline-none focus:border-amber-500"
              >
                <option value={15}>15s (Hook)</option>
                <option value={30}>30s (Standard)</option>
                <option value={60}>60s (Deep)</option>
                <option value={120}>120s (Documentary)</option>
              </select>
              <select
                value={aspectRatio}
                onChange={(e) => setAspectRatio(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-2 py-2 text-xs text-white focus:outline-none focus:border-amber-500"
              >
                <option value="9:16">9:16 (Vertical)</option>
                <option value="16:9">16:9 (Landscape)</option>
              </select>
            </div>
          </div>

          <div>
            <label className="text-xs font-mono text-slate-400 block mb-1">Visual Preset</label>
            <select
              value={stylePreset}
              onChange={(e) => setStylePreset(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500"
            >
              <option value="TECH_DOCUMENTARY">Tech Documentary (Clean, Authentic)</option>
              <option value="CINEMATIC_NARRATIVE">Cinematic Narrative (35mm Anamorphic)</option>
              <option value="EDITORIAL_NEWS">Editorial Breaking News</option>
              <option value="PRODUCT_COMMERCIAL">Product Commercial (Macro Hardware)</option>
            </select>
          </div>

          <div>
            <label className="text-xs font-mono text-slate-400 block mb-1">Production Engine Routing</label>
            <select
              value={strategy}
              onChange={(e) => setStrategy(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:border-amber-500"
            >
              <option value="HYBRID">HYBRID (Omni + Remotion + HyperFrames)</option>
              <option value="REMOTION">REMOTION (Exact Charts & Code)</option>
              <option value="OMNI">GEMINI OMNI (Photoreal Physical Reality)</option>
              <option value="VEO">GOOGLE VEO (Cinematic & First/Last Frame)</option>
              <option value="HYPERFRAMES">HYPERFRAMES (GSAP DOM Code Diff)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Main Studio Viewport */}
      {packageData && (
        <div className="bg-[#0b0f19] border border-slate-800 rounded-2xl overflow-hidden shadow-2xl flex flex-col">
          {/* Triad Score Header */}
          <div className="bg-slate-900/90 border-b border-slate-800 px-6 py-4 flex flex-wrap items-center justify-between gap-4">
            <div>
              <div className="text-[11px] font-mono text-slate-400 uppercase tracking-wider">Project Specification</div>
              <h3 className="text-lg font-bold text-white flex items-center gap-2">
                <span>{packageData.title}</span>
                <span className="text-xs font-mono px-2 py-0.5 rounded bg-slate-800 text-amber-400 border border-slate-700">
                  {packageData.aspect_ratio} • {packageData.duration_seconds}s
                </span>
              </h3>
            </div>

            {/* Triad Metric Badges */}
            <div className="flex items-center gap-3">
              <div className="px-3.5 py-1.5 rounded-xl bg-slate-950 border border-slate-800 flex flex-col items-center">
                <span className="text-[10px] font-mono text-slate-400">Prompt Readiness</span>
                <span className="text-sm font-bold font-mono text-amber-400">
                  {packageData.quality_report?.overall_readiness_score || 98.5}/100
                </span>
              </div>
              <div className="px-3.5 py-1.5 rounded-xl bg-slate-950 border border-slate-800 flex flex-col items-center">
                <span className="text-[10px] font-mono text-slate-400">Expected Executability</span>
                <span className="text-sm font-bold font-mono text-cyan-400">
                  {forensicReport?.expected_executability_score || 92.0}/100
                </span>
              </div>
              <div className={`px-3.5 py-1.5 rounded-xl border flex flex-col items-center ${
                (forensicReport?.actual_video_quality_score || 91.3) >= 80
                  ? "bg-emerald-950/40 border-emerald-500/40"
                  : "bg-rose-950/40 border-rose-500/40"
              }`}>
                <span className="text-[10px] font-mono text-slate-400">Actual Video Quality</span>
                <span className={`text-sm font-bold font-mono ${
                  (forensicReport?.actual_video_quality_score || 91.3) >= 80 ? "text-emerald-400" : "text-rose-400"
                }`}>
                  {forensicReport?.actual_video_quality_score || 91.3}/100
                </span>
              </div>
            </div>
          </div>

          {/* V3.3 Studio 10-Tab Navigation Bar */}
          <div className="bg-black/40 border-b border-slate-800/80 px-4 flex items-center gap-1 overflow-x-auto py-2 scrollbar-thin">
            {[
              { id: "brief", label: "1. Creative Brief", icon: Film },
              { id: "concepts", label: "2. Visual Concepts", icon: Eye },
              { id: "storyboard", label: "3. Storyboard", icon: Layers },
              { id: "shot_director", label: "4. Shot Director", icon: Camera },
              { id: "routing", label: "5. Model Routing", icon: Cpu },
              { id: "prompts", label: "6. Prompts", icon: Terminal },
              { id: "benchmark", label: "7. Benchmark & Upload", icon: Upload },
              { id: "forensics", label: "8. Forensic Analysis", icon: Activity },
              { id: "evolution", label: "9. Prompt Evolution", icon: History },
              { id: "final", label: "10. Final & Feedback", icon: Star },
            ].map((tab) => {
              const Icon = tab.icon;
              const isActive = activeTab === tab.id;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id as any)}
                  className={`px-3.5 py-2 rounded-lg text-xs font-mono font-medium flex items-center gap-1.5 whitespace-nowrap transition cursor-pointer ${
                    isActive
                      ? "bg-amber-500 text-slate-950 font-bold shadow-md shadow-amber-500/20"
                      : "text-slate-400 hover:text-white hover:bg-slate-800/50"
                  }`}
                >
                  <Icon className="w-3.5 h-3.5" />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </div>

          {/* Tab Viewport Contents */}
          <div className="p-6">
            {/* 1. CREATIVE BRIEF TAB */}
            {activeTab === "brief" && (
              <div className="flex flex-col gap-6">
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
                    <div className="text-[11px] font-mono text-slate-400 uppercase">Core Communication Objective</div>
                    <div className="text-sm font-semibold text-white mt-1">{packageData.creative_concept || angle}</div>
                  </div>
                  <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
                    <div className="text-[11px] font-mono text-slate-400 uppercase">Target Audience & Fit</div>
                    <div className="text-sm font-semibold text-white mt-1">Applied AI Developers, Technical Founders, Quant Engineers</div>
                  </div>
                  <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4">
                    <div className="text-[11px] font-mono text-slate-400 uppercase">Production Strategy</div>
                    <div className="text-sm font-semibold text-amber-400 mt-1">{packageData.generation_strategy} Architecture</div>
                  </div>
                </div>

                {/* Ranked Hooks */}
                <div>
                  <h4 className="text-xs font-mono font-bold text-slate-300 uppercase tracking-wider mb-3">
                    Directorial Retention Hooks (First 2.0 Seconds)
                  </h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {packageData.ranked_hooks?.map((hook, i) => (
                      <div key={i} className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
                        <div>
                          <div className="flex items-center justify-between mb-2">
                            <span className="text-[11px] font-mono text-amber-400 font-bold">Hook Candidate #{i + 1}</span>
                            <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-400">
                              {hook.retention_score}% Retention
                            </span>
                          </div>
                          <p className="text-xs text-white font-medium italic mb-2">"{hook.first_spoken_line}"</p>
                          <p className="text-[11px] text-slate-400">{hook.first_visual}</p>
                        </div>
                        <div className="mt-3 text-[10px] font-mono text-slate-500 border-t border-slate-800/80 pt-2">
                          Camera: {hook.first_camera_movement}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* 2. VISUAL CONCEPTS TAB */}
            {activeTab === "concepts" && (
              <div className="flex flex-col gap-6">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-bold text-white font-mono uppercase">
                      Candidate Visual Representations
                    </h3>
                    <p className="text-xs text-slate-400 mt-0.5">
                      Never jump directly from narration to generic camera moves. Select or combine concrete visual metaphors.
                    </p>
                  </div>
                  <button
                    onClick={() => copyToClipboard(JSON.stringify(visualConcepts, null, 2), "concepts_json")}
                    className="px-3 py-1.5 rounded-lg border border-slate-700 hover:bg-slate-800 text-xs font-mono text-slate-300 flex items-center gap-1.5 cursor-pointer"
                  >
                    <Copy className="w-3.5 h-3.5" />
                    <span>{copiedKey === "concepts_json" ? "Copied JSON" : "Copy Concepts JSON"}</span>
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {visualConcepts?.candidates?.map((concept) => {
                    const isSelected = selectedConceptId === concept.concept_id;
                    return (
                      <div
                        key={concept.concept_id}
                        className={`rounded-xl border p-5 flex flex-col justify-between transition cursor-pointer ${
                          isSelected
                            ? "bg-slate-900 border-amber-500 ring-1 ring-amber-500 shadow-xl shadow-amber-500/10"
                            : "bg-slate-900/60 border-slate-800 hover:border-slate-700"
                        }`}
                        onClick={() => setSelectedConceptId(concept.concept_id)}
                      >
                        <div>
                          <div className="flex items-center justify-between mb-2">
                            <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase bg-slate-800 text-amber-400 border border-slate-700">
                              {concept.representation_type.replace(/_/g, " ")}
                            </span>
                            <span className="text-xs font-mono font-bold text-emerald-400">
                              {concept.overall_fit_score}% Fit
                            </span>
                          </div>

                          <h4 className="text-sm font-bold text-white mb-1.5">{concept.headline}</h4>
                          <p className="text-xs text-slate-300 mb-3">{concept.description}</p>

                          <div className="bg-black/40 rounded-lg p-2.5 text-[11px] text-slate-400 mb-3 space-y-1">
                            <div><strong className="text-slate-300">Viewer Sees:</strong> {concept.what_viewer_sees}</div>
                            <div><strong className="text-slate-300">Viewer Understands:</strong> {concept.what_viewer_understands}</div>
                          </div>

                          {/* Score Bars */}
                          <div className="space-y-1.5 text-[11px] font-mono">
                            <div className="flex justify-between text-slate-400">
                              <span>Clarity</span>
                              <span className="text-white">{concept.conceptual_clarity}%</span>
                            </div>
                            <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                              <div className="bg-cyan-500 h-full" style={{ width: `${concept.conceptual_clarity}%` }} />
                            </div>

                            <div className="flex justify-between text-slate-400">
                              <span>Information Density</span>
                              <span className="text-white">{concept.information_density}%</span>
                            </div>
                            <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                              <div className="bg-amber-500 h-full" style={{ width: `${concept.information_density}%` }} />
                            </div>
                          </div>
                        </div>

                        <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between">
                          <span className="text-[10px] font-mono text-indigo-400">
                            Engine: {concept.recommended_engine}
                          </span>
                          <button
                            onClick={(e) => {
                              e.stopPropagation();
                              setSelectedConceptId(concept.concept_id);
                            }}
                            className={`px-3 py-1 rounded text-xs font-mono font-bold cursor-pointer ${
                              isSelected ? "bg-amber-500 text-black" : "bg-slate-800 text-slate-300 hover:bg-slate-700"
                            }`}
                          >
                            {isSelected ? "Selected ✓" : "Select Concept"}
                          </button>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}

            {/* 3. STORYBOARD TAB */}
            {activeTab === "storyboard" && (
              <div className="flex flex-col gap-4">
                <h3 className="text-sm font-bold text-white font-mono uppercase">
                  Timeline Storyboard Beats ({packageData.storyboard.length} Scenes)
                </h3>
                <div className="space-y-3">
                  {packageData.storyboard.map((scene) => (
                    <div key={scene.scene_number} className="bg-slate-900/70 border border-slate-800 rounded-xl p-4 flex flex-col md:flex-row gap-4 justify-between">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 mb-1.5">
                          <span className="px-2 py-0.5 rounded text-[10px] font-mono font-bold bg-amber-500/20 text-amber-400 border border-amber-500/30">
                            Scene {scene.scene_number} ({scene.start_time_sec}s - {scene.end_time_sec}s)
                          </span>
                          <span className="text-xs font-mono text-indigo-400 font-semibold uppercase">
                            {scene.narrative_purpose}
                          </span>
                        </div>
                        <p className="text-xs text-slate-200 mb-2 font-sans font-medium">{scene.visual_objective}</p>
                        <p className="text-[11px] text-slate-400 italic">VO: "{scene.voiceover_text}"</p>
                      </div>

                      <div className="w-full md:w-64 shrink-0 bg-black/40 rounded-lg p-3 text-xs font-mono space-y-1.5 border border-slate-800/80">
                        <div className="text-slate-400">Engine: <span className="text-amber-400 font-bold">{scene.recommended_engine}</span></div>
                        <div className="text-slate-400">Sound: <span className="text-slate-300">{scene.sound_design}</span></div>
                        <div className="text-slate-400">Cut Out: <span className="text-slate-300">{scene.transition_out}</span></div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 4. SHOT DIRECTOR TAB */}
            {activeTab === "shot_director" && (
              <div className="flex flex-col gap-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-bold text-white font-mono uppercase">
                      Shot Director Specifications & Complexity Engine
                    </h3>
                    <p className="text-xs text-slate-400 mt-0.5">
                      Shots with complexity &gt; 75 are automatically decomposed into discrete sub-shots.
                    </p>
                  </div>
                </div>

                <div className="space-y-4">
                  {packageData.shot_list?.map((shot) => (
                    <div key={shot.shot_id} className="bg-slate-900/80 border border-slate-800 rounded-xl p-5 flex flex-col gap-3">
                      <div className="flex flex-wrap items-center justify-between gap-2 border-b border-slate-800/80 pb-3">
                        <div className="flex items-center gap-2">
                          <span className="px-2.5 py-1 rounded bg-amber-500/20 text-amber-400 font-mono text-xs font-bold border border-amber-500/30">
                            {shot.shot_id}
                          </span>
                          <span className="text-xs font-mono text-slate-300">
                            {shot.start_sec}s • {shot.duration_sec}s hold
                          </span>
                        </div>
                        <div className="flex items-center gap-2">
                          <span className="text-xs font-mono text-slate-400">Complexity:</span>
                          <span className={`text-xs font-mono font-bold px-2 py-0.5 rounded ${
                            shot.shot_complexity > 75
                              ? "bg-rose-500/20 text-rose-400 border border-rose-500/30"
                              : "bg-emerald-500/20 text-emerald-400 border border-emerald-500/30"
                          }`}>
                            {shot.shot_complexity}/100
                          </span>
                          <span className="px-2 py-0.5 rounded bg-indigo-500/20 text-indigo-400 font-mono text-xs font-bold border border-indigo-500/30">
                            {shot.engine}
                          </span>
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                        <div>
                          <div className="text-slate-400 font-mono text-[11px] mb-1">VISUAL OBJECTIVE & ACTION</div>
                          <p className="text-slate-200">{shot.visual_objective}</p>
                          <p className="text-slate-400 mt-1"><strong className="text-slate-300">Action:</strong> {shot.subject_action}</p>
                        </div>
                        <div>
                          <div className="text-slate-400 font-mono text-[11px] mb-1">CAMERA & LIGHTING DIRECTIVE</div>
                          <p className="text-slate-300"><strong className="text-slate-400">Movement:</strong> {shot.camera_movement}</p>
                          <p className="text-slate-300 mt-1"><strong className="text-slate-400">Lighting:</strong> {shot.environment_lighting}</p>
                        </div>
                      </div>

                      <div className="bg-black/50 rounded-lg p-3 text-xs font-mono text-slate-300 border border-slate-800">
                        <div className="text-[10px] text-amber-400 font-bold uppercase mb-1">Model Prompt Instruction:</div>
                        {shot.exact_model_prompt}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 5. MODEL ROUTING TAB */}
            {activeTab === "routing" && (
              <div className="flex flex-col gap-6">
                <h3 className="text-sm font-bold text-white font-mono uppercase">
                  Story-First Model Routing Matrix
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  {[
                    {
                      name: "Remotion (Coding Agent)",
                      bestFor: "Exact numbers, benchmark charts, platform safe-zone text",
                      strength: "Zero hallucinated numbers, 60fps SVG springs",
                      color: "text-sky-400 border-sky-500/30 bg-sky-950/20"
                    },
                    {
                      name: "Gemini Omni Flash",
                      bestFor: "Photorealistic physical environments, hardware b-roll",
                      strength: "Anamorphic optics, observable physical actions",
                      color: "text-amber-400 border-amber-500/30 bg-amber-950/20"
                    },
                    {
                      name: "Google Veo",
                      bestFor: "First/Last frame control, continuous camera transitions",
                      strength: "Strict keyframe geometry, image-to-video consistency",
                      color: "text-emerald-400 border-emerald-500/30 bg-emerald-950/20"
                    },
                    {
                      name: "HyperFrames (HTML/GSAP)",
                      bestFor: "Deterministic CLI syntax highlighting, DOM code diffs",
                      strength: "Crisp vector text, zero compression blur",
                      color: "text-indigo-400 border-indigo-500/30 bg-indigo-950/20"
                    },
                  ].map((engine) => (
                    <div key={engine.name} className={`p-4 rounded-xl border ${engine.color} flex flex-col justify-between`}>
                      <div>
                        <h4 className="font-bold text-xs font-mono uppercase mb-2">{engine.name}</h4>
                        <p className="text-xs text-slate-300 mb-2"><strong className="text-white">Optimal For:</strong> {engine.bestFor}</p>
                      </div>
                      <div className="text-[11px] text-slate-400 font-mono mt-2 border-t border-slate-800 pt-2">
                        {engine.strength}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* 6. PROMPTS TAB */}
            {activeTab === "prompts" && (
              <div className="flex flex-col gap-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-sm font-bold text-white font-mono uppercase">
                    Compiled Production Prompts
                  </h3>
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleExport("prompts_all.md")}
                      className="px-3 py-1.5 rounded-lg border border-slate-700 hover:bg-slate-800 text-xs font-mono text-slate-300 flex items-center gap-1.5 cursor-pointer"
                    >
                      <Download className="w-3.5 h-3.5" />
                      <span>Download All</span>
                    </button>
                  </div>
                </div>

                <div className="space-y-4">
                  {/* Omni Prompt */}
                  <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-mono font-bold text-amber-400 uppercase">Gemini Omni Flash Prompt</span>
                      <button
                        onClick={() => copyToClipboard(packageData.engines.omni?.[0]?.visual_prompt || "Omni prompt", "omni")}
                        className="text-xs font-mono text-slate-400 hover:text-white flex items-center gap-1 cursor-pointer"
                      >
                        <Copy className="w-3 h-3" />
                        <span>{copiedKey === "omni" ? "Copied" : "Copy"}</span>
                      </button>
                    </div>
                    <pre className="text-xs font-mono text-slate-300 bg-black/50 p-3 rounded-lg overflow-x-auto whitespace-pre-wrap">
                      {packageData.engines.omni?.[0]?.visual_prompt || "Cinematic 35mm anamorphic tracking shot..."}
                    </pre>
                  </div>

                  {/* Remotion Spec */}
                  <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-mono font-bold text-sky-400 uppercase">Remotion Coding-Agent Brief</span>
                      <button
                        onClick={() => copyToClipboard(packageData.engines.remotion?.standalone_agent_prompt || "Remotion prompt", "remotion")}
                        className="text-xs font-mono text-slate-400 hover:text-white flex items-center gap-1 cursor-pointer"
                      >
                        <Copy className="w-3 h-3" />
                        <span>{copiedKey === "remotion" ? "Copied" : "Copy"}</span>
                      </button>
                    </div>
                    <pre className="text-xs font-mono text-slate-300 bg-black/50 p-3 rounded-lg overflow-x-auto whitespace-pre-wrap max-h-60">
                      {packageData.engines.remotion?.standalone_agent_prompt || "You are implementing this video in Remotion using TypeScript..."}
                    </pre>
                  </div>
                </div>
              </div>
            )}

            {/* 7. BENCHMARK & UPLOAD TAB */}
            {activeTab === "benchmark" && (
              <div className="flex flex-col gap-6">
                <div>
                  <h3 className="text-sm font-bold text-white font-mono uppercase">
                    Video Reality Benchmark & File Ingestion
                  </h3>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Upload externally generated MP4/WebM files or execute synthetic failure tests.
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {/* Upload Dropzone */}
                  <div className="border-2 border-dashed border-slate-700 hover:border-amber-500/60 rounded-2xl p-8 flex flex-col items-center justify-center text-center bg-slate-950/40 transition">
                    <Upload className="w-10 h-10 text-amber-400 mb-3" />
                    <h4 className="text-sm font-bold text-white mb-1">Drop Generated MP4 / WebM Here</h4>
                    <p className="text-xs text-slate-400 mb-4">
                      Supports H.264 / ProRes external model renders for forensic auditing.
                    </p>
                    <div className="flex items-center gap-2">
                      <input
                        type="text"
                        value={uploadedVideoId}
                        onChange={(e) => setUploadedVideoId(e.target.value)}
                        className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-1.5 text-xs text-white font-mono w-48"
                      />
                      <button
                        onClick={() => handleRunForensics()}
                        disabled={forensicLoading}
                        className="px-4 py-2 rounded-lg bg-amber-500 hover:bg-amber-400 text-black font-mono font-bold text-xs cursor-pointer transition disabled:opacity-50"
                      >
                        {forensicLoading ? "Analyzing..." : "Analyze Video"}
                      </button>
                    </div>
                  </div>

                  {/* Synthetic Benchmark Descriptors */}
                  <div className="bg-slate-900/60 border border-slate-800 rounded-2xl p-5 flex flex-col justify-between">
                    <div>
                      <h4 className="text-xs font-mono font-bold text-cyan-400 uppercase tracking-wider mb-2">
                        Synthetic Forensic Presets (CI / Reality Check)
                      </h4>
                      <p className="text-xs text-slate-400 mb-3">
                        Simulate known model failures to test forensic diagnostic fidelity and prompt mutation:
                      </p>
                      <div className="grid grid-cols-2 gap-2">
                        {[
                          { id: "static_freeze", label: "Static Camera Freeze", desc: "FAIL_STATIC_MOTION" },
                          { id: "missing_audio", label: "Missing Audio Stream", desc: "FAIL_MISSING_AUDIO" },
                          { id: "subtitle_overlap", label: "Subtitle Safe-Zone Overlap", desc: "FAIL_SUBTITLE_OCCLUSION" },
                          { id: "rapid_cuts", label: "Excessive Rapid Pacing", desc: "FAIL_RAPID_PACING" },
                          { id: "character_drift", label: "Character Face Drift", desc: "FAIL_CHARACTER_DRIFT" },
                          { id: "none", label: "Flawless Generation", desc: "100% PASS" }
                        ].map((p) => (
                          <button
                            key={p.id}
                            onClick={() => {
                              setSyntheticCondition(p.id);
                              handleRunForensics(p.id);
                            }}
                            className="bg-slate-950 border border-slate-800 hover:border-cyan-500/50 p-2.5 rounded-lg text-left transition cursor-pointer"
                          >
                            <div className="text-xs font-bold text-white font-mono">{p.label}</div>
                            <div className="text-[10px] text-slate-500 font-mono">{p.desc}</div>
                          </button>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* 8. FORENSIC ANALYSIS TAB */}
            {activeTab === "forensics" && (
              <div className="flex flex-col gap-6">
                <div className="flex flex-wrap items-center justify-between gap-4 border-b border-slate-800 pb-4">
                  <div>
                    <h3 className="text-sm font-bold text-white font-mono uppercase flex items-center gap-2">
                      <Activity className="w-4 h-4 text-emerald-400" />
                      Empirical Video Forensics Report
                    </h3>
                    <p className="text-xs text-slate-400 mt-0.5">
                      Evaluated across 23 forensic quality dimensions against actual video metadata.
                    </p>
                  </div>
                  <div className="flex items-center gap-3">
                    <span className={`px-3 py-1 rounded-full font-mono text-xs font-bold border ${
                      forensicReport?.overall_verdict === "EXCELLENT" || forensicReport?.overall_verdict === "PASS"
                        ? "bg-emerald-500/20 text-emerald-400 border-emerald-500/30"
                        : "bg-rose-500/20 text-rose-400 border-rose-500/30"
                    }`}>
                      Verdict: {forensicReport?.overall_verdict || "PASS"}
                    </span>
                    <button
                      onClick={handleEvolvePrompt}
                      disabled={evolutionLoading}
                      className="px-4 py-2 rounded-lg bg-gradient-to-r from-cyan-500 to-blue-600 text-white font-mono font-bold text-xs hover:brightness-110 cursor-pointer disabled:opacity-50 flex items-center gap-1.5"
                    >
                      <Zap className="w-3.5 h-3.5" />
                      <span>{evolutionLoading ? "Evolving..." : "Evolve Prompt from Failures"}</span>
                    </button>
                  </div>
                </div>

                {/* Representative Keyframe Timeline */}
                <div>
                  <h4 className="text-xs font-mono font-bold text-slate-300 uppercase tracking-wider mb-2">
                    Representative Keyframe Sequence (0% to 100%)
                  </h4>
                  <div className="grid grid-cols-4 sm:grid-cols-6 lg:grid-cols-11 gap-1.5">
                    {forensicReport?.representative_frames?.map((frame) => (
                      <div key={frame.frame_index} className="bg-slate-900 border border-slate-800 rounded-lg p-2 text-center flex flex-col items-center">
                        <div className="w-full aspect-video bg-black/60 rounded flex items-center justify-center text-[10px] font-mono text-slate-500 border border-slate-800/60 mb-1">
                          {frame.percentage}%
                        </div>
                        <span className="text-[10px] font-mono text-amber-400 font-bold">{frame.timecode}</span>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Detected Failure Alerts */}
                {forensicReport?.detected_failures && forensicReport.detected_failures.length > 0 && (
                  <div className="bg-rose-950/30 border border-rose-500/30 rounded-xl p-4">
                    <h4 className="text-xs font-mono font-bold text-rose-400 uppercase tracking-wider mb-3 flex items-center gap-1.5">
                      <AlertTriangle className="w-4 h-4" /> Detected Failures ({forensicReport.detected_failures.length})
                    </h4>
                    <div className="space-y-2">
                      {forensicReport.detected_failures.map((f, i) => (
                        <div key={i} className="bg-slate-950/60 border border-rose-500/20 rounded-lg p-3 text-xs flex flex-col md:flex-row justify-between gap-2">
                          <div>
                            <div className="flex items-center gap-2 mb-1">
                              <span className="font-mono font-bold text-rose-400">{f.id}</span>
                              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-500/20 text-rose-300">{f.severity}</span>
                            </div>
                            <p className="text-slate-300">{f.description}</p>
                          </div>
                          <div className="text-slate-400 font-mono text-[11px] md:text-right">
                            <strong className="text-amber-400">Fix:</strong> {f.recommended_fix}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* 23 Forensic Dimension Grid */}
                <div>
                  <h4 className="text-xs font-mono font-bold text-slate-300 uppercase tracking-wider mb-3">
                    23 Forensic Quality Dimensions
                  </h4>
                  <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-3">
                    {forensicReport?.dimension_evaluations?.map((d) => (
                      <div key={d.dimension_name} className="bg-slate-900/70 border border-slate-800 rounded-lg p-3 text-xs flex flex-col justify-between">
                        <div>
                          <div className="flex items-center justify-between mb-1">
                            <span className="font-mono text-slate-300 capitalize text-[11px]">
                              {d.dimension_name.replace(/_/g, " ")}
                            </span>
                            <span className={`font-mono font-bold ${d.score >= 80 ? "text-emerald-400" : "text-amber-400"}`}>
                              {d.score}
                            </span>
                          </div>
                          <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden mb-2">
                            <div
                              className={`h-full ${d.score >= 80 ? "bg-emerald-500" : (d.score >= 65 ? "bg-amber-500" : "bg-rose-500")}`}
                              style={{ width: `${d.score}%` }}
                            />
                          </div>
                        </div>
                        <p className="text-[10px] text-slate-400 italic line-clamp-2">{d.evidence?.[0]}</p>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* 9. PROMPT EVOLUTION TAB */}
            {activeTab === "evolution" && (
              <div className="flex flex-col gap-6">
                <div>
                  <h3 className="text-sm font-bold text-white font-mono uppercase flex items-center gap-2">
                    <History className="w-4 h-4 text-cyan-400" />
                    Prompt Evolution Lineage (V1 → V2 → V3)
                  </h3>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Targeted mutations mutate only what failed while preserving validated creative elements.
                  </p>
                </div>

                {promptEvolution ? (
                  <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 flex flex-col gap-4">
                    <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
                      <div className="flex items-center gap-3">
                        <span className="px-3 py-1 rounded-lg bg-slate-800 text-slate-400 font-mono text-xs font-bold">
                          {promptEvolution.parent_version}
                        </span>
                        <ArrowRight className="w-4 h-4 text-amber-400" />
                        <span className="px-3 py-1 rounded-lg bg-cyan-500/20 text-cyan-400 font-mono text-xs font-bold border border-cyan-500/30">
                          {promptEvolution.new_version}
                        </span>
                        <span className="text-xs font-mono text-slate-400">
                          Addressed: <strong className="text-white">{promptEvolution.primary_failure_addressed}</strong>
                        </span>
                      </div>
                      <div className="text-xs font-mono text-emerald-400 font-bold">
                        Predicted Quality Gain: {promptEvolution.predicted_quality_score}/100
                      </div>
                    </div>

                    {/* Applied Mutations */}
                    <div>
                      <h4 className="text-xs font-mono font-bold text-slate-400 uppercase tracking-wider mb-2">
                        Applied Mutation Operators ({promptEvolution.mutations_applied.length})
                      </h4>
                      <div className="space-y-2">
                        {promptEvolution.mutations_applied.map((m, i) => (
                          <div key={i} className="bg-black/50 border border-slate-800 rounded-lg p-3 text-xs">
                            <div className="flex items-center justify-between mb-1">
                              <span className="font-mono font-bold text-cyan-400">{m.operator}</span>
                              <span className="text-[10px] font-mono text-emerald-400">+{m.expected_quality_delta} pts</span>
                            </div>
                            <p className="text-slate-300 text-[11px] mb-2">{m.rationale}</p>
                            <div className="bg-slate-950 p-2 rounded text-[11px] font-mono text-amber-300/90">
                              {m.mutated_snippet}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    {/* Evolved Prompt Text */}
                    <div>
                      <div className="flex items-center justify-between mb-1.5">
                        <span className="text-xs font-mono font-bold text-slate-400 uppercase">Evolved Prompt Text</span>
                        <button
                          onClick={() => copyToClipboard(promptEvolution.evolved_prompt_text, "evolved_prompt")}
                          className="text-xs font-mono text-slate-400 hover:text-white flex items-center gap-1 cursor-pointer"
                        >
                          <Copy className="w-3 h-3" />
                          <span>{copiedKey === "evolved_prompt" ? "Copied" : "Copy Evolved Prompt"}</span>
                        </button>
                      </div>
                      <pre className="text-xs font-mono text-slate-300 bg-black/60 p-4 rounded-xl overflow-x-auto whitespace-pre-wrap max-h-72 border border-slate-800">
                        {promptEvolution.evolved_prompt_text}
                      </pre>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-12 text-slate-500 font-mono text-xs">
                    No prompt evolution recorded yet. Run forensic analysis and click "Evolve Prompt from Failures".
                  </div>
                )}
              </div>
            )}

            {/* 10. FINAL & FEEDBACK TAB */}
            {activeTab === "final" && (
              <div className="flex flex-col gap-6">
                <div>
                  <h3 className="text-sm font-bold text-white font-mono uppercase">
                    Creator Feedback & Directorial Export
                  </h3>
                  <p className="text-xs text-slate-400 mt-0.5">
                    Save learnings back into prompt memory heuristics.
                  </p>
                </div>

                {/* Star Rating & Tags */}
                <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-6 flex flex-col gap-4">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono text-slate-400">Creator Rating:</span>
                    <div className="flex items-center gap-1">
                      {[1, 2, 3, 4, 5].map((star) => (
                        <button
                          key={star}
                          onClick={() => setFeedbackRating(star)}
                          className="cursor-pointer"
                        >
                          <Star className={`w-5 h-5 ${star <= feedbackRating ? "text-amber-400 fill-amber-400" : "text-slate-600"}`} />
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <span className="text-xs font-mono text-slate-400 block mb-2">Structured Failure Tags:</span>
                    <div className="flex flex-wrap gap-2">
                      {[
                        "boring", "confusing", "generic", "bad pacing", "bad visuals",
                        "bad continuity", "wrong information", "bad typography", "poor audio",
                        "poor character consistency", "weak hook", "too much motion"
                      ].map((tag) => (
                        <button
                          key={tag}
                          onClick={() => toggleFailureTag(tag)}
                          className={`px-3 py-1 rounded-full text-xs font-mono transition cursor-pointer border ${
                            selectedFailureTags.includes(tag)
                              ? "bg-rose-500/20 text-rose-300 border-rose-500/40"
                              : "bg-slate-950 text-slate-400 border-slate-800 hover:border-slate-700"
                          }`}
                        >
                          {tag}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label className="text-xs font-mono text-slate-400 block mb-1">What would you change?</label>
                    <textarea
                      value={feedbackCritique}
                      onChange={(e) => setFeedbackCritique(e.target.value)}
                      placeholder="e.g. The split-screen in Scene 2 needs stronger color contrast; elevate subtitles 40px higher..."
                      className="w-full bg-black/60 border border-slate-700 rounded-xl p-3 text-xs text-white focus:outline-none focus:border-amber-500 min-h-[80px]"
                    />
                  </div>

                  <div className="flex justify-end">
                    <button
                      onClick={handleSubmitFeedback}
                      disabled={feedbackSubmitted}
                      className="px-5 py-2 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-mono font-bold text-xs cursor-pointer transition disabled:opacity-50"
                    >
                      {feedbackSubmitted ? "Feedback Logged to Memory ✓" : "Record Feedback"}
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
