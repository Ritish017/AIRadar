# AI Viral Radar V3 — Environment Variables Specification

The system follows strict security principles regarding secrets and credentials:
- **No hardcoded API keys** in source code, client bundles, or extension scripts.
- Environment-driven configuration via `pydantic-settings` or `.env`.

---

## Variable Reference

| Variable | Required | Default | Description |
| :--- | :--- | :--- | :--- |
| `APP_ENV` | No | `development` | Environment mode: `development`, `staging`, `production`. |
| `DEBUG` | No | `true` | Enables verbose SQL query logging and debug telemetry. |
| `FIRECRAWL_API_KEY` | **Yes** (in prod) | `""` | Firecrawl API key for search, scraping, and web extraction. |
| `FIRECRAWL_BASE_URL`| No | `https://api.firecrawl.dev` | Firecrawl API endpoint URL. |
| `GEMINI_API_KEY` | **Yes** (in prod) | `""` | Google Gemini API key (`google.genai` SDK). |
| `GEMINI_MODEL` | No | `gemini-2.5-flash` | Gemini model name for intelligence and prompt generation. |
| `DATABASE_URL` | No | `sqlite+aiosqlite:///./viral_radar.db` | Async SQLAlchemy database URI. |
| `REDIS_URL` | No | `redis://localhost:6379/0` | Optional Redis broker URL for Celery background tasks. |
| `DISCOVERY_INTERVAL`| No | `300` | Ingestion poll frequency in seconds (default: 5 minutes). |
| `TREND_INTERVAL` | No | `600` | Trend re-clustering and momentum decay cycle (seconds). |
| `CORS_ORIGINS` | No | `["*"]` | Allowed CORS origins for browser dashboard & extension. |

---

## Security Guidelines

> [!CAUTION]
> 1. **Never commit `.env` or production credentials to git.**
> 2. Chrome extension Manifest V3 runs purely client-side; all requests to Gemini and Firecrawl MUST proxy through the FastAPI backend (`http://localhost:8000/api/...`).
> 3. Content from untrusted external sources (scraped web pages, Reddit, X) is strictly treated as untrusted data and isolated in structured system prompt templates to prevent prompt injection.
