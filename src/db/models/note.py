"""Note model for SQLAlchemy ORM."""

from enum import Enum
from typing import List, Optional

from sqlalchemy import JSON, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import ARRAY as PG_ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base
from src.db.mixins import SoftDeleteMixin, TimestampMixin, UUIDMixin


class ContentType(str, Enum):
    """Enum for content types of notes."""

    TEXT = "text"
    VOICE = "voice"
    PDF = "pdf"
    IMAGE = "image"


class NoteSource(str, Enum):
    """Enum for note sources."""

    TELEGRAM = "telegram"
    API = "api"


class Note(Base, UUIDMixin, TimestampMixin, SoftDeleteMixin):
    """Note model representing user notes and content.

    Attributes:
        id: Unique UUID primary key
        user_id: Foreign key to User
        content: The note content (text, transcription, etc.)
        content_type: Type of content (text, voice, pdf, image)
        source: Source of the note (telegram, api)
        file_path: Optional path to stored file
        summary: Optional AI-generated summary
        tags: Optional list of tags
        vector_embedding: Optional vector embedding for search (pgvector)
        metadata: Optional JSON metadata
        created_at: Timestamp when note was created
        updated_at: Timestamp when note was last updated
        deleted_at: Timestamp for soft delete (optional)
    """

    __tablename__ = "notes"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    content_type: Mapped[ContentType] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )
    source: Mapped[NoteSource] = mapped_column(
        String(20),
        nullable=False,
        index=True,
    )
    file_path: Mapped[Optional[str]] = mapped_column(
        String(512),
        nullable=True,
    )
    summary: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )
    tags: Mapped[Optional[List[str]]] = mapped_column(
        PG_ARRAY(String(100)),
        nullable=True,
        default=None,
    )
    # vector_embedding will be added later when pgvector extension is properly set up
    # For now, we'll use a JSONB field to store the embedding as a workaround
    vector_embedding: Mapped[Optional[List[float]]] = mapped_column(
        JSON,
        nullable=True,
    )
    # Using 'note_metadata' instead of 'metadata' which is reserved in SQLAlchemy
    note_metadata: Mapped[Optional[dict]] = mapped_column(
        "metadata",  # Column name in DB is still 'metadata'
        JSON,
        nullable=True,
    )

    __table_args__ = (Index("idx_notes_user_created", "user_id", "created_at"),)
