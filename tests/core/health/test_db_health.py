"""Tests for check_db_health function."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from src.core.health import check_db_health


@pytest.mark.asyncio
async def test_db_health_returns_true_when_connected():
    """Test that check_db_health returns True when database is connected."""
    from sqlalchemy import text

    # Create mock connection
    mock_conn = MagicMock()
    mock_conn.execute = AsyncMock()

    # Create mock async context manager for connect()
    class MockConnectionCM:
        async def __aenter__(self):
            return mock_conn

        async def __aexit__(self, *args):
            pass

    mock_connect_cm = MockConnectionCM()

    mock_engine = MagicMock()
    mock_engine.connect.return_value = mock_connect_cm

    with patch("src.db.session.engine", mock_engine):
        # Check health
        result = await check_db_health()

        assert result is True


@pytest.mark.asyncio
async def test_db_health_returns_false_when_disconnected():
    """Test that check_db_health returns False when database is disconnected."""

    # Create mock async context manager that raises exception
    class MockConnectionCM:
        async def __aenter__(self):
            raise Exception("Connection failed")

        async def __aexit__(self, *args):
            pass

    mock_connect_cm = MockConnectionCM()

    mock_engine = MagicMock()
    mock_engine.connect.return_value = mock_connect_cm

    with patch("src.db.session.engine", mock_engine):
        # Check health
        result = await check_db_health()

        assert result is False
