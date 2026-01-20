"""Note repository with specific note-related queries."""

import logging
from typing import List

from uuid import UUID
from sqlalchemy import select, or_
from sqlalchemy.exc import DatabaseError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Note, ContentType
from src.db.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class NoteRepository(BaseRepository[Note]):
    """Repository for Note model with specific queries."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize NoteRepository.

        Args:
            session: Async database session
        """
        super().__init__(Note, session)

    async def list_by_user(self, user_id: UUID, offset: int, limit: int) -> List[Note]:
        """List notes for a specific user.

        Args:
            user_id: User ID to filter by
            offset: Number of items to skip
            limit: Maximum number of items to return

        Returns:
            List of Note instances for the user
        """
        try:
            stmt = select(Note).where(Note.user_id == user_id)
            stmt = stmt.where(Note.deleted_at.is_(None))
            stmt = stmt.order_by(Note.created_at.desc())
            stmt = stmt.offset(offset).limit(limit)

            result = await self.session.execute(stmt)
            notes = list(result.scalars().all())

            logger.debug(
                f"Listed {len(notes)} notes for user_id={user_id} (offset={offset}, limit={limit})"
            )

            return notes

        except (SQLAlchemyError, DatabaseError) as e:
            logger.error(f"Error listing notes for user_id={user_id}: {e}")
            raise

    async def search_by_content(
        self, user_id: UUID, query: str, offset: int, limit: int
    ) -> List[Note]:
        """Search notes by content text.

        Args:
            user_id: User ID to filter by
            query: Search query string
            offset: Number of items to skip
            limit: Maximum number of items to return

        Returns:
            List of Note instances matching the query
        """
        try:
            # Use case-insensitive ILIKE for PostgreSQL, or LIKE for SQLite
            # This will work on both
            search_pattern = f"%{query}%"

            stmt = select(Note).where(Note.user_id == user_id)
            stmt = stmt.where(Note.content.ilike(search_pattern))
            stmt = stmt.where(Note.deleted_at.is_(None))
            stmt = stmt.order_by(Note.created_at.desc())
            stmt = stmt.offset(offset).limit(limit)

            result = await self.session.execute(stmt)
            notes = list(result.scalars().all())

            logger.debug(
                f"Found {len(notes)} notes for user_id={user_id} "
                f"matching query='{query}' (offset={offset}, limit={limit})"
            )

            return notes

        except (SQLAlchemyError, DatabaseError) as e:
            logger.error(f"Error searching notes for user_id={user_id} with query='{query}': {e}")
            raise

    async def list_by_content_type(
        self, user_id: UUID, content_type: ContentType, offset: int, limit: int
    ) -> List[Note]:
        """List notes by content type for a user.

        Args:
            user_id: User ID to filter by
            content_type: Content type to filter by
            offset: Number of items to skip
            limit: Maximum number of items to return

        Returns:
            List of Note instances with the specified content type
        """
        try:
            stmt = select(Note).where(Note.user_id == user_id)
            stmt = stmt.where(Note.content_type == content_type)
            stmt = stmt.where(Note.deleted_at.is_(None))
            stmt = stmt.order_by(Note.created_at.desc())
            stmt = stmt.offset(offset).limit(limit)

            result = await self.session.execute(stmt)
            notes = list(result.scalars().all())

            logger.debug(
                f"Listed {len(notes)} {content_type} notes for user_id={user_id} "
                f"(offset={offset}, limit={limit})"
            )

            return notes

        except (SQLAlchemyError, DatabaseError) as e:
            logger.error(f"Error listing {content_type} notes for user_id={user_id}: {e}")
            raise
