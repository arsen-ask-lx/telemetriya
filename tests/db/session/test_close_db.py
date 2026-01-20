"""Tests for close_db function."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.db.session import close_db


@pytest.mark.asyncio
async def test_close_db_disposes_engine():
    """Test that close_db disposes engine."""
    with patch("src.db.session.engine") as mock_engine:
        mock_engine.dispose = AsyncMock()

        # Call close_db
        await close_db()

        # Verify dispose was called
        mock_engine.dispose.assert_called_once()


@pytest.mark.asyncio
async def test_close_db_is_idempotent():
    """Test that close_db can be called multiple times safely."""
    with patch("src.db.session.engine") as mock_engine:
        mock_engine.dispose = AsyncMock()

        # Call close_db multiple times
        await close_db()
        await close_db()
        await close_db()

        # Should not raise any exceptions
        # Test passes if no exceptions are raised
