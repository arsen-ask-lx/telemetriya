"""Tests for connection retry logic."""

import pytest
from unittest.mock import AsyncMock, patch
import asyncio
from sqlalchemy.ext.asyncio import AsyncEngine

from src.db.session import init_db


@pytest.mark.asyncio
async def test_retry_on_connection_error():
    """Test that connection retry happens on connection error."""
    with patch("src.db.session.create_async_engine") as mock_create_engine:
        # Fail first time, succeed on second
        mock_engine = AsyncMock(spec=AsyncEngine)
        mock_create_engine.side_effect = [
            Exception("Connection failed"),
            mock_engine,
        ]

        # Should succeed after retry
        await init_db()

        assert mock_create_engine.call_count == 2


@pytest.mark.asyncio
async def test_retry_with_exponential_backoff():
    """Test that retry uses exponential backoff (1, 2, 4 seconds)."""
    with patch("src.db.session.create_async_engine") as mock_create_engine:
        with patch("asyncio.sleep") as mock_sleep:
            # Fail 2 times, succeed on 3rd
            mock_engine = AsyncMock(spec=AsyncEngine)
            mock_create_engine.side_effect = [
                Exception("Connection failed"),
                Exception("Connection failed"),
                mock_engine,
            ]

            await init_db()

            # Verify sleep was called with exponential backoff
            # First retry: 1 second, second retry: 2 seconds
            assert mock_sleep.call_count == 2
            mock_sleep.assert_any_call(1)
            mock_sleep.assert_any_call(2)


@pytest.mark.asyncio
async def test_retry_max_attempts():
    """Test that retry stops after max attempts (3 attempts)."""
    with patch("src.db.session.create_async_engine") as mock_create_engine:
        with patch("asyncio.sleep"):
            # Always fail
            mock_create_engine.side_effect = Exception("Connection failed")

            # Should raise exception after max attempts
            with pytest.raises(Exception, match="Failed to connect to database after 3 attempts"):
                await init_db()

            # Verify tried 3 times
            assert mock_create_engine.call_count == 3
