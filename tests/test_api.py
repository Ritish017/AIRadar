import pytest
import httpx
from backend.main import app
from backend.db.session import init_db

@pytest.mark.asyncio
async def test_api_e2e_pipeline():
    await init_db()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # 1. Health check
        res = await client.get("/api/health")
        assert res.status_code == 200
        assert res.json()["status"] == "healthy"

        # 2. Trigger ingestion / collect
        res = await client.post("/api/collect")
        assert res.status_code == 200
        stats = res.json()["stats"]
        assert stats["total_fetched"] > 0

        # 3. Get Feed
        res = await client.get("/api/feed?sort_by=viral&time_range=all")
        assert res.status_code == 200
        feed_data = res.json()
        assert feed_data["total"] > 0
        items = feed_data["items"]
        assert len(items) > 0

        first_item = items[0]
        item_id = first_item["id"]
        assert first_item["viral_score"] > 0
        assert first_item["url"] != ""

        # 4. Get Trending
        res = await client.get("/api/trending")
        assert res.status_code == 200
        trending_data = res.json()
        assert len(trending_data["trending_items"]) > 0

        # 5. Get Topics
        res = await client.get("/api/topics")
        assert res.status_code == 200
        topics = res.json()
        assert len(topics) > 0

        # 6. Analyze Content Item
        res = await client.post(f"/api/content/{item_id}/analyze")
        assert res.status_code == 200
        analysis = res.json()
        assert "summary" in analysis
        assert len(analysis["why_viral"]) > 0
        assert analysis["hook_type"] is not None

        # 7. Generate Original Post Variants
        res = await client.post(
            f"/api/content/{item_id}/generate",
            json={
                "tones": ["technical"],
                "variants": ["news", "hot_take", "educational", "thread", "question"],
                "length": "medium"
            }
        )
        assert res.status_code == 200
        variants = res.json()
        assert len(variants) >= 5
        types = [v["variant_type"] for v in variants]
        assert "news" in types
        assert "thread" in types
        assert "builder" in types
        for v in variants:
            assert v["is_safe"] is True
            assert v["similarity_score"] < 0.65

        # 8. Save Content Item
        res = await client.post(
            f"/api/content/{item_id}/save",
            json={"status": "Idea", "notes": "High priority post for tomorrow"}
        )
        assert res.status_code == 200
        saved_obj = res.json()
        assert saved_obj["status"] == "Idea"

        # 9. Get Saved Items
        res = await client.get("/api/saved")
        assert res.status_code == 200
        saved_list = res.json()
        assert len(saved_list) >= 1

        # 10. Voice Profile Get & Update
        res = await client.get("/api/voice-profile")
        assert res.status_code == 200
        vp = res.json()
        assert len(vp["voice_examples"]) > 0

        res = await client.post(
            "/api/voice-profile",
            json={
                "name": "Custom Founder Voice",
                "tone_preference": "Bold & Pragmatic",
                "voice_examples": ["AI architectures that can't run under 200ms are dead on arrival."],
                "guidelines": "Short punchy sentences."
            }
        )
        assert res.status_code == 200
        assert res.json()["tone_preference"] == "Bold & Pragmatic"

        # 11. Custom Tweet Analysis (for Chrome Extension)
        res = await client.post(
            "/api/analyze-custom-tweet",
            json={
                "text": "We just trained a 1B reasoning model that solves Math Olympiad problems.",
                "author": "Frontier AI Lab",
                "author_handle": "@frontier_ai",
                "likes": 12000,
                "reposts": 2300,
                "replies": 450,
                "views": 850000
            }
        )
        assert res.status_code == 200
        custom_data = res.json()
        assert custom_data["viral_score"] > 60
        assert custom_data["analysis"]["summary"] != ""
