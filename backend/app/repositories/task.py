from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.task import Task
from backend.app.repositories.base import BaseRepository


class TaskRepository(BaseRepository[Task]):
    def __init__(self, db: AsyncSession):
        super().__init__(Task, db)

    async def get_multi_by_owner(
        self, *, owner_id: str, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        """
        Fetch tasks belonging to a specific user with pagination.
        """
        query = (
            select(self.model)
            .where(self.model.owner_id == owner_id)
            .offset(skip)
            .limit(limit)
        )
        result = await self.db.execute(query)
        return list(result.scalars().all())
