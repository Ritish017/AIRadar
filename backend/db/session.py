import logging
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from backend.config import settings

logger = logging.getLogger(__name__)

# Configure engine
connect_args = {}
if "sqlite" in settings.DATABASE_URL:
    connect_args["check_same_thread"] = False

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    connect_args=connect_args,
    future=True
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

def _run_migrations(connection):
    """Safely adds newly declared columns to SQLite tables if missing."""
    try:
        # Check content_items table columns
        cols_res = connection.execute(text("PRAGMA table_info(content_items)"))
        existing_cols = {row[1] for row in cols_res.fetchall()}

        if existing_cols:
            migrations = [
                ("source_quality", "ALTER TABLE content_items ADD COLUMN source_quality VARCHAR(20) DEFAULT 'Tier 1'"),
                ("primary_source_url", "ALTER TABLE content_items ADD COLUMN primary_source_url VARCHAR(1024)"),
                ("source_count", "ALTER TABLE content_items ADD COLUMN source_count INTEGER DEFAULT 1"),
                ("viral_potential", "ALTER TABLE content_items ADD COLUMN viral_potential FLOAT DEFAULT 75.0"),
                ("confirmed_facts", "ALTER TABLE content_items ADD COLUMN confirmed_facts JSON DEFAULT '[]'"),
                ("uncertain_claims", "ALTER TABLE content_items ADD COLUMN uncertain_claims JSON DEFAULT '[]'"),
                ("last_seen_at", "ALTER TABLE content_items ADD COLUMN last_seen_at DATETIME")
            ]
            for col_name, sql in migrations:
                if col_name not in existing_cols:
                    connection.execute(text(sql))
                    logger.info(f"Added missing column '{col_name}' to content_items")

        # Check analyses table columns
        cols_res_a = connection.execute(text("PRAGMA table_info(analyses)"))
        existing_cols_a = {row[1] for row in cols_res_a.fetchall()}

        if existing_cols_a:
            a_migrations = [
                ("confirmed_facts", "ALTER TABLE analyses ADD COLUMN confirmed_facts JSON DEFAULT '[]'"),
                ("uncertain_claims", "ALTER TABLE analyses ADD COLUMN uncertain_claims JSON DEFAULT '[]'"),
                ("viral_potential", "ALTER TABLE analyses ADD COLUMN viral_potential FLOAT DEFAULT 75.0")
            ]
            for col_name, sql in a_migrations:
                if col_name not in existing_cols_a:
                    connection.execute(text(sql))
                    logger.info(f"Added missing column '{col_name}' to analyses")

        # Check topics table columns
        cols_res_t = connection.execute(text("PRAGMA table_info(topics)"))
        existing_cols_t = {row[1] for row in cols_res_t.fetchall()}

        if existing_cols_t:
            t_migrations = [
                ("lifecycle_stage", "ALTER TABLE topics ADD COLUMN lifecycle_stage VARCHAR(50) DEFAULT 'RISING'"),
                ("opportunity_score", "ALTER TABLE topics ADD COLUMN opportunity_score FLOAT DEFAULT 70.0"),
                ("opportunity_type", "ALTER TABLE topics ADD COLUMN opportunity_type VARCHAR(50) DEFAULT 'RISING_OPPORTUNITY'"),
                ("competition_score", "ALTER TABLE topics ADD COLUMN competition_score FLOAT DEFAULT 40.0"),
                ("novelty_score", "ALTER TABLE topics ADD COLUMN novelty_score FLOAT DEFAULT 80.0"),
                ("audience_fit_score", "ALTER TABLE topics ADD COLUMN audience_fit_score FLOAT DEFAULT 85.0"),
                ("momentum_change_pct", "ALTER TABLE topics ADD COLUMN momentum_change_pct FLOAT DEFAULT 0.0"),
                ("momentum_direction", "ALTER TABLE topics ADD COLUMN momentum_direction VARCHAR(50) DEFAULT 'STABLE'"),
                ("recommended_action", "ALTER TABLE topics ADD COLUMN recommended_action VARCHAR(50) DEFAULT 'POST_SOON'"),
                ("action_reason", "ALTER TABLE topics ADD COLUMN action_reason TEXT"),
                ("recommended_angle", "ALTER TABLE topics ADD COLUMN recommended_angle TEXT"),
                ("alternative_angles", "ALTER TABLE topics ADD COLUMN alternative_angles JSON DEFAULT '[]'"),
                ("saturated_angles", "ALTER TABLE topics ADD COLUMN saturated_angles JSON DEFAULT '[]'"),
                ("under_served_angles", "ALTER TABLE topics ADD COLUMN under_served_angles JSON DEFAULT '[]'"),
                ("recommended_hook_type", "ALTER TABLE topics ADD COLUMN recommended_hook_type VARCHAR(100) DEFAULT 'contrarian'"),
                ("hook_strategy", "ALTER TABLE topics ADD COLUMN hook_strategy TEXT"),
                ("recommended_format", "ALTER TABLE topics ADD COLUMN recommended_format VARCHAR(50) DEFAULT 'single_post'"),
                ("format_scores", "ALTER TABLE topics ADD COLUMN format_scores JSON DEFAULT '{}'"),
                ("primary_audience", "ALTER TABLE topics ADD COLUMN primary_audience VARCHAR(100) DEFAULT 'AI Engineers'"),
                ("secondary_audiences", "ALTER TABLE topics ADD COLUMN secondary_audiences JSON DEFAULT '[]'"),
                ("created_at", "ALTER TABLE topics ADD COLUMN created_at DATETIME")
            ]
            for col_name, sql in t_migrations:
                if col_name not in existing_cols_t:
                    connection.execute(text(sql))
                    logger.info(f"Added missing column '{col_name}' to topics")

    except Exception as e:
        logger.warning(f"Schema migration notice: {e}")

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        if "sqlite" in settings.DATABASE_URL:
            await conn.run_sync(_run_migrations)
