"""Mixin classes for SQLAlchemy models.

These mixins provide common functionality that is shared across
multiple models in the application.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Uuid


class TimestampMixin:
    """Mixin that adds created_at and updated_at timestamp fields.

    The timestamps are automatically set on creation and updated
    whenever the model is modified.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.utcnow(),
        nullable=False,
        index=True,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.utcnow(),
        onupdate=lambda: datetime.utcnow(),
        nullable=False,
    )


class UUIDMixin:
    """Mixin that adds a UUID primary key field.

    This provides a unique identifier for each model instance
    using UUIDv4 for better security and global uniqueness.
    """

    id: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        default=uuid4,
        nullable=False,
    )


class SoftDeleteMixin:
    """Mixin that adds soft delete functionality.

    Instead of permanently deleting records, this mixin adds a
    deleted_at field that can be used to mark records as deleted
    while keeping them in the database for auditing purposes.
    """

    deleted_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        index=True,
    )

    @property
    def is_deleted(self) -> bool:
        """Check if the record is marked as deleted."""
        return self.deleted_at is not None
