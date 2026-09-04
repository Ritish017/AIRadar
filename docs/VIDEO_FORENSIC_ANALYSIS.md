# AI Viral Radar V3.3: Video Forensic Analysis

## 1. Overview

The **Video Forensic Analyzer** (`backend/services/video/video_forensic_analyzer.py`) audits actual generated video files or synthetic manifests across **23 forensic quality dimensions**. It replaces subjective human guessing with empirical stream measurements and verified perceptual criteria.

---

## 2. Physical Stream Parameter Extraction

When a media file is provided, the forensic engine invokes `ffprobe` (falling back gracefully to pure filesystem heuristics):
- **Container Format & Codec**: `H.264`, `ProRes`, `AAC` stream validation.
- **Resolution & Aspect Ratio**: Exact pixel width, height, and ratio (`9:16`, `16:9`, `1:1`).
- **Framerate & Drift**: Verified FPS (`24.0`, `30.0`, `60.0`) and total frame count.
- **Audio Presence**: Verification of physical audio track, bit rate, and channel count.
- **Scene Cut Frequency**: Automatic detection of cut density over time.
- **Keyframe Generation**: Extraction of 11 representative keyframe positions at 0%, 10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, 90%, and 100% of duration.

---

## 3. The 23 Forensic Quality Dimensions

Each dimension is scored from 0.0 to 100.0, assigned a status (`PASS` &ge; 85, `WARN` 65–84, `FAIL` &lt; 65), and accompanied by concrete diagnostic evidence:

1. **narrative_clarity**: Does the visual storyline communicate the intended technical claim without ambiguity?
2. **hook_strength**: Does the first 1.5–2.0 seconds create an immediate visual pattern interrupt?
3. **visual_relevance**: Do on-screen elements directly illustrate the spoken narration, or are they arbitrary B-roll?
4. **story_progression**: Does the video evolve logically from context to proof to takeaway?
5. **shot_variety**: Is there adequate variation in framing, scale, and angle?
6. **pacing**: Is the cutting tempo matched to viewer cognitive processing capacity?
7. **motion_quality**: Is camera and subject motion smooth, motivated, and free of frozen optical flow?
8. **composition**: Are rule-of-thirds, center-weighting, and visual balance maintained?
9. **temporal_consistency**: Are frame transitions free of stutter, duplicate frame drops, and boiling?
10. **character_consistency**: Do facial features, eyewear, and clothing remain immutable across cuts?
11. **object_consistency**: Do persistent devices, chips, and tools maintain geometry across shots?
12. **text_accuracy**: Are on-screen letters, numbers, and symbols crisp, legible, and uncorrupted?
13. **typography_quality**: Does typography respect font hierarchy, weight, and tracking?
14. **audio_quality**: Is voiceover clearly audible with appropriate music ducking?
15. **lip_sync**: Do speech phonemes align with mouth shapes when characters speak?
16. **visual_artifacts**: Is the render free of edge tearing, compression banding, and noise?
17. **generative_glitches**: Is the render free of extra limbs, morphing objects, and surreal drift?
18. **continuity**: Does lighting temperature and environmental layout match across cuts?
19. **platform_fitness**: Does the video adhere to platform safe zones (e.g. TikTok/Reels UI margins)?
20. **originality**: Is the video free of repetitive clichés (neon cyberpunk, floating holograms)?
21. **information_density**: Is the visual delivery rich in insight per second?
22. **emotional_impact**: Does the creative treatment evoke the intended tone (urgency, awe, clarity)?
23. **professional_polish**: Does the composite look like commercial studio-grade production?

---

## 4. Visual Quality Gate & Verdict Policy

The overall verdict is determined by strict gatekeeping rules:

```python
# Failure penalties
failure_penalty = (len(crit_fails) * 16.0) + (len(high_fails) * 8.0)
actual_video_quality = max(10.0, round(base_quality - failure_penalty, 1))

# Gatekeeping verdict
if crit_fails or actual_video_quality < 65.0 or len(failed_dims) >= 2:
    verdict = "FAIL"
elif high_fails or failed_dims or warn_dims or actual_video_quality < 80.0:
    verdict = "WARN"
elif actual_video_quality >= 90.0 and not failed_dims and not warn_dims:
    verdict = "EXCELLENT"
else:
    verdict = "PASS"
```

A video with high narrative clarity but zero audio track will **never pass**; it immediately receives a `FAIL` verdict due to the critical audio failure.
