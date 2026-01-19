"""User model for SQLAlchemy ORM."""

from typing import Optional

from sqlalchemy import BigInteger, Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base
from src.db.mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin


class User(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """User model representing Telegram users in the system.

    Attributes:
        id: Unique UUID primary key
        telegram_id: Telegram user ID (unique)
        username: Optional Telegram username
        first_name: Optional first name
        last_name: Optional last name
        language_code: Optional language code (e.g., 'en', 'ru')
        is_active: Whether the user is active
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
        deleted_at: Timestamp for soft delete (optional)
    """

    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        nullable=False,
        index=True,
    )
    username: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    first_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    last_name: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )
    language_code: Mapped[Optional[str]] = mapped_column(
        String(10),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
        index=True,
    )
