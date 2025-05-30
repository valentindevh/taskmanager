from typing import List, Optional

from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.background_tasks import process_task_in_background
from app.models.task import TaskStatus
from app.repositories.task_repository import TaskRepository
from app.schemas.task import TaskCreate, TaskInDB, TaskLog, TaskUpdate

class TaskService:
    def __init__(self, db: AsyncSession):
        self.repository = TaskRepository(db)

    async def create_task(self, task_create: TaskCreate) -> TaskInDB:
        task = await self.repository.create_task(
            title=task_create.title,
            description=task_create.description,
            priority=task_create.priority
        )
        return TaskInDB.from_orm(task)

    async def get_task(self, task_id: int) -> Optional[TaskInDB]:
        task = await self.repository.get_task_by_id(task_id)
        return TaskInDB.from_orm(task) if task else None

    async def get_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        title: str = None,
        status: str = None
    ) -> List[TaskInDB]:
        tasks = await self.repository.get_all_tasks(skip, limit, title, status)
        return [TaskInDB.from_orm(task) for task in tasks]

    async def update_task(
        self,
        task_id: int,
        task_update: TaskUpdate
    ) -> Optional[TaskInDB]:
        update_data = task_update.dict(exclude_unset=True)
        task = await self.repository.update_task(task_id, **update_data)
        return TaskInDB.from_orm(task) if task else None

    async def delete_task(self, task_id: int) -> bool:
        return await self.repository.delete_task(task_id)

    async def process_task(
        self,
        task_id: int,
        background_tasks: BackgroundTasks
    ) -> Optional[TaskInDB]:
        task = await self.repository.get_task_by_id(task_id)
        if not task:
            return None

        await process_task_in_background(task_id, background_tasks, self.repository.db)
        return TaskInDB.from_orm(task)

    async def get_task_logs(self, task_id: int) -> List[TaskLog]:
        logs = await self.repository.get_task_logs(task_id)
        return [TaskLog.from_orm(log) for log in logs]