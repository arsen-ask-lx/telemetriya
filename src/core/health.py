"""Health check utilities."""

from sqlalchemy import text


async def check_db_health() -> bool:
    """Check if database connection is healthy.

    Returns:
        True if database is accessible, False otherwise.
    """
    from src.db.session import engine as db_engine

    if db_engine is None:
        return False

    try:
        async with db_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return True
    except Exception:
        return False
