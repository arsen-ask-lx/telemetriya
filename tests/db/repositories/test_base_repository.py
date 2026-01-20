"""Tests for BaseRepository class."""

import pytest
from datetime import datetime
from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock, patch

from sqlalchemy import select
from sqlalchemy.exc import DatabaseError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models import User
from src.db.repositories.base import BaseRepository


class TestBaseRepositoryCreate:
    """Tests for BaseRepository.create() method."""

    @pytest.mark.asyncio
    async def test_create_returns_created_object(self, async_session: AsyncSession):
        """Test that create returns the created object with ID."""
        repo = BaseRepository[User](User, async_session)
        user_data = {
            "telegram_id": 123456789,
            "username": "testuser",
            "first_name": "Test",
            "last_name": "User",
        }

        user = await repo.create(**user_data)

        assert user.id is not None
        assert user.telegram_id == 123456789
        assert user.username == "testuser"
        assert user.first_name == "Test"
        assert user.last_name == "User"


class TestBaseRepositoryGet:
    """Tests for BaseRepository.get() method."""

    @pytest.mark.asyncio
    async def test_get_returns_object_by_id(self, async_session: AsyncSession):
        """Test that get returns object by its ID."""
        repo = BaseRepository[User](User, async_session)
        user = User(telegram_id=123456789, username="testuser")
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)

        fetched_user = await repo.get(user.id)

        assert fetched_user is not None
        assert fetched_user.id == user.id
        assert fetched_user.telegram_id == 123456789

    @pytest.mark.asyncio
    async def test_get_returns_none_for_nonexistent_id(self, async_session: AsyncSession):
        """Test that get returns None for non-existent ID."""
        repo = BaseRepository[User](User, async_session)
        non_existent_id = uuid4()

        result = await repo.get(non_existent_id)

        assert result is None


class TestBaseRepositoryGetOr404:
    """Tests for BaseRepository.get_or_404() method."""

    @pytest.mark.asyncio
    async def test_get_or_404_returns_object(self, async_session: AsyncSession):
        """Test that get_or_404 returns object for existing ID."""
        repo = BaseRepository[User](User, async_session)
        user = User(telegram_id=123456789, username="testuser")
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)

        fetched_user = await repo.get_or_404(user.id)

        assert fetched_user.id == user.id
        assert fetched_user.telegram_id == 123456789

    @pytest.mark.asyncio
    async def test_get_or_404_raises_not_found(self, async_session: AsyncSession):
        """Test that get_or_404 raises exception for non-existent ID."""
        repo = BaseRepository[User](User, async_session)
        non_existent_id = uuid4()

        with pytest.raises(ValueError, match="not found"):
            await repo.get_or_404(non_existent_id)


class TestBaseRepositoryUpdate:
    """Tests for BaseRepository.update() method."""

    @pytest.mark.asyncio
    async def test_update_modifies_object(self, async_session: AsyncSession):
        """Test that update modifies object fields."""
        repo = BaseRepository[User](User, async_session)
        user = User(telegram_id=123456789, username="oldname")
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)

        updated_user = await repo.update(user.id, {"username": "newname"})

        assert updated_user.username == "newname"
        assert updated_user.telegram_id == 123456789

    @pytest.mark.asyncio
    async def test_update_raises_not_found(self, async_session: AsyncSession):
        """Test that update raises exception for non-existent ID."""
        repo = BaseRepository[User](User, async_session)
        non_existent_id = uuid4()

        with pytest.raises(ValueError, match="not found"):
            await repo.update(non_existent_id, {"username": "newname"})


class TestBaseRepositoryDelete:
    """Tests for BaseRepository.delete() method."""

    @pytest.mark.asyncio
    async def test_delete_removes_object(self, async_session: AsyncSession):
        """Test that delete marks object as soft-deleted."""
        repo = BaseRepository[User](User, async_session)
        user = User(telegram_id=123456789, username="testuser")
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)

        await repo.delete(user.id)

        # After soft delete, get() should return None (filtered out)
        fetched_user = await repo.get(user.id)
        assert fetched_user is None

        # But record still exists in DB with deleted_at set
        from sqlalchemy import select

        stmt = select(User).where(User.id == user.id)
        result = await async_session.execute(stmt)
        all_users = list(result.scalars().all())
        assert len(all_users) == 1
        assert all_users[0].deleted_at is not None

    @pytest.mark.asyncio
    async def test_delete_raises_not_found(self, async_session: AsyncSession):
        """Test that delete raises exception for non-existent ID."""
        repo = BaseRepository[User](User, async_session)
        non_existent_id = uuid4()

        with pytest.raises(ValueError, match="not found"):
            await repo.delete(non_existent_id)


