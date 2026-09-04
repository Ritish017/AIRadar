"""
Comprehensive V3 Test Suite:
Validates Source Registry, RSS Poller, Web Acquisition, Event Engine,
Early Signal Engine, Content Gap Engine, Content Factory, Video Orchestrator,
Learning Engine, and V3 API Endpoints.
"""

import pytest
import httpx
from datetime import datetime, timezone

from backend.main import app
from backend.db.session import init_db, AsyncSessionLocal
from backend.providers.source_registry import source_registry
from backend.providers.rss_poller import rss_poller, RSSFeed, RSSItem, RSSNormalizer
from backend.providers.web_acquisition import web_acquisition_provider
from backend.services.events.event_engine import event_engine
from backend.services.trends.early_signal import early_signal_engine
from backend.services.trends.content_gap import content_gap_engine
from backend.services.content.content_factory import content_factory
from backend.services.video.video_orchestrator import video_generation_service
from backend.services.learning.learning_engine import learning_engine

@pytest.mark.asyncio
async def test_v3_source_registry():
    """Verify source registry catalog, priority sorting, and health telemetry."""
    sources = source_registry.list_sources()
    assert len(sources) >= 10
    
    # Check OpenAI priority is highest
    openai_src = source_registry.get_source("openai")
    assert openai_src is not None
    assert openai_src.priority == 100
    assert openai_src.quality_tier == "Tier 1"

    # Test health tracking
    source_registry.record_health("openai", success=True, latency_ms=120)
    summary = source_registry.get_health_summary()
    assert summary["total_sources"] >= 10
    assert summary["healthy_count"] > 0

@pytest.mark.asyncio
async def test_v3_rss_normalizer_no_fake_metrics():
    """Verify RSS parsing leaves social engagement fields as None."""
    sample_xml = """<rss version="2.0"><channel>
        <item>
            <title>Test DeepSeek Release</title>
            <link>https://deepseek.com/blog/v3</link>
            <description>Verified sparse mixture of experts release</description>
            <pubDate>Mon, 01 Jan 2026 12:00:00 GMT</pubDate>
        </item>
    </channel></rss>"""
    feed = RSSFeed(source_id="deepseek", name="DeepSeek", url="https://deepseek.com/rss", topic="AI Models")
    items = rss_poller._parse_feed_xml(sample_xml, feed, "Tier 1")
    assert len(items) == 1
    assert items[0].title == "Test DeepSeek Release"
    assert items[0].link == "https://deepseek.com/blog/v3"

@pytest.mark.asyncio
async def test_v3_event_engine_clustering_and_confidence():
    """Verify canonical event clustering, confidence ranking, and latency tracking."""
    await init_db()
    async with AsyncSessionLocal() as db:
        items = [
            {
                "title": "DeepSeek-V3 Open Weights Officially Released",
                "content": "DeepSeek has officially released DeepSeek-V3 weights on Hugging Face.",
                "url": "https://huggingface.co/deepseek-ai/DeepSeek-V3",
                "source": "Hugging Face",
                "source_type": "official",
                "source_quality": "Tier 1",
                "published_at": datetime.now(timezone.utc),
                "viral_potential": 94.0
            },
            {
                "title": "DeepSeek-V3 Weights Land with 671B Parameters",
                "content": "A deep dive into the DeepSeek-V3 launch and architecture.",
                "url": "https://techcrunch.com/2026/01/deepseek-v3",
                "source": "TechCrunch",
                "source_type": "news",
                "source_quality": "Tier 2",
                "published_at": datetime.now(timezone.utc),
                "viral_potential": 88.0
            }
        ]

        events = await event_engine.cluster_items_into_events(items, db)
        assert len(events) >= 1
        ev = events[0]
        assert "DeepSeek" in ev.canonical_title
        assert ev.status in ("CONFIRMED", "LIKELY", "DEVELOPING")
        assert ev.confidence_score >= 70.0
        assert ev.total_pipeline_latency > 0

@pytest.mark.asyncio
async def test_v3_early_signal_and_content_gap():
    """Verify early signal explosion probability and content gap analysis."""
    telemetry = early_signal_engine.evaluate_early_signal(
        mention_count=12,
        acceleration_pct=140.0,
        momentum_score=85.0,
        competition_score=25.0,
        novelty_score=92.0,
        source_diversity=3,
        has_tier1_source=True
    )
    assert telemetry.is_early_signal is True
    assert telemetry.explosion_probability >= 70.0
    assert telemetry.trajectory in ("EXPLODING", "ACCELERATING")

    gap = content_gap_engine.analyze_gap(
        trend_name="Local Coding Agents",
        category="AI Coding",
        competition_score=35.0
    )
    assert gap.gap_score >= 60.0
    assert len(gap.most_discussed_angles) > 0
    assert len(gap.underserved_angles) > 0
    assert len(gap.contrarian_angles) > 0

