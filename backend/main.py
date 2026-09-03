import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import settings
from backend.db.session import init_db, AsyncSessionLocal
from backend.api.v1 import router as api_router
from backend.providers.manager import provider_manager
from backend.workers.scheduler import run_periodic_ingestion

logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("ai_viral_radar")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database schemas...")
    await init_db()

    # Initial bootstrap ingestion if database is fresh
    try:
        async with AsyncSessionLocal() as session:
            logger.info("Running initial content collection bootstrap...")
            await provider_manager.ingest_all(session)
    except Exception as e:
        logger.warning(f"Initial ingestion warning: {e}")

    # Start background ingestion worker
    bg_task = asyncio.create_task(run_periodic_ingestion())

    yield

    # Clean shutdown
    bg_task.cancel()
    logger.info("Shutdown complete.")

app = FastAPI(
    title="AI Viral Radar API",
    description="Discover viral AI content, analyze hook & virality dynamics, and synthesize original high-signal posts.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for Web Dashboard and Chrome Extension
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

@app.get("/")
async def root():
    return {
        "product": "AI Viral Radar",
        "tagline": "Find what's going viral in AI before everyone else.",
        "docs_url": "/docs",
        "api_health": "/api/health"
    }
