# Data Providers Specification — AI Viral Radar

Web data acquisition in AI Viral Radar is centralized through **Firecrawl**, combined with authorized pluggable X feeds and an offline Mock Provider for high-fidelity demo operation.

---

## Active Providers

```
backend/providers/
├── base.py                 # Abstract BaseProvider interface
├── manager.py              # Provider manager, deduplicator & orchestrator
├── firecrawl_provider.py   # Primary Web Research & Scraping Provider
├── mock_provider.py        # High-signal verified AI breakthroughs (Demo Mode)
└── x_provider.py           # Pluggable X provider (API v2 + Curated Syndicate)
```

---

## 1. Firecrawl Provider (`backend/providers/firecrawl_provider.py`)

### Responsibilities
- **AI Web Search**: Queries live internet sources using dynamically rotated query groups.
- **Page Extraction**: Extracts clean markdown content and structured metadata.
- **Source Quality Classification**: Tiers incoming links based on domain authority.
- **Cost & Rate Limiting**: Caps search results per cycle (`MAX_SEARCH_RESULTS`) and performs deterministic keyword pre-filtering before invoking AI.

### Source Quality Tiering
- **Tier 1 (Official)**:
  `openai.com`, `anthropic.com`, `deepmind.google`, `ai.meta.com`, `blogs.nvidia.com`, `huggingface.co`, `github.com`, `arxiv.org`, `microsoft.com`, `mistral.ai`.
- **Tier 2 (Tech Press)**:
  `techcrunch.com`, `theverge.com`, `arstechnica.com`, `venturebeat.com`, `wired.com`, `technologyreview.com`.
- **Tier 3 (Community)**:
  `reddit.com`, forums, aggregators, general discussion blogs.

---

## 2. Pluggable X Provider (`backend/providers/x_provider.py`)

### Policy & Security Boundaries
- **Zero Scraping of Private Endpoints**: Does not bypass authentication, CAPTCHAs, or access controls.
- **Authorized API Connection**: When `X_API_BEARER_TOKEN` is set in `.env`, connects to official Twitter API v2.
- **Curated Public AI Syndicate**: When API keys are not provided, operates on permitted public syndication without fabricating unverified metric counts.

---

## 3. Mock Provider (`backend/providers/mock_provider.py`)

- Contains 8 realistic, high-signal AI developments (OpenAI, DeepSeek, Anthropic, Google DeepMind, NVIDIA, Meta).
- Guarantees 100% operational demo functionality out of the box when running offline or without live external API keys.
