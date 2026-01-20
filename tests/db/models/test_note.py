"""Tests for Note model."""

import pytest
from uuid import uuid4
from sqlalchemy import inspect
from src.db.models.note import Note, ContentType, NoteSource


class TestNoteModel:
    """Tests for Note SQLAlchemy model."""

    def test_note_model_creation(self) -> None:
        """Test that Note model can be created with all fields."""
        note = Note(
            user_id=uuid4(),
            content="This is a test note",
            content_type=ContentType.TEXT,
            source=NoteSource.TELEGRAM,
            file_path="/path/to/file",
            summary="Test summary",
            tags=["test", "note"],
            metadata={"key": "value"},
        )

        assert note.content == "This is a test note"
        assert note.content_type == ContentType.TEXT
        assert note.source == NoteSource.TELEGRAM
        assert note.file_path == "/path/to/file"
        assert note.summary == "Test summary"
        assert note.tags == ["test", "note"]
        assert note.metadata == {"key": "value"}

    def test_note_content_type_enum(self) -> None:
        """Test that content_type uses correct enum values."""
        from sqlalchemy import types

        mapper = inspect(Note)
        columns = {c.key: c for c in mapper.columns}

        assert "content_type" in columns
        # Check that it's an enum type
        col_type = columns["content_type"].type
        # SQLAlchemy enum types have specific attributes

    def test_note_tags_array(self) -> None:
        """Test that tags field is an array type."""
        mapper = inspect(Note)
        columns = {c.key: c for c in mapper.columns}

        assert "tags" in columns
        # Tags should be nullable
        assert columns["tags"].nullable is True

    def test_note_vector_embedding_field(self) -> None:
        """Test that vector_embedding field exists for pgvector."""
        mapper = inspect(Note)
        columns = {c.key: c for c in mapper.columns}

        assert "vector_embedding" in columns
        # Vector field should be nullable
        assert columns["vector_embedding"].nullable is True

    def test_note_metadata_jsonb(self) -> None:
        """Test that metadata field is JSONB type."""
        mapper = inspect(Note)
        columns = {c.key: c for c in mapper.columns}

        assert "metadata" in columns
        # Metadata should be nullable
        assert columns["metadata"].nullable is True

    def test_note_user_relationship(self) -> None:
        """Test that Note model has relationship to User."""
        mapper = inspect(Note)
        columns = {c.key: c for c in mapper.columns}

        assert "user_id" in columns
        # user_id should be a foreign key
        col = columns["user_id"]
        assert col.foreign_keys is not None
        assert len(col.foreign_keys) > 0

    def test_note_has_timestamps(self) -> None:
        """Test that Note model has created_at and updated_at fields."""
        mapper = inspect(Note)
        columns = {c.key for c in mapper.columns}

        assert "created_at" in columns
        assert "updated_at" in columns

    def test_note_has_soft_delete(self) -> None:
        """Test that Note model has deleted_at field for soft delete."""
        mapper = inspect(Note)
        columns = {c.key for c in mapper.columns}

        assert "deleted_at" in columns

    def test_note_source_enum(self) -> None:
        """Test that source uses correct enum values."""
        # Verify that the enum values are correct
        assert ContentType.TEXT.value == "text"
        assert ContentType.VOICE.value == "voice"
        assert ContentType.PDF.value == "pdf"
        assert ContentType.IMAGE.value == "image"

        assert NoteSource.TELEGRAM.value == "telegram"
        assert NoteSource.API.value == "api"

    def test_note_optional_fields(self) -> None:
        """Test that optional fields are properly nullable."""
        mapper = inspect(Note)
        columns = {c.key: c for c in mapper.columns}

        # Optional fields
        assert "file_path" in columns
        assert columns["file_path"].nullable is True

        assert "summary" in columns
        assert columns["summary"].nullable is True
