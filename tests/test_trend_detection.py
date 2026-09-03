from datetime import datetime, timezone
from backend.services.virality.trend_detection import trend_detector

def test_topic_clustering_and_momentum():
    items = [
        {
            "title": "OpenAI releases new reasoning model",
            "content": "OpenAI announces reasoning model with computer use",
            "source_type": "x",
            "topic": "Models",
            "viral_score": 95
        },
        {
            "title": "OpenAI announces reasoning improvements",
            "content": "New reasoning benchmark from OpenAI beats previous records",
            "source_type": "reddit",
            "topic": "Models",
            "viral_score": 90
        },
        {
            "title": "Reasoning model released by OpenAI",
            "content": "Deep dive into OpenAI's reasoning architecture",
            "source_type": "news",
            "topic": "Models",
            "viral_score": 88
        },
        {
            "title": "Figure AI humanoid robot fleet demo",
            "content": "Autonomous humanoid robots deployed in commercial warehouse",
            "source_type": "x",
            "topic": "Robotics",
            "viral_score": 84
        }
    ]

    clusters = trend_detector.cluster_topics(items)
    assert len(clusters) >= 2

    # OpenAI reasoning items should cluster together with multi-source status
    top_cluster = clusters[0]
    assert top_cluster["item_count"] >= 2
    assert len(top_cluster["sources_summary"]) >= 2
    assert "Exploding" in top_cluster["status"] or "Surging" in top_cluster["status"]
    assert top_cluster["momentum"] > 150.0