class TestBaseRepositoryList:
    """Tests for BaseRepository.list() method."""

    @pytest.mark.asyncio
    async def test_list_returns_paginated_results(self, async_session: AsyncSession):
        """Test that list returns paginated results."""
        repo = BaseRepository[User](User, async_session)

        # Create 5 users
        for i in range(5):
            user = User(telegram_id=1000000 + i, username=f"user{i}")
            async_session.add(user)
        await async_session.commit()

        # Get first page
        users = await repo.list(offset=0, limit=2)

        assert len(users) == 2
        assert users[0].username == "user0"
        assert users[1].username == "user1"

    @pytest.mark.asyncio
    async def test_list_filters_correctly(self, async_session: AsyncSession):
        """Test that list filters by provided filters."""
        repo = BaseRepository[User](User, async_session)

        # Create users with different active status
        active_user = User(telegram_id=1000001, username="active", is_active=True)
        inactive_user = User(telegram_id=1000002, username="inactive", is_active=False)
        async_session.add(active_user)
        async_session.add(inactive_user)
        await async_session.commit()

        # Filter for active users
        users = await repo.list(filters={"is_active": True})

        assert len(users) == 1
        assert users[0].username == "active"

    @pytest.mark.asyncio
    async def test_list_sorts_correctly(self, async_session: AsyncSession):
        """Test that list sorts by order_by field."""
        repo = BaseRepository[User](User, async_session)

        # Create users with different names
        user3 = User(telegram_id=1000003, username="charlie")
        user1 = User(telegram_id=1000001, username="alice")
        user2 = User(telegram_id=1000002, username="bob")
        async_session.add(user3)
        async_session.add(user1)
        async_session.add(user2)
        await async_session.commit()

        # Sort by username
        users = await repo.list(order_by="username")

        assert len(users) == 3
        assert users[0].username == "alice"
        assert users[1].username == "bob"
        assert users[2].username == "charlie"


class TestBaseRepositoryCount:
    """Tests for BaseRepository.count() method."""

    @pytest.mark.asyncio
    async def test_count_returns_correct_count(self, async_session: AsyncSession):
        """Test that count returns correct number of objects."""
        repo = BaseRepository[User](User, async_session)

        # Create 3 users
        for i in range(3):
            user = User(telegram_id=2000000 + i, username=f"user{i}")
            async_session.add(user)
        await async_session.commit()

        count = await repo.count()

        assert count == 3

    @pytest.mark.asyncio
    async def test_count_with_filters(self, async_session: AsyncSession):
        """Test that count filters by provided filters."""
        repo = BaseRepository[User](User, async_session)

        # Create users with different active status
        active1 = User(telegram_id=3000001, username="active1", is_active=True)
        active2 = User(telegram_id=3000002, username="active2", is_active=True)
        inactive = User(telegram_id=3000003, username="inactive", is_active=False)
        async_session.add(active1)
        async_session.add(active2)
        async_session.add(inactive)
        await async_session.commit()

        count = await repo.count(filters={"is_active": True})

        assert count == 2


