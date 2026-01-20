"""Tests for ReminderRepository class."""

import pytest
from uuid import uuid4
from datetime import datetime, timedelta
from unittest.mock import AsyncMock

from sqlalchemy.exc import DatabaseError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import Reminder
from src.db.repositories.reminder import ReminderRepository


class TestReminderRepository:
    """Tests for ReminderRepository specific methods."""

    @pytest.mark.asyncio
    async def test_list_by_user_filters_correctly(self, async_session: AsyncSession):
        """Test that list_by_user returns reminders for specific user."""
        repo = ReminderRepository(async_session)
        user1_id = uuid4()
        user2_id = uuid4()

        reminder1 = Reminder(user_id=user1_id, remind_at=datetime.utcnow(), message="Reminder 1")
        reminder2 = Reminder(user_id=user1_id, remind_at=datetime.utcnow(), message="Reminder 2")
        reminder3 = Reminder(user_id=user2_id, remind_at=datetime.utcnow(), message="Reminder 3")
        async_session.add(reminder1)
        async_session.add(reminder2)
        async_session.add(reminder3)
        await async_session.commit()

        reminders = await repo.list_by_user(user1_id, offset=0, limit=10)

        assert len(reminders) == 2
        assert all(reminder.user_id == user1_id for reminder in reminders)

    @pytest.mark.asyncio
    async def test_list_pending_filters_by_datetime(self, async_session: AsyncSession):
        """Test that list_pending returns reminders before specified time."""
        repo = ReminderRepository(async_session)
        now = datetime.utcnow()

        # Reminder in the past
        past_reminder = Reminder(
            user_id=uuid4(), remind_at=now - timedelta(hours=1), message="Past reminder"
        )
        # Reminder in the future
        future_reminder = Reminder(
            user_id=uuid4(), remind_at=now + timedelta(hours=1), message="Future reminder"
        )
        # Reminder at current time
        now_reminder = Reminder(user_id=uuid4(), remind_at=now, message="Now reminder")
        async_session.add(past_reminder)
        async_session.add(future_reminder)
        async_session.add(now_reminder)
        await async_session.commit()

        reminders = await repo.list_pending(before=now, offset=0, limit=10)

        # Should include past reminder and now reminder
        assert len(reminders) >= 1
        assert all(reminder.remind_at <= now for reminder in reminders)

    @pytest.mark.asyncio
    async def test_list_unsent_filters_by_is_sent(self, async_session: AsyncSession):
        """Test that list_unsent returns only unsent reminders."""
        repo = ReminderRepository(async_session)
        user_id = uuid4()

        unsent1 = Reminder(
            user_id=user_id, remind_at=datetime.utcnow(), message="Unsent 1", is_sent=False
        )
        unsent2 = Reminder(
            user_id=user_id, remind_at=datetime.utcnow(), message="Unsent 2", is_sent=False
        )
        sent = Reminder(user_id=user_id, remind_at=datetime.utcnow(), message="Sent", is_sent=True)
        async_session.add(unsent1)
        async_session.add(unsent2)
        async_session.add(sent)
        await async_session.commit()

        reminders = await repo.list_unsent(user_id, offset=0, limit=10)

        assert len(reminders) == 2
        assert all(not reminder.is_sent for reminder in reminders)


