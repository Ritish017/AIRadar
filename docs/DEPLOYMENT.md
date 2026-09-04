# AI Viral Radar V3 — Deployment & Production Guide

This guide covers deployment instructions for running AI Viral Radar V3 in both development and production environments.

---

## 1. System Requirements

- **Python**: 3.11+ (Python 3.14 compatible)
- **Node.js**: 18.0+ (Node 20+ recommended)
- **Database**: SQLite (Local / Dev) or PostgreSQL with `pgvector` (Production)
- **Cache / Message Queue**: Redis 6.0+ (Optional for celery background jobs)

---

## 2. Environment Configuration

Create a `.env` file in the project root:

```ini
# Environment
APP_ENV=production
DEBUG=false

# Firecrawl Web Acquisition (Primary Layer)
FIRECRAWL_API_KEY=fc-xxxxxxxxxxxxxxxxxxxx
FIRECRAWL_BASE_URL=https://api.firecrawl.dev

# Google Gemini AI Provider (Primary Intelligence)
GEMINI_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxx
GEMINI_MODEL=gemini-2.5-flash

# Database Configuration
DATABASE_URL=sqlite+aiosqlite:///./viral_radar.db
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/viral_radar

# Polling Intervals (Seconds)
DISCOVERY_INTERVAL=300
TREND_INTERVAL=600

# CORS & Security
CORS_ORIGINS=["http://localhost:5173", "chrome-extension://*"]
```

---

## 3. Running Services Locally

### Backend (FastAPI + Uvicorn)
```bash
# Activate virtual environment if configured
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
- API Docs: `http://localhost:8000/docs`
- Health Endpoint: `http://localhost:8000/api/health`
- SSE Live Stream: `http://localhost:8000/api/events/live`

### Frontend (React + Vite)
```bash
cd apps/web
npm install
npm run dev -- --port 5173
```
- Dashboard Terminal: `http://localhost:5173`

### Production Build
```bash
cd apps/web
npm run build
```

---

## 4. Chrome Extension V3 Setup

1. Open Google Chrome and navigate to `chrome://extensions/`.
2. Enable **Developer mode** (toggle in upper right).
3. Click **Load unpacked**.
4. Select the `extension/` directory from this repository.
5. The extension icon will appear in the browser toolbar with 4 V3 tabs: `⚡ LIVE`, `📈 TRENDS`, `🎯 OPPS`, `✍ CREATE`.