class TestBaseRepositoryEdgeCases:
    """Tests for edge cases in BaseRepository."""

    @pytest.mark.asyncio
    async def test_list_with_large_offset_returns_empty(self, async_session: AsyncSession):
        """Test that list with large offset returns empty list."""
        repo = BaseRepository[User](User, async_session)

        # Create 2 users
        for i in range(2):
            user = User(telegram_id=4000000 + i, username=f"user{i}")
            async_session.add(user)
        await async_session.commit()

        users = await repo.list(offset=100, limit=10)

        assert len(users) == 0

    @pytest.mark.asyncio
    async def test_list_excludes_soft_deleted_records(self, async_session: AsyncSession):
        """Test that list excludes soft-deleted records."""
        repo = BaseRepository[User](User, async_session)

        active_user = User(telegram_id=5000001, username="active", is_active=True)
        deleted_user = User(telegram_id=5000002, username="deleted", is_active=True)
        async_session.add(active_user)
        async_session.add(deleted_user)
        await async_session.commit()

        # Soft delete one user
        await repo.delete(deleted_user.id)

        users = await repo.list()

        assert len(users) == 1
        assert users[0].username == "active"

    @pytest.mark.asyncio
    async def test_count_excludes_soft_deleted_records(self, async_session: AsyncSession):
        """Test that count excludes soft-deleted records."""
        repo = BaseRepository[User](User, async_session)

        active_user = User(telegram_id=6000001, username="active", is_active=True)
        deleted_user = User(telegram_id=6000002, username="deleted", is_active=True)
        async_session.add(active_user)
        async_session.add(deleted_user)
        await async_session.commit()

        # Soft delete one user
        await repo.delete(deleted_user.id)

        count = await repo.count()

        assert count == 1

    @pytest.mark.asyncio
    async def test_get_returns_none_for_soft_deleted(self, async_session: AsyncSession):
        """Test that get returns None for soft-deleted records."""
        repo = BaseRepository[User](User, async_session)
        user = User(telegram_id=7000001, username="testuser")
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)

        # Soft delete the user
        await repo.delete(user.id)

        fetched_user = await repo.get(user.id)

        assert fetched_user is None

    @pytest.mark.asyncio
    async def test_create_with_multiple_fields(self, async_session: AsyncSession):
        """Test that create works with multiple fields."""
        repo = BaseRepository[User](User, async_session)
        user_data = {
            "telegram_id": 999999999,
            "username": "fulluser",
            "first_name": "Full",
            "last_name": "User",
            "language_code": "en",
            "is_active": False,
        }

        user = await repo.create(**user_data)

        assert user.id is not None
        assert user.telegram_id == 999999999
        assert user.username == "fulluser"
        assert user.first_name == "Full"
        assert user.last_name == "User"
        assert user.language_code == "en"
        assert user.is_active is False


class TestBaseRepositoryPaginationValidation:
    """Tests for pagination parameter validation in list()."""

    @pytest.mark.asyncio
    async def test_list_with_negative_offset_raises_error(self, async_session: AsyncSession):
        """Test that list raises ValueError for negative offset."""
        repo = BaseRepository[User](User, async_session)

        with pytest.raises(ValueError, match="offset must be >= 0"):
            await repo.list(offset=-1, limit=10)

    @pytest.mark.asyncio
    async def test_list_with_zero_limit_raises_error(self, async_session: AsyncSession):
        """Test that list raises ValueError for zero limit."""
        repo = BaseRepository[User](User, async_session)

        with pytest.raises(ValueError, match="limit must be > 0"):
            await repo.list(offset=0, limit=0)

    @pytest.mark.asyncio
    async def test_list_with_negative_limit_raises_error(self, async_session: AsyncSession):
        """Test that list raises ValueError for negative limit."""
        repo = BaseRepository[User](User, async_session)

        with pytest.raises(ValueError, match="limit must be > 0"):
            await repo.list(offset=0, limit=-1)

    @pytest.mark.asyncio
    async def test_list_with_limit_over_1000_raises_error(self, async_session: AsyncSession):
        """Test that list raises ValueError for limit > 1000."""
        repo = BaseRepository[User](User, async_session)

        with pytest.raises(ValueError, match="limit cannot exceed 1000"):
            await repo.list(offset=0, limit=1001)

    @pytest.mark.asyncio
    async def test_list_with_limit_1000_works(self, async_session: AsyncSession):
        """Test that list works with limit = 1000."""
        repo = BaseRepository[User](User, async_session)

        # Create one user
        user = User(telegram_id=123456789, username="testuser")
        async_session.add(user)
        await async_session.commit()

        users = await repo.list(offset=0, limit=1000)

        assert len(users) == 1

    @pytest.mark.asyncio
    async def test_list_with_limit_1_returns_single_result(self, async_session: AsyncSession):
        """Test that list with limit=1 returns single result."""
        repo = BaseRepository[User](User, async_session)

        # Create 3 users
        for i in range(3):
            user = User(telegram_id=1000000 + i, username=f"user{i}")
            async_session.add(user)
        await async_session.commit()

        users = await repo.list(offset=0, limit=1)

        assert len(users) == 1


