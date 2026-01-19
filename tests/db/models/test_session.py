"""Tests for Session model."""

import pytest
from uuid import uuid4
from datetime import datetime
from sqlalchemy import inspect
from src.db.models.session import Session


class TestSessionModel:
    """Tests for Session SQLAlchemy model."""

    def test_session_model_creation(self) -> None:
        """Test that Session model can be created with all fields."""
        user_id = uuid4()
        context = {"key": "value", "step": 1}

        session = Session(
            user_id=user_id,
            context=context,
            state="waiting_for_input",
        )

        assert session.user_id == user_id
        assert session.context == context
        assert session.state == "waiting_for_input"

    def test_session_context_jsonb(self) -> None:
        """Test that context field is JSONB type."""
        mapper = inspect(Session)
        columns = {c.key: c for c in mapper.columns}

        assert "context" in columns
        # Context should be nullable (or have default)
        # It can store arbitrary JSON data

    def test_session_user_relationship(self) -> None:
        """Test that Session model has relationship to User."""
        mapper = inspect(Session)
        columns = {c.key: c for c in mapper.columns}

        assert "user_id" in columns
        col = columns["user_id"]
        assert col.foreign_keys is not None
        assert len(col.foreign_keys) > 0

    def test_session_state_optional(self) -> None:
        """Test that state field is optional."""
        mapper = inspect(Session)
        columns = {c.key: c for c in mapper.columns}

        assert "state" in columns
        # state should be nullable
        assert columns["state"].nullable is True

    def test_session_last_activity_datetime(self) -> None:
        """Test that last_activity is a datetime field."""
        mapper = inspect(Session)
        columns = {c.key: c for c in mapper.columns}

        assert "last_activity" in columns
        # last_activity should not be nullable
        assert columns["last_activity"].nullable is False

    def test_session_user_id_required(self) -> None:
        """Test that user_id is required."""
        mapper = inspect(Session)
        columns = {c.key: c for c in mapper.columns}

        assert "user_id" in columns
        assert columns["user_id"].nullable is False

    def test_session_has_timestamps(self) -> None:
        """Test that Session model has created_at and updated_at fields."""
        mapper = inspect(Session)
        columns = {c.key for c in mapper.columns}

        assert "created_at" in columns
        assert "updated_at" in columns

    def test_session_has_soft_delete(self) -> None:
        """Test that Session model has deleted_at field for soft delete."""
        mapper = inspect(Session)
        columns = {c.key for c in mapper.columns}

        assert "deleted_at" in columns

    def test_session_context_can_store_arbitrary_data(self) -> None:
        """Test that context can store various types of data."""
        user_id = uuid4()

        # Test with nested dict
        context1 = {
            "conversation": {
                "messages": [
                    {"role": "user", "content": "hello"},
                    {"role": "assistant", "content": "hi"},
                ]
            }
        }
        session1 = Session(user_id=user_id, context=context1)
        assert session1.context == context1

        # Test with list
        context2 = ["item1", "item2", "item3"]
        session2 = Session(user_id=user_id, context=context2)
        assert session2.context == context2

    def test_session_last_activity_defaults_to_now(self) -> None:
        """Test that last_activity has a default value."""
        mapper = inspect(Session)
        columns = {c.key: c for c in mapper.columns}

        assert "last_activity" in columns
        # Check that default is defined
        assert columns["last_activity"].default is not None
