from typing import AsyncGenerator
from backend.app.db.session import SessionLocal
from sqlalchemy.ext.asyncio import AsyncSession

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for getting async database sessions.
    Ensures session is closed after the request is finished.
    """
    async with SessionLocal() as session:
        yield session
