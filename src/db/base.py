"""Base declarative class for SQLAlchemy models."""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models.

    This is the standard SQLAlchemy 2.0 declarative base.
    """

    pass