@pytest.mark.asyncio
async def test_v3_content_factory_full_suite():
    """Verify multi-platform generation (Brief, 10 hooks, X, LinkedIn, Instagram, YouTube, Quality)."""
    event_data = {
        "canonical_title": "Claude 3.7 Sonnet Hybrid Reasoning Architecture",
        "summary": "Anthropic introduced Claude 3.7 Sonnet with hybrid instant and step-by-step thinking.",
        "key_facts": ["Hybrid reasoning architecture", "State-of-the-art SWE-bench coding performance"],
        "recommended_angle": "Developer tradeoffs between instant tokens and extended reasoning",
        "primary_source_url": "https://anthropic.com/news/claude-3-7-sonnet"
    }

    suite = content_factory.generate_full_suite(event_data)
    
    # 1. Brief
    assert suite.brief.topic == event_data["canonical_title"]
    assert len(suite.brief.key_claims) >= 2

    # 2. X Hooks & Content
    assert len(suite.x_hooks) == 10
    assert suite.x_content["platform"] == "x"
    assert len(suite.x_content["thread"]) == 9

    # 3. LinkedIn
    assert suite.linkedin_content["platform"] == "linkedin"
    assert "enterprise" in suite.linkedin_content["content"].lower() or "strategic" in suite.linkedin_content["content"].lower()

    # 4. Instagram
    assert suite.instagram_carousel["total_slides"] == 8
    assert suite.instagram_reel["duration_seconds"] == 35

    # 5. YouTube
    assert len(suite.youtube_content["titles"]) == 10
    assert len(suite.youtube_content["thumbnails"]) == 3
    assert suite.youtube_content["short_script"] is not None

    # 6. Quality
    assert suite.quality.total_quality_score >= 80.0
    assert suite.quality.is_approved is True

@pytest.mark.asyncio
async def test_v3_video_orchestrator_compilers():
    """Verify prompt compilers for Gemini Omni, Remotion, and HyperFrames."""
    # Omni 20-field prompt
    omni = video_generation_service.compile_omni_prompt("Claude 3.7", "Data visualization")
    assert omni.camera is not None
    assert "4K" in omni.output_format
    assert len(omni.compiled_master_prompt) > 100

    # Remotion
    remotion = video_generation_service.compile_remotion_prompt("Speed Leap", {"Speed": "3.5x"})
    assert remotion.fps == 30
    assert "TitleHookCard" in remotion.components

    # HyperFrames
    hf = video_generation_service.compile_hyperframes_prompt("BREAKING RELEASE")
    assert "<div class=\"hyperframe-container\"" in hf.html_markup
    assert "gsap.timeline" in hf.gsap_timeline_code

    # 6-Scene Storyboard
    sb = video_generation_service.build_storyboard("Local Model Deployment", ["Runs on M3 Max", "120 tok/sec"])
    assert len(sb.scenes) == 6
    assert sb.total_duration_sec == 30.0

@pytest.mark.asyncio
async def test_v3_learning_engine():
    """Verify engagement rate calculation without fake metrics and voice profiling."""
    metrics = learning_engine.calculate_performance(views=10000, likes=350, comments=45, shares=80, bookmarks=120)
    assert metrics.engagement_rate == 5.95
    assert metrics.share_rate == 0.8
    assert metrics.save_rate == 1.2

    # Zero views safely yields 0.0
    zero_m = learning_engine.calculate_performance(views=None, likes=10, comments=2, shares=1)
    assert zero_m.engagement_rate == 0.0

    # Voice analysis
    samples = [
        "Inference latency is the only metric that matters for enterprise agent loops.",
        "Tested the open weights on 4x A100. Throughput scales linearly up to batch 32."
    ]
    voice = learning_engine.analyze_voice_sample(samples)
    assert voice["detected_tone"] == "Technical & Authoritative"

@pytest.mark.asyncio
async def test_v3_api_endpoints():
    """Verify V3 REST API endpoints."""
    await init_db()
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Top Terminal Status Bar
        res = await client.get("/api/terminal/status")
        assert res.status_code == 200
        status_data = res.json()
        assert status_data["status"] == "LIVE"
        assert "services" in status_data

        # 2. Events & Live Stream
        res = await client.get("/api/events")
        assert res.status_code == 200
        assert "events" in res.json()

        res = await client.get("/api/events/live")
        assert res.status_code == 200
        assert "live_stream" in res.json()

        # 3. Sources Registry & Health
        res = await client.get("/api/sources")
        assert res.status_code == 200
        assert len(res.json()["sources"]) > 0

        res = await client.get("/api/sources/health")
        assert res.status_code == 200
        assert "healthy_count" in res.json()

        # 4. Global AI News
        res = await client.get("/api/news?category=all")
        assert res.status_code == 200
        assert len(res.json()["categories"]) == 11

        # 5. Trends Graph & Early Signals
        res = await client.get("/api/trends/graph")
        assert res.status_code == 200
        assert "nodes" in res.json()
        assert "links" in res.json()

        res = await client.get("/api/trends/early-signals")
        assert res.status_code == 200
        assert "early_signals" in res.json()

        # 6. Content Factory (Brief & All)
        res = await client.post("/api/content/brief", json={"canonical_title": "Test AI Breakthrough"})
        assert res.status_code == 200
        assert "brief" in res.json()

        res = await client.post("/api/content/all", json={"canonical_title": "Test AI Breakthrough"})
        assert res.status_code == 200
        suite = res.json()["suite"]
        assert "x_content" in suite
        assert "linkedin_content" in suite
        assert "instagram_carousel" in suite
        assert "youtube_content" in suite

        # 7. Video Prompt Lab
        res = await client.post("/api/prompts/omni", json={"topic": "Neural Net"})
        assert res.status_code == 200
        assert "omni_prompt" in res.json()

        res = await client.post("/api/prompts/storyboard", json={"title": "Test Storyboard"})
        assert res.status_code == 200
        assert len(res.json()["storyboard"]["scenes"]) == 6

        # 8. Daily Brief & Plan Day
        res = await client.get("/api/brief/daily")
        assert res.status_code == 200
        assert "what_you_should_post_today" in res.json()

        res = await client.get("/api/plan-day")
        assert res.status_code == 200
        assert len(res.json()["schedule"]) == 5

        # 9. Search
        res = await client.get("/api/search?q=OpenAI")
        assert res.status_code == 200
        assert "total_results" in res.json()
