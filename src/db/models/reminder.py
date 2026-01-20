"""Reminder model for SQLAlchemy ORM."""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, ForeignKey, Index, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base
from src.db.mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin


class Reminder(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Reminder model representing user reminders.

    Attributes:
        id: Unique UUID primary key
        user_id: Foreign key to User
        note_id: Optional foreign key to Note
        remind_at: When to send the reminder
        message: The reminder message
        is_sent: Whether the reminder has been sent
        created_at: Timestamp when reminder was created
        updated_at: Timestamp when reminder was last updated
        deleted_at: Timestamp for soft delete (optional)
    """

    __tablename__ = "reminders"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    note_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("notes.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    remind_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )
    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    is_sent: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )

    __table_args__ = (Index("idx_reminders_user_remind", "user_id", "remind_at"),)
