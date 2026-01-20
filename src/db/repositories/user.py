"""User repository with specific user-related queries."""

import logging
from typing import Optional

from uuid import UUID
from sqlalchemy import select, or_
from sqlalchemy.exc import DatabaseError, SQLAlchemyError, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from src.db.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository[User]):
    """Repository for User model with specific queries."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize UserRepository.

        Args:
            session: Async database session
        """
        super().__init__(User, session)

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Get user by Telegram ID.

        Args:
            telegram_id: Telegram user ID

        Returns:
            User instance or None if not found
        """
        try:
            stmt = select(User).where(User.telegram_id == telegram_id)
            stmt = stmt.where(User.deleted_at.is_(None))

            result = await self.session.execute(stmt)
            user = result.scalar_one_or_none()

            if user:
                logger.debug(f"Retrieved user with telegram_id={telegram_id}")
            else:
                logger.debug(f"User with telegram_id={telegram_id} not found")

            return user

        except (SQLAlchemyError, DatabaseError) as e:
            logger.error(f"Error retrieving user with telegram_id={telegram_id}: {e}")
            raise

    async def get_or_create_by_telegram_id(self, telegram_id: int, **kwargs) -> User:
        """Get existing user or create new one.

        Args:
            telegram_id: Telegram user ID
            **kwargs: Additional user fields for creation if needed

        Returns:
            User instance (existing or newly created)

        Raises:
            DatabaseError: If database operation fails (other than IntegrityError)
        """
        try:
            # Try to get existing user
            user = await self.get_by_telegram_id(telegram_id)

            if user:
                logger.debug(f"Returning existing user with telegram_id={telegram_id}")
                return user

        except (SQLAlchemyError, DatabaseError):
            # If get fails, we'll try to create and handle race condition below
            pass

        try:
            # Create new user
            new_user = User(telegram_id=telegram_id, **kwargs)
            self.session.add(new_user)
            await self.session.commit()
            await self.session.refresh(new_user)

            logger.debug(f"Created new user with telegram_id={telegram_id}")

            return new_user

        except IntegrityError:
            # Another request created the user, try getting it again
            await self.session.rollback()
            user = await self.get_by_telegram_id(telegram_id)
            if not user:
                raise RuntimeError(
                    f"Failed to retrieve user after IntegrityError for telegram_id={telegram_id}"
                )
            logger.debug(f"Retrieved user after race condition for telegram_id={telegram_id}")
            return user

    async def list_active_users(self, offset: int, limit: int) -> list[User]:
        """List active users (not deleted and is_active=True).

        Args:
            offset: Number of items to skip
            limit: Maximum number of items to return

        Returns:
            List of active User instances
        """
        try:
            stmt = select(User).where(User.is_active.is_(True))
            stmt = stmt.where(User.deleted_at.is_(None))
            stmt = stmt.offset(offset).limit(limit)

            result = await self.session.execute(stmt)
            users = list(result.scalars().all())

            logger.debug(f"Listed {len(users)} active users (offset={offset}, limit={limit})")

            return users

        except (SQLAlchemyError, DatabaseError) as e:
            logger.error(f"Error listing active users: {e}")
            raise
