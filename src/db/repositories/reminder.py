"""Reminder repository with specific reminder-related queries."""

import logging
from datetime import datetime
from typing import List

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Reminder
from src.db.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class ReminderRepository(BaseRepository[Reminder]):
    """Repository for Reminder model with specific queries."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize ReminderRepository.

        Args:
            session: Async database session
        """
        super().__init__(Reminder, session)

    async def list_by_user(self, user_id: UUID, offset: int, limit: int) -> List[Reminder]:
        """List reminders for a specific user.

        Args:
            user_id: User ID to filter by
            offset: Number of items to skip
            limit: Maximum number of items to return

        Returns:
            List of Reminder instances for the user
        """
        try:
            stmt = select(Reminder).where(Reminder.user_id == user_id)
            stmt = stmt.where(Reminder.deleted_at.is_(None))
            stmt = stmt.order_by(Reminder.remind_at.asc())
            stmt = stmt.offset(offset).limit(limit)

            result = await self.session.execute(stmt)
            reminders = list(result.scalars().all())

            logger.debug(
                f"Listed {len(reminders)} reminders for user_id={user_id} "
                f"(offset={offset}, limit={limit})"
            )

            return reminders

        except (SQLAlchemyError, DatabaseError) as e:
            logger.error(f"Error listing reminders for user_id={user_id}: {e}")
            raise

    async def list_pending(self, before: datetime, offset: int, limit: int) -> List[Reminder]:
        """List reminders that are due before a specific time.

        Args:
            before: Datetime threshold
            offset: Number of items to skip
            limit: Maximum number of items to return

        Returns:
            List of Reminder instances due before the specified time
        """
        try:
            stmt = select(Reminder).where(Reminder.remind_at <= before)
            stmt = stmt.where(Reminder.deleted_at.is_(None))
            stmt = stmt.order_by(Reminder.remind_at.asc())
            stmt = stmt.offset(offset).limit(limit)

            result = await self.session.execute(stmt)
            reminders = list(result.scalars().all())

            logger.debug(
                f"Listed {len(reminders)} pending reminders before {before} "
                f"(offset={offset}, limit={limit})"
            )

            return reminders

        except (SQLAlchemyError, DatabaseError) as e:
            logger.error(f"Error listing pending reminders before {before}: {e}")
            raise

    async def list_unsent(self, user_id: UUID, offset: int, limit: int) -> List[Reminder]:
        """List unsent reminders for a specific user.

        Args:
            user_id: User ID to filter by
            offset: Number of items to skip
            limit: Maximum number of items to return

        Returns:
            List of unsent Reminder instances for the user
        """
        try:
            stmt = select(Reminder).where(Reminder.user_id == user_id)
            stmt = stmt.where(Reminder.is_sent.is_(False))
            stmt = stmt.where(Reminder.deleted_at.is_(None))
            stmt = stmt.order_by(Reminder.remind_at.asc())
            stmt = stmt.offset(offset).limit(limit)

            result = await self.session.execute(stmt)
            reminders = list(result.scalars().all())

            logger.debug(
                f"Listed {len(reminders)} unsent reminders for user_id={user_id} "
                f"(offset={offset}, limit={limit})"
            )

            return reminders

        except (SQLAlchemyError, DatabaseError) as e:
            logger.error(f"Error listing unsent reminders for user_id={user_id}: {e}")
            raise
