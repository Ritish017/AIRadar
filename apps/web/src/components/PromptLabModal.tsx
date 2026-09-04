import React, { useState, useEffect } from "react";
import { 
  X, Video, Copy, Check, Sparkles, Film, Code, 
  Layers, Sliders, RefreshCw, Play 
} from "lucide-react";
import { V3Event, OmniPromptPayload, StoryboardScene } from "../types";

interface PromptLabModalProps {
  event: V3Event | null;
  isOpen: boolean;
  onClose: () => void;
}

export const PromptLabModal: React.FC<PromptLabModalProps> = ({
  event,
  isOpen,
  onClose
}) => {
  const [activeEngine, setActiveEngine] = useState<"omni" | "remotion" | "hyperframes" | "storyboard">("omni");
  const [loading, setLoading] = useState<boolean>(false);
  const [omniPrompt, setOmniPrompt] = useState<OmniPromptPayload | null>(null);
  const [remotionData, setRemotionData] = useState<any | null>(null);
  const [hyperframesData, setHyperframesData] = useState<any | null>(null);
  const [storyboardScenes, setStoryboardScenes] = useState<StoryboardScene[]>([]);
  const [copied, setCopied] = useState<boolean>(false);
  const [stylePreset, setStylePreset] = useState<string>("Cinematic Tech News");
  const [aspectRatio, setAspectRatio] = useState<string>("9:16");

  const compilePrompts = async () => {
    if (!event) return;
    setLoading(true);
    try {
      // 1. Compile Omni prompt
      const omniRes = await fetch("/api/prompts/omni", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic: event.title,
          scene_description: event.summary,
          aspect_ratio: aspectRatio,
          style: stylePreset
        })
      });
      if (omniRes.ok) {
        const d = await omniRes.json();
        setOmniPrompt(d.omni_prompt);
      }

      // 2. Compile Remotion prompt
      const remRes = await fetch("/api/prompts/remotion", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic: event.title,
          metrics: { "Viral Potential": `${event.momentum_score}/100`, "Throughput": "4x", "Cost": "-70%" }
        })
      });
      if (remRes.ok) {
        const d = await remRes.json();
        setRemotionData(d.remotion_prompt);
      }

      // 3. Compile HyperFrames prompt
      const hfRes = await fetch("/api/prompts/hyperframes", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic: event.title,
          badge: event.status
        })
      });
      if (hfRes.ok) {
        const d = await hfRes.json();
        setHyperframesData(d.hyperframes_prompt);
      }

      // 4. Compile 6-Scene Storyboard
      const sbRes = await fetch("/api/prompts/storyboard", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: event.title,
          key_claims: event.key_facts || [event.title],
          counterpoint: "Context retention under multi-turn agent execution"
        })
      });
      if (sbRes.ok) {
        const d = await sbRes.json();
        setStoryboardScenes(d.storyboard.scenes || []);
      }
    } catch (err) {
      console.error("Failed to compile video prompts", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isOpen && event) {
      compilePrompts();
    }
  }, [isOpen, event, stylePreset, aspectRatio]);

  if (!isOpen || !event) return null;

  const handleCopy = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-6 bg-black/85 backdrop-blur-md overflow-y-auto">
      <div className="bg-[#090d16] border border-slate-700 rounded-2xl w-full max-w-4xl max-h-[90vh] flex flex-col shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="p-4 sm:p-5 border-b border-slate-800 flex items-center justify-between bg-[#0e1322]">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-lg bg-rose-500/20 border border-rose-500/30">
              <Video className="w-5 h-5 text-rose-400" />
            </div>
            <div>
              <h2 className="text-base sm:text-lg font-black text-white flex items-center gap-2">
                Video & Motion Prompt Lab
                <span className="bg-rose-500/20 text-rose-300 border border-rose-500/30 text-[10px] font-mono px-2 py-0.5 rounded font-bold">
                  MULTI-MODEL ROUTER
                </span>
              </h2>
              <p className="text-xs text-slate-400 line-clamp-1">{event.title}</p>
            </div>
          </div>

          <button onClick={onClose} className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Engine Tabs */}
        <div className="bg-[#0b0f19] px-5 py-2.5 border-b border-slate-800 flex flex-wrap items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setActiveEngine("omni")}
              className={`px-3 py-1.5 rounded-lg font-mono font-semibold transition flex items-center gap-1.5 ${
                activeEngine === "omni"
                  ? "bg-rose-950 text-rose-300 border border-rose-800"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Film className="w-3.5 h-3.5" />
              <span>Gemini Omni (Cinematic 20-Field)</span>
            </button>

            <button
              onClick={() => setActiveEngine("remotion")}
              className={`px-3 py-1.5 rounded-lg font-mono font-semibold transition flex items-center gap-1.5 ${
                activeEngine === "remotion"
                  ? "bg-sky-950 text-sky-300 border border-sky-800"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Code className="w-3.5 h-3.5 text-sky-400" />
              <span>Remotion (React Canvas)</span>
            </button>

            <button
              onClick={() => setActiveEngine("hyperframes")}
              className={`px-3 py-1.5 rounded-lg font-mono font-semibold transition flex items-center gap-1.5 ${
                activeEngine === "hyperframes"
                  ? "bg-amber-950 text-amber-300 border border-amber-800"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Play className="w-3.5 h-3.5 text-amber-400" />
              <span>HyperFrames (HTML/GSAP)</span>
            </button>

            <button
              onClick={() => setActiveEngine("storyboard")}
              className={`px-3 py-1.5 rounded-lg font-mono font-semibold transition flex items-center gap-1.5 ${
                activeEngine === "storyboard"
                  ? "bg-violet-950 text-violet-300 border border-violet-800"
                  : "text-slate-400 hover:text-slate-200"
              }`}
            >
              <Layers className="w-3.5 h-3.5 text-violet-400" />
              <span>6-Scene Storyboard</span>
            </button>
          </div>

          {activeEngine === "omni" && (
            <div className="flex items-center gap-2 text-xs font-mono">
              <select
                value={aspectRatio}
                onChange={(e) => setAspectRatio(e.target.value)}
                className="bg-slate-900 border border-slate-700 text-slate-200 px-2 py-1 rounded"
              >
                <option value="9:16">9:16 Vertical</option>
                <option value="16:9">16:9 Widescreen</option>
                <option value="1:1">1:1 Square</option>
              </select>

              <select
                value={stylePreset}
                onChange={(e) => setStylePreset(e.target.value)}
                className="bg-slate-900 border border-slate-700 text-slate-200 px-2 py-1 rounded"
              >
                <option value="Cinematic Tech News">Cinematic Tech News</option>
                <option value="Dark Cyberpunk Lab">Dark Cyberpunk Lab</option>
                <option value="Minimalist Studio">Minimalist Studio</option>
              </select>
            </div>
          )}
        </div>

        {/* Content Body */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4">
          {loading ? (
            <div className="py-20 text-center space-y-3">
              <RefreshCw className="w-8 h-8 text-rose-400 animate-spin mx-auto" />
              <p className="text-xs font-mono text-slate-400">Compiling multi-model prompt configurations...</p>
            </div>
          ) : (
            <>
              {/* OMNI ENGINE */}
              {activeEngine === "omni" && omniPrompt && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono text-slate-400 font-bold">
                      COMPILED MASTER PROMPT (20-FIELD STRUCTURED)
                    </span>
                    <button
                      onClick={() => handleCopy(omniPrompt.compiled_master_prompt)}
                      className="flex items-center gap-1 text-xs font-mono bg-slate-800 hover:bg-slate-700 text-slate-200 px-2.5 py-1 rounded transition"
                    >
                      {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                      <span>Copy Master Prompt</span>
                    </button>
                  </div>

                  <div className="bg-[#070a12] p-4 rounded-xl border border-slate-800 font-mono text-xs text-slate-200 whitespace-pre-wrap leading-relaxed">
                    {omniPrompt.compiled_master_prompt}
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                    <div className="bg-[#0d121f] p-3 rounded-lg border border-slate-800 space-y-1">
                      <span className="text-slate-500 font-mono">Camera:</span>
                      <p className="text-slate-200">{omniPrompt.camera.shot}, {omniPrompt.camera.lens}, {omniPrompt.camera.movement}</p>
                    </div>
                    <div className="bg-[#0d121f] p-3 rounded-lg border border-slate-800 space-y-1">
                      <span className="text-slate-500 font-mono">Lighting & Materials:</span>
                      <p className="text-slate-200">{omniPrompt.lighting} | {omniPrompt.materials}</p>
                    </div>
                  </div>
                </div>
              )}

              {/* REMOTION ENGINE */}
              {activeEngine === "remotion" && remotionData && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono text-slate-400 font-bold">REMOTION REACT COMPOSITION SPEC</span>
                    <button
                      onClick={() => handleCopy(remotionData.render_command)}
                      className="text-xs font-mono bg-sky-900/60 hover:bg-sky-800 text-sky-200 px-2.5 py-1 rounded transition flex items-center gap-1"
                    >
                      <Copy className="w-3.5 h-3.5" />
                      <span>Copy Render Command</span>
                    </button>
                  </div>

                  <div className="bg-[#070a12] p-4 rounded-xl border border-slate-800 font-mono text-xs text-sky-300 whitespace-pre-wrap">
                    {remotionData.render_command}
                  </div>

                  <div className="bg-[#0e1322] p-4 rounded-xl border border-slate-800 space-y-2 text-xs">
                    <span className="font-mono text-slate-400 font-bold">Timeline Scene Breakdown (30 FPS):</span>
                    <div className="space-y-2">
                      {remotionData.timeline_scenes.map((scene: any, idx: number) => (
                        <div key={idx} className="flex items-center justify-between bg-slate-900 p-2.5 rounded border border-slate-800">
                          <span className="text-slate-300 font-semibold">{scene.component}</span>
                          <span className="font-mono text-slate-500">Frame {scene.from} to {scene.from + scene.duration} ({scene.duration / 30}s)</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              {/* HYPERFRAMES ENGINE */}
              {activeEngine === "hyperframes" && hyperframesData && (
                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-mono text-slate-400 font-bold">HTML-NATIVE MARKUP & PAUSED GSAP TIMELINE</span>
                    <button
                      onClick={() => handleCopy(hyperframesData.html_markup + "\n\n" + hyperframesData.gsap_timeline_code)}
                      className="text-xs font-mono bg-amber-950/60 hover:bg-amber-900 text-amber-200 px-2.5 py-1 rounded transition flex items-center gap-1"
                    >
                      <Copy className="w-3.5 h-3.5" />
                      <span>Copy HTML & GSAP</span>
                    </button>
                  </div>

                  <div className="space-y-2">
                    <span className="text-[11px] font-mono text-slate-500">HTML Container Markup:</span>
                    <pre className="bg-[#070a12] p-3 rounded-lg border border-slate-800 text-[11px] text-amber-300 overflow-x-auto">
                      {hyperframesData.html_markup}
                    </pre>
                  </div>

                  <div className="space-y-2">
                    <span className="text-[11px] font-mono text-slate-500">Paused GSAP Timeline:</span>
                    <pre className="bg-[#070a12] p-3 rounded-lg border border-slate-800 text-[11px] text-emerald-300 overflow-x-auto">
                      {hyperframesData.gsap_timeline_code}
                    </pre>
                  </div>
                </div>
              )}

              {/* 6-SCENE STORYBOARD */}
              {activeEngine === "storyboard" && (
                <div className="space-y-3">
                  <h3 className="text-xs font-mono font-bold text-slate-400 uppercase">30-Second High-Retention Storyboard</h3>
                  <div className="space-y-3">
                    {storyboardScenes.map((scene) => (
                      <div key={scene.scene_number} className="bg-[#0d121f] border border-slate-800 rounded-xl p-3.5 text-xs space-y-2">
                        <div className="flex items-center justify-between">
                          <span className="font-mono text-violet-400 font-bold">
                            Scene {scene.scene_number} ({scene.timecode}) - {scene.beat_type}
                          </span>
                          <span className="font-mono text-[10px] bg-slate-800 text-slate-300 px-2 py-0.5 rounded">
                            Engine: {scene.recommended_engine}
                          </span>
                        </div>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          <div>
                            <span className="text-slate-500 font-mono text-[10px]">Narration Voiceover:</span>
                            <p className="text-white font-medium">{scene.narration}</p>
                          </div>
                          <div>
                            <span className="text-slate-500 font-mono text-[10px]">Visual & Camera:</span>
                            <p className="text-slate-300">{scene.visual_direction} ({scene.camera_instruction})</p>
                          </div>
                        </div>

                        <div className="bg-slate-900/80 p-2 rounded text-[10px] text-slate-400 border border-slate-800 flex items-center justify-between">
                          <span><strong>Asset Prompt: </strong>{scene.asset_prompt}</span>
                          <button onClick={() => handleCopy(scene.asset_prompt)} className="p-1 hover:text-white">
                            <Copy className="w-3 h-3" />
                          </button>
                        </div>
                      </div>
                    ))}
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
