# AI Viral Radar V3 — Reality Audit (Phase 0)

This audit inspects every claimed feature in the V3 codebase to determine whether it is genuinely implemented, connected end-to-end, tested, production-ready, or if gaps exist that must be closed in V3.1.

---

## 1. Comprehensive Feature Matrix

| Feature | Implemented? | Connected? | Actually Used? | Tested? | Production Quality? | Problems / Gaps Identified | Recommended Fix for V3.1 |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- | :--- |
| **Firecrawl Web Layer** | Yes | Yes | Yes | Yes (`test_firecrawl_provider.py`) | High | Query list is relatively static; lacks dynamic queries generated from recent entities & trend acceleration. | Add dynamic query generator based on detected entities and trend velocity. |
| **RSS Fast Discovery** | Yes | Yes | Yes | Yes (`test_v3_core.py`) | Medium | Only polling configured feeds; lacks automated discovery signal trigger to search for primary source. | Add Primary Source Verification pipeline when discovery signal appears. |
| **Canonical Event Engine** | Yes | Yes | Yes | Yes (`test_v3_core.py`, `test_v3_e2e_pipeline.py`) | High | Multi-source clustering verified for 3 sources; needs stress testing on 10, 20, 50 sources to evaluate precision and false split/merge rates. | Create clustering precision benchmark on large multi-source fixtures. |
| **Contradiction Detection** | Partial | Partial | No | No | Low | Engine tags `CONFIRMED` or `LIKELY` based on source count, but doesn't explicitly detect conflicting facts (e.g. date discrepancies). | Build dedicated `ContradictionEngine` to flag conflicting reports and mark `DEVELOPING`. |
| **Pipeline Latency Tracking** | Yes | Yes | Yes | Yes | High | Calculates single-event `total_pipeline_latency`, but system lacks global rolling aggregates (Average, Median, P95 Time-to-Radar). | Add rolling latency KPI calculator (Avg, Median, P95) exposed on `/api/health` and status bar. |
| **Freshness Metrics** | Yes | Yes | Yes | Yes | Medium | Uses published timestamp; needs explicit `age_seconds` and `age_minutes` fields on every item and result. | Compute and serialize `age_seconds` and `age_minutes` on all events/news items. |
| **Early Signal Engine** | Yes | Yes | Yes | Yes (`test_v3_core.py`) | High | Works well; explosion probability needs clear UI labeling as "MODEL ESTIMATE" to maintain probabilistic discipline. | Explicitly label `explosion_probability` as model estimate in schemas and UI. |
| **Content Gap Engine** | Yes | Yes | Yes | Yes | High | Identifies 8 angles; needs expansion to 10 angles and explicit answers to: *"What is everyone saying? What should we NOT repeat? What is missing?"* | Add Critical Content Gap breakdown: Saturated take vs Underserved opportunity. |
| **𝕏 Hook Engine** | Yes | Yes | Yes | Yes | High | Generates 10 hooks and scores them, but always outputs top 1; needs explicit categorization of `BEST HOOK`, `SAFE ALTERNATIVE`, and `HIGH-RISK HOOK`. | Output classified hook recommendations: Best, Safe Alternative, High-Risk/High-Reward. |
| **𝕏 Post Structure** | Yes | Yes | Yes | Yes | Medium | Uses structured post/thread, but tends to default to standard structure; needs dynamic archetype selection (hot take, contrarian, lesson, etc.). | Dynamically select post format structure based on event category. |
| **Contextual CTAs** | Yes | Yes | Yes | Yes | High | Supported in factory; needs explicit `none` CTA option when hard CTAs feel spammy. | Ensure CTA generator can produce `None` when content is purely informative. |
| **Instagram Engine** | Yes | Yes | Yes | Yes | High | Generates 8-slide carousel and 35s Reel; needs visual prompts per slide and timed beats. | Enhance carousel slide asset prompts and reel timestamps. |
| **YouTube Engine** | Yes | Yes | Yes | Yes | High | 10 titles, 3 thumbnails, scripts present; needs structured Retention Risk analysis (`LOW`, `MEDIUM`, `HIGH`). | Implement YouTube retention model with open loop and pattern break analysis. |
| **Video Orchestrator** | Yes | Yes | Yes | Yes (`test_v3_core.py`, `test_v3_e2e_pipeline.py`) | High | Routes to Omni, Remotion, HyperFrames; needs explicit **Hybrid Video** support (Omni footage + Remotion overlays). | Add `compile_hybrid_prompt()` combining Omni cinematic background and Remotion telemetry. |
| **Quality Gate** | Yes | Yes | Yes | Yes | High | 9 dimensions present; needs 10th dimension (`editorial_quality`) and claim-level evidence mapping (`claim`, `source`, `confidence`). | Add 10th dimension and granular claim verification output. |
| **Live Updates (SSE)** | Yes | Yes | Yes | Manual | High | `/api/events/live` works; UI needs pause/resume live stream button and new event highlight animations. | Add pause/resume live feed controls and visual pulse indicators in `LiveRadarView.tsx`. |
| **User Feedback Loop** | Partial | No | No | No | Low | Learning engine calculates performance rates, but there is no direct UI button for user rating (👍 Strong / 😐 Average / 👎 Weak) and reason. | Add feedback endpoint `/api/content/feedback` and UI buttons in Content Studio. |
| **Source Monitors** | Schema only | Partial | No | Partial | Medium | Database table `user_monitors` exists; needs CRUD endpoints and active polling hook. | Add `/api/monitors` API endpoints for managing custom source monitors. |

---

## 2. Conclusion & V3.1 Roadmap

The core V3 foundation is solid, with all 40 tests passing and the frontend cleanly building.
To fulfill the V3.1 mandate of **proving real-world efficacy**, we will implement:
1. **Dynamic Firecrawl Discovery & Primary Source Verification flow**
2. **Contradiction Detection Engine**
3. **Event Engine Clustering Precision Benchmark (10, 20, 50 source fixtures)**
4. **Calculated Rolling Latency KPIs (Avg, Median, P95 Time-to-Radar)**
5. **Content Engine Enhancements (Best/Safe/High-Risk hooks, Dynamic structures, Hybrid video, 10-dimension Quality Gate)**
6. **YouTube Retention Risk Model**
7. **User Feedback API & Learning Loop Integration**
8. **20-Event Real World Benchmark (`docs/CONTENT_COMPETITIVE_BENCHMARK.md` & `docs/DISCOVERY_BENCHMARK.md`)**
