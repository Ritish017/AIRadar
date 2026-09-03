import math

def calculate_engagement_rate(
    views: int,
    likes: int,
    reposts: int,
    replies: int,
    quotes: int = 0
) -> float:
    """
    Calculates engagement rate as a percentage.
    If views are known (> 0), engagement rate = (interactions / views) * 100.
    If views are 0 (e.g. RSS or Reddit), uses an estimated baseline.
    """
    total_interactions = (likes * 1.0) + (reposts * 2.0) + (replies * 1.5) + (quotes * 2.5)

    if views > 0:
        rate = (total_interactions / views) * 100.0
        return round(min(100.0, rate), 2)
    else:
        # Fallback estimation for platforms where views are not publicly exposed
        estimated_views = max(1000, total_interactions * 15)
        rate = (total_interactions / estimated_views) * 100.0
        return round(min(100.0, rate), 2)


def calculate_base_engagement_score(
    views: int,
    likes: int,
    reposts: int,
    replies: int,
    quotes: int = 0
) -> float:
    """
    Calculates raw weighted engagement points.
    Reposts and quotes carry heavy virality signal.
    Uses log compression to avoid mega-accounts crushing all nascent viral posts.
    """
    weighted_interactions = (
        (likes * 1.5) +
        (reposts * 4.0) +
        (replies * 2.5) +
        (quotes * 5.0) +
        (views / 300.0 if views > 0 else 0)
    )

    if weighted_interactions <= 0:
        return 5.0

    # Log scaling gives a value typically between 10 and 60
    base_score = 10.0 + (math.log10(weighted_interactions + 1) * 11.5)
    return min(70.0, max(5.0, base_score))
