# Trend Intelligence & Content Opportunity Engine — Audit

**Date**: September 2026  
**System**: AI Viral Radar  
**Audit Scope**: Trend detection, historical momentum tracking, lifecycle determination, competition analysis, opportunity scoring, timing & angle recommendations, and strategic AI agents.

---

## 1. Executive Summary & Classification Matrix

| Feature Area | Current Status | Notes & Code Reality |
| :--- | :--- | :--- |
| **Story Clustering** | **PARTIAL** | Basic `fuzz.token_set_ratio` clustering in `backend/services/virality/trend_detection.py`. Lacks hierarchical naming and canonical entity grouping. |
| **Historical Trend Tracking** | **MISSING** | No observation history stored over time. Observations are ephemeral single-snapshot estimates in `backend/providers/manager.py`. |
| **Historical Momentum Engine** | **MISSING** | Currently computes single-snapshot formula `(count * 45) + (source_count * 60) + (avg_viral * 1.5)`. Does not track changes across time or detect acceleration/deceleration. |
| **Trend Lifecycle Engine** | **MISSING** | Only 4 simple labels (`🔥 Exploding`, `⚡ Surging`, `📈 Rising`, `💤 Steady`). The 7-stage lifecycle (`EMERGING`, `RISING`, `EXPLODING`, `PEAK`, `SATURATED`, `DECLINING`, `DEAD`) is not implemented. |
| **Competition Analysis** | **MISSING** | No semantic angle decomposition, no competition scoring, no detection of `saturated_angles[]` vs `under_served_angles[]`. |
| **Opportunity Scoring** | **MISSING** | No composite `opportunity_score` ($0-100$) integrating momentum, novelty, competition, audience fit, and discussion potential. |
| **Content Opportunity Types** | **MISSING** | Classifications such as `EARLY_DISCOVERY`, `RISING_OPPORTUNITY`, `HIGH_REACH`, `NICHE_HIGH_VALUE`, `OVERSATURATED` are not implemented. |
| **Timing Recommendation** | **MISSING** | No deterministic action recommendations (`POST_NOW`, `POST_SOON`, `WATCH`, `WAIT`, `SKIP`) with rationales. |
| **Content Angle Intelligence** | **PARTIAL** | Generic `recommended_angle` generated per content item; does not analyze market gaps across existing coverage for a trend. |
| **Hook Intelligence** | **PARTIAL** | Single `hook_type` label in content analysis; lacks strategic hook matrix (10 types: contrarian, data-driven, prediction, etc.) and specific hook strategies. |
| **Format Intelligence** | **MISSING** | Fixed formats in post generator; no format suitability ranking (`single_post`, `thread`, `chart`, `short_video`, etc.). |
| **Audience Intelligence** | **PARTIAL** | Simple text string `audience` on individual articles; lacks persona breakdown, primary/secondary targeting, and audience fit scoring. |
| **Gemini Strategic Agent** | **MISSING** | Gemini is currently used strictly for individual post analysis and variant generation (`gemini_provider.py`). No holistic trend-level strategist (`trend_strategist.py`). |
| **"What Should I Post?" Engine** | **MISSING** | No dedicated endpoint or UI view ranking top 5 opportunities with full strategic recommendations. |
| **Trend Radar View** | **PARTIAL** | Simple list of 5 trending topics in Overview; no interactive visualization mapped by momentum, opportunity, and competition. |
| **Traceable Source Evidence** | **PARTIAL** | Displays a single link; lacks structured multi-source attribution matrix (primary, supporting, press, repo). |
| **Personal Performance Feedback** | **MISSING** | No `content_performance` schema or historical engagement tracking for personal feedback loops. |

---

## 2. Detailed Gap Analysis

### 1. Trend Detection & Historical Observations
- **Current State**: `TrendDetector.cluster_topics(items)` runs on the current in-memory list during an ingestion cycle. The `topics` table only stores a single timestamp `updated_at`.
- **Requirement**: Store individual timestamped observations in `trend_observations` (`mention_count`, `source_count`, `source_diversity`, `social_mentions`, `new_items`, `momentum_score`, `competition_score`, `opportunity_score`).
- **Required Fix**: Build `backend/services/trends/trend_momentum.py` with multi-hour window analysis, calculating percentage rate of change and acceleration vectors (`ACCELERATING`, `STABLE`, `DECELERATING`). When history is absent, explicitly return `INSUFFICIENT HISTORY`.

