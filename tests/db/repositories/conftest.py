"""Test fixtures for repository tests."""

import pytest
from uuid import uuid4
from datetime import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.db.base import Base
from src.db.models import User, Note, Reminder, TodoistTask


@pytest.fixture(scope="function", autouse=True)
def remove_tags_from_note_model():
    """Remove tags attribute from Note model for SQLite tests."""
    # Save original
    original_mapped_attrs = list(Note.__mapper__.attrs)

    # Filter out tags from mapped attributes
    Note.__mapper__.attrs = [attr for attr in original_mapped_attrs if attr.key != "tags"]

    yield

    # Restore
    Note.__mapper__.attrs = original_mapped_attrs


@pytest.fixture(scope="function")
async def async_engine():
    """Create async engine for testing."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
    )
    yield engine
    await engine.dispose()


@pytest.fixture(scope="function")
async def async_session(async_engine: AsyncEngine):
    """Create async session for testing."""
    async with async_engine.begin() as conn:
        # Create all tables except notes (which has PG_ARRAY for tags)
        for table in Base.metadata.sorted_tables:
            if table.name != "notes":
                await conn.run_sync(table.create, checkfirst=True)

        # Create notes table manually without tags column for SQLite
        await conn.run_sync(
            lambda connection: connection.execute(
                text("""
            CREATE TABLE IF NOT EXISTS notes (
                user_id CHAR(32) NOT NULL,
                content TEXT NOT NULL,
                content_type VARCHAR(20) NOT NULL,
                source VARCHAR(20) NOT NULL,
                file_path VARCHAR(512),
                summary TEXT,
                vector_embedding JSON,
                metadata JSON,
                id CHAR(32) NOT NULL PRIMARY KEY,
                created_at DATETIME,
                updated_at DATETIME,
                deleted_at DATETIME
            )
        """)
            )
        )

    async_session_maker = async_sessionmaker(
        async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session_maker() as session:
        yield session

    async with async_engine.begin() as conn:
        # Drop notes table manually
        await conn.run_sync(
            lambda connection: connection.execute(text("DROP TABLE IF EXISTS notes"))
        )
        # Drop other tables via metadata
        for table in reversed(Base.metadata.sorted_tables):
            if table.name != "notes":
                await conn.run_sync(table.drop)


@pytest.fixture
def sample_user():
    """Create a sample user object."""
    return User(
        id=uuid4(),
        telegram_id=123456789,
        username="testuser",
        first_name="Test",
        last_name="User",
        language_code="en",
        is_active=True,
    )


@pytest.fixture
def sample_note():
    """Create a sample note object."""
    return Note(
        id=uuid4(),
        user_id=uuid4(),
        content="This is a test note",
        content_type="text",
        source="telegram",
        summary="Test summary",
        tags=None,
        note_metadata={"key": "value"},
    )


@pytest.fixture
def sample_reminder():
    """Create a sample reminder object."""
    return Reminder(
        id=uuid4(),
        user_id=uuid4(),
        remind_at=datetime.utcnow(),
        message="Test reminder",
        is_sent=False,
    )


@pytest.fixture
def sample_todoist_task():
    """Create a sample Todoist task object."""
    return TodoistTask(
        id=uuid4(),
        user_id=uuid4(),
        todoist_task_id=123456789,
        content="Test task",
        sync_status="pending",
        is_completed=False,
    )


@pytest.fixture
def mock_db_error():
    """Create a mock DatabaseError for testing error handling."""
    from sqlalchemy.exc import DatabaseError

    return DatabaseError("test error", {}, Exception("test"))
