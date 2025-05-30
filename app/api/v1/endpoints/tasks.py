from typing import List, Optional

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import DatabaseSession
from app.schemas.task import TaskCreate, TaskInDB, TaskLog, TaskUpdate
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("/", response_model=TaskInDB, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    db: DatabaseSession,
) -> TaskInDB:
    task_service = TaskService(db)
    return await task_service.create_task(task_create)

@router.get("/", response_model=List[TaskInDB])
async def get_tasks(
    db: DatabaseSession,
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    status: Optional[str] = None,
    ) -> List[TaskInDB]:
    task_service = TaskService(db)
    return await task_service.get_tasks(skip, limit, title, status)

@router.get("/{task_id}", response_model=TaskInDB)
async def get_task(
    task_id: int,
    db: DatabaseSession,
) -> TaskInDB:
    task_service = TaskService(db)
    task = await task_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskInDB)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: DatabaseSession,
) -> TaskInDB:
    task_service = TaskService(db)
    task = await task_service.update_task(task_id, task_update)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    db: DatabaseSession,
) -> None:
    task_service = TaskService(db)
    success = await task_service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

@router.post("/{task_id}/process", response_model=TaskInDB)
async def process_task(
    task_id: int,
    background_tasks: BackgroundTasks,
    db: DatabaseSession,
) -> TaskInDB:
    task_service = TaskService(db)
    task = await task_service.process_task(task_id, background_tasks)
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.get("/{task_id}/logs", response_model=List[TaskLog])
async def get_task_logs(
    task_id: int,
    db: DatabaseSession,
) -> List[TaskLog]:
    task_service = TaskService(db)
    return await task_service.get_task_logs(task_id)