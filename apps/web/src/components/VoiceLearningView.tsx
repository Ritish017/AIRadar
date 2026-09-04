import React, { useState, useEffect } from "react";
import { Mic, BarChart3, Sparkles, Check, RefreshCw, Layers } from "lucide-react";
import { VoiceProfile } from "../types";

export const VoiceLearningView: React.FC = () => {
  const [profile, setProfile] = useState<VoiceProfile | null>(null);
  const [samplesText, setSamplesText] = useState<string>("");
  const [learningInsights, setLearningInsights] = useState<any[]>([]);
  const [calibrating, setCalibrating] = useState<boolean>(false);
  const [savedSuccess, setSavedSuccess] = useState<boolean>(false);

  // Performance recording form
  const [postTopic, setPostTopic] = useState<string>("");
  const [views, setViews] = useState<string>("");
  const [likes, setLikes] = useState<string>("");
  const [reposts, setReposts] = useState<string>("");
  const [comments, setComments] = useState<string>("");
  const [recordedRate, setRecordedRate] = useState<number | null>(null);

  const fetchProfile = async () => {
    try {
      const res = await fetch("/api/voice-profile");
      if (res.ok) {
        const data = await res.json();
        setProfile(data);
        if (data.voice_examples) {
          setSamplesText(data.voice_examples.join("\n\n---\n\n"));
        }
      }

      const lRes = await fetch("/api/performance/learning-profile");
      if (lRes.ok) {
        const ld = await lRes.json();
        setLearningInsights(ld.learned_insights || []);
      }
    } catch (err) {
      console.error("Failed to load voice profile", err);
    }
  };

  useEffect(() => {
    fetchProfile();
  }, []);

  const handleCalibrateVoice = async () => {
    const rawSamples = samplesText.split("\n\n---\n\n").map(s => s.trim()).filter(Boolean);
    if (rawSamples.length === 0) return;

    setCalibrating(true);
    try {
      const res = await fetch("/api/voice/calibrate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ samples: rawSamples })
      });

      if (res.ok) {
        const data = await res.json();
        setProfile(data.profile);
        setSavedSuccess(true);
        setTimeout(() => setSavedSuccess(false), 3000);
      }
    } catch (err) {
      console.error("Voice calibration failed", err);
    } finally {
      setCalibrating(false);
    }
  };

  const handleRecordPerformance = async () => {
    if (!postTopic) return;
    try {
      const res = await fetch("/api/performance", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          topic: postTopic,
          views: views ? parseInt(views) : null,
          likes: likes ? parseInt(likes) : null,
          reposts: reposts ? parseInt(reposts) : null,
          replies: comments ? parseInt(comments) : null
        })
      });

      if (res.ok) {
        const d = await res.json();
        setRecordedRate(d.engagement_rate);
        fetchProfile();
      }
    } catch (err) {
      console.error("Failed to record performance", err);
    }
  };

  return (
    <div className="space-y-6 pb-12">
      {/* Header */}
      <div className="bg-[#0d121f] border border-slate-800 p-5 rounded-xl">
        <h1 className="text-xl font-black text-white flex items-center gap-2">
          <Mic className="w-5 h-5 text-indigo-400" />
          Voice Learning Loop & Performance Calibration
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Iterative learning loop: AI analyzes your published content metrics and calibrates generation prompts to match your authentic voice.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Left Column: Voice Profile Analyzer */}
        <div className="lg:col-span-7 bg-[#0e1322] border border-slate-800 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-sm font-bold text-white">Voice Samples Analyzer</h2>
              <p className="text-xs text-slate-400">Paste 2 or 3 of your top-performing posts separated by '---'.</p>
            </div>

            <button
              onClick={handleCalibrateVoice}
              disabled={calibrating}
              className="bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold px-3.5 py-1.5 rounded-lg transition flex items-center gap-1.5"
            >
              <Sparkles className="w-3.5 h-3.5" />
              <span>{calibrating ? "Calibrating..." : "Calibrate Voice"}</span>
            </button>
          </div>

          <textarea
            rows={7}
            value={samplesText}
            onChange={(e) => setSamplesText(e.target.value)}
            placeholder="Inference latency is the only metric that matters for enterprise agent loops...&#10;&#10;---&#10;&#10;Tested the open weights on 4x A100. Throughput scales linearly up to batch 32."
            className="w-full bg-[#070a12] border border-slate-800 rounded-lg p-3 text-xs text-slate-200 font-sans focus:outline-none focus:border-indigo-500"
          />

          {savedSuccess && (
            <div className="flex items-center gap-2 text-xs text-emerald-400 font-mono">
              <Check className="w-4 h-4" />
              <span>Voice profile calibrated and saved to database successfully!</span>
            </div>
          )}

          {profile && (
            <div className="bg-[#070a12] border border-slate-800/80 rounded-lg p-4 space-y-2 text-xs">
              <div className="flex items-center justify-between">
                <span className="font-mono text-slate-400 font-bold">CURRENT DETECTED TONE</span>
                <span className="font-mono text-indigo-400 font-bold">{profile.tone_preference}</span>
              </div>
              <div>
                <span className="font-mono text-slate-500 text-[11px] block">ACTIVE GUIDELINES</span>
                <p className="text-slate-300 text-xs mt-0.5">{profile.guidelines}</p>
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Performance Telemetry & Recorder */}
        <div className="lg:col-span-5 space-y-5">
          {/* Record Metric Box */}
          <div className="bg-[#0e1322] border border-slate-800 rounded-xl p-5 space-y-3">
            <h2 className="text-sm font-bold text-white flex items-center gap-2">
              <BarChart3 className="w-4 h-4 text-emerald-400" />
              Log Real Post Performance
            </h2>
            <p className="text-xs text-slate-400">Empirical metrics teach the engine what performs with your audience.</p>

            <div className="space-y-2.5 text-xs">
              <div>
                <label className="text-slate-400 font-mono text-[10px] block mb-1">POST TOPIC / HEADLINE</label>
                <input
                  type="text"
                  value={postTopic}
                  onChange={(e) => setPostTopic(e.target.value)}
                  placeholder="DeepSeek-V3 Architecture"
                  className="w-full bg-[#070a12] border border-slate-800 rounded p-2 text-white"
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-slate-400 font-mono text-[10px] block mb-1">VIEWS (IMPRESSIONS)</label>
                  <input
                    type="number"
                    value={views}
                    onChange={(e) => setViews(e.target.value)}
                    placeholder="12500"
                    className="w-full bg-[#070a12] border border-slate-800 rounded p-2 text-white"
                  />
                </div>
                <div>
                  <label className="text-slate-400 font-mono text-[10px] block mb-1">LIKES</label>
                  <input
                    type="number"
                    value={likes}
                    onChange={(e) => setLikes(e.target.value)}
                    placeholder="420"
                    className="w-full bg-[#070a12] border border-slate-800 rounded p-2 text-white"
                  />
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div>
                  <label className="text-slate-400 font-mono text-[10px] block mb-1">REPOSTS</label>
                  <input
                    type="number"
                    value={reposts}
                    onChange={(e) => setReposts(e.target.value)}
                    placeholder="85"
                    className="w-full bg-[#070a12] border border-slate-800 rounded p-2 text-white"
                  />
                </div>
                <div>
                  <label className="text-slate-400 font-mono text-[10px] block mb-1">COMMENTS</label>
                  <input
                    type="number"
                    value={comments}
                    onChange={(e) => setComments(e.target.value)}
                    placeholder="34"
                    className="w-full bg-[#070a12] border border-slate-800 rounded p-2 text-white"
                  />
                </div>
              </div>

              <button
                onClick={handleRecordPerformance}
                className="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-semibold py-2 rounded text-xs transition mt-2"
              >
                Log Performance Data
              </button>

              {recordedRate !== null && (
                <div className="p-2.5 bg-emerald-950/60 border border-emerald-800/60 rounded text-center text-xs font-mono text-emerald-300">
                  Calculated Engagement Rate: <strong>{recordedRate}%</strong>
                </div>
              )}
            </div>
          </div>

          {/* Learned Insights */}
          <div className="bg-[#0e1322] border border-slate-800 rounded-xl p-5 space-y-3">
            <h3 className="text-xs font-mono font-bold text-slate-400 uppercase">
              Calibrated Audience Guidelines
            </h3>
            <div className="space-y-2 text-xs">
              {learningInsights.map((ins, i) => (
                <div key={i} className="flex items-start gap-2 bg-[#070a12] p-2.5 rounded border border-slate-800/80">
                  <span className="text-emerald-400 font-bold">•</span>
                  <p className="text-slate-300">{ins}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
