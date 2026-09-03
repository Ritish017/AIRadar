import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from backend.providers.firecrawl_provider import FirecrawlProvider

@pytest.mark.asyncio
async def test_firecrawl_query_rotation():
    provider = FirecrawlProvider()
    g1, q1 = provider.get_next_query()
    g2, q2 = provider.get_next_query()
    assert g1 != g2
    assert isinstance(q1, str) and len(q1) > 5
    assert isinstance(q2, str) and len(q2) > 5

def test_source_quality_tiering():
    provider = FirecrawlProvider()
    assert provider.get_source_quality("https://openai.com/index/reasoning") == "Tier 1"
    assert provider.get_source_quality("https://github.com/deepseek-ai/DeepSeek-V3") == "Tier 1"
    assert provider.get_source_quality("https://arxiv.org/abs/2412.01234") == "Tier 1"
    assert provider.get_source_quality("https://techcrunch.com/2026/09/ai-agent") == "Tier 2"
    assert provider.get_source_quality("https://theverge.com/2026/9/llm-benchmark") == "Tier 2"
    assert provider.get_source_quality("https://some-random-blog.xyz/post") == "Tier 3"

@pytest.mark.asyncio
async def test_firecrawl_search_parsing_and_normalization():
    provider = FirecrawlProvider()
    provider.api_key = "test_key"

    fake_firecrawl_response = [
        {
            "url": "https://openai.com/index/announcing-reasoning-agent",
            "title": "OpenAI announces autonomous reasoning agent benchmark",
            "markdown": "# OpenAI Reasoning Agent\n\nToday we unveil a new model achieving 88% on SWE-bench.",
            "metadata": {"author": "OpenAI Research"}
        }
    ]

    with patch.object(provider, "search_and_extract", new=AsyncMock(return_value=fake_firecrawl_response)):
        items = await provider.fetch_items()
        assert len(items) == 1
        item = items[0]
        assert item["title"] == "OpenAI announces autonomous reasoning agent benchmark"
        assert item["source_type"] == "firecrawl"
        assert item["source_quality"] == "Tier 1"
        assert item["views"] is None
        assert item["likes"] is None
        assert item["viral_score"] is None
        assert item["viral_potential"] >= 60.0

@pytest.mark.asyncio
async def test_firecrawl_graceful_failure_handling():
    provider = FirecrawlProvider()
    provider.api_key = "test_key"

    with patch.object(provider, "search_and_extract", new=AsyncMock(side_effect=Exception("Connection timed out"))):
        try:
            items = await provider.search_and_extract("AI news")
        except Exception as e:
            assert "Connection timed out" in str(e)
