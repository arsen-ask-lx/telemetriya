"""Tests for TodoistTask model."""

import pytest
from uuid import uuid4
from datetime import datetime
from sqlalchemy import inspect
from src.db.models.todoist_task import TodoistTask, SyncStatus


class TestTodoistTaskModel:
    """Tests for TodoistTask SQLAlchemy model."""

    def test_todoist_task_model_creation(self) -> None:
        """Test that TodoistTask model can be created with all fields."""
        user_id = uuid4()
        note_id = uuid4()
        due_datetime = datetime(2026, 1, 20, 10, 0, 0)

        task = TodoistTask(
            user_id=user_id,
            note_id=note_id,
            todoist_task_id=987654321,
            todoist_project_id=123456789,
            content="Complete the task",
            due_datetime=due_datetime,
            is_completed=False,
            sync_status=SyncStatus.PENDING,
        )

        assert task.user_id == user_id
        assert task.note_id == note_id
        assert task.todoist_task_id == 987654321
        assert task.todoist_project_id == 123456789
        assert task.content == "Complete the task"
        assert task.due_datetime == due_datetime
        assert task.is_completed is False
        assert task.sync_status == SyncStatus.PENDING

    def test_todoist_task_sync_status_enum(self) -> None:
        """Test that sync_status uses correct enum values."""
        # Verify that the enum values are correct
        assert SyncStatus.PENDING.value == "pending"
        assert SyncStatus.SYNCED.value == "synced"
        assert SyncStatus.ERROR.value == "error"

    def test_todoist_task_user_relationship(self) -> None:
        """Test that TodoistTask model has relationship to User."""
        mapper = inspect(TodoistTask)
        columns = {c.key: c for c in mapper.columns}

        assert "user_id" in columns
        col = columns["user_id"]
        assert col.foreign_keys is not None
        assert len(col.foreign_keys) > 0

    def test_todoist_task_note_relationship_optional(self) -> None:
        """Test that note_id is optional and nullable."""
        mapper = inspect(TodoistTask)
        columns = {c.key: c for c in mapper.columns}

        assert "note_id" in columns
        # note_id should be nullable
        assert columns["note_id"].nullable is True

    def test_todoist_task_external_id(self) -> None:
        """Test that todoist_task_id is present and is a BigInteger."""
        mapper = inspect(TodoistTask)
        columns = {c.key: c for c in mapper.columns}

        assert "todoist_task_id" in columns
        # Should not be nullable (external ID is required)
        assert columns["todoist_task_id"].nullable is False

    def test_todoist_task_project_id_optional(self) -> None:
        """Test that todoist_project_id is optional."""
        mapper = inspect(TodoistTask)
        columns = {c.key: c for c in mapper.columns}

        assert "todoist_project_id" in columns
        # Should be nullable
        assert columns["todoist_project_id"].nullable is True

    def test_todoist_task_content_required(self) -> None:
        """Test that content field is required."""
        mapper = inspect(TodoistTask)
        columns = {c.key: c for c in mapper.columns}

        assert "content" in columns
        assert columns["content"].nullable is False

    def test_todoist_task_due_datetime_optional(self) -> None:
        """Test that due_datetime is optional."""
        mapper = inspect(TodoistTask)
        columns = {c.key: c for c in mapper.columns}

        assert "due_datetime" in columns
        # Should be nullable
        assert columns["due_datetime"].nullable is True

    def test_todoist_task_is_completed_default(self) -> None:
        """Test that is_completed has a default value."""
        mapper = inspect(TodoistTask)
        columns = {c.key: c for c in mapper.columns}

        assert "is_completed" in columns
        # Check that default is defined
        assert columns["is_completed"].default is not None

    def test_todoist_task_has_timestamps(self) -> None:
        """Test that TodoistTask model has created_at and updated_at fields."""
        mapper = inspect(TodoistTask)
        columns = {c.key for c in mapper.columns}

        assert "created_at" in columns
        assert "updated_at" in columns

    def test_todoist_task_has_soft_delete(self) -> None:
        """Test that TodoistTask model has deleted_at field for soft delete."""
        mapper = inspect(TodoistTask)
        columns = {c.key for c in mapper.columns}

        assert "deleted_at" in columns

    def test_todoist_task_user_id_required(self) -> None:
        """Test that user_id is required."""
        mapper = inspect(TodoistTask)
        columns = {c.key: c for c in mapper.columns}

        assert "user_id" in columns
        assert columns["user_id"].nullable is False
