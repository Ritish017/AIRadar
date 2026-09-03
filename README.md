# ⚡ AI Viral Radar (Production Edition)

> **"Discover breaking AI developments before everyone else and turn verified intelligence into original, high-signal X content."**

AI Viral Radar is a full-stack intelligence system and creator copilot. It utilizes **Firecrawl** as its primary web research and extraction layer to monitor live AI developments across the web, evaluates virality using a scientific dual-score engine, deconstructs psychological viral hooks and fact-checks claims using **Google Gemini**, and synthesizes original, copyright-safe, attributed X posts tailored to your voice profile.

---

## 🚀 Key Highlights & Philosophy

- **Centralized Firecrawl Research**: Web discovery and page markdown extraction are unified through Firecrawl with dynamic query rotation and source quality tiering (Tier 1: Official, Tier 2: Tech Press, Tier 3: Community).
- **Google Gemini AI Engine**: Powered by Google Gemini (`gemini-2.5-flash` or `gemini-1.5-flash`) for structured fact-checking (`✓ Confirmed` vs `⚠ Unverified`) and original post generation.
- **Scientific Dual Virality Engine**: Differentiates between measurable **Viral Score** (when metrics exist) and deterministic **Viral Potential** (when metrics are absent). Never fabricates false interaction metrics.
- **Not a Tweet-Copying Tool**: Generates 6 distinct original formats (News, Hot Take, Educational, Builder Angle, Thread, Question). Anti-copy safeguards (`RapidFuzz` + 3-gram Jaccard overlap) enforce conceptual originality (< 0.60 similarity threshold).
- **Prompt Injection Defense**: All scraped and untrusted web content is encapsulated within `<source_content>` delimiters with strict system security directives.
- **Zero-Friction Demo Mode**: Operates out of the box with realistic verified AI announcements and an intelligent heuristic cognitive engine even when running offline or without API keys.

---

## 🏛 System Architecture

```
                                  AI VIRAL RADAR
                                
   +-------------------------------------------------------------------------+
   |                             DATA INGESTION                              |
   |   Firecrawl Web Search & Extract | Pluggable X | Mock Provider          |
   +------------------------------------+------------------------------------+
                                        |
                                        v
   +-------------------------------------------------------------------------+
   |                           FASTAPI BACKEND                               |
   |                                                                         |
   |   [Provider Manager]  --->  [Normalizer & Fingerprint Deduplicator]     |
   |                                        |                                |
   |   [Dual Virality Scorer] <-------------+                                |
   |   - Measurable Viral Score (0-100)     |                                |
   |   - Predicted Viral Potential (0-100)  v                                |
   |   - Freshness Decay (28h half-life) [Trend Detector & Topic Clustering] |
   |                                        |                                |
   |                                        v                                |
   |                             [Database: SQLite / Postgres]               |
   |                                        |                                |
   |   [Google Gemini Engine]               v                                |
   |   - Hook & Multi-Source Facts   <--- [REST API Layer /api]              |
   |   - 6 Variant Post Synthesizer         |                                |
   |   - Anti-Copy Safeguards (<0.60)       |                                |
   |   - Personal Voice Profiler            |                                |
   +----------------------------------------+--------------------------------+
                                            |
                         +------------------+------------------+
                         |                                     |
                         v                                     v
             +-----------------------+             +-----------------------+
             |     WEB DASHBOARD     |             |   CHROME EXTENSION    |
             |   (React 18 + Vite)   |             |     (Manifest V3)     |
             |  Linear/Arc Aesthetic |             |  In-Page X Assistant  |
             +-----------------------+             +-----------------------+
```

---

## 📂 Project Structure

```
c:\ViralConetntCreator\
├── apps/
│   └── web/                                # React 18 / Vite / TypeScript Dashboard
│       ├── src/
│       │   ├── components/                 # ContentCard, AnalysisModal, PostStudio
│       │   ├── lib/api.ts                  # Typed API client
│       │   ├── types.ts                    # Domain interfaces
│       │   └── App.tsx                     # Main layout & tab orchestration
│       └── vite.config.ts
├── extension/                              # Chrome Manifest V3 Extension
│   ├── manifest.json
│   ├── icons/                              # 16px, 48px, 128px assets
│   └── src/
│       ├── background/background.js        # Background worker & badge updates
│       ├── content/content.js              # X.com in-page assistant widget
│       ├── popup/popup.html & popup.js     # Compact popup radar
│       └── options/options.html & js       # Extension settings (Gemini default)
├── backend/                                # Python FastAPI Service
│   ├── api/v1.py                           # REST endpoints (/feed, /analyze, /generate)
│   ├── config.py                           # Pydantic Settings
│   ├── db/
│   │   ├── session.py                      # Async SQLAlchemy engine & migrations
│   │   └── models.py                       # ContentItem, Analysis, GeneratedPost
│   ├── providers/
│   │   ├── base.py                         # BaseProvider interface
│   │   ├── firecrawl_provider.py           # Centralized Firecrawl search & extract
│   │   ├── mock_provider.py                # High-signal demo data
│   │   ├── x_provider.py                   # Pluggable X provider
│   │   └── manager.py                      # Ingestion orchestrator & deduplicator
│   ├── services/
│   │   ├── virality/                       # Scorer, velocity, dual potential
│   │   ├── ai/                             # Google Gemini provider, prompts
│   │   └── originality/similarity.py       # Anti-copy similarity checker
│   ├── workers/scheduler.py                # Background discovery loop
│   └── main.py                             # App lifespan & CORS
├── docs/                                   # Documentation suite
│   ├── ARCHITECTURE.md
│   ├── API.md
│   ├── DATA_MODEL.md
│   ├── EXTENSION.md
│   ├── PROVIDERS.md
│   ├── AI_PIPELINE.md
│   └── SETUP.md
├── tests/                                  # 21 unit & integration tests
├── .env.example
├── .gitignore
└── README.md
```

---

## ⚡ Quick Start

### 1. Environment Configuration
```powershell
cp .env.example .env
```

Set your API keys in `.env` (optional, operates in Demo Mode if left blank):
```ini
GEMINI_API_KEY=
FIRECRAWL_API_KEY=
```

### 2. Start the Backend API
```powershell
uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
```
Interactive API documentation: `http://127.0.0.1:8000/docs`

### 3. Start the Web Dashboard
```powershell
cd apps\web
npm run dev
```
Open `http://localhost:5173` in your browser.

### 4. Load the Chrome Extension
1. Open Google Chrome and visit `chrome://extensions/`.
2. Toggle **Developer mode** to **ON** (top right).
3. Click **Load unpacked** and select `c:\ViralConetntCreator\extension`.
4. Pin **AI Viral Radar** to your toolbar.

---

## 🧪 Automated Testing

Run the test suite (all 21 tests pass):
```powershell
python -m pytest tests/ -v
```

Validates:
- Firecrawl query rotation, tiering, search parsing, and network error recovery.
- Google Gemini structured output, prompt injection defense, and 6-format post generation.
- Dual virality scoring with measurable metrics and predicted viral potential without metrics.
- Anti-copy similarity safeguards and topic clustering.
- End-to-end API pipeline.