class TestReminderRepositoryEdgeCases:
    """Tests for ReminderRepository edge cases."""

    @pytest.mark.asyncio
    async def test_list_by_user_with_no_results(self, async_session: AsyncSession):
        """Test that list_by_user returns empty list when no reminders for user."""
        repo = ReminderRepository(async_session)
        user_id = uuid4()

        # Create reminder for different user
        other_user_id = uuid4()
        reminder = Reminder(
            user_id=other_user_id, remind_at=datetime.utcnow(), message="Other user reminder"
        )
        async_session.add(reminder)
        await async_session.commit()

        reminders = await repo.list_by_user(user_id, offset=0, limit=10)

        assert len(reminders) == 0

    @pytest.mark.asyncio
    async def test_list_by_user_excludes_soft_deleted(self, async_session: AsyncSession):
        """Test that list_by_user excludes soft-deleted reminders."""
        repo = ReminderRepository(async_session)
        user_id = uuid4()

        reminder1 = Reminder(user_id=user_id, remind_at=datetime.utcnow(), message="Reminder 1")
        reminder2 = Reminder(user_id=user_id, remind_at=datetime.utcnow(), message="Reminder 2")
        async_session.add(reminder1)
        async_session.add(reminder2)
        await async_session.commit()
        await async_session.refresh(reminder1)

        # Soft delete one reminder
        await repo.delete(reminder1.id)

        reminders = await repo.list_by_user(user_id, offset=0, limit=10)

        assert len(reminders) == 1
        assert reminders[0].message == "Reminder 2"

    @pytest.mark.asyncio
    async def test_list_pending_with_no_pending_reminders(self, async_session: AsyncSession):
        """Test that list_pending returns empty list when no pending reminders."""
        repo = ReminderRepository(async_session)
        now = datetime.utcnow()

        # Only future reminders
        future_reminder = Reminder(
            user_id=uuid4(), remind_at=now + timedelta(hours=1), message="Future reminder"
        )
        async_session.add(future_reminder)
        await async_session.commit()

        reminders = await repo.list_pending(before=now, offset=0, limit=10)

        assert len(reminders) == 0

    @pytest.mark.asyncio
    async def test_list_pending_excludes_soft_deleted(self, async_session: AsyncSession):
        """Test that list_pending excludes soft-deleted reminders."""
        repo = ReminderRepository(async_session)
        now = datetime.utcnow()

        past_reminder = Reminder(
            user_id=uuid4(), remind_at=now - timedelta(hours=1), message="Past reminder"
        )
        async_session.add(past_reminder)
        await async_session.commit()
        await async_session.refresh(past_reminder)

        # Soft delete the reminder
        await repo.delete(past_reminder.id)

        reminders = await repo.list_pending(before=now, offset=0, limit=10)

        assert len(reminders) == 0

    @pytest.mark.asyncio
    async def test_list_unsent_with_no_unsent_reminders(self, async_session: AsyncSession):
        """Test that list_unsent returns empty list when all reminders are sent."""
        repo = ReminderRepository(async_session)
        user_id = uuid4()

        sent1 = Reminder(
            user_id=user_id, remind_at=datetime.utcnow(), message="Sent 1", is_sent=True
        )
        sent2 = Reminder(
            user_id=user_id, remind_at=datetime.utcnow(), message="Sent 2", is_sent=True
        )
        async_session.add(sent1)
        async_session.add(sent2)
        await async_session.commit()

        reminders = await repo.list_unsent(user_id, offset=0, limit=10)

        assert len(reminders) == 0

    @pytest.mark.asyncio
    async def test_list_unsent_excludes_soft_deleted(self, async_session: AsyncSession):
        """Test that list_unsent excludes soft-deleted reminders."""
        repo = ReminderRepository(async_session)
        user_id = uuid4()

        unsent1 = Reminder(
            user_id=user_id, remind_at=datetime.utcnow(), message="Unsent 1", is_sent=False
        )
        unsent2 = Reminder(
            user_id=user_id, remind_at=datetime.utcnow(), message="Unsent 2", is_sent=False
        )
        async_session.add(unsent1)
        async_session.add(unsent2)
        await async_session.commit()
        await async_session.refresh(unsent1)

        # Soft delete one unsent reminder
        await repo.delete(unsent1.id)

        reminders = await repo.list_unsent(user_id, offset=0, limit=10)

        assert len(reminders) == 1
        assert reminders[0].message == "Unsent 2"

    @pytest.mark.asyncio
    async def test_list_by_user_respects_pagination(self, async_session: AsyncSession):
        """Test that list_by_user respects pagination parameters."""
        repo = ReminderRepository(async_session)
        user_id = uuid4()

        # Create 5 reminders
        for i in range(5):
            reminder = Reminder(
                user_id=user_id, remind_at=datetime.utcnow(), message=f"Reminder {i}"
            )
            async_session.add(reminder)
        await async_session.commit()

        # First page
        reminders = await repo.list_by_user(user_id, offset=0, limit=2)
        assert len(reminders) == 2

        # Second page
        reminders = await repo.list_by_user(user_id, offset=2, limit=2)
        assert len(reminders) == 2

    @pytest.mark.asyncio
    async def test_list_pending_respects_pagination(self, async_session: AsyncSession):
        """Test that list_pending respects pagination parameters."""
        repo = ReminderRepository(async_session)
        now = datetime.utcnow()

        # Create 5 past reminders
        for i in range(5):
            reminder = Reminder(
                user_id=uuid4(),
                remind_at=now - timedelta(hours=i + 1),
                message=f"Reminder {i}",
            )
            async_session.add(reminder)
        await async_session.commit()

        # First page
        reminders = await repo.list_pending(before=now, offset=0, limit=2)
        assert len(reminders) == 2

        # Second page
        reminders = await repo.list_pending(before=now, offset=2, limit=2)
        assert len(reminders) == 2

    @pytest.mark.asyncio
    async def test_list_unsent_respects_pagination(self, async_session: AsyncSession):
        """Test that list_unsent respects pagination parameters."""
        repo = ReminderRepository(async_session)
        user_id = uuid4()

        # Create 5 unsent reminders
        for i in range(5):
            reminder = Reminder(
                user_id=user_id, remind_at=datetime.utcnow(), message=f"Reminder {i}", is_sent=False
            )
            async_session.add(reminder)
        await async_session.commit()

        # First page
        reminders = await repo.list_unsent(user_id, offset=0, limit=2)
        assert len(reminders) == 2

        # Second page
        reminders = await repo.list_unsent(user_id, offset=2, limit=2)
        assert len(reminders) == 2


