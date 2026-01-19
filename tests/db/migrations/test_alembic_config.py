"""Tests for Alembic configuration and setup."""

import os
from pathlib import Path

import pytest


class TestAlembicConfig:
    """Tests for Alembic configuration files and structure."""

    def test_alembic_directory_exists(self) -> None:
        """Test that the alembic directory exists."""
        alembic_dir = Path(__file__).parent.parent.parent.parent / "alembic"
        assert alembic_dir.exists(), f"alembic directory does not exist at {alembic_dir}"
        assert alembic_dir.is_dir(), f"alembic is not a directory at {alembic_dir}"

    def test_alembic_ini_exists(self) -> None:
        """Test that alembic.ini exists in the project root."""
        root_dir = Path(__file__).parent.parent.parent.parent
        alembic_ini = root_dir / "alembic.ini"
        assert alembic_ini.exists(), f"alembic.ini does not exist at {alembic_ini}"
        assert alembic_ini.is_file(), f"alembic.ini is not a file at {alembic_ini}"

    def test_env_py_exists(self) -> None:
        """Test that alembic/env.py exists."""
        env_py = Path(__file__).parent.parent.parent.parent / "alembic" / "env.py"
        assert env_py.exists(), f"alembic/env.py does not exist at {env_py}"
        assert env_py.is_file(), f"alembic/env.py is not a file at {env_py}"

    def test_versions_directory_exists(self) -> None:
        """Test that the alembic/versions directory exists."""
        versions_dir = Path(__file__).parent.parent.parent.parent / "alembic" / "versions"
        assert versions_dir.exists(), f"alembic/versions directory does not exist at {versions_dir}"
        assert versions_dir.is_dir(), f"alembic/versions is not a directory at {versions_dir}"

    def test_script_py_mako_exists(self) -> None:
        """Test that alembic/script.py.mako exists."""
        script_py_mako = Path(__file__).parent.parent.parent.parent / "alembic" / "script.py.mako"
        assert script_py_mako.exists(), f"alembic/script.py.mako does not exist at {script_py_mako}"
        assert script_py_mako.is_file(), f"alembic/script.py.mako is not a file at {script_py_mako}"

    def test_env_py_contains_async_imports(self) -> None:
        """Test that env.py contains async engine imports."""
        env_py = Path(__file__).parent.parent.parent.parent / "alembic" / "env.py"
        content = env_py.read_text()

        # Check for async imports
        assert "AsyncEngine" in content or "async_engine_from_config" in content, (
            "env.py should import async engine from sqlalchemy.ext.asyncio"
        )

    def test_env_py_imports_models(self) -> None:
        """Test that env.py imports all models."""
        env_py = Path(__file__).parent.parent.parent.parent / "alembic" / "env.py"
        content = env_py.read_text()

        # Check that models are imported
        assert "from src.db.models import" in content or "import src.db.models" in content, (
            "env.py should import models from src.db.models"
        )

    def test_alembic_ini_database_url_configured(self) -> None:
        """Test that alembic.ini has database URL configuration."""
        root_dir = Path(__file__).parent.parent.parent.parent
        alembic_ini = root_dir / "alembic.ini"
        content = alembic_ini.read_text()

        # Check for database URL configuration
        assert "sqlalchemy.url" in content, (
            "alembic.ini should contain sqlalchemy.url configuration"
        )
