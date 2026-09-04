# Open Source Resources & Architecture References

Before engineering the V3 architecture for **AI Viral Radar**, we analyzed production-grade open-source tools, aggregators, and video composition frameworks. Below is the curated record of selected resources, licenses, and what we conceptually borrowed or leveraged.

---

## 1. Web Acquisition & Extraction

### **Firecrawl** (`firecrawl-py` / Firecrawl API)
- **Repository/Service**: `mendableai/firecrawl`
- **License**: Apache 2.0 / Commercial API
- **Purpose**: Unified web discovery, deep markdown extraction, and search across Web, News, Research, and GitHub.
- **Why Useful**: Converts unstructured web and news pages into clean, LLM-ready markdown, eliminating fragile ad-hoc HTML scrapers and browser automation for general web retrieval.
- **Architectural Implementation**: Primary acquisition provider with query rotation, quality tiering (Tier 1 Official, Tier 2 News, Tier 3 Community), and freshness filters.

---

## 2. Fast Discovery & Feeds

### **Feedparser & Fast XML Parsing**
- **Repository**: `kurtmckee/feedparser` & Python `xml.etree.ElementTree`
- **License**: BSD 2-Clause / Python Software Foundation
- **Purpose**: Fast, low-latency RSS and Atom feed ingestion for breaking updates.
- **Why Useful**: Instant discovery signal from official corporate and research feeds (OpenAI News, Anthropic, Google AI, ArXiv) before indexers crawl them.
- **Architectural Implementation**: Fast discovery layer in `RSSPoller` with conditional HTTP headers (`If-Modified-Since`, `ETag`) and deep Firecrawl verification for complete article extraction.

---

## 3. Semantic Deduplication & Anti-Copy Safeguards

### **RapidFuzz & N-Gram Jaccard Distance**
- **Repository**: `rapidfuzz/RapidFuzz`
- **License**: MIT
- **Purpose**: High-speed string matching, Levenshtein distance, token sort ratios, and n-gram overlap.
- **Why Useful**: Fast in-memory deduplication and anti-plagiarism verification against source texts (< 0.60 similarity threshold).
- **Architectural Implementation**: Powering the `OriginalityChecker` and the `EventEngine` clustering pipeline.

---

## 4. Video Generation & Composition Engines

### **Remotion**
- **Repository**: `remotion-dev/remotion`
- **License**: Custom Permissive / Company-backed
- **Purpose**: Programmatic React-based video composition, data visualizations, and animated infographics.
- **Why Useful**: Deterministic rendering of charts, code snippets, benchmarks, and dynamic captions without hallucinated visual artifacts.
- **Architectural Implementation**: `RemotionPromptEngine` generates structured composition configs (`composition`, `fps`, `resolution`, `scene breakdown`, `transitions`, `typography`, `caption behavior`).

### **HyperFrames**
- **Architecture**: HTML-native deterministic video and motion graphic composition with GSAP and Lottie runtimes.
- **License**: Open standard / HTML5
- **Purpose**: Lightweight, deterministic HTML/CSS motion design with paused GSAP timelines.
- **Why Useful**: Uses standard browser DOM with `data-start`, `data-duration`, `data-track-index` attributes for frame-by-frame predictable animation.
- **Architectural Implementation**: `HyperFramesPromptEngine` compiles HTML markup, CSS styling, and paused GSAP timeline scripts for animated cards and breaking-news alerts.

### **Gemini Omni Video Model**
- **Model**: Google DeepMind Gemini Omni Multi-Modal Generation
- **Purpose**: Cinematic, photorealistic video clips, scene extensions, and creative B-roll.
- **Why Useful**: High fidelity visual generation when driven by production-grade, 20-field structured camera, lighting, physics, and continuity prompts.
- **Architectural Implementation**: `OmniPromptCompiler` transforms event facts into exhaustive, film-grade cinematic prompts.

---

## 5. UI & State Architecture

### **Lucide React & Tailwind CSS**
- **Repository**: `lucide-icons/lucide`, `tailwindlabs/tailwindcss`
- **License**: ISC / MIT
- **Purpose**: High-density terminal aesthetics, semantic indicators, and responsive data-dense layouts.
- **Architectural Implementation**: Powering the Linear/Arc-inspired dark-mode Live Radar dashboard, relationship graph, and Content Studio.