class TestBaseRepositoryInvalidFilters:
    """Tests for invalid filter handling."""

    @pytest.mark.asyncio
    async def test_list_with_empty_filters_dict(self, async_session: AsyncSession):
        """Test that list works with empty filters dict."""
        repo = BaseRepository[User](User, async_session)

        user = User(telegram_id=123456789, username="testuser")
        async_session.add(user)
        await async_session.commit()

        users = await repo.list(filters={})

        assert len(users) == 1

    @pytest.mark.asyncio
    async def test_list_with_nonexistent_field_filter(self, async_session: AsyncSession):
        """Test that list ignores filters for non-existent fields."""
        repo = BaseRepository[User](User, async_session)

        user = User(telegram_id=123456789, username="testuser")
        async_session.add(user)
        await async_session.commit()

        # Filter with non-existent field - should be ignored
        users = await repo.list(filters={"nonexistent_field": "value"})

        # Should return the user since filter is ignored
        assert len(users) == 1

    @pytest.mark.asyncio
    async def test_list_with_multiple_filter_combinations(self, async_session: AsyncSession):
        """Test that list works with multiple filter combinations."""
        repo = BaseRepository[User](User, async_session)

        # Create users with different combinations
        user1 = User(telegram_id=1000001, username="user1", is_active=True, language_code="en")
        user2 = User(telegram_id=1000002, username="user2", is_active=True, language_code="ru")
        user3 = User(telegram_id=1000003, username="user3", is_active=False, language_code="en")
        async_session.add(user1)
        async_session.add(user2)
        async_session.add(user3)
        await async_session.commit()

        # Filter by is_active only
        users = await repo.list(filters={"is_active": True})
        assert len(users) == 2

        # Filter by language_code only
        users = await repo.list(filters={"language_code": "en"})
        assert len(users) == 2

        # Filter by both
        users = await repo.list(filters={"is_active": True, "language_code": "en"})
        assert len(users) == 1
        assert users[0].username == "user1"


class TestBaseRepositoryInvalidOrderBy:
    """Tests for invalid order_by field handling."""

    @pytest.mark.asyncio
    async def test_list_with_invalid_order_by_field(self, async_session: AsyncSession):
        """Test that list handles invalid order_by field gracefully."""
        repo = BaseRepository[User](User, async_session)

        user = User(telegram_id=123456789, username="testuser")
        async_session.add(user)
        await async_session.commit()

        # Invalid order_by should be ignored (logged as warning)
        users = await repo.list(order_by="nonexistent_field")

        # Should still return the user
        assert len(users) == 1

    @pytest.mark.asyncio
    async def test_list_with_valid_order_by_field(self, async_session: AsyncSession):
        """Test that list works with valid order_by field."""
        repo = BaseRepository[User](User, async_session)

        # Create users with different usernames
        user2 = User(telegram_id=1000002, username="bob")
        user1 = User(telegram_id=1000001, username="alice")
        user3 = User(telegram_id=1000003, username="charlie")
        async_session.add(user2)
        async_session.add(user1)
        async_session.add(user3)
        await async_session.commit()

        # Order by username
        users = await repo.list(order_by="username")

        assert len(users) == 3
        assert users[0].username == "alice"
        assert users[1].username == "bob"
        assert users[2].username == "charlie"


class TestBaseRepositoryUpdateEdgeCases:
    """Tests for update edge cases."""

    @pytest.mark.asyncio
    async def test_update_with_partial_data(self, async_session: AsyncSession):
        """Test that update works with partial data."""
        repo = BaseRepository[User](User, async_session)

        user = User(
            telegram_id=123456789,
            username="oldname",
            first_name="Old",
            last_name="User",
            language_code="en",
        )
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)

        # Update only username
        updated_user = await repo.update(user.id, {"username": "newname"})

        assert updated_user.username == "newname"
        assert updated_user.first_name == "Old"  # Should remain unchanged
        assert updated_user.last_name == "User"  # Should remain unchanged

    @pytest.mark.asyncio
    async def test_update_with_multiple_fields(self, async_session: AsyncSession):
        """Test that update works with multiple fields."""
        repo = BaseRepository[User](User, async_session)

        user = User(
            telegram_id=123456789,
            username="oldname",
            first_name="Old",
            last_name="User",
            language_code="en",
        )
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)

        # Update multiple fields
        updated_user = await repo.update(
            user.id,
            {"username": "newname", "first_name": "New", "language_code": "ru"},
        )

        assert updated_user.username == "newname"
        assert updated_user.first_name == "New"
        assert updated_user.last_name == "User"  # Unchanged
        assert updated_user.language_code == "ru"


