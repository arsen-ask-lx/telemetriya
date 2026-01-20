"""Base repository with generic CRUD operations.

Note: Generic T doesn't know about 'id' attribute from UUIDMixin,
so we use type: ignore[attr-defined] where needed.
"""

import logging
from datetime import datetime, timezone
from typing import Any, Generic, List, Optional, TypeVar, Union
from uuid import UUID

from pydantic import ValidationError
from sqlalchemy import select, update, delete as sql_delete, func
from sqlalchemy.exc import DatabaseError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.db.mixins import SoftDeleteMixin

logger = logging.getLogger(__name__)

T = TypeVar("T", bound=DeclarativeBase)


class BaseRepository(Generic[T]):
    """Generic base repository with CRUD operations.

    Provides standard create, read, update, delete, list, and count operations
    for any SQLAlchemy model. Supports soft delete if the model has deleted_at field.

    Attributes:
        model: The SQLAlchemy model class
        session: Async database session
    """

    def __init__(self, model: type[T], session: AsyncSession) -> None:
        """Initialize repository with model and session.

        Args:
            model: SQLAlchemy model class
            session: Async database session
        """
        self.model = model
        self.session = session

    async def create(self, **kwargs: Any) -> T:
        """Create a new model instance.

        Args:
            **kwargs: Model field values

        Returns:
            Created model instance with ID

        Raises:
            DatabaseError: If database operation fails
        """
        try:
            instance = self.model(**kwargs)
            self.session.add(instance)
            await self.session.commit()
            await self.session.refresh(instance)

            logger.debug(f"Created {self.model.__name__} with id={instance.id}")  # type: ignore[attr-defined]

            return instance

        except (SQLAlchemyError, DatabaseError) as e:
            await self.session.rollback()
            logger.error(f"Error creating {self.model.__name__}: {e}")
            raise

    async def get(self, id: UUID) -> Optional[T]:
        """Get model instance by ID.

        Args:
            id: UUID of the instance

        Returns:
            Model instance or None if not found or soft-deleted
        """
        try:
            stmt = select(self.model).where(getattr(self.model, "id") == id)  # type: ignore[attr-defined]
            # Exclude soft-deleted records if model has SoftDeleteMixin
            if issubclass(self.model, SoftDeleteMixin):
                stmt = stmt.where(self.model.deleted_at.is_(None))

            result = await self.session.execute(stmt)
            instance = result.scalar_one_or_none()

            if instance:
                logger.debug(f"Retrieved {self.model.__name__} with id={id}")
            else:
                logger.debug(f"{self.model.__name__} with id={id} not found")

            return instance

        except (SQLAlchemyError, DatabaseError) as e:
            logger.error(f"Error retrieving {self.model.__name__} with id={id}: {e}")
            raise

    async def get_or_404(self, id: UUID) -> T:
        """Get model instance by ID or raise error.

        Args:
            id: UUID of the instance

        Returns:
            Model instance

        Raises:
            ValueError: If instance not found
        """
        instance = await self.get(id)

        if instance is None:
            raise ValueError(f"{self.model.__name__} with id={id} not found")

        return instance

    async def update(self, id: UUID, updates: dict[str, Any]) -> T:
        """Update model instance.

        Args:
            id: UUID of the instance
            updates: Dictionary of field values to update

        Returns:
            Updated model instance

        Raises:
            ValueError: If instance not found
            DatabaseError: If database operation fails
        """
        try:
            instance = await self.get_or_404(id)

            # Build update statement
            stmt = (
                update(self.model)
                .where(self.model.id == id)  # type: ignore[attr-defined]
                .values(**updates)
                .returning(self.model)
            )

            # Exclude soft-deleted records if model has SoftDeleteMixin
            if issubclass(self.model, SoftDeleteMixin):
                stmt = stmt.where(self.model.deleted_at.is_(None))

            result = await self.session.execute(stmt)
            updated_instance = result.scalar_one()
            await self.session.commit()
            await self.session.refresh(updated_instance)

            logger.debug(f"Updated {self.model.__name__} with id={id}")

            return updated_instance

        except ValueError:
            raise
        except (SQLAlchemyError, DatabaseError) as e:
            await self.session.rollback()
            logger.error(f"Error updating {self.model.__name__} with id={id}: {e}")
            raise

    async def delete(self, id: UUID) -> None:
        """Delete model instance (soft delete if supported).

        Args:
            id: UUID of the instance

        Raises:
            ValueError: If instance not found
            DatabaseError: If database operation fails
        """
        try:
            instance = await self.get_or_404(id)

            # Use soft delete if model has SoftDeleteMixin
            if issubclass(self.model, SoftDeleteMixin):
                stmt = (
                    update(self.model)
                    .where(self.model.id == id)  # type: ignore[attr-defined]
                    .values(deleted_at=datetime.now(timezone.utc))
                )
                await self.session.execute(stmt)
                await self.session.commit()
                logger.debug(f"Soft deleted {self.model.__name__} with id={id}")
            else:
                # Hard delete
                stmt = sql_delete(self.model).where(self.model.id == id)  # type: ignore[attr-defined]
                await self.session.execute(stmt)
                await self.session.commit()
                logger.debug(f"Hard deleted {self.model.__name__} with id={id}")

        except ValueError:
            raise
        except (SQLAlchemyError, DatabaseError) as e:
            await self.session.rollback()
            logger.error(f"Error deleting {self.model.__name__} with id={id}: {e}")
            raise

    async def list(
        self,
        offset: int = 0,
        limit: int = 100,
        filters: dict[str, Any] | None = None,
        order_by: str | None = None,
    ) -> List[T]:
        """List model instances with pagination, filtering, and sorting.

        Args:
            offset: Number of items to skip (must be >= 0)
            limit: Maximum number of items to return (must be > 0)
            filters: Dictionary of field filters (e.g., {"is_active": True})
            order_by: Field name to sort by (e.g., "created_at", "username")

        Returns:
            List of model instances

        Raises:
            ValueError: If offset or limit are invalid
            DatabaseError: If database operation fails
        """
        # Validate pagination parameters
        if offset < 0:
            raise ValueError(f"offset must be >= 0, got {offset}")
        if limit <= 0:
            raise ValueError(f"limit must be > 0, got {limit}")
        if limit > 1000:
            raise ValueError(f"limit cannot exceed 1000, got {limit}")

        try:
            stmt = select(self.model)

            # Apply filters
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key):
                        stmt = stmt.where(getattr(self.model, key) == value)

            # Exclude soft-deleted records if model has SoftDeleteMixin
            if issubclass(self.model, SoftDeleteMixin):
                stmt = stmt.where(self.model.deleted_at.is_(None))

            # Apply sorting
            if order_by:
                if hasattr(self.model, order_by):
                    order_field = getattr(self.model, order_by)
                    stmt = stmt.order_by(order_field)
                else:
                    logger.warning(f"Invalid order_by field '{order_by}' for {self.model.__name__}")

            # Apply pagination
            stmt = stmt.offset(offset).limit(limit)

            result = await self.session.execute(stmt)
            instances = list(result.scalars().all())

            logger.debug(
                f"Listed {len(instances)} {self.model.__name__} instances "
                f"(offset={offset}, limit={limit}, filters={filters}, order_by={order_by})"
            )

            return instances

        except (SQLAlchemyError, DatabaseError) as e:
            logger.error(f"Error listing {self.model.__name__} instances: {e}")
            raise

    async def count(self, filters: dict[str, Any] | None = None) -> int:
        """Count model instances with optional filtering.

        Args:
            filters: Dictionary of field filters (e.g., {"is_active": True})

        Returns:
            Number of matching instances

        Raises:
            DatabaseError: If database operation fails
        """
        try:
            stmt = select(func.count(self.model.id))  # type: ignore[attr-defined]

            # Apply filters
            if filters:
                for key, value in filters.items():
                    if hasattr(self.model, key):
                        stmt = stmt.where(getattr(self.model, key) == value)

            # Exclude soft-deleted records if model has SoftDeleteMixin
            if issubclass(self.model, SoftDeleteMixin):
                stmt = stmt.where(self.model.deleted_at.is_(None))

            result = await self.session.execute(stmt)
            count = result.scalar() or 0

            logger.debug(f"Counted {count} {self.model.__name__} instances (filters={filters})")

            return count

        except (SQLAlchemyError, DatabaseError) as e:
            logger.error(f"Error counting {self.model.__name__} instances: {e}")
            raise
