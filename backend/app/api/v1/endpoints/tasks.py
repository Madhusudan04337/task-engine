import uuid
from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.app.api import deps
from backend.app.models.user import User
from backend.app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from backend.app.services.task import TaskService

router = APIRouter()


@router.get("/", response_model=List[TaskResponse])
async def read_tasks(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve tasks for the current user.
    """
    task_service = TaskService(db)
    return await task_service.get_user_tasks(
        owner_id=current_user.id, skip=skip, limit=limit
    )


@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_in: TaskCreate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Create a new task for the current user.
    """
    task_service = TaskService(db)
    return await task_service.create_task(
        owner_id=current_user.id, task_in=task_in.model_dump()
    )


@router.get("/{id}", response_model=TaskResponse)
async def read_task(
    id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Get a specific task by ID.
    """
    task_service = TaskService(db)
    return await task_service.get_task_with_auth(task_id=id, user_id=current_user.id)


@router.put("/{id}", response_model=TaskResponse)
async def update_task(
    id: uuid.UUID,
    task_in: TaskUpdate,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Update a task.
    """
    task_service = TaskService(db)
    return await task_service.update_task(
        task_id=id, user_id=current_user.id, task_in=task_in.model_dump(exclude_unset=True)
    )


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
):
    """
    Delete a task.
    """
    task_service = TaskService(db)
    await task_service.delete_task(task_id=id, user_id=current_user.id)
    return None
