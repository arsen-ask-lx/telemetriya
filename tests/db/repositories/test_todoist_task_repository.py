"""Tests for TodoistTaskRepository class."""

import pytest
from uuid import uuid4
from unittest.mock import AsyncMock

from sqlalchemy.exc import DatabaseError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import TodoistTask, User, SyncStatus
from src.db.repositories.todoist_task import TodoistTaskRepository


class TestTodoistTaskRepository:
    """Tests for TodoistTaskRepository specific methods."""

    @pytest.mark.asyncio
    async def test_get_by_todoist_id_returns_task(self, async_session: AsyncSession):
        """Test that get_by_todoist_id returns task for existing todoist_task_id."""
        repo = TodoistTaskRepository(async_session)
        task = TodoistTask(
            user_id=uuid4(),
            todoist_task_id=123456789,
            content="Test task",
            sync_status="pending",
        )
        async_session.add(task)
        await async_session.commit()
        await async_session.refresh(task)

        fetched_task = await repo.get_by_todoist_id(123456789)

        assert fetched_task is not None
        assert fetched_task.todoist_task_id == 123456789
        assert fetched_task.content == "Test task"

    @pytest.mark.asyncio
    async def test_get_by_todoist_id_returns_none(self, async_session: AsyncSession):
        """Test that get_by_todoist_id returns None for non-existent todoist_task_id."""
        repo = TodoistTaskRepository(async_session)

        result = await repo.get_by_todoist_id(999999999)

        assert result is None

    @pytest.mark.asyncio
    async def test_list_by_sync_status_filters_correctly(self, async_session: AsyncSession):
        """Test that list_by_sync_status returns tasks with specific sync status."""
        repo = TodoistTaskRepository(async_session)

        pending1 = TodoistTask(
            user_id=uuid4(),
            todoist_task_id=1001,
            content="Pending 1",
            sync_status=SyncStatus.PENDING,
        )
        pending2 = TodoistTask(
            user_id=uuid4(),
            todoist_task_id=1002,
            content="Pending 2",
            sync_status=SyncStatus.PENDING,
        )
        synced = TodoistTask(
            user_id=uuid4(), todoist_task_id=2001, content="Synced", sync_status=SyncStatus.SYNCED
        )
        async_session.add(pending1)
        async_session.add(pending2)
        async_session.add(synced)
        await async_session.commit()

        tasks = await repo.list_by_sync_status(SyncStatus.PENDING, offset=0, limit=10)

        assert len(tasks) == 2
        assert all(task.sync_status == SyncStatus.PENDING for task in tasks)

    @pytest.mark.asyncio
    async def test_list_by_user_filters_correctly(self, async_session: AsyncSession):
        """Test that list_by_user returns tasks for specific user."""
        repo = TodoistTaskRepository(async_session)
        user1_id = uuid4()
        user2_id = uuid4()

        task1 = TodoistTask(
            user_id=user1_id, todoist_task_id=1001, content="Task 1", sync_status="pending"
        )
        task2 = TodoistTask(
            user_id=user1_id, todoist_task_id=1002, content="Task 2", sync_status="pending"
        )
        task3 = TodoistTask(
            user_id=user2_id, todoist_task_id=2001, content="Task 3", sync_status="pending"
        )
        async_session.add(task1)
        async_session.add(task2)
        async_session.add(task3)
        await async_session.commit()

        tasks = await repo.list_by_user(user1_id, offset=0, limit=10)

        assert len(tasks) == 2
        assert all(task.user_id == user1_id for task in tasks)


class TestTodoistTaskRepositoryEdgeCases:
    """Tests for TodoistTaskRepository edge cases."""

    @pytest.mark.asyncio
    async def test_get_by_todoist_id_excludes_soft_deleted(self, async_session: AsyncSession):
        """Test that get_by_todoist_id excludes soft-deleted tasks."""
        repo = TodoistTaskRepository(async_session)

        task = TodoistTask(
            user_id=uuid4(), todoist_task_id=123456789, content="Test task", sync_status="pending"
        )
        async_session.add(task)
        await async_session.commit()
        await async_session.refresh(task)

        # Soft delete the task
        await repo.delete(task.id)

        # get_by_todoist_id should return None
        fetched_task = await repo.get_by_todoist_id(123456789)
        assert fetched_task is None

    @pytest.mark.asyncio
    async def test_list_by_sync_status_with_no_results(self, async_session: AsyncSession):
        """Test that list_by_sync_status returns empty list when no tasks with status."""
        repo = TodoistTaskRepository(async_session)

        # Create tasks with different status
        task = TodoistTask(
            user_id=uuid4(), todoist_task_id=1001, content="Task 1", sync_status=SyncStatus.SYNCED
        )
        async_session.add(task)
        await async_session.commit()

        tasks = await repo.list_by_sync_status(SyncStatus.PENDING, offset=0, limit=10)

        assert len(tasks) == 0

    @pytest.mark.asyncio
    async def test_list_by_sync_status_excludes_soft_deleted(self, async_session: AsyncSession):
        """Test that list_by_sync_status excludes soft-deleted tasks."""
        repo = TodoistTaskRepository(async_session)

        pending1 = TodoistTask(
            user_id=uuid4(),
            todoist_task_id=1001,
            content="Pending 1",
            sync_status=SyncStatus.PENDING,
        )
        pending2 = TodoistTask(
            user_id=uuid4(),
            todoist_task_id=1002,
            content="Pending 2",
            sync_status=SyncStatus.PENDING,
        )
        async_session.add(pending1)
        async_session.add(pending2)
        await async_session.commit()
        await async_session.refresh(pending1)

        # Soft delete one pending task
        await repo.delete(pending1.id)

        tasks = await repo.list_by_sync_status(SyncStatus.PENDING, offset=0, limit=10)

        assert len(tasks) == 1
        assert tasks[0].todoist_task_id == 1002

    @pytest.mark.asyncio
    async def test_list_by_user_with_no_results(self, async_session: AsyncSession):
        """Test that list_by_user returns empty list when no tasks for user."""
        repo = TodoistTaskRepository(async_session)
        user_id = uuid4()

        # Create task for different user
        other_user_id = uuid4()
        task = TodoistTask(
            user_id=other_user_id,
            todoist_task_id=1001,
            content="Other user task",
            sync_status="pending",
        )
        async_session.add(task)
        await async_session.commit()

        tasks = await repo.list_by_user(user_id, offset=0, limit=10)

        assert len(tasks) == 0

    @pytest.mark.asyncio
    async def test_list_by_user_excludes_soft_deleted(self, async_session: AsyncSession):
        """Test that list_by_user excludes soft-deleted tasks."""
        repo = TodoistTaskRepository(async_session)
        user_id = uuid4()

        task1 = TodoistTask(
            user_id=user_id, todoist_task_id=1001, content="Task 1", sync_status="pending"
        )
        task2 = TodoistTask(
            user_id=user_id, todoist_task_id=1002, content="Task 2", sync_status="pending"
        )
        async_session.add(task1)
        async_session.add(task2)
        await async_session.commit()
        await async_session.refresh(task1)

        # Soft delete one task
        await repo.delete(task1.id)

        tasks = await repo.list_by_user(user_id, offset=0, limit=10)

        assert len(tasks) == 1
        assert tasks[0].todoist_task_id == 1002

    @pytest.mark.asyncio
    async def test_list_by_sync_status_respects_pagination(self, async_session: AsyncSession):
        """Test that list_by_sync_status respects pagination parameters."""
        repo = TodoistTaskRepository(async_session)

        # Create 5 tasks with same status
        for i in range(5):
            task = TodoistTask(
                user_id=uuid4(),
                todoist_task_id=1000 + i,
                content=f"Task {i}",
                sync_status=SyncStatus.PENDING,
            )
            async_session.add(task)
        await async_session.commit()

        # First page
        tasks = await repo.list_by_sync_status(SyncStatus.PENDING, offset=0, limit=2)
        assert len(tasks) == 2

        # Second page
        tasks = await repo.list_by_sync_status(SyncStatus.PENDING, offset=2, limit=2)
        assert len(tasks) == 2

    @pytest.mark.asyncio
    async def test_list_by_user_respects_pagination(self, async_session: AsyncSession):
        """Test that list_by_user respects pagination parameters."""
        repo = TodoistTaskRepository(async_session)
        user_id = uuid4()

        # Create 5 tasks for the same user
        for i in range(5):
            task = TodoistTask(
                user_id=user_id,
                todoist_task_id=1000 + i,
                content=f"Task {i}",
                sync_status="pending",
            )
            async_session.add(task)
        await async_session.commit()

        # First page
        tasks = await repo.list_by_user(user_id, offset=0, limit=2)
        assert len(tasks) == 2

        # Second page
        tasks = await repo.list_by_user(user_id, offset=2, limit=2)
        assert len(tasks) == 2


