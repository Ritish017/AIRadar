import asyncio
import logging
from backend.db.session import AsyncSessionLocal
from backend.providers.manager import provider_manager
from backend.config import settings

logger = logging.getLogger(__name__)

async def run_periodic_ingestion():
    """Background task running periodic content collection."""
    logger.info("Starting background ingestion worker")
    while True:
        try:
            async with AsyncSessionLocal() as session:
                stats = await provider_manager.ingest_all(session)
                logger.info(f"Periodic ingestion cycle complete: {stats}")
        except Exception as e:
            logger.error(f"Error in background ingestion loop: {e}")

        # Wait configured minutes
        await asyncio.sleep(settings.DISCOVERY_INTERVAL_MINUTES * 60)