class TestReminderRepositoryErrorHandling:
    """Tests for ReminderRepository error handling using mocks."""

    @pytest.mark.asyncio
    async def test_list_by_user_handles_database_error(self):
        """Test that list_by_user handles database error."""
        # Create mock session that raises DatabaseError
        mock_session = AsyncMock(spec=AsyncSession)
        mock_execute = AsyncMock(side_effect=DatabaseError("test error", {}, Exception()))
        mock_session.execute = mock_execute

        repo = ReminderRepository(mock_session)

        with pytest.raises(DatabaseError):
            await repo.list_by_user(uuid4(), offset=0, limit=10)

    @pytest.mark.asyncio
    async def test_list_pending_handles_database_error(self):
        """Test that list_pending handles database error."""
        # Create mock session that raises DatabaseError
        mock_session = AsyncMock(spec=AsyncSession)
        mock_execute = AsyncMock(side_effect=DatabaseError("test error", {}, Exception()))
        mock_session.execute = mock_execute

        repo = ReminderRepository(mock_session)

        with pytest.raises(DatabaseError):
            await repo.list_pending(datetime.utcnow(), offset=0, limit=10)

    @pytest.mark.asyncio
    async def test_list_unsent_handles_database_error(self):
        """Test that list_unsent handles database error."""
        # Create mock session that raises DatabaseError
        mock_session = AsyncMock(spec=AsyncSession)
        mock_execute = AsyncMock(side_effect=DatabaseError("test error", {}, Exception()))
        mock_session.execute = mock_execute

        repo = ReminderRepository(mock_session)

        with pytest.raises(DatabaseError):
            await repo.list_unsent(uuid4(), offset=0, limit=10)

    @pytest.mark.asyncio
    async def test_list_by_user_handles_sqlalchemy_error(self):
        """Test that list_by_user handles generic SQLAlchemyError."""
        # Create mock session that raises SQLAlchemyError
        mock_session = AsyncMock(spec=AsyncSession)
        mock_execute = AsyncMock(side_effect=SQLAlchemyError("test error"))
        mock_session.execute = mock_execute

        repo = ReminderRepository(mock_session)

        with pytest.raises(SQLAlchemyError):
            await repo.list_by_user(uuid4(), offset=0, limit=10)

    @pytest.mark.asyncio
    async def test_list_pending_handles_sqlalchemy_error(self):
        """Test that list_pending handles generic SQLAlchemyError."""
        # Create mock session that raises SQLAlchemyError
        mock_session = AsyncMock(spec=AsyncSession)
        mock_execute = AsyncMock(side_effect=SQLAlchemyError("test error"))
        mock_session.execute = mock_execute

        repo = ReminderRepository(mock_session)

        with pytest.raises(SQLAlchemyError):
            await repo.list_pending(datetime.utcnow(), offset=0, limit=10)

    @pytest.mark.asyncio
    async def test_list_unsent_handles_sqlalchemy_error(self):
        """Test that list_unsent handles generic SQLAlchemyError."""
        # Create mock session that raises SQLAlchemyError
        mock_session = AsyncMock(spec=AsyncSession)
        mock_execute = AsyncMock(side_effect=SQLAlchemyError("test error"))
        mock_session.execute = mock_execute

        repo = ReminderRepository(mock_session)

        with pytest.raises(SQLAlchemyError):
            await repo.list_unsent(uuid4(), offset=0, limit=10)
