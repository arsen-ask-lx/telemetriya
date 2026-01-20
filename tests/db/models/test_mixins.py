"""Tests for mixin classes."""

from datetime import datetime
from sqlalchemy import inspect
from src.db.mixins import (
    TimestampMixin,
    UUIDMixin,
    SoftDeleteMixin,
)


class TestTimestampMixin:
    """Tests for TimestampMixin."""

    def test_timestamp_mixin_fields(self) -> None:
        """Test that TimestampMixin has created_at and updated_at fields."""
        # Create a simple model with the mixin
        from sqlalchemy import Column
        from sqlalchemy.types import DateTime
        from src.db.base import Base

        class TestModel(Base, TimestampMixin):
            __tablename__ = "test_timestamp"
            __table_args__ = {"extend_existing": True}
            id = Column("id", type_=None, primary_key=True)  # Placeholder

        mapper = inspect(TestModel)
        columns = {c.key for c in mapper.columns}

        assert "created_at" in columns
        assert "updated_at" in columns


class TestUUIDMixin:
    """Tests for UUIDMixin."""

    def test_uuid_mixin_fields(self) -> None:
        """Test that UUIDMixin has id field as UUID primary key."""
        from sqlalchemy import Column
        from uuid import UUID
        from src.db.base import Base

        class TestModel(Base, UUIDMixin):
            __tablename__ = "test_uuid"
            __table_args__ = {"extend_existing": True}

        mapper = inspect(TestModel)
        columns = {c.key: c for c in mapper.columns}

        assert "id" in columns
        assert columns["id"].primary_key is True


class TestSoftDeleteMixin:
    """Tests for SoftDeleteMixin."""

    def test_soft_delete_mixin_fields(self) -> None:
        """Test that SoftDeleteMixin has deleted_at field (optional datetime)."""
        from sqlalchemy import Column
        from sqlalchemy.types import DateTime
        from src.db.base import Base

        class TestModel(Base, SoftDeleteMixin):
            __tablename__ = "test_soft_delete"
            __table_args__ = {"extend_existing": True}
            id = Column("id", type_=None, primary_key=True)  # Placeholder

        mapper = inspect(TestModel)
        columns = {c.key for c in mapper.columns}

        assert "deleted_at" in columns


class TestMixinsTogether:
    """Tests for using multiple mixins together."""

    def test_mixins_work_together(self) -> None:
        """Test that all mixins work together without conflicts."""
        from src.db.base import Base

        class TestModel(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
            __tablename__ = "test_all_mixins"
            __table_args__ = {"extend_existing": True}

        mapper = inspect(TestModel)
        columns = {c.key for c in mapper.columns}

        # All mixin fields should be present
        assert "id" in columns
        assert "created_at" in columns
        assert "updated_at" in columns
        assert "deleted_at" in columns
