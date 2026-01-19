"""Initial schema

Revision ID: dc9f11620792
Revises:
Create Date: 2026-01-19 14:39:20.925489

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "dc9f11620792"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema.

    Creates pgvector and uuid-ossp extensions, and creates all initial tables.
    """
    # Create pgvector extension for vector similarity search
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Create uuid-ossp extension for UUID generation
    op.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')

    # Create users table
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("telegram_id", sa.BigInteger(), nullable=False),
        sa.Column("username", sa.String(length=255), nullable=True),
        sa.Column("first_name", sa.String(length=255), nullable=True),
        sa.Column("last_name", sa.String(length=255), nullable=True),
        sa.Column("language_code", sa.String(length=10), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("telegram_id"),
    )
    op.create_index(op.f("ix_users_telegram_id"), "users", ["telegram_id"])
    op.create_index(op.f("ix_users_is_active"), "users", ["is_active"])

    # Create notes table
    op.create_table(
        "notes",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("content_type", sa.String(length=20), nullable=False),
        sa.Column("source", sa.String(length=20), nullable=False),
        sa.Column("file_path", sa.String(length=512), nullable=True),
        sa.Column("summary", sa.Text(), nullable=True),
        sa.Column("tags", sa.ARRAY(sa.String(length=100)), nullable=True),
        sa.Column("vector_embedding", sa.JSON(), nullable=True),
        sa.Column("metadata", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_notes_user_id"), "notes", ["user_id"])
    op.create_index(op.f("ix_notes_content_type"), "notes", ["content_type"])
    op.create_index(op.f("ix_notes_source"), "notes", ["source"])
    op.create_index(op.f("ix_notes_user_created"), "notes", ["user_id", "created_at"])

    # Create reminders table
    op.create_table(
        "reminders",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("note_id", sa.UUID(), nullable=True),
        sa.Column("remind_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("is_sent", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["note_id"], ["notes.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_reminders_user_id"), "reminders", ["user_id"])
    op.create_index(op.f("ix_reminders_note_id"), "reminders", ["note_id"])
    op.create_index(op.f("ix_reminders_remind_at"), "reminders", ["remind_at"])
    op.create_index(op.f("ix_reminders_is_sent"), "reminders", ["is_sent"])
    op.create_index(op.f("ix_reminders_user_remind"), "reminders", ["user_id", "remind_at"])

    # Create todoist_tasks table
    op.create_table(
        "todoist_tasks",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("note_id", sa.UUID(), nullable=True),
        sa.Column("todoist_task_id", sa.BigInteger(), nullable=False),
        sa.Column("todoist_project_id", sa.BigInteger(), nullable=True),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("due_datetime", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_completed", sa.Boolean(), nullable=False),
        sa.Column("sync_status", sa.String(length=20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["note_id"], ["notes.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_todoist_tasks_user_id"), "todoist_tasks", ["user_id"])
    op.create_index(op.f("ix_todoist_tasks_note_id"), "todoist_tasks", ["note_id"])
    op.create_index(op.f("ix_todoist_tasks_todoist_task_id"), "todoist_tasks", ["todoist_task_id"])
    op.create_index(op.f("ix_todoist_tasks_is_completed"), "todoist_tasks", ["is_completed"])
    op.create_index(op.f("ix_todoist_tasks_sync_status"), "todoist_tasks", ["sync_status"])
    op.create_index(op.f("ix_todoist_tasks_user_sync"), "todoist_tasks", ["user_id", "sync_status"])

    # Create sessions table
    op.create_table(
        "sessions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("context", sa.JSON(), nullable=False),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("last_activity", sa.DateTime(timezone=True), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_sessions_user_id"), "sessions", ["user_id"])
    op.create_index(op.f("ix_sessions_state"), "sessions", ["state"])
    op.create_index(op.f("ix_sessions_last_activity"), "sessions", ["last_activity"])
    op.create_index(op.f("ix_sessions_user_activity"), "sessions", ["user_id", "last_activity"])


def downgrade() -> None:
    """Downgrade schema.

    Drops all tables and extensions in reverse order.
    """
    # Drop tables in reverse order (due to foreign keys)
    op.drop_index(op.f("ix_sessions_user_activity"), table_name="sessions")
    op.drop_index(op.f("ix_sessions_last_activity"), table_name="sessions")
    op.drop_index(op.f("ix_sessions_state"), table_name="sessions")
    op.drop_index(op.f("ix_sessions_user_id"), table_name="sessions")
    op.drop_table("sessions")

    op.drop_index(op.f("ix_todoist_tasks_user_sync"), table_name="todoist_tasks")
    op.drop_index(op.f("ix_todoist_tasks_sync_status"), table_name="todoist_tasks")
    op.drop_index(op.f("ix_todoist_tasks_is_completed"), table_name="todoist_tasks")
    op.drop_index(op.f("ix_todoist_tasks_todoist_task_id"), table_name="todoist_tasks")
    op.drop_index(op.f("ix_todoist_tasks_note_id"), table_name="todoist_tasks")
    op.drop_index(op.f("ix_todoist_tasks_user_id"), table_name="todoist_tasks")
    op.drop_table("todoist_tasks")

    op.drop_index(op.f("ix_reminders_user_remind"), table_name="reminders")
    op.drop_index(op.f("ix_reminders_is_sent"), table_name="reminders")
    op.drop_index(op.f("ix_reminders_remind_at"), table_name="reminders")
    op.drop_index(op.f("ix_reminders_note_id"), table_name="reminders")
    op.drop_index(op.f("ix_reminders_user_id"), table_name="reminders")
    op.drop_table("reminders")

    op.drop_index(op.f("ix_notes_user_created"), table_name="notes")
    op.drop_index(op.f("ix_notes_source"), table_name="notes")
    op.drop_index(op.f("ix_notes_content_type"), table_name="notes")
    op.drop_index(op.f("ix_notes_user_id"), table_name="notes")
    op.drop_table("notes")

    op.drop_index(op.f("ix_users_is_active"), table_name="users")
    op.drop_index(op.f("ix_users_telegram_id"), table_name="users")
    op.drop_table("users")

    # Drop extensions
    op.execute("DROP EXTENSION IF EXISTS vector")
    op.execute('DROP EXTENSION IF EXISTS "uuid-ossp"')
