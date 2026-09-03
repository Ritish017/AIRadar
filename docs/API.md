# AI Viral Radar — REST API Reference

The AI Viral Radar backend exposes a versioned, RESTful API running on FastAPI with asynchronous I/O and strict Pydantic v2 validation.

Base URL: `http://127.0.0.1:8000/api`  
Interactive Swagger Docs: `http://127.0.0.1:8000/docs`  
ReDoc: `http://127.0.0.1:8000/redoc`

---

## Endpoints Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Service health, timestamp, and active provider count |
| `POST` | `/collect` | Trigger manual ingestion across all data providers |
| `GET` | `/feed` | Filtered, sorted, and paginated viral AI feed |
| `GET` | `/trending` | Top 5 viral items and exploding topic clusters |
| `GET` | `/topics` | Detected topics with momentum and source distribution |
| `GET` | `/content/{id}` | Detailed content item with analysis and generated variants |
| `POST` | `/content/{id}/analyze` | Trigger or retrieve cached AI virality breakdown |
| `POST` | `/content/{id}/generate` | Generate 5 original post variants with voice calibration |
| `POST` | `/content/{id}/save` | Save story to user library with workflow status |
| `GET` | `/saved` | List all saved stories and notes |
| `DELETE` | `/saved/{id}` | Remove story from saved list |
| `GET` | `/voice-profile` | Fetch user's voice profile guidelines and examples |
| `POST` | `/voice-profile` | Update user's writing sample and voice profile |
| `POST` | `/analyze-custom-tweet` | Immediate analysis endpoint for Chrome extension |

---

## Detailed Endpoint Documentation

### 1. GET `/feed`
Retrieves paginated content items with multi-dimensional filtering.

**Query Parameters:**
- `topic` (string, optional): Category filter (`Models`, `Agents`, `Research`, `Startups`, `Robotics`, `Coding`, `Open Source`, `AI Tools`, `Companies`, or `All`).
- `sort_by` (string, default: `viral`): `viral`, `rising`, `newest`, `engagement`, `velocity`.
- `time_range` (string, default: `24h`): `15m`, `1h`, `6h`, `24h`, `7d`, `all`.
- `min_viral_score` (float, optional): Filter by minimum viral score (0-100).
- `page` (int, default: 1): Page number.
- `page_size` (int, default: 20): Items per page (max: 100).

**Example Response:**
```json
{
  "total": 42,
  "page": 1,
  "page_size": 20,
  "items": [
    {
      "id": "3a82207b-89fc-4876-b31c-3086eb293ab7",
      "source": "OpenAI",
      "source_type": "x",
      "title": "OpenAI releases new reasoning model with native computer use",
      "content": "OpenAI has officially launched a new lightweight reasoning architecture...",
      "url": "https://openai.com/index/announcing-reasoning-computer-use",
      "author": "OpenAI",
      "author_handle": "@OpenAI",
      "published_at": "2026-09-02T18:00:00Z",
      "views": 2400000,
      "likes": 31200,
      "reposts": 5800,
      "replies": 1240,
      "viral_score": 96.4,
      "engagement_velocity": 340.0,
      "topic": "Models",
      "hook_type": "breaking_news"
    }
  ]
}
```

---

### 2. POST `/content/{id}/analyze`
Analyzes why an item went viral, extracts key factual claims, and evaluates hook psychology. Results are cached in the database.

**Example Response:**
```json
{
  "summary": "OpenAI launched a reasoning model featuring direct OS computer control, achieving 84.6% on SWE-bench Verified.",
  "main_claim": "Lightweight reasoning model outperforms previous frontier systems with 42% lower latency.",
  "why_viral": [
    "Claims SOTA or outperforms larger established models on key benchmarks",
    "Sparked debates among practitioners regarding test set contamination vs real gains",
    "High proof-of-work credibility with reproducible code and weights"
  ],
  "hook_type": "milestone",
  "content_type": "release",
  "key_facts": [
    "84.6% success rate on SWE-bench Verified",
    "42% latency reduction compared to predecessor",
    "Tier 3 API access activated immediately"
  ],
  "important_entities": ["OpenAI", "SWE-bench", "Computer Use"],
  "audience": "AI Engineers, Technical Founders, and Machine Learning Researchers",
  "recommended_angle": "Highlight the practical developer implications: how this reduces deployment friction or unlocks new agentic workflows."
}
```

---

### 3. POST `/content/{id}/generate`
Generates 5 distinct original post variants while enforcing anti-copy similarity constraints and applying personal voice guidelines.

**Request Body:**
```json
{
  "tones": ["technical"],
  "variants": ["news", "hot_take", "educational", "thread", "question"],
  "length": "medium",
  "include_voice_profile": true
}
```

**Example Response:**
```json
[
  {
    "variant_type": "news",
    "tone": "technical",
    "length": "medium",
    "content": "⚡ OpenAI releases new reasoning model with native computer use\n\nOpenAI just unveiled this milestone. The standout detail: 84.6% success rate on SWE-bench Verified.\n\nFull breakdown & docs: https://openai.com/index/announcing-reasoning-computer-use",
    "thread_items": [],
    "similarity_score": 0.28,
    "is_safe": true,
    "attribution_included": true
  },
  {
    "variant_type": "hot_take",
    "tone": "technical",
    "length": "medium",
    "content": "Hot take on OpenAI releases new reasoning model with native computer use:\n\nEveryone is fixated on the headline metric, but the real leverage is what this does to developer toolchains...",
    "similarity_score": 0.19,
    "is_safe": true,
    "attribution_included": true
  },
  {
    "variant_type": "thread",
    "tone": "technical",
    "length": "medium",
    "content": "1/4 🧵 OpenAI releases new reasoning model is going viral today...",
    "thread_items": [
      "1/4 🧵 OpenAI releases new reasoning model is going viral today. Here is the technical breakdown...",
      "2/4 The core advancement: 84.6% success rate on SWE-bench Verified...",
      "3/4 Why it matters: Instead of requiring massive compute clusters...",
      "4/4 Bottom line: Full details and source paper: https://openai.com/..."
    ],
    "similarity_score": 0.22,
    "is_safe": true,
    "attribution_included": true
  }
]
```

---

### 4. POST `/analyze-custom-tweet`
Lightweight endpoint for Chrome Extension or user-submitted text.

**Request Body:**
```json
{
  "text": "DeepSeek-V3 weights just dropped on Hugging Face. 671B MoE model matches Llama 3.1 405B on coding.",
  "author": "Research Lead",
  "author_handle": "@research_lead",
  "url": "https://x.com/research_lead/status/123",
  "likes": 8400,
  "reposts": 1600,
  "replies": 320,
  "views": 450000
}
```
