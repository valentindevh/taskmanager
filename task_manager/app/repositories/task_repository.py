from typing import List, Optional

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task, TaskLog, TaskStatus
from app.repositories.base import BaseRepository

class TaskRepository(BaseRepository[Task]):
    def __init__(self, db: AsyncSession):
        super().__init__(Task, db)

    async def create_task(self, title: str, description: str = None, priority: int = 1) -> Task:
        task = Task(title=title, description=description, priority=priority)
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        await self._log_task_status(task.id, TaskStatus.PENDING)
        return task

    async def get_task_by_id(self, task_id: int) -> Optional[Task]:
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        return result.scalars().first()

    async def get_all_tasks(
        self,
        skip: int = 0,
        limit: int = 100,
        title: str = None,
        status: str = None
    ) -> List[Task]:
        query = select(Task)
        if title:
            query = query.where(Task.title.contains(title))
        if status:
            query = query.where(Task.status == status)
        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        old_task = await self.get_task_by_id(task_id)
        if not old_task:
            return None

        if "status" in kwargs and kwargs["status"] != old_task.status:
            await self._log_task_status(task_id, kwargs["status"])

        await self.db.execute(update(Task).where(Task.id == task_id).values(**kwargs))
        await self.db.commit()
        return await self.get_task_by_id(task_id)

    async def update_task_status(self, task_id: int, status: TaskStatus) -> Optional[Task]:
        return await self.update_task(task_id, status=status)

    async def delete_task(self, task_id: int) -> bool:
        result = await self.db.execute(delete(Task).where(Task.id == task_id))
        await self.db.commit()
        return result.rowcount > 0

    async def _log_task_status(self, task_id: int, status: str) -> None:
        task_log = TaskLog(task_id=task_id, status=status)
        self.db.add(task_log)
        await self.db.commit()

    async def get_task_logs(self, task_id: int) -> List[TaskLog]:
        result = await self.db.execute(select(TaskLog).where(TaskLog.task_id == task_id))
        return result.scalars().all()