"""Tests for connection pool configuration."""

import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncEngine

from src.db.session import init_db


@pytest.mark.asyncio
async def test_pool_size_configured():
    """Test that pool_size is configured correctly."""
    with patch("src.db.session.create_async_engine") as mock_create_engine:
        mock_engine = AsyncMock(spec=AsyncEngine)
        mock_create_engine.return_value = mock_engine

        await init_db()

        call_kwargs = mock_create_engine.call_args.kwargs
        assert call_kwargs.get("pool_size") == 10


@pytest.mark.asyncio
async def test_max_overflow_configured():
    """Test that max_overflow is configured correctly."""
    with patch("src.db.session.create_async_engine") as mock_create_engine:
        mock_engine = AsyncMock(spec=AsyncEngine)
        mock_create_engine.return_value = mock_engine

        await init_db()

        call_kwargs = mock_create_engine.call_args.kwargs
        assert call_kwargs.get("max_overflow") == 20


@pytest.mark.asyncio
async def test_pool_pre_ping_enabled():
    """Test that pool_pre_ping is enabled."""
    with patch("src.db.session.create_async_engine") as mock_create_engine:
        mock_engine = AsyncMock(spec=AsyncEngine)
        mock_create_engine.return_value = mock_engine

        await init_db()

        call_kwargs = mock_create_engine.call_args.kwargs
        assert call_kwargs.get("pool_pre_ping") is True


@pytest.mark.asyncio
async def test_pool_recycle_configured():
    """Test that pool_recycle is configured correctly (3600 seconds = 1 hour)."""
    with patch("src.db.session.create_async_engine") as mock_create_engine:
        mock_engine = AsyncMock(spec=AsyncEngine)
        mock_create_engine.return_value = mock_engine

        await init_db()

        call_kwargs = mock_create_engine.call_args.kwargs
        assert call_kwargs.get("pool_recycle") == 3600
