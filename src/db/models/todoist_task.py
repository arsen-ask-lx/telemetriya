"""TodoistTask model for SQLAlchemy ORM."""

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Index, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base
from src.db.mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin


class SyncStatus(str, Enum):
    """Enum for Todoist sync status."""

    PENDING = "pending"
    SYNCED = "synced"
    ERROR = "error"


class TodoistTask(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """TodoistTask model representing tasks synced with Todoist.

    Attributes:
        id: Unique UUID primary key
        user_id: Foreign key to User
        note_id: Optional foreign key to Note
        todoist_task_id: External Todoist task ID
        todoist_project_id: Optional external Todoist project ID
        content: Task content/title
        due_datetime: Optional due datetime
        is_completed: Whether task is completed
        sync_status: Sync status with Todoist
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
        deleted_at: Timestamp for soft delete (optional)
    """

    __tablename__ = "todoist_tasks"

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
    todoist_task_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        unique=True,
        index=True,
    )
    todoist_project_id: Mapped[Optional[int]] = mapped_column(
        BigInteger,
        nullable=True,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    due_datetime: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    is_completed: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        index=True,
    )
    sync_status: Mapped[SyncStatus] = mapped_column(
        String(20),
        default=SyncStatus.PENDING,
        nullable=False,
        index=True,
    )

    __table_args__ = (Index("idx_todoist_tasks_user_sync", "user_id", "sync_status"),)