class TestTodoistTaskRepositoryErrorHandling:
    """Tests for TodoistTaskRepository error handling using mocks."""

    @pytest.mark.asyncio
    async def test_get_by_todoist_id_handles_database_error(self):
        """Test that get_by_todoist_id handles database error."""
        # Create mock session that raises DatabaseError
        mock_session = AsyncMock(spec=AsyncSession)
        mock_execute = AsyncMock(side_effect=DatabaseError("test error", {}, Exception()))
        mock_session.execute = mock_execute

        repo = TodoistTaskRepository(mock_session)

        with pytest.raises(DatabaseError):
            await repo.get_by_todoist_id(123456789)

    @pytest.mark.asyncio
    async def test_list_by_sync_status_handles_database_error(self):
        """Test that list_by_sync_status handles database error."""
        # Create mock session that raises DatabaseError
        mock_session = AsyncMock(spec=AsyncSession)
        mock_execute = AsyncMock(side_effect=DatabaseError("test error", {}, Exception()))
        mock_session.execute = mock_execute

        repo = TodoistTaskRepository(mock_session)

        with pytest.raises(DatabaseError):
            await repo.list_by_sync_status(SyncStatus.PENDING, offset=0, limit=10)

    @pytest.mark.asyncio
    async def test_list_by_user_handles_database_error(self):
        """Test that list_by_user handles database error."""
        # Create mock session that raises DatabaseError
        mock_session = AsyncMock(spec=AsyncSession)
        mock_execute = AsyncMock(side_effect=DatabaseError("test error", {}, Exception()))
        mock_session.execute = mock_execute

        repo = TodoistTaskRepository(mock_session)

        with pytest.raises(DatabaseError):
            await repo.list_by_user(uuid4(), offset=0, limit=10)

    @pytest.mark.asyncio
    async def test_get_by_todoist_id_handles_sqlalchemy_error(self):
        """Test that get_by_todoist_id handles generic SQLAlchemyError."""
        # Create mock session that raises SQLAlchemyError
        mock_session = AsyncMock(spec=AsyncSession)
        mock_execute = AsyncMock(side_effect=SQLAlchemyError("test error"))
        mock_session.execute = mock_execute

        repo = TodoistTaskRepository(mock_session)

        with pytest.raises(SQLAlchemyError):
            await repo.get_by_todoist_id(123456789)

    @pytest.mark.asyncio
    async def test_list_by_sync_status_handles_sqlalchemy_error(self):
        """Test that list_by_sync_status handles generic SQLAlchemyError."""
        # Create mock session that raises SQLAlchemyError
        mock_session = AsyncMock(spec=AsyncSession)
        mock_execute = AsyncMock(side_effect=SQLAlchemyError("test error"))
        mock_session.execute = mock_execute

        repo = TodoistTaskRepository(mock_session)

        with pytest.raises(SQLAlchemyError):
            await repo.list_by_sync_status(SyncStatus.PENDING, offset=0, limit=10)

    @pytest.mark.asyncio
    async def test_list_by_user_handles_sqlalchemy_error(self):
        """Test that list_by_user handles generic SQLAlchemyError."""
        # Create mock session that raises SQLAlchemyError
        mock_session = AsyncMock(spec=AsyncSession)
        mock_execute = AsyncMock(side_effect=SQLAlchemyError("test error"))
        mock_session.execute = mock_execute

        repo = TodoistTaskRepository(mock_session)

        with pytest.raises(SQLAlchemyError):
            await repo.list_by_user(uuid4(), offset=0, limit=10)
