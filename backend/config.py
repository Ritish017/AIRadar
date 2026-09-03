import os
from typing import List, Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "AI Viral Radar"
    APP_ENV: str = "development"
    PORT: int = 8000
    HOST: str = "127.0.0.1"
    DEBUG: bool = True
    DEMO_MODE: bool = True

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./viral_radar.db"

    # Google Gemini AI Configuration (Primary AI Provider)
    DEFAULT_AI_PROVIDER: str = "gemini"  # gemini, offline
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-2.5-flash"  # e.g., gemini-2.5-flash, gemini-1.5-flash
    OPENAI_API_KEY: Optional[str] = None

    # Firecrawl Configuration (Primary Web Research & Scraping Layer)
    FIRECRAWL_API_KEY: Optional[str] = None
    FIRECRAWL_API_URL: str = "https://api.firecrawl.dev"

    # Discovery & Rate Limits
    DISCOVERY_INTERVAL_MINUTES: int = 30
    MAX_SEARCH_RESULTS: int = 5
    MAX_PAGES_PER_DISCOVERY: int = 10
    MAX_AI_ANALYSES_PER_RUN: int = 6
    VIRAL_THRESHOLD: float = 70.0

    # Pluggable X Provider Bearer Token (Optional)
    X_API_BEARER_TOKEN: Optional[str] = None

    # Anti-Copy Similarity Safeguard Threshold (0.0 to 1.0)
    SIMILARITY_THRESHOLD: float = 0.60

    # CORS Origins
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
