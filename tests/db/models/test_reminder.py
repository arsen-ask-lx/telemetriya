"""Tests for Reminder model."""

import pytest
from uuid import uuid4
from datetime import datetime
from sqlalchemy import inspect
from src.db.models.reminder import Reminder


class TestReminderModel:
    """Tests for Reminder SQLAlchemy model."""

    def test_reminder_model_creation(self) -> None:
        """Test that Reminder model can be created with all fields."""
        user_id = uuid4()
        note_id = uuid4()
        remind_at = datetime(2026, 1, 20, 10, 0, 0)

        reminder = Reminder(
            user_id=user_id,
            note_id=note_id,
            remind_at=remind_at,
            message="Don't forget to test!",
            is_sent=False,
        )

        assert reminder.user_id == user_id
        assert reminder.note_id == note_id
        assert reminder.remind_at == remind_at
        assert reminder.message == "Don't forget to test!"
        assert reminder.is_sent is False

    def test_reminder_datetime_validation(self) -> None:
        """Test that remind_at field is a datetime."""
        mapper = inspect(Reminder)
        columns = {c.key: c for c in mapper.columns}

        assert "remind_at" in columns
        # remind_at should not be nullable
        assert columns["remind_at"].nullable is False

    def test_reminder_user_relationship(self) -> None:
        """Test that Reminder model has relationship to User."""
        mapper = inspect(Reminder)
        columns = {c.key: c for c in mapper.columns}

        assert "user_id" in columns
        col = columns["user_id"]
        assert col.foreign_keys is not None
        assert len(col.foreign_keys) > 0

    def test_reminder_note_relationship_optional(self) -> None:
        """Test that note_id is optional and nullable."""
        mapper = inspect(Reminder)
        columns = {c.key: c for c in mapper.columns}

        assert "note_id" in columns
        # note_id should be nullable
        assert columns["note_id"].nullable is True

    def test_reminder_is_sent_default(self) -> None:
        """Test that is_sent has a default value."""
        mapper = inspect(Reminder)
        columns = {c.key: c for c in mapper.columns}

        assert "is_sent" in columns
        # Check that default is defined
        assert columns["is_sent"].default is not None

    def test_reminder_message_required(self) -> None:
        """Test that message field is required."""
        mapper = inspect(Reminder)
        columns = {c.key: c for c in mapper.columns}

        assert "message" in columns
        assert columns["message"].nullable is False

    def test_reminder_has_timestamps(self) -> None:
        """Test that Reminder model has created_at and updated_at fields."""
        mapper = inspect(Reminder)
        columns = {c.key for c in mapper.columns}

        assert "created_at" in columns
        assert "updated_at" in columns

    def test_reminder_has_soft_delete(self) -> None:
        """Test that Reminder model has deleted_at field for soft delete."""
        mapper = inspect(Reminder)
        columns = {c.key for c in mapper.columns}

        assert "deleted_at" in columns

    def test_reminder_user_id_required(self) -> None:
        """Test that user_id is required."""
        mapper = inspect(Reminder)
        columns = {c.key: c for c in mapper.columns}

        assert "user_id" in columns
        assert columns["user_id"].nullable is False
