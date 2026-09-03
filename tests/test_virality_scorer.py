from datetime import datetime, timezone, timedelta
from backend.services.virality.scorer import virality_scorer
from backend.services.virality.engagement import calculate_base_engagement_score, calculate_engagement_rate
from backend.services.virality.velocity import calculate_velocity_multiplier

def test_engagement_rate_with_views():
    rate = calculate_engagement_rate(views=100000, likes=5000, reposts=1000, replies=500)
    assert 0 < rate <= 100
    assert rate == 7.75

def test_engagement_rate_without_views():
    rate = calculate_engagement_rate(views=0, likes=100, reposts=50, replies=20)
    assert 0 < rate <= 100

def test_freshness_decay():
    now = datetime.now(timezone.utc)
    fresh = virality_scorer.calculate_freshness_multiplier(now - timedelta(minutes=30))
    stale = virality_scorer.calculate_freshness_multiplier(now - timedelta(days=3))
    assert fresh > stale
    assert fresh >= 0.95
    assert stale <= 0.40

def test_velocity_multiplier():
    now = datetime.now(timezone.utc)
    mult, pct = calculate_velocity_multiplier(now - timedelta(minutes=30), likes=5000, reposts=1000, replies=500)
    assert mult >= 2.0
    assert pct > 100.0

def test_viral_score_bounds_and_classification():
    now = datetime.now(timezone.utc)
    res = virality_scorer.score_item(
        published_at=now - timedelta(minutes=40),
        views=2500000,
        likes=35000,
        reposts=6000,
        replies=1200
    )
    assert 0.0 <= res["viral_score"] <= 100.0
    assert res["viral_score"] >= 80.0
    assert res["classification"] in ["Hot", "Viral"]
    assert "Exploding" in res["badge"] or "Hot" in res["badge"]

def test_low_engagement_post():
    now = datetime.now(timezone.utc)
    res = virality_scorer.score_item(
        published_at=now - timedelta(days=2),
        views=200,
        likes=2,
        reposts=0,
        replies=0
    )
    assert res["viral_score"] <= 35.0
    assert res["classification"] in ["Low", "Normal"]

def test_missing_social_metrics_uses_viral_potential():
    now = datetime.now(timezone.utc)
    # When metrics are missing (e.g. newly discovered web article)
    res = virality_scorer.score_item(
        published_at=now - timedelta(hours=1),
        title="OpenAI announces breakthrough reasoning model SOTA on SWE-bench",
        content="New open weights release with massive benchmarks and developer API.",
        views=None,
        likes=None,
        reposts=None,
        source_quality="Tier 1"
    )
    assert res["viral_score"] is None
    assert res["engagement_rate"] is None
    assert res["viral_potential"] >= 70.0
    assert "Viral Potential" in res["badge"]
