"""Session model for SQLAlchemy ORM."""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import JSON

from src.db.base import Base
from src.db.mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin


class Session(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Session model representing user conversation sessions.

    Attributes:
        id: Unique UUID primary key
        user_id: Foreign key to User
        context: JSON context data for the conversation
        state: Optional current state in the conversation flow
        last_activity: Timestamp of last user activity
        created_at: Timestamp when session was created
        updated_at: Timestamp when session was last updated
        deleted_at: Timestamp for soft delete (optional)
    """

    __tablename__ = "sessions"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    context: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=False,
    )
    state: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        index=True,
    )
    last_activity: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.utcnow(),
        nullable=False,
        index=True,
    )

    __table_args__ = (Index("idx_sessions_user_activity", "user_id", "last_activity"),)
