from typing import List, Optional
import uuid

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.models.task import Task
from backend.app.repositories.task import TaskRepository


class TaskService:
    def __init__(self, db: AsyncSession):
        self.task_repo = TaskRepository(db)

    async def get_user_tasks(
        self, owner_id: uuid.UUID, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        """
        Retrieve tasks for a specific user.
        """
        return await self.task_repo.get_multi_by_owner(
            owner_id=str(owner_id), skip=skip, limit=limit
        )

    async def create_task(self, owner_id: uuid.UUID, task_in: dict) -> Task:
        """
        Create a new task for a user.
        """
        task_data = task_in.copy()
        task_data["owner_id"] = owner_id
        return await self.task_repo.create(obj_in=task_data)

    async def get_task_with_auth(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Task:
        """
        Fetch a task and verify ownership.
        """
        task = await self.task_repo.get(task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
            )
        
        if task.owner_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions to access this task",
            )
        return task

    async def update_task(
        self, task_id: uuid.UUID, user_id: uuid.UUID, task_in: dict
    ) -> Task:
        """
        Update a task after verifying ownership.
        """
        task = await self.get_task_with_auth(task_id, user_id)
        return await self.task_repo.update(db_obj=task, obj_in=task_in)

    async def delete_task(self, task_id: uuid.UUID, user_id: uuid.UUID) -> Task:
        """
        Delete a task after verifying ownership.
        """
        task = await self.get_task_with_auth(task_id, user_id)
        return await self.task_repo.remove(id=task_id)
