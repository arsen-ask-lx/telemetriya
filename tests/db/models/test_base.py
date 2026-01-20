"""Test Base declarative class."""

import pytest
from sqlalchemy import inspect
from src.db.base import Base


class TestBase:
    """Tests for Base declarative class."""

    def test_base_is_declarative_base(self) -> None:
        """Test that Base is a SQLAlchemy declarative base."""
        # Base should have metadata
        assert hasattr(Base, "metadata")
        assert Base.metadata is not None

    def test_base_has_metadata(self) -> None:
        """Test that Base.metadata is a MetaData object."""
        from sqlalchemy.schema import MetaData

        assert isinstance(Base.metadata, MetaData)
        # Metadata should contain all model tables after models are imported
        assert len(Base.metadata.tables) >= 0
        # Expected tables: users, notes, reminders, todoist_tasks, sessions
        table_names = set(Base.metadata.tables.keys())
        expected_tables = {"users", "notes", "reminders", "todoist_tasks", "sessions"}
        assert expected_tables.issubset(table_names)
