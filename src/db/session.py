"""Database session and connection management."""

import asyncio
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.core.config import get_settings

# Global engine and session factory
engine: AsyncEngine | None = None
async_session_factory: async_sessionmaker[AsyncSession] | None = None


async def init_db() -> None:
    """Initialize database connection pool.

    Creates AsyncEngine with connection pooling configured.
    Should be called once at application startup.

    Connection pool parameters:
        - pool_size: 10 (default number of connections)
        - max_overflow: 20 (maximum additional connections)
        - pool_pre_ping: True (test connections before use)
        - pool_recycle: 3600 (recycle connections after 1 hour)

    Raises:
        Exception: If connection fails after 3 retry attempts.
    """
    global engine, async_session_factory

    settings = get_settings()
    db_url = settings.db_url

    # Connection retry logic with exponential backoff
    max_attempts = 3
    for attempt in range(1, max_attempts + 1):
        try:
            engine = create_async_engine(
                db_url,
                pool_size=10,
                max_overflow=20,
                pool_pre_ping=True,
                pool_recycle=3600,
                echo=settings.debug,
            )

            # Test connection
            from sqlalchemy import text

            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))

            # Create session factory
            async_session_factory = async_sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False,
            )

            return

        except Exception as e:
            if attempt < max_attempts:
                # Exponential backoff: 1s, 2s, 4s
                backoff = 2 ** (attempt - 1)
                await asyncio.sleep(backoff)
            else:
                raise Exception(f"Failed to connect to database after {max_attempts} attempts: {e}")


async def close_db() -> None:
    """Close database connection pool gracefully.

    Disposes all connections in the pool.
    Should be called once at application shutdown.
    """
    global engine, async_session_factory

    if engine is not None:
        await engine.dispose()
        engine = None
        async_session_factory = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database session.

    Yields an AsyncSession for each request.
    Automatically closes the session after use.

    Yields:
        AsyncSession: Database session for the request.
    """
    global async_session_factory

    if async_session_factory is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")

    async with async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()
