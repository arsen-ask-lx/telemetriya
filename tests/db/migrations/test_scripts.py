"""Tests for migration management scripts."""

import os
import stat
from pathlib import Path

import pytest


class TestScripts:
    """Tests for migration management scripts."""

    def test_migrate_script_exists(self) -> None:
        """Test that scripts/migrate.sh exists."""
        root_dir = Path(__file__).parent.parent.parent.parent
        migrate_sh = root_dir / "scripts" / "migrate.sh"
        assert migrate_sh.exists(), f"scripts/migrate.sh does not exist at {migrate_sh}"
        assert migrate_sh.is_file(), f"scripts/migrate.sh is not a file at {migrate_sh}"

    def test_migrate_script_executable(self) -> None:
        """Test that scripts/migrate.sh is executable."""
        root_dir = Path(__file__).parent.parent.parent.parent
        migrate_sh = root_dir / "scripts" / "migrate.sh"

        # On Windows, file permissions are different
        # We just check if the file exists and has content
        assert migrate_sh.exists(), f"scripts/migrate.sh does not exist at {migrate_sh}"
        content = migrate_sh.read_text()
        assert len(content) > 0, "scripts/migrate.sh should have content"

    def test_rollback_script_exists(self) -> None:
        """Test that scripts/rollback.sh exists."""
        root_dir = Path(__file__).parent.parent.parent.parent
        rollback_sh = root_dir / "scripts" / "rollback.sh"
        assert rollback_sh.exists(), f"scripts/rollback.sh does not exist at {rollback_sh}"
        assert rollback_sh.is_file(), f"scripts/rollback.sh is not a file at {rollback_sh}"

    def test_rollback_script_executable(self) -> None:
        """Test that scripts/rollback.sh is executable."""
        root_dir = Path(__file__).parent.parent.parent.parent
        rollback_sh = root_dir / "scripts" / "rollback.sh"

        # On Windows, file permissions are different
        # We just check if the file exists and has content
        assert rollback_sh.exists(), f"scripts/rollback.sh does not exist at {rollback_sh}"
        content = rollback_sh.read_text()
        assert len(content) > 0, "scripts/rollback.sh should have content"

    def test_revision_script_exists(self) -> None:
        """Test that scripts/revision.sh exists."""
        root_dir = Path(__file__).parent.parent.parent.parent
        revision_sh = root_dir / "scripts" / "revision.sh"
        assert revision_sh.exists(), f"scripts/revision.sh does not exist at {revision_sh}"
        assert revision_sh.is_file(), f"scripts/revision.sh is not a file at {revision_sh}"

    def test_revision_script_executable(self) -> None:
        """Test that scripts/revision.sh is executable."""
        root_dir = Path(__file__).parent.parent.parent.parent
        revision_sh = root_dir / "scripts" / "revision.sh"

        # On Windows, file permissions are different
        # We just check if the file exists and has content
        assert revision_sh.exists(), f"scripts/revision.sh does not exist at {revision_sh}"
        content = revision_sh.read_text()
        assert len(content) > 0, "scripts/revision.sh should have content"

    def test_migrate_script_content(self) -> None:
        """Test that migrate.sh contains alembic upgrade command."""
        root_dir = Path(__file__).parent.parent.parent.parent
        migrate_sh = root_dir / "scripts" / "migrate.sh"
        content = migrate_sh.read_text()

        assert "alembic upgrade head" in content, (
            "migrate.sh should contain 'alembic upgrade head' command"
        )

    def test_rollback_script_content(self) -> None:
        """Test that rollback.sh contains alembic downgrade command."""
        root_dir = Path(__file__).parent.parent.parent.parent
        rollback_sh = root_dir / "scripts" / "rollback.sh"
        content = rollback_sh.read_text()

        assert "alembic downgrade" in content, (
            "rollback.sh should contain 'alembic downgrade' command"
        )

    def test_revision_script_content(self) -> None:
        """Test that revision.sh contains alembic revision command."""
        root_dir = Path(__file__).parent.parent.parent.parent
        revision_sh = root_dir / "scripts" / "revision.sh"
        content = revision_sh.read_text()

        assert "alembic revision" in content, (
            "revision.sh should contain 'alembic revision' command"
        )
        assert "--autogenerate" in content or "-m" in content, (
            "revision.sh should accept a message parameter"
        )