### 2. 7-Stage Trend Lifecycle
- **Current State**: Arbitrary threshold checks based on snapshot counts.
- **Requirement**: Deterministic lifecycle rules based on velocity, acceleration, trend age, source growth, and competition:
  - `EMERGING`: Low absolute volume, high acceleration, young age.
  - `RISING`: Steady positive momentum, multi-source growth.
  - `EXPLODING`: Peak acceleration ($>250\%$), cross-source explosion.
  - `PEAK`: Maximum absolute volume, velocity inflection point (deceleration starts).
  - `SATURATED`: High volume + high competition + low novelty.
  - `DECLINING`: Negative momentum, falling mention rates.
  - `DEAD`: Negligible activity over $>72$ hours.

### 3. Competition & Angle Gap Analysis
- **Current State**: Does not group or analyze content angles.
- **Requirement**: Build `backend/services/trends/trend_competition.py` to semantically categorize existing stories into angles (e.g., *Generic Announcement*, *Benchmark Interpretation*, *Developer Economics*, *Reliability Bottlenecks*, *Philosophical Debate*), evaluate density to compute `competition_score` ($0-100$), and identify `saturated_angles[]` and `under_served_angles[]`.

### 4. Deterministic Opportunity Scoring Framework
- **Formula Specification**:
  $$\text{Opportunity} = 0.22 \cdot \text{Mom} + 0.15 \cdot \text{Fresh} + 0.15 \cdot \text{Nov} + 0.15 \cdot \text{AudFit} + 0.10 \cdot \text{Disc} + 0.10 \cdot \text{Imp} + 0.05 \cdot \text{Tier} + 0.08 \cdot (100 - \text{Comp})$$
- Classify into actionable opportunity tiers: `EARLY_DISCOVERY`, `RISING_OPPORTUNITY`, `BREAKING`, `HIGH_REACH`, `NICHE_HIGH_VALUE`, `OVERSATURATED`, `DECLINING`, `SKIP`.
- Determine timing: `POST_NOW`, `POST_SOON`, `WATCH`, `WAIT`, `SKIP` with human-readable rationale.

### 5. Gemini Strategic Intelligence Agent
- **Requirement**: Implement `backend/services/ai/trend_strategist.py` passing structured trend telemetry into Gemini with strict prompt injection defense (`<source_content>`), generating verified JSON analysis of:
  - What actually happened & what changed recently
  - Saturated narratives vs under-served white space
  - Primary & secondary audiences
  - Recommended high-signal angle & 10-type hook strategy
  - Format recommendations with confidence scores
  - Timing verdict & claims to strictly avoid.

---

## 3. Implementation Roadmap
1. Create `trend_observations` and `content_performance` database tables with zero-downtime SQLite migrations.
2. Build modular trend intelligence services in `backend/services/trends/`:
   - `trend_detector.py`
   - `trend_momentum.py`
   - `trend_lifecycle.py`
   - `trend_competition.py`
   - `trend_audience.py`
   - `trend_opportunity.py`
   - `trend_strategy.py`
3. Build `backend/services/ai/trend_strategist.py` utilizing Gemini Flash with structured Pydantic validation.
4. Expose REST endpoints: `/api/opportunities`, `/api/trends`, `/api/trends/{id}`, `/api/trends/{id}/strategy`.
5. Upgrade Web Dashboard (`apps/web`):
   - **Content Opportunities View** ("What Should I Post?" Engine)
   - **Trend Radar Visualizer**
   - **Trend Detail Strategic Drawer**
   - Seamless one-click transfer into **Post Studio** with pre-filled strategy.
6. Upgrade Chrome Extension with top opportunity banner and in-page trend lifecycle pill on X.
7. Write unit and integration test suite and verify 100% passing.
