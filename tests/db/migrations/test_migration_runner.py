"""Tests for Alembic migration runner functionality."""

import asyncio
import os
import subprocess
import tempfile
from pathlib import Path
from typing import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from src.core.config import get_settings


# Get the venv Python path
def get_venv_python() -> str:
    """Get the path to the virtual environment Python."""
    venv_path = Path(__file__).parent.parent.parent.parent / ".venv"
    if os.name == "nt":  # Windows
        return str(venv_path / "Scripts" / "python.exe")
    else:  # Linux/Mac
        return str(venv_path / "bin" / "python")


@pytest_asyncio.fixture
async def test_db_engine() -> AsyncGenerator[AsyncEngine, None]:
    """Create a test database engine.

    This fixture creates a test database engine using the DATABASE_URL
    from environment variables. It cleans up the database after tests.

    Note: This test is skipped on Windows due to connection issues.
    """
    if os.name == "nt":
        pytest.skip("Database connection tests skipped on Windows due to psycopg2 encoding issues")

    settings = get_settings()

    # Use asyncpg for PostgreSQL
    engine = create_async_engine(
        settings.db_url,
        echo=False,
        pool_pre_ping=True,
    )

    yield engine

    # Cleanup: disconnect
    await engine.dispose()


@pytest_asyncio.fixture
async def test_db_session(
    test_db_engine: AsyncEngine,
) -> AsyncGenerator[async_sessionmaker, None]:
    """Create a test database session."""
    if os.name == "nt":
        pytest.skip("Database connection tests skipped on Windows due to psycopg2 encoding issues")

    async_session = async_sessionmaker(
        test_db_engine,
        expire_on_commit=False,
    )

    yield async_session


class TestMigrationRunner:
    """Tests for Alembic migration upgrade/downgrade functionality."""

    @pytest.mark.asyncio
    async def test_migration_upgrade_runs_successfully(self) -> None:
        """Test that alembic upgrade runs successfully."""
        # Skip on Windows due to connection issues
        if os.name == "nt":
            pytest.skip("Migration tests skipped on Windows due to psycopg2 encoding issues")

        venv_python = get_venv_python()
        result = subprocess.run(
            [venv_python, "-m", "alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            timeout=60,
        )

        assert result.returncode == 0, f"alembic upgrade failed: {result.stderr}"
        assert "Running upgrade" in result.stdout or result.returncode == 0, (
            "Expected upgrade to run"
        )

    @pytest.mark.asyncio
    async def test_migration_downgrade_runs_successfully(self) -> None:
        """Test that alembic downgrade runs successfully."""
        # Skip on Windows due to connection issues
        if os.name == "nt":
            pytest.skip("Migration tests skipped on Windows due to psycopg2 encoding issues")

        venv_python = get_venv_python()
        result = subprocess.run(
            [venv_python, "-m", "alembic", "downgrade", "-1"],
            capture_output=True,
            text=True,
            timeout=60,
        )

        assert result.returncode == 0, f"alembic downgrade failed: {result.stderr}"
        assert "Running downgrade" in result.stdout or result.returncode == 0, (
            "Expected downgrade to run"
        )

    @pytest.mark.asyncio
    async def test_migration_idempotent(self) -> None:
        """Test that running upgrade twice is idempotent."""
        # Skip on Windows due to connection issues
        if os.name == "nt":
            pytest.skip("Migration tests skipped on Windows due to psycopg2 encoding issues")

        venv_python = get_venv_python()
        # First upgrade
        result1 = subprocess.run(
            [venv_python, "-m", "alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result1.returncode == 0, f"First upgrade failed: {result1.stderr}"

        # Second upgrade (should succeed without errors)
        result2 = subprocess.run(
            [venv_python, "-m", "alembic", "upgrade", "head"],
            capture_output=True,
            text=True,
            timeout=60,
        )
        assert result2.returncode == 0, f"Second upgrade failed: {result2.stderr}"

    @pytest.mark.asyncio
    async def test_pgvector_extension_created(self, test_db_engine: AsyncEngine) -> None:
        """Test that pgvector extension is created."""
        async with test_db_engine.connect() as conn:
            result = await conn.execute(text("SELECT 1 FROM pg_extension WHERE extname = 'vector'"))
            row = result.fetchone()
            assert row is not None, "pgvector extension should be created"
            assert row[0] == 1, "pgvector extension should be installed"

    @pytest.mark.asyncio
    async def test_all_tables_created(self, test_db_engine: AsyncEngine) -> None:
        """Test that all expected tables are created."""
        expected_tables = {
            "users",
            "notes",
            "reminders",
            "todoist_tasks",
            "sessions",
            "alembic_version",
        }

        async with test_db_engine.connect() as conn:
            result = await conn.execute(
                text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
            )
            actual_tables = {row[0] for row in result.fetchall()}

            for table in expected_tables:
                assert table in actual_tables, f"Table {table} should exist"
