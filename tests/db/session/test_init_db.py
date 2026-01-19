"""Tests for init_db function."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from sqlalchemy.ext.asyncio import AsyncEngine

from src.db.session import init_db


@pytest.mark.asyncio
async def test_init_db_creates_engine():
    """Test that init_db creates an AsyncEngine."""
    # Mock the create_async_engine function
    with patch("src.db.session.create_async_engine") as mock_create_engine:
        mock_engine = AsyncMock(spec=AsyncEngine)
        mock_create_engine.return_value = mock_engine

        # Call init_db
        await init_db()

        # Verify create_async_engine was called
        mock_create_engine.assert_called_once()


@pytest.mark.asyncio
async def test_init_db_configures_pool_correctly():
    """Test that init_db configures pool with correct parameters."""
    with patch("src.db.session.create_async_engine") as mock_create_engine:
        mock_engine = AsyncMock(spec=AsyncEngine)
        mock_create_engine.return_value = mock_engine

        # Call init_db
        await init_db()

        # Get the call arguments
        call_kwargs = mock_create_engine.call_args.kwargs

        # Verify pool parameters
        assert call_kwargs.get("pool_size") == 10
        assert call_kwargs.get("max_overflow") == 20
        assert call_kwargs.get("pool_pre_ping") is True
        assert call_kwargs.get("pool_recycle") == 3600


@pytest.mark.asyncio
async def test_init_db_retry_on_connection_failure():
    """Test that init_db retries on connection failure."""
    with patch("src.db.session.create_async_engine") as mock_create_engine:
        # Fail first 2 times, succeed on 3rd
        mock_engine = AsyncMock(spec=AsyncEngine)
        mock_create_engine.side_effect = [
            Exception("Connection failed"),
            Exception("Connection failed"),
            mock_engine,
        ]

        # Call init_db - should succeed after retries
        await init_db()

        # Verify create_async_engine was called 3 times
        assert mock_create_engine.call_count == 3
