"""FastAPI dependencies."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database session.

    This is a wrapper around src.db.session.get_db() for use
    in FastAPI route handlers.

    Yields:
        AsyncSession: Database session for the request.
    """
    async for session in get_db():
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """FastAPI lifespan context manager.

    Initializes database on startup and closes on shutdown.

    Args:
        app: FastAPI application instance.

    Yields:
        None
    """
    from src.db.session import close_db, init_db

    # Startup
    await init_db()

    yield

    # Shutdown
    await close_db()
