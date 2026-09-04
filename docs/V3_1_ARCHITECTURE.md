# AI Viral Radar V3.1 — Architectural Blueprint & System Specifications

**Document Version:** 3.1.0  
**System Classification:** Real-Time Global AI Intelligence & Content Operating System  
**Core Technologies:** Python 3.14, FastAPI, SQLAlchemy (Async SQLite), Firecrawl API, Google Gemini 2.5 (`google.genai`), React 18, Vite, TypeScript, TailwindCSS, Lucide Icons.  

---

## 1. System Overview & Ingestion Flow

AI Viral Radar V3.1 operates as an autonomous, high-precision intelligence radar and content synthesis operating system. It ingests global AI research and commercial breakthroughs, extracts verifiable facts, corroborates claims across independent sources, and manufactures platform-native assets.

```
┌────────────────────────────────────────────────────────────────────────┐
│                        AI VIRAL RADAR V3.1 FLOW                        │
└──────────────────────────────────┬─────────────────────────────────────┘
                                   │
     ┌─────────────────────────────┴─────────────────────────────┐
     ▼                                                           ▼
[Firecrawl Web Acquisition]                           [Official RSS Discovery]
- Deep Search & Batch Scraping                        - arXiv (cs.AI, cs.LG, cs.CL)
- Markdown Extraction                                 - Hugging Face Daily Papers
- Primary Source Resolver                             - GitHub Trending Releases
     │                                                           │
     └─────────────────────────────┬─────────────────────────────┘
                                   │
                                   ▼
                   [EventEngine: Clustering & Merging]
                   - Exact & Canonical Normalized URLs
                   - Span-Based Model & Tool Disambiguation
                   - Extended Window Corroborator (Multi-Phase Updates)
                   - Primary Source Quality Tiering
                                   │
                                   ▼
                    [ContradictionEngine: Validation]
                    - Percentage & Metric Delta Detector
                    - Benchmark Score Claim Inconsistencies
                    - Dispute Keywords ("dispute", "refutes", "falsified")
                    - Conflict Warning Injection & "WAIT" Gating
                                   │
                                   ▼
             [Trend & Signal Engine: Mathematical Forecasting]
             - Early Signal Detection (Velocity × Diversity)
             - Explosion Probability (Logistic Sigmoid Model)
             - Content Gap Engine (Saturated vs Underserved Angles)
                                   │
                                   ▼
                    [Multi-Platform Content Factory]
                    - Pre-Generation Brief (Claims & Contrarian Angles)
                    - 10-Hook Category Scorer & Candidate Generator
                    - X / LinkedIn / Instagram Carousel / YouTube Synthesizer
                    - 10-Dimension Quality & 3-gram Originality Gate
                                   │
                                   ▼
                     [Video Prompt Orchestrator]
                     - Remotion React / TypeScript Code
                     - Gemini Omni 8K Photorealistic Video Prompts
                     - HyperFrames Scene-by-Scene JSON Specs
```

---

## 2. Mathematical Formulations

### 2.1 Early Signal Score ($S_{\text{early}}$)
Quantifies whether an intelligence item represents an emerging breakout before mainstream saturation:

$$S_{\text{early}} = \min\left(100.0, \; \left(V_{\text{accel}} \times 0.35 + D_{\text{sources}} \times 0.30 + N_{\text{novelty}} \times 0.20 + Q_{\text{tier}} \times 0.15\right)\right)$$

Where:
* $V_{\text{accel}}$: Normalized acceleration of mentions over the last 6-hour window.
* $D_{\text{sources}}$: Source diversity entropy across distinct domains.
* $N_{\text{novelty}}$: Inverse lexical similarity against established 30-day topic clusters.
* $Q_{\text{tier}}$: Source authority score ($1.0$ for Tier 1 official/academic, $0.65$ for Tier 2 news, $0.35$ for Tier 3 social).

### 2.2 Explosion Probability ($P_{\text{explosion}}$)
Predicts the likelihood that an emerging trend continues its growth trajectory into viral breakout status:

$$P_{\text{explosion}} = \frac{1}{1 + e^{-k (S_{\text{early}} - x_0)}}$$