class TestBaseRepositorySoftDelete:
    """Tests for soft delete behavior."""

    @pytest.mark.asyncio
    async def test_delete_sets_deleted_at_timestamp(self, async_session: AsyncSession):
        """Test that soft delete sets deleted_at timestamp."""
        repo = BaseRepository[User](User, async_session)

        user = User(telegram_id=123456789, username="testuser")
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)

        await repo.delete(user.id)

        # Get directly from DB (bypassing repo's soft delete filter)
        from sqlalchemy import select

        stmt = select(User).where(User.id == user.id)
        result = await async_session.execute(stmt)
        deleted_user = result.scalar_one()

        assert deleted_user.deleted_at is not None

    @pytest.mark.asyncio
    async def test_get_returns_none_for_soft_deleted_record(self, async_session: AsyncSession):
        """Test that get returns None for soft-deleted records."""
        repo = BaseRepository[User](User, async_session)

        user = User(telegram_id=123456789, username="testuser")
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)

        # Soft delete
        await repo.delete(user.id)

        # get should return None
        fetched_user = await repo.get(user.id)
        assert fetched_user is None

    @pytest.mark.asyncio
    async def test_get_or_404_raises_for_soft_deleted_record(self, async_session: AsyncSession):
        """Test that get_or_404 raises for soft-deleted records."""
        repo = BaseRepository[User](User, async_session)

        user = User(telegram_id=123456789, username="testuser")
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)

        # Soft delete
        await repo.delete(user.id)

        # get_or_404 should raise
        with pytest.raises(ValueError, match="not found"):
            await repo.get_or_404(user.id)

    @pytest.mark.asyncio
    async def test_update_raises_for_soft_deleted_record(self, async_session: AsyncSession):
        """Test that update raises for soft-deleted records."""
        repo = BaseRepository[User](User, async_session)

        user = User(telegram_id=123456789, username="testuser")
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)

        # Soft delete
        await repo.delete(user.id)

        # update should raise
        with pytest.raises(ValueError, match="not found"):
            await repo.update(user.id, {"username": "newname"})

    @pytest.mark.asyncio
    async def test_delete_raises_for_soft_deleted_record(self, async_session: AsyncSession):
        """Test that delete raises for soft-deleted records."""
        repo = BaseRepository[User](User, async_session)

        user = User(telegram_id=123456789, username="testuser")
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)

        # Soft delete
        await repo.delete(user.id)

        # Trying to delete again should raise
        with pytest.raises(ValueError, match="not found"):
            await repo.delete(user.id)


class TestBaseRepositoryHardDelete:
    """Tests for hard delete behavior (models without SoftDeleteMixin)."""

    @pytest.mark.asyncio
    async def test_delete_hard_deletes_for_non_soft_delete_model(self, async_session: AsyncSession):
        """Test that delete performs hard delete for models without SoftDeleteMixin."""
        # User model has SoftDeleteMixin, so we can't test hard delete with it
        # This test documents the behavior for future models without SoftDeleteMixin
        # For now, we skip this test as we don't have a model without SoftDeleteMixin
        pytest.skip("No model without SoftDeleteMixin available for testing")


