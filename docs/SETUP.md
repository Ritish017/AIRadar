# Setup & Operational Guide — AI Viral Radar

## Prerequisites

- **Python**: 3.11 or greater (Tested on Python 3.14)
- **Node.js**: v18 or greater (Tested on Node.js v24.11)
- **Package Managers**: `pip`, `npm`
- **Browser**: Google Chrome (for Manifest V3 extension)

---

## 1. Environment Configuration

Copy `.env.example` to `.env` in the project root:

```powershell
cp .env.example .env
```

Configure your parameters in `.env`:
```ini
APP_ENV=development
PORT=8000
HOST=127.0.0.1
DEBUG=true
DEMO_MODE=true

# Database (Default: SQLite for zero-config portable execution)
DATABASE_URL=sqlite+aiosqlite:///./viral_radar.db

# Primary AI Provider: Google Gemini (Leave blank for offline demo mode)
GEMINI_API_KEY=
GEMINI_MODEL=gemini-2.5-flash

# Primary Web Scraping & Research: Firecrawl (Leave blank for offline demo mode)
FIRECRAWL_API_KEY=

# Discovery & Automation Limits
DISCOVERY_INTERVAL_MINUTES=30
VIRAL_THRESHOLD=70.0
MAX_SEARCH_RESULTS=5
MAX_PAGES_PER_DISCOVERY=10

# Anti-Copy Safeguard Threshold
SIMILARITY_THRESHOLD=0.60
```

---

## 2. Backend Startup

To start the FastAPI backend server with automatic reload:

```powershell
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```

Interactive Swagger documentation:
`http://127.0.0.1:8000/docs`

Health check:
`http://127.0.0.1:8000/api/health`

---

## 3. Web Dashboard Startup

In a separate terminal:

```powershell
cd apps\web
npm run dev
```

Open your browser at:
`http://localhost:5173`

---

## 4. Loading the Chrome Extension

1. Open Google Chrome and visit `chrome://extensions/`.
2. Toggle **Developer mode** to **ON** in the top-right corner.
3. Click the **Load unpacked** button in the top-left toolbar.
4. Select the directory:
   ```
   c:\ViralConetntCreator\extension
   ```
5. Pin **AI Viral Radar** to your Chrome toolbar.

---

## 5. Running the Test Suite

Run the full pytest suite (21 unit and integration tests):

```powershell
python -m pytest tests/ -v
```
