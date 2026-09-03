import React, { useState, useEffect } from "react";
import { VoiceProfile } from "../types";
import { fetchVoiceProfile, updateVoiceProfile } from "../lib/api";
import { Mic, Plus, Trash2, Check, Sparkles } from "lucide-react";

export const VoiceProfileView: React.FC = () => {
  const [profile, setProfile] = useState<VoiceProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [savedSuccess, setSavedSuccess] = useState(false);
  const [newExample, setNewExample] = useState("");

  useEffect(() => {
    fetchVoiceProfile()
      .then((res) => {
        setProfile(res);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching voice profile:", err);
        setLoading(false);
      });
  }, []);

  const handleSave = async () => {
    if (!profile) return;
    try {
      const updated = await updateVoiceProfile(profile);
      setProfile(updated);
      setSavedSuccess(true);
      setTimeout(() => setSavedSuccess(false), 2500);
    } catch (err) {
      console.error("Error updating voice profile:", err);
    }
  };

  const handleAddExample = () => {
    if (!newExample.trim() || !profile) return;
    setProfile({
      ...profile,
      voice_examples: [...profile.voice_examples, newExample.trim()]
    });
    setNewExample("");
  };

  const handleRemoveExample = (idx: number) => {
    if (!profile) return;
    const updated = [...profile.voice_examples];
    updated.splice(idx, 1);
    setProfile({ ...profile, voice_examples: updated });
  };

  if (loading) {
    return (
      <div className="py-20 text-center text-slate-400">
        <Sparkles className="w-8 h-8 animate-spin mx-auto mb-2 text-brand-400" />
        <p>Loading personal voice calibration...</p>
      </div>
    );
  }

  if (!profile) return null;

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      <div>
        <h2 className="text-xl font-bold text-white tracking-tight flex items-center space-x-2">
          <Mic className="w-5 h-5 text-brand-400" />
          <span>My Voice Persona</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Train the AI post generator to mimic your unique cadence, sentence rhythms, technical depth, and formatting.
        </p>
      </div>

      <div className="glass-panel rounded-2xl p-6 space-y-6 border border-slate-800">
        {/* Profile Name & Tone */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Persona Name
            </label>
            <input
              type="text"
              value={profile.name}
              onChange={(e) => setProfile({ ...profile, name: e.target.value })}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Preferred Tone Baseline
            </label>
            <input
              type="text"
              value={profile.tone_preference}
              onChange={(e) => setProfile({ ...profile, tone_preference: e.target.value })}
              placeholder="e.g. Technical, Authoritative, Sarcastic, Concise"
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2 text-sm text-white focus:border-brand-500 focus:outline-none"
            />
          </div>
        </div>

        {/* Writing Guidelines */}
        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
            Stylistic Rules & Constraints
          </label>
          <textarea
            rows={2}
            value={profile.guidelines || ""}
            onChange={(e) => setProfile({ ...profile, guidelines: e.target.value })}
            placeholder="e.g., Short sentences. Never use hashtags. Focus on production failure modes."
            className="w-full bg-slate-900 border border-slate-700 rounded-xl p-3 text-xs text-white focus:border-brand-500 focus:outline-none"
          />
        </div>

        {/* Examples List */}
        <div>
          <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">
            Reference Posts ({profile.voice_examples.length})
          </label>
          <p className="text-xs text-slate-500 mb-3">
            Add 2–5 authentic posts you have written in the past.
          </p>

          <div className="space-y-2.5 mb-4">
            {profile.voice_examples.map((ex, idx) => (
              <div
                key={idx}
                className="p-3.5 rounded-xl bg-slate-900/80 border border-slate-800 flex items-start justify-between gap-3 text-xs text-slate-200"
              >
                <span className="leading-relaxed">"{ex}"</span>
                <button
                  onClick={() => handleRemoveExample(idx)}
                  className="p-1 text-slate-500 hover:text-rose-400 transition flex-shrink-0"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            ))}
          </div>

          {/* Add New Example */}
          <div className="flex gap-2">
            <input
              type="text"
              value={newExample}
              onChange={(e) => setNewExample(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleAddExample()}
              placeholder="Paste an authentic post example here..."
              className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2 text-xs text-white focus:border-brand-500 focus:outline-none"
            />
            <button
              onClick={handleAddExample}
              className="px-4 py-2 rounded-xl text-xs font-semibold bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 flex items-center space-x-1"
            >
              <Plus className="w-3.5 h-3.5" />
              <span>Add</span>
            </button>
          </div>
        </div>

        {/* Save Button */}
        <div className="flex items-center justify-end space-x-3 pt-4 border-t border-slate-800">
          {savedSuccess && (
            <span className="text-xs text-emerald-400 font-semibold flex items-center space-x-1">
              <Check className="w-4 h-4" />
              <span>Voice profile saved!</span>
            </span>
          )}
          <button
            onClick={handleSave}
            className="px-6 py-2.5 rounded-xl text-xs font-bold bg-brand-600 hover:bg-brand-500 text-white transition shadow-lg shadow-brand-500/25"
          >
            Save Voice Profile
          </button>
        </div>
      </div>
    </div>
  );
};