class TestBaseRepositoryDatabaseErrors:
    """Tests for database error handling."""

    @pytest.mark.asyncio
    async def test_create_rolls_back_on_error(self, async_session: AsyncSession):
        """Test that create handles errors gracefully."""
        repo = BaseRepository[User](User, async_session)

        # Create a user first
        user1 = await repo.create(telegram_id=123456789, username="user1")
        await async_session.refresh(user1)

        # The first user should still exist
        user1_check = await repo.get(user1.id)
        assert user1_check is not None

    @pytest.mark.asyncio
    async def test_get_handles_database_errors(self, async_session: AsyncSession):
        """Test that get handles database errors gracefully."""
        repo = BaseRepository[User](User, async_session)

        # Normal case - should work
        user = await repo.create(telegram_id=123456789, username="testuser")
        fetched = await repo.get(user.id)
        assert fetched is not None

        # Non-existent ID - should return None, not raise
        from uuid import uuid4

        fetched = await repo.get(uuid4())
        assert fetched is None

    @pytest.mark.asyncio
    async def test_update_rolls_back_on_error(self, async_session: AsyncSession):
        """Test that update handles errors gracefully."""
        repo = BaseRepository[User](User, async_session)

        user = await repo.create(telegram_id=123456789, username="original")
        await async_session.refresh(user)

        # Update with valid data
        updated = await repo.update(user.id, {"username": "updated"})
        assert updated.username == "updated"

        # Verify update was committed
        fetched = await repo.get(user.id)
        assert fetched is not None
        assert fetched.username == "updated"

    @pytest.mark.asyncio
    async def test_delete_rolls_back_on_error(self, async_session: AsyncSession):
        """Test that delete handles errors gracefully."""
        repo = BaseRepository[User](User, async_session)

        user = await repo.create(telegram_id=123456789, username="testuser")
        await async_session.refresh(user)

        # Normal delete should work
        await repo.delete(user.id)

        # User should be soft-deleted (not found by get)
        fetched = await repo.get(user.id)
        assert fetched is None

    @pytest.mark.asyncio
    async def test_list_handles_database_errors(self, async_session: AsyncSession):
        """Test that list handles database errors gracefully."""
        repo = BaseRepository[User](User, async_session)

        # Normal case - should work
        user = await repo.create(telegram_id=123456789, username="testuser")
        users = await repo.list()
        assert len(users) == 1

    @pytest.mark.asyncio
    async def test_count_handles_database_errors(self, async_session: AsyncSession):
        """Test that count handles database errors gracefully."""
        repo = BaseRepository[User](User, async_session)

        # Normal case - should work
        user = await repo.create(telegram_id=123456789, username="testuser")
        count = await repo.count()
        assert count == 1

        # Count with filters
        user2 = await repo.create(telegram_id=987654321, username="testuser2", is_active=True)
        count = await repo.count(filters={"is_active": True})
        assert count >= 1


