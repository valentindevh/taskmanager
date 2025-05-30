import asyncio
from typing import Any

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.task_repository import TaskRepository
from app.models.task import TaskStatus

async def process_task_in_background(
    task_id: int,
    background_tasks: BackgroundTasks,
    db: AsyncSession
) -> None:
    background_tasks.add_task(process_task, task_id, db)

async def process_task(task_id: int, db: AsyncSession) -> None:
    task_repo = TaskRepository(db)
    task = await task_repo.get_task_by_id(task_id)
    if not task:
        return

    await task_repo.update_task_status(task_id, TaskStatus.IN_PROGRESS)
    
    # Simulate long-running task
    await asyncio.sleep(5)
    
    await task_repo.update_task_status(task_id, TaskStatus.COMPLETED)