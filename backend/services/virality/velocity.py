from datetime import datetime, timezone
import math

def calculate_velocity_multiplier(
    published_at: datetime,
    likes: int,
    reposts: int,
    replies: int,
    views: int = 0
) -> tuple[float, float]:
    """
    Computes:
    1. velocity_per_hour: interactions per hour since publication.
    2. velocity_multiplier: scalar between 0.8 and 2.5 applied to the viral score.
    """
    now = datetime.now(timezone.utc)
    if published_at.tzinfo is None:
        published_at_utc = published_at.replace(tzinfo=timezone.utc)
    else:
        published_at_utc = published_at

    age_seconds = max(60.0, (now - published_at_utc).total_seconds())
    age_hours = age_seconds / 3600.0

    total_interactions = (likes * 1.0) + (reposts * 2.5) + (replies * 2.0)
    velocity_per_hour = total_interactions / age_hours

    # Acceleration factor based on interactions per hour
    # Rapid accumulation in the first few hours produces high multiplier
    if velocity_per_hour > 2000:
        multiplier = 2.4
    elif velocity_per_hour > 1000:
        multiplier = 2.0
    elif velocity_per_hour > 400:
        multiplier = 1.6
    elif velocity_per_hour > 150:
        multiplier = 1.3
    elif velocity_per_hour > 50:
        multiplier = 1.1
    elif velocity_per_hour > 10:
        multiplier = 1.0
    else:
        multiplier = 0.85

    # Percentage velocity vs expected baseline
    expected_baseline = max(5.0, age_hours * 15.0)
    velocity_pct = round(((velocity_per_hour / expected_baseline) - 1.0) * 100.0, 1)

    return multiplier, velocity_pct
