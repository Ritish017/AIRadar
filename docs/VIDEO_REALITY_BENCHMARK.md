# AI Viral Radar V3.3: Video Reality Benchmark

## 1. Primary Product Principle & The Reality Shift

In legacy AI video prompt tools, quality is almost universally conflated with prompt syntax:
> *"The prompt compiler produced valid JSON with high descriptive vocabulary, therefore the video quality is 98/100."*

**AI Viral Radar V3.3 explicitly rejects this assumption.**

A structurally valid prompt can still produce an unwatchable, boring, or severely corrupted video when rendered by external diffusion models. V3.3 strictly decouples specification quality from empirical output quality, reporting a triad of distinct scores:

```
┌─────────────────────────────────────────────────────────────┐
│                   V3.3 TRIAD QUALITY METRIC                  │
├─────────────────────────────────────────────────────────────┤
│ 1. Prompt Readiness:        98.5 / 100  (Specification)     │
│ 2. Expected Executability:  92.0 / 100  (Model Match)       │
│ 3. Actual Video Quality:    71.2 / 100  (Forensic Reality)  │
└─────────────────────────────────────────────────────────────┘
```

The system stops measuring only whether prompts are syntactically valid and starts measuring whether those prompts produce compelling, coherent, executable videos.

---

## 2. End-to-End Creative Intelligence Loop

```mermaid
graph TD
    A[Real World Event / Trend] --> B[Content Intelligence & Angle]
    B --> C[Visual Concept Engine]
    C --> D[Storyboard Engine]
    D --> E[Shot Director & Complexity Analyzer]
    E --> F[Continuity Engine & Anti-Slop Audit]
    F --> G[Story-First Model Router]
    G --> H[Model Prompt Compilers]
    H --> I[External Video Generation / Upload]
    I --> J[Video Forensic Analyzer (23 Dimensions)]
    J --> K[Hierarchical Failure Classifier]
    K --> L[Prompt-vs-Output Diagnostics]
    L --> M[Prompt Evolution Engine (V1 -> V2 -> V3)]
    M --> H
    J --> N[Prompt Memory & Learned Heuristics]
```

---

## 3. External Video Ingestion & Validation Workflow

AI Viral Radar is an **AI Creative Director, Compiler, and Quality Intelligence System**. It does not assume that external generation is always executed locally in-process.

### Supported Production Workflow:
1. **Generate Prompt**: Compile production-ready specifications for Gemini Omni, Google Veo, Remotion, or HyperFrames.
2. **Copy Prompt**: 1-click copy into external tools or coding agents.
3. **Generate Externally**: Render with Gemini Omni Flash, Google Veo, or headlessly via `npx remotion render`.
4. **Upload Result**: Ingest the generated MP4/MOV/WebM back into the Video Reality Benchmark.
5. **Forensic Analysis**: Extract physical stream parameters, audit 23 forensic dimensions, generate keyframe timeline (0%–100%), and detect failures.
6. **Diagnose & Evolve**: Automatically identify why the model drifted from directorial intent and mutate the prompt (e.g. inject linear camera dolly vectors, tighten character anchors, elevate platform safe-zone margins).
7. **Generate Again**: Copy revised prompt V2 and re-render with higher predicted quality.

---

## 4. The 10 Golden Benchmark Suites

Located in `benchmarks/video/`, each benchmark represents a distinct creative challenge with complete input-to-output artifacts:

| Benchmark Case | Category | Expected Visual Concept | Expected Engine Routing | Key Reality Challenge |
| :--- | :--- | :--- | :--- | :--- |
| `001_ai_model_launch` | Product | Split-Screen / Macro Semiconductor | HYBRID (Omni + Remotion) | Dual-stream latency contrast |
| `002_benchmark_comparison` | Data | Data Visualization / Dynamic Chart | REMOTION | Zero hallucinated numbers |
| `003_future_scenario` | Cinematic | Photorealistic Daylight Cityscape | GEMINI OMNI / VEO | Zero neon cyberpunk clichés |
| `004_technical_interface` | Technical | Code Diff / Terminal Stream | HYPERFRAMES | DOM legibility at 60 FPS |
| `005_research_explainer` | Educational | Mathematical Matrix / Attention Flow | HYBRID (Math + Particles) | Rigorous pedagogical intuition |
| `006_character_dialogue` | Character | Shot-Reverse-Shot Conversation | VEO (Character Bible Anchor) | Cross-cut facial bone drift |
| `007_instagram_reel` | Social Short | Kinetic Typography / Split Screen | HYBRID (Veo + Remotion) | First 1.5s retention hook |
| `008_youtube_short` | Social Short | Macro Chip Detail + Bandwidth Gauge | HYBRID (Omni + Remotion) | Semiconductor physics clarity |
| `009_youtube_explainer` | Long-form | Historical Timeline / Multi-Scene | HYBRID MULTI-SCENE | 120s narrative arc coherence |
| `010_breaking_news` | News | Documentary / Source Quotes | HYBRID (Remotion + Archive) | Strict journalistic grounding |

Each suite contains:
- `event.json`
- `content_brief.json`
- `visual_concepts.json`
- `storyboard.json`
- `prompts/` (`omni_prompt_v1.txt`, `veo_prompt_v1.txt`, `remotion_spec_v1.json`, `hyperframes_spec_v1.json`)
- `generated/` (`manifest.json`)
- `evaluation/` (`forensic_report.json`, `failure_classification.json`, `prompt_diagnostics.json`)
- `human_feedback.json`
- `evolution/` (`prompt_evolution.json`)

---

## 5. Synthetic Forensic Test Suite

To guarantee analyzer reliability in continuous integration, `tests/test_v3_3_synthetic_forensics.py` verifies deterministic failure detection:
- **Test Video A (Static Freeze)**: Verifies `FAIL_STATIC_MOTION` detection when optical flow vectors remain zero; mutates camera trajectory to continuous linear dolly.
- **Test Video B (Rapid Cuts)**: Verifies `FAIL_RAPID_PACING` when scene transitions exceed cognitive limits; decomposes beats into 3.0s holds.
- **Test Video C (Temporal Stutter)**: Verifies `FAIL_TEMPORAL_STUTTER` on repeated identical frames.
- **Test Video D (Wrong Resolution)**: Verifies `FAIL_WRONG_ASPECT_RATIO` when 16:9 is uploaded for vertical 9:16 distribution.
- **Test Video E (Missing Audio)**: Verifies `FAIL_MISSING_AUDIO` critical severity failure.
- **Test Video F (Safe-Zone Overlap)**: Verifies `FAIL_SUBTITLE_OCCLUSION` when text overlaps TikTok/Reels UI dead-zones.
