# AI Viral Radar V3 — Testing & Quality Assurance Guide

AI Viral Radar V3 maintains a rigorous automated testing suite covering all layers of the platform: ingestion, deduplication, event clustering, trend calculations, prompt injection defenses, multi-platform content generation, video prompt compilation, and complete end-to-end simulation pipelines.

---

## 1. Test Suite Overview

| Test Module | Coverage Area | Assertions / Invariants |
| :--- | :--- | :--- |
| `tests/test_v3_e2e_pipeline.py` | Full Pipeline Simulation | Multi-source event discovery $\to$ deduplication $\to$ confidence $\to$ momentum $\to$ content gap $\to$ brief $\to$ 𝕏/LI/IG/YT generation $\to$ Omni/Remotion/HyperFrames prompts. |
| `tests/test_v3_core.py` | V3 Core Engines | Source registry health, RSS normalization, Event Engine clustering, early signals, Prompt Lab compilers, Learning Engine metrics. |
| `tests/test_trend_intelligence.py` | Trend & Momentum | Acceleration formula, lifecycle stages, angle decomposition, audience persona matching, opportunity scoring. |
| `tests/test_firecrawl_provider.py` | Firecrawl Web Layer | Query rotation, quality tiering, normalization, graceful degradation & fallback. |
| `tests/test_gemini_provider.py` | Gemini AI Provider | Structured JSON outputs, markdown fence extraction, prompt injection defense, variant generation. |
| `tests/test_similarity.py` | Anti-Copy & Originality | Jaccard N-gram similarity, near-copy rejection, original synthesis acceptance. |
| `tests/test_virality_scorer.py` | Telemetry Scoring | Engagement rate calculations, velocity multipliers, bounds checks, missing views fallback. |
| `tests/test_api.py` | REST API Endpoints | End-to-end HTTP responses for trends, content generation, and stories. |

---

## 2. Executing Automated Tests

### Run Full Test Suite (40/40 Passing Tests)
```bash
python -m pytest tests/ -v
```

### Run V3 End-to-End Pipeline Only
```bash
python -m pytest tests/test_v3_e2e_pipeline.py -v
```

### Run with Coverage Telemetry
```bash
python -m pytest tests/ --cov=backend --cov-report=term-missing
```

---

## 3. Frontend Verification
```bash
cd apps/web
npm run build
```
Confirms clean TypeScript compilation (0 errors) and Vite bundle production packaging.
