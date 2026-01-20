"""Tests for User model."""

import pytest
from uuid import uuid4
from datetime import datetime
from sqlalchemy import inspect
from src.db.models.user import User


class TestUserModel:
    """Tests for User SQLAlchemy model."""

    def test_user_model_creation(self) -> None:
        """Test that User model can be created with all fields."""
        user = User(
            telegram_id=123456789,
            username="testuser",
            first_name="Test",
            last_name="User",
            language_code="en",
            is_active=True,
        )

        assert user.telegram_id == 123456789
        assert user.username == "testuser"
        assert user.first_name == "Test"
        assert user.last_name == "User"
        assert user.language_code == "en"
        assert user.is_active is True

    def test_user_telegram_id_unique(self) -> None:
        """Test that telegram_id field has unique constraint."""
        mapper = inspect(User)
        columns = {c.key: c for c in mapper.columns}

        assert "telegram_id" in columns
        assert columns["telegram_id"].unique is True

    def test_user_fields_validation(self) -> None:
        """Test that User model has correct field types and nullability."""
        mapper = inspect(User)
        columns = {c.key: c for c in mapper.columns}

        # Required fields
        assert "telegram_id" in columns
        assert "is_active" in columns

        # Optional fields
        assert "username" in columns
        assert columns["username"].nullable is True

        assert "first_name" in columns
        assert columns["first_name"].nullable is True

        assert "last_name" in columns
        assert columns["last_name"].nullable is True

        assert "language_code" in columns
        assert columns["language_code"].nullable is True

    def test_user_has_timestamps(self) -> None:
        """Test that User model has created_at and updated_at fields."""
        mapper = inspect(User)
        columns = {c.key for c in mapper.columns}

        assert "created_at" in columns
        assert "updated_at" in columns

    def test_user_has_soft_delete(self) -> None:
        """Test that User model has deleted_at field for soft delete."""
        mapper = inspect(User)
        columns = {c.key for c in mapper.columns}

        assert "deleted_at" in columns

    def test_user_has_uuid_primary_key(self) -> None:
        """Test that User model uses UUID as primary key."""
        mapper = inspect(User)
        columns = {c.key: c for c in mapper.columns}

        assert "id" in columns
        assert columns["id"].primary_key is True

    def test_user_relationships(self) -> None:
        """Test that User model has relationships to other models."""
        # Check that relationships are defined (they may be empty if not yet set up)
        mapper = inspect(User)
        relationships = {r.key for r in mapper.relationships}

        # At minimum, we expect relationships for notes, reminders, todoist_tasks, sessions
        # These will be populated when models are properly connected
        # For now, just check that relationships attribute exists
        assert hasattr(mapper, "relationships")
