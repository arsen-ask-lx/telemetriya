"""TodoistTask repository with specific Todoist-related queries."""

import logging
from typing import List, Optional

from uuid import UUID
from sqlalchemy import select
from sqlalchemy.exc import DatabaseError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import TodoistTask, SyncStatus
from src.db.repositories.base import BaseRepository

logger = logging.getLogger(__name__)


class TodoistTaskRepository(BaseRepository[TodoistTask]):
    """Repository for TodoistTask model with specific queries."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize TodoistTaskRepository.

        Args:
            session: Async database session
        """
        super().__init__(TodoistTask, session)

    async def get_by_todoist_id(self, todoist_task_id: int) -> Optional[TodoistTask]:
        """Get task by Todoist task ID.

        Args:
            todoist_task_id: External Todoist task ID

        Returns:
            TodoistTask instance or None if not found
        """
        try:
            stmt = select(TodoistTask).where(TodoistTask.todoist_task_id == todoist_task_id)
            stmt = stmt.where(TodoistTask.deleted_at.is_(None))

            result = await self.session.execute(stmt)
            task = result.scalar_one_or_none()

            if task:
                logger.debug(f"Retrieved TodoistTask with todoist_task_id={todoist_task_id}")
            else:
                logger.debug(f"TodoistTask with todoist_task_id={todoist_task_id} not found")

            return task

        except (SQLAlchemyError, DatabaseError) as e:
            logger.error(
                f"Error retrieving TodoistTask with todoist_task_id={todoist_task_id}: {e}"
            )
            raise

    async def list_by_sync_status(
        self, sync_status: SyncStatus, offset: int, limit: int
    ) -> List[TodoistTask]:
        """List tasks by sync status.

        Args:
            sync_status: Sync status to filter by
            offset: Number of items to skip
            limit: Maximum number of items to return

        Returns:
            List of TodoistTask instances with the specified sync status
        """
        try:
            stmt = select(TodoistTask).where(TodoistTask.sync_status == sync_status)
            stmt = stmt.where(TodoistTask.deleted_at.is_(None))
            stmt = stmt.order_by(TodoistTask.created_at.desc())
            stmt = stmt.offset(offset).limit(limit)

            result = await self.session.execute(stmt)
            tasks = list(result.scalars().all())

            logger.debug(
                f"Listed {len(tasks)} TodoistTasks with sync_status={sync_status} "
                f"(offset={offset}, limit={limit})"
            )

            return tasks

        except (SQLAlchemyError, DatabaseError) as e:
            logger.error(f"Error listing TodoistTasks with sync_status={sync_status}: {e}")
            raise

    async def list_by_user(self, user_id: UUID, offset: int, limit: int) -> List[TodoistTask]:
        """List tasks for a specific user.

        Args:
            user_id: User ID to filter by
            offset: Number of items to skip
            limit: Maximum number of items to return

        Returns:
            List of TodoistTask instances for the user
        """
        try:
            stmt = select(TodoistTask).where(TodoistTask.user_id == user_id)
            stmt = stmt.where(TodoistTask.deleted_at.is_(None))
            stmt = stmt.order_by(TodoistTask.created_at.desc())
            stmt = stmt.offset(offset).limit(limit)

            result = await self.session.execute(stmt)
            tasks = list(result.scalars().all())

            logger.debug(
                f"Listed {len(tasks)} TodoistTasks for user_id={user_id} "
                f"(offset={offset}, limit={limit})"
            )

            return tasks

        except (SQLAlchemyError, DatabaseError) as e:
            logger.error(f"Error listing TodoistTasks for user_id={user_id}: {e}")
            raise
