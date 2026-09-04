# AI Viral Radar V3 — System Architecture

AI Viral Radar V3 is a **Real-Time Global AI Intelligence & Content Operating System** that continuously monitors frontier AI developments, clusters multi-source articles into verified canonical events, identifies high-leverage content gaps, synthesizes platform-native social content, compiles production-ready video prompts, and learns iteratively from audience performance feedback.

---

## 1. Global End-to-End System Topology

```mermaid
flowchart TD
    subgraph GlobalInternet [Global Internet & Information Sources]
        Lab[Frontier AI Labs: OpenAI, DeepMind, Anthropic, Meta]
        News[Tech Press: Reuters, TechCrunch, The Verge]
        Research[Research Preprints: arXiv, Papers With Code]
        Code[Developer Ecosystem: GitHub, Hugging Face]
    end

    subgraph AcquisitionLayer [Web Acquisition Provider]
        Firecrawl[Firecrawl Web Search, Extract & Scrape]
        RSS[Fast Signal RSS Poller]
        Health[Source Registry & Health Telemetry]
        Lab --> Firecrawl
        News --> Firecrawl
        Research --> Firecrawl
        Code --> Firecrawl
        Lab --> RSS
        Research --> RSS
        Firecrawl --> Health
        RSS --> Health
    end

    subgraph EventLayer [Canonical Event Engine]
        Dedupe[Canonical URL & Token Deduplication]
        Cluster[Multi-Source Event Clustering]
        Conf[Confidence & Verification Tiering: CONFIRMED, LIKELY, DEVELOPING]
        Latency[Time-to-Radar Latency Telemetry]
        Health --> Dedupe --> Cluster --> Conf --> Latency
    end

    subgraph IntelligenceLayer [Trend & Opportunity Engine V3]
        Early[Early Signal Engine: Explosion Probability]
        Gap[Content Gap Engine: Underserved vs Saturated Angles]
        Graph[Trend Relationship Network Graph]
        Opp[Opportunity Scoring & POST NOW Telemetry]
        Latency --> Early
        Latency --> Gap
        Latency --> Graph
        Early --> Opp
        Gap --> Opp
    end

    subgraph ContentLayer [Multi-Platform Content Studio]
        Brief[Pre-Generation Strategic Brief]
        X[𝕏 Engine: 10 Hooks & 9-Tweet Thread]
        LI[LinkedIn Engine: Enterprise Thought Leadership]
        IG[Instagram Engine: 8-Slide Carousel & 35s Reel]
        YT[YouTube Engine: 10 Titles, 3 Thumbnails & Scripts]
        Quality[9-Dimension Quality Assurance Evaluator]
        Opp --> Brief --> X & LI & IG & YT --> Quality
    end

    subgraph VideoLayer [Video Orchestration & Prompt Lab]
        Router{Tool Router}
        Omni[Gemini Omni: 20-Field Cinematic Prompt]
        Remotion[Remotion: Programmatic React & Charts]
        Hyper[HyperFrames: Deterministic HTML/GSAP]
        Storyboard[6-Scene Video Storyboard]
        Brief --> Storyboard --> Router
        Router --> Omni & Remotion & Hyper
    end

    subgraph LearningLayer [Performance & Personal Voice Engine]
        Perf[Social Telemetry: Views, Likes, Shares, Retentions]
        Voice[My Voice Calibration & Sample Extraction]
        Profile[PersonalContentProfile Update Loop]
        Perf --> Voice --> Profile
        Profile -. Feedback Bias .-> ContentLayer
    end

    subgraph ClientApplications [Client Presentation Tier]
        Radar[Live Radar Terminal Dashboard: React 18 + Vite]
        SSE[Server-Sent Events: /api/events/live]
        Ext[Chrome Extension V3: 4 Tabs & In-Page Assistant]
        Latency --> SSE --> Radar
        Opp --> Radar & Ext
        Quality --> Radar & Ext
        Omni --> Radar & Ext
    end
```

---

## 2. Core Operational Pillars

### 1. Probability Over False Guarantees
The system **never** claims "guaranteed virality". It operates entirely on probabilistic scoring:
- **Opportunity Score** ($0 - 100$)
- **Distribution Potential**
- **Hook Strength** ($0 - 100$)
- **Explosion Probability** ($0 - 100\%$)
- **Content Gap Score**

### 2. Centralized Firecrawl Acquisition
All external web discovery, research scraping, and verification flows strictly through `WebAcquisitionProvider`. Brittle custom scrapers and headless browser sessions are completely eliminated for acquisition.

### 3. Google Gemini Primary Intelligence
Gemini 2.5 Flash powers strategic editorial briefs, 10-hook generation, thread composition, multi-platform adaptation, and 20-field cinematic video prompts. All external input is treated as untrusted and wrapped in safety fences to prevent prompt injection.

### 4. Tri-Engine Video Routing
- **Gemini Omni**: Photorealistic neural visuals, B-roll, continuous camera motion.
- **Remotion**: Programmatic benchmark charts, code terminals, animated captions.
- **HyperFrames**: HTML5/CSS3 dynamic cards, telemetry badges, frame-accurate paused GSAP animations.

### 5. Learning Loop
Actual performance metrics (impressions, retention, engagement rates) feed back into `PersonalContentProfile`, updating winning hook patterns and informing future angle recommendations.