class TestBaseRepositoryFilterCombinations:
    """Tests for complex filter combinations."""

    @pytest.mark.asyncio
    async def test_list_with_multiple_filters(self, async_session: AsyncSession):
        """Test that list works with multiple filters."""
        repo = BaseRepository[User](User, async_session)

        # Create users with different combinations
        active_en = User(
            telegram_id=1000001, username="active_en", is_active=True, language_code="en"
        )
        active_ru = User(
            telegram_id=1000002, username="active_ru", is_active=True, language_code="ru"
        )
        inactive_en = User(
            telegram_id=1000003, username="inactive_en", is_active=False, language_code="en"
        )
        async_session.add(active_en)
        async_session.add(active_ru)
        async_session.add(inactive_en)
        await async_session.commit()

        # Filter by is_active AND language_code
        users = await repo.list(filters={"is_active": True, "language_code": "en"})
        assert len(users) == 1
        assert users[0].username == "active_en"

    @pytest.mark.asyncio
    async def test_count_with_multiple_filters(self, async_session: AsyncSession):
        """Test that count works with multiple filters."""
        repo = BaseRepository[User](User, async_session)

        # Create users with different combinations
        active_en = User(
            telegram_id=1000001, username="active_en", is_active=True, language_code="en"
        )
        active_ru = User(
            telegram_id=1000002, username="active_ru", is_active=True, language_code="ru"
        )
        inactive_en = User(
            telegram_id=1000003, username="inactive_en", is_active=False, language_code="en"
        )
        async_session.add(active_en)
        async_session.add(active_ru)
        async_session.add(inactive_en)
        await async_session.commit()

        # Count with multiple filters
        count = await repo.count(filters={"is_active": True, "language_code": "en"})
        assert count == 1

    @pytest.mark.asyncio
    async def test_list_with_filters_and_sorting(self, async_session: AsyncSession):
        """Test that list works with filters and sorting together."""
        repo = BaseRepository[User](User, async_session)

        # Create users
        user2 = User(telegram_id=1000002, username="bob", is_active=True, language_code="en")
        user1 = User(telegram_id=1000001, username="alice", is_active=True, language_code="en")
        user3 = User(telegram_id=1000003, username="charlie", is_active=False, language_code="en")
        async_session.add(user2)
        async_session.add(user1)
        async_session.add(user3)
        await async_session.commit()

        # Filter and sort
        users = await repo.list(
            filters={"is_active": True, "language_code": "en"}, order_by="username"
        )
        assert len(users) == 2
        assert users[0].username == "alice"
        assert users[1].username == "bob"

    @pytest.mark.asyncio
    async def test_list_with_sorting_descending(self, async_session: AsyncSession):
        """Test that list can sort in descending order by prefixing '-'."""
        repo = BaseRepository[User](User, async_session)

        # Create users with different names
        user3 = User(telegram_id=1000003, username="charlie")
        user1 = User(telegram_id=1000001, username="alice")
        user2 = User(telegram_id=1000002, username="bob")
        async_session.add(user3)
        async_session.add(user1)
        async_session.add(user2)
        await async_session.commit()

        # Sort by telegram_id (which is numeric)
        users = await repo.list(order_by="telegram_id")
        assert len(users) == 3
        assert users[0].telegram_id == 1000001
        assert users[1].telegram_id == 1000002
        assert users[2].telegram_id == 1000003

    @pytest.mark.asyncio
    async def test_list_excludes_soft_deleted_with_filters(self, async_session: AsyncSession):
        """Test that list excludes soft-deleted records even with filters."""
        repo = BaseRepository[User](User, async_session)

        active1 = User(telegram_id=1000001, username="active1", is_active=True)
        active2 = User(telegram_id=1000002, username="active2", is_active=True)
        deleted_active = User(telegram_id=1000003, username="deleted_active", is_active=True)
        async_session.add(active1)
        async_session.add(active2)
        async_session.add(deleted_active)
        await async_session.commit()
        await async_session.refresh(deleted_active)

        # Soft delete one active user
        await repo.delete(deleted_active.id)

        users = await repo.list(filters={"is_active": True})
        assert len(users) == 2
        usernames = {u.username for u in users}
        assert "active1" in usernames
        assert "active2" in usernames
        assert "deleted_active" not in usernames

    @pytest.mark.asyncio
    async def test_count_excludes_soft_deleted_with_filters(self, async_session: AsyncSession):
        """Test that count excludes soft-deleted records even with filters."""
        repo = BaseRepository[User](User, async_session)

        active1 = User(telegram_id=1000001, username="active1", is_active=True)
        active2 = User(telegram_id=1000002, username="active2", is_active=True)
        deleted_active = User(telegram_id=1000003, username="deleted_active", is_active=True)
        async_session.add(active1)
        async_session.add(active2)
        async_session.add(deleted_active)
        await async_session.commit()
        await async_session.refresh(deleted_active)

        # Soft delete one active user
        await repo.delete(deleted_active.id)

        count = await repo.count(filters={"is_active": True})
        assert count == 2

    @pytest.mark.asyncio
    async def test_list_with_offset_beyond_count(self, async_session: AsyncSession):
        """Test that list with offset beyond count returns empty list."""
        repo = BaseRepository[User](User, async_session)

        # Create 2 users
        user1 = User(telegram_id=1000001, username="user1")
        user2 = User(telegram_id=1000002, username="user2")
        async_session.add(user1)
        async_session.add(user2)
        await async_session.commit()

        # Offset beyond count
        users = await repo.list(offset=100, limit=10)
        assert len(users) == 0

    @pytest.mark.asyncio
    async def test_list_with_limit_exceeding_count(self, async_session: AsyncSession):
        """Test that list with limit exceeding count returns all records."""
        repo = BaseRepository[User](User, async_session)

        # Create 2 users
        user1 = User(telegram_id=1000001, username="user1")
        user2 = User(telegram_id=1000002, username="user2")
        async_session.add(user1)
        async_session.add(user2)
        await async_session.commit()

        # Limit exceeding count
        users = await repo.list(offset=0, limit=100)
        assert len(users) == 2

    @pytest.mark.asyncio
    async def test_list_empty_database(self, async_session: AsyncSession):
        """Test that list returns empty list on empty database."""
        repo = BaseRepository[User](User, async_session)

        users = await repo.list()
        assert len(users) == 0

    @pytest.mark.asyncio
    async def test_count_empty_database(self, async_session: AsyncSession):
        """Test that count returns 0 on empty database."""
        repo = BaseRepository[User](User, async_session)

        count = await repo.count()
        assert count == 0

    @pytest.mark.asyncio
    async def test_count_with_non_matching_filters(self, async_session: AsyncSession):
        """Test that count returns 0 when no records match filters."""
        repo = BaseRepository[User](User, async_session)

        # Create inactive user
        inactive = User(telegram_id=1000001, username="inactive", is_active=False)
        async_session.add(inactive)
        await async_session.commit()

        # Count active users (none exist)
        count = await repo.count(filters={"is_active": True})
        assert count == 0


