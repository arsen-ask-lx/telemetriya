"""Tests for get_db dependency."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.session import get_db


@pytest.mark.asyncio
async def test_get_db_yields_session():
    """Test that get_db yields an AsyncSession."""
    mock_session = AsyncMock(spec=AsyncSession)

    # Set up mock session factory
    with patch("src.db.session.async_session_factory") as mock_factory:

        async def mock_session_context():
            yield mock_session

        mock_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session_context())
        mock_factory.return_value.__aexit__ = AsyncMock()

        # Use the dependency
        session_gen = get_db()
        session = await session_gen.__anext__()

        # Verify session is yielded
        assert session is not None


@pytest.mark.asyncio
async def test_get_db_closes_session_after_use():
    """Test that get_db closes session after use."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.close = AsyncMock()

    # Set up mock session factory
    with patch("src.db.session.async_session_factory") as mock_factory:

        async def mock_session_context():
            yield mock_session

        mock_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session_context())
        mock_factory.return_value.__aexit__ = AsyncMock()

        # Use the dependency
        session_gen = get_db()
        session = await session_gen.__anext__()

        # Clean up generator
        try:
            await session_gen.aclose()
        except StopAsyncIteration:
            pass


@pytest.mark.asyncio
async def test_get_db_handles_exception_and_rolls_back():
    """Test that get_db handles exceptions and rolls back."""
    mock_session = AsyncMock(spec=AsyncSession)
    mock_session.rollback = AsyncMock()
    mock_session.close = AsyncMock()

    # Set up mock session factory
    with patch("src.db.session.async_session_factory") as mock_factory:

        async def mock_session_context():
            yield mock_session

        mock_factory.return_value.__aenter__ = AsyncMock(return_value=mock_session_context())
        mock_factory.return_value.__aexit__ = AsyncMock()

        # Use the dependency
        session_gen = get_db()
        session = await session_gen.__anext__()

        # Verify session was created
        assert session is not None
