# AI Viral Radar V3 — REST API & SSE Reference

The **AI Viral Radar V3** backend exposes asynchronous RESTful endpoints and Server-Sent Events (SSE) running on FastAPI.

Base URL: `http://127.0.0.1:8000/api`  
Interactive OpenAPI / Swagger: `http://127.0.0.1:8000/docs`

---

## Complete Endpoints Matrix

| Domain | Method | Endpoint | Description |
| :--- | :--- | :--- | :--- |
| **System** | `GET` | `/health` | Ingestion health, database status, and latency KPIs |
| **Live Radar** | `GET` | `/events` | List clustered canonical events with latency telemetry |
| **Live Radar** | `GET` | `/events/live` | **Server-Sent Events (SSE)** real-time breaking events stream |
| **Live Radar** | `GET` | `/events/{id}` | Detailed event view with timeline and source clustering |
| **Global News** | `GET` | `/news` | 11-category dedicated Global AI News intelligence center |
| **Sources** | `GET` | `/sources` | Configurable source registry (Official, News, Research, Community) |
| **Sources** | `GET` | `/sources/health` | Live operational health and latency monitor for sources |
| **Trends** | `GET` | `/trends` | Trend radar list with lifecycle stages and early signals |
| **Trends** | `GET` | `/trends/{id}` | Detailed trend analysis, acceleration, and historical observations |
| **Trends** | `GET` | `/trends/{id}/gap` | Semantic angle decomposition and content gap analysis |
| **Trends** | `GET` | `/trend-graph` | Interactive force-directed relationship network graph |
| **Content Studio**| `POST` | `/content/brief` | Generates pre-generation editorial brief (`ContentBriefData`) |
| **Content Studio**| `POST` | `/content/all` | **One-Click Multi-Platform Factory** (𝕏, LinkedIn, Instagram, YouTube) |
| **Content Studio**| `POST` | `/content/x` | 𝕏 10-hook evaluator and 9-post thread generator |
| **Content Studio**| `POST` | `/content/linkedin`| Long-form executive thought leadership post |
| **Content Studio**| `POST` | `/content/instagram`| 8-slide visual carousel and 35s Reel concept |
| **Content Studio**| `POST` | `/content/youtube` | 10 titles, 3 thumbnails, cold open, short & long scripts |
| **Prompt Lab** | `POST` | `/prompts/omni` | 20-field structured Gemini Omni cinematic prompt compiler |
| **Prompt Lab** | `POST` | `/prompts/remotion`| React Remotion programmatic animation specification |
| **Prompt Lab** | `POST` | `/prompts/hyperframes` | HTML5 + GSAP deterministic motion graphics code |
| **Prompt Lab** | `POST` | `/storyboard` | 6-scene structured video storyboard (0-30s) |
| **Learning** | `GET` | `/performance/metrics` | User engagement analytics and winning characteristics |
| **Learning** | `POST` | `/performance/log` | Logs post performance to update `PersonalContentProfile` |
| **Learning** | `POST` | `/voice/analyze` | Analyzes writing samples to calibrate My Voice tone |
| **Workflow** | `GET` | `/briefing/daily` | "What Happened While I Was Away?" morning briefing |
| **Workflow** | `GET` | `/plan-my-day` | Recommended 5-slot daily multi-platform schedule |
| **Workflow** | `GET/POST`| `/queue` | Editorial queue management (`IDEA` $\to$ `PUBLISHED`) |
| **Monitors** | `GET/POST`| `/monitors` | Custom topic, domain, and GitHub repository monitors |
| **Search** | `GET` | `/search` | Unified global search across events, trends, and content |

---

## Key V3 Request / Response Specifications

### 1. Server-Sent Events Stream: `GET /api/events/live`
Clients subscribe to a persistent HTTP connection (`text/event-stream`). The server pushes new breaking events and keepalive pings without requiring full page refreshes.

**Example SSE Event:**
```text
event: breaking_event
data: {
  "id": "e81d42a7-6f19-4820-928f-7c15e8bc41a9",
  "canonical_title": "OpenAI Announces GPT-5 Orion with Autonomous Tool Loops",
  "status": "CONFIRMED",
  "confidence_score": 98.0,
  "momentum_score": 96.0,
  "opportunity_score": 94.0,
  "sources": ["OpenAI", "Reuters", "TechCrunch"],
  "total_pipeline_latency": 31.2,
  "published_at": "2026-09-04T12:00:00Z"
}
```

---

### 2. Multi-Platform Generation: `POST /api/content/all`

**Request Body:**
```json
{
  "event_id": "e81d42a7-6f19-4820-928f-7c15e8bc41a9",
  "angle": "Developer Architecture & Workflow Migration",
  "audience": "AI Engineers & Systems Builders"
}
```

**Response Body:**
```json
{
  "suite": {
    "brief": {
      "topic": "OpenAI Announces GPT-5 Orion with Autonomous Tool Loops",
      "angle": "Developer Architecture & Workflow Migration",
      "hook_strategy": "Contrarian / Architecture Shift",
      "key_claims": ["Native autonomous reasoning loops without outer orchestrator"],
      "counterpoint": "Slight token degradation observed on 100k+ multi-turn context"
    },
    "x_hooks": [
      {
        "hook_text": "Everyone is benchmarking Orion's raw throughput. They're missing the real shift: autonomous agent loops without LangChain.",
        "hook_score": 94.0,
        "hook_type": "Contrarian",
        "curiosity": 95.0,
        "specificity": 92.0
      }
    ],
    "x_content": {
      "platform": "x",
      "single_post": "...",
      "thread": ["1/9 Hook...", "2/9 Context...", "9/9 CTA..."]
    },
    "linkedin_content": {
      "platform": "linkedin",
      "content": "The economics of enterprise AI just shifted with today's announcement of Orion..."
    },
    "instagram_carousel": {
      "total_slides": 8,
      "slides": [
        {"slide_number": 1, "headline": "...", "visual_direction": "..."}
      ]
    },
    "youtube_content": {
      "titles": ["Orion Benchmark Breakdown: What OpenAI Didn't Announce"],
      "thumbnails": [{"subject": "...", "text": "NO ORCHESTRATOR?"}],
      "short_script": "..."
    },
    "quality": {
      "total_quality_score": 91.5,
      "is_approved": true,
      "dimension_scores": {
        "fact_check": 95.0,
        "originality": 92.0,
        "platform_fit": 94.0
      }
    }
  }
}
```