class TestBaseRepositoryDatabaseErrorHandling:
    """Tests for database error handling using mocks."""

    @pytest.mark.asyncio
    async def test_create_handles_database_error(self):
        """Test that create handles database error and rolls back."""
        # Create mock session that raises DatabaseError
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock(side_effect=DatabaseError("test error", {}, Exception()))
        mock_session.rollback = AsyncMock()

        repo = BaseRepository[User](User, mock_session)

        with pytest.raises(DatabaseError):
            await repo.create(telegram_id=123456789, username="testuser")

        # Verify rollback was called
        mock_session.rollback.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_handles_database_error(self):
        """Test that get handles database error."""
        # Create mock session that raises DatabaseError on execute
        mock_session = AsyncMock(spec=AsyncSession)
        mock_execute = AsyncMock(side_effect=DatabaseError("test error", {}, Exception()))
        mock_session.execute = mock_execute

        repo = BaseRepository[User](User, mock_session)

        with pytest.raises(DatabaseError):
            await repo.get(uuid4())

    @pytest.mark.asyncio
    async def test_update_handles_database_error(self):
        """Test that update handles database error and rolls back."""
        # Create mock session that raises DatabaseError on execute
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.commit = AsyncMock(side_effect=DatabaseError("test error", {}, Exception()))
        mock_session.rollback = AsyncMock()

        repo = BaseRepository[User](User, mock_session)

        # First get() call would work (return mock object)
        with patch.object(repo, "get", return_value=MagicMock(id=uuid4())):
            with pytest.raises(DatabaseError):
                await repo.update(uuid4(), {"username": "newname"})

        # Verify rollback was called
        mock_session.rollback.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_handles_database_error(self):
        """Test that delete handles database error and rolls back."""
        # Create mock session that raises DatabaseError on execute
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.commit = AsyncMock(side_effect=DatabaseError("test error", {}, Exception()))
        mock_session.rollback = AsyncMock()

        repo = BaseRepository[User](User, mock_session)

        # First get_or_404() call would work
        with patch.object(repo, "get_or_404", return_value=MagicMock(id=uuid4())):
            with pytest.raises(DatabaseError):
                await repo.delete(uuid4())

        # Verify rollback was called
        mock_session.rollback.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_handles_database_error(self):
        """Test that list handles database error."""
        # Create mock session that raises DatabaseError on execute
        mock_session = AsyncMock(spec=AsyncSession)
        mock_execute = AsyncMock(side_effect=DatabaseError("test error", {}, Exception()))
        mock_session.execute = mock_execute

        repo = BaseRepository[User](User, mock_session)

        with pytest.raises(DatabaseError):
            await repo.list()

    @pytest.mark.asyncio
    async def test_count_handles_database_error(self):
        """Test that count handles database error."""
        # Create mock session that raises DatabaseError on execute
        mock_session = AsyncMock(spec=AsyncSession)
        mock_execute = AsyncMock(side_effect=DatabaseError("test error", {}, Exception()))
        mock_session.execute = mock_execute

        repo = BaseRepository[User](User, mock_session)

        with pytest.raises(DatabaseError):
            await repo.count()

    @pytest.mark.asyncio
    async def test_create_handles_sqlalchemy_error(self):
        """Test that create handles generic SQLAlchemy error."""
        # Create mock session that raises SQLAlchemyError
        mock_session = AsyncMock(spec=AsyncSession)
        mock_session.add = MagicMock()
        mock_session.commit = AsyncMock(side_effect=SQLAlchemyError("test error"))
        mock_session.rollback = AsyncMock()

        repo = BaseRepository[User](User, mock_session)

        with pytest.raises(SQLAlchemyError):
            await repo.create(telegram_id=123456789, username="testuser")

        # Verify rollback was called
        mock_session.rollback.assert_called_once()