Where $k = 0.08$ and $x_0 = 50.0$.
* *Probabilistic Label:* Expressed strictly as `"MODEL ESTIMATE: X% probability of continued trajectory"`. The system never claims guaranteed virality.

### 2.3 Rolling Latency KPIs
Measures the operational health and pipeline velocity across the ingestion, verification, and analysis stages:

$$\text{Time-to-Radar (TTR)} = t_{\text{surfaced}} - t_{\text{published}}$$
$$\bar{L} = \frac{1}{N} \sum_{i=1}^N \text{TTR}_i, \quad M = \text{Median}(\text{TTR}), \quad P_{95} = \text{Quantile}_{0.95}(\text{TTR})$$

---

## 3. ContradictionEngine Architecture

The ContradictionEngine (`backend/services/events/contradiction_engine.py`) prevents false information and unverified hype from being promoted as confirmed intelligence.

### Detection Mechanisms:
1. **Benchmark Metric Conflict:** Detects conflicting numerical claims for the same benchmark (e.g., `"Anthropic reports 70.3% on SWE-bench"` vs `"SWE-bench maintainers report 49.2%"`).
2. **Dispute Keyword Extraction:** Flags explicit controversy triggers (`"dispute"`, `"refutes"`, `"falsified"`, `"unverified"`, `"benchleak"`, `"contamination"`).
3. **Automated Action Gating:**
   * Automatically changes Event Status to `DEVELOPING`.
   * Overrides Recommended Action to `WAIT`.
   * Sets Recommended Angle to `"Conflicting claims across sources. Await secondary replication."`
   * Injects `[CONFLICT DETECTED: <description>]` banner into the story summary.

---

## 4. Multi-Platform Content Factory & Originality Guard

The Content Factory synthesizes native copy for each social surface while enforcing strict quality controls:

* **Pre-Generation Content Brief:** Synthesizes `topic`, `target_audience`, `key_claims`, `counterpoint`, and `actionable_takeaway`.
* **N-gram Originality Evaluator:** Computes word 3-gram Jaccard overlap between the synthesized text and the raw source text:

$$J_{3\text{-gram}}(S, G) = \frac{|\text{ngrams}_3(S) \cap \text{ngrams}_3(G)|}{|\text{ngrams}_3(S) \cup \text{ngrams}_3(G)|}$$

* If $J < 0.20$: Originality Score $= 92.0$ (High Originality).
* If $J \ge 0.35$: Originality Score $= \max(55.0, (1 - J) \times 100)$ and triggers a re-phrase alert.

---

## 5. Hybrid Video Prompt Synthesis Architecture

The `VideoPromptOrchestrator` (`backend/services/video/video_orchestrator.py`) provides unified multi-engine compilation:

1. **Remotion Engine:** Emits full React / TypeScript files with motion physics, spring configurations, and theme tokens.
2. **Gemini Omni Engine:** Emits cinematic, photorealistic multi-modal generation prompts specifying lighting, lens geometry, and atmospheric foley.
3. **HyperFrames Engine:** Emits declarative, multi-track animation JSON graphs ready for cloud rendering pipelines.

---

## 6. Frontend Radar Terminal Architecture

The web application (`apps/web`) is built with React 18, Vite, and TailwindCSS:

* **Top Global Status Bar:** Displays active Time-to-Radar (Avg/Median/P95), live breaking and emerging counts, and real-time health badges for Firecrawl, Gemini, and SQLite.
* **Live Radar Feed:** Real-time stream of incoming events with verification badges (`CONFIRMED`, `DEVELOPING`, `LIKELY`, `UNVERIFIED`).
* **Conflict Warning Banners:** Prominently alerts creators when an event has conflicting source claims.
* **Content Generation Studio:** 1-click synthesis of X threads, LinkedIn posts, Instagram carousels, YouTube scripts, and Remotion/Gemini Omni video prompts.
* **Performance Learning Loop:** Allows creators to record impressions, saves, likes, and watch-time, which the `LearningEngine` utilizes to calibrate future hook weights.
