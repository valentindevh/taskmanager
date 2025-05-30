from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict

class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 1
    status: TaskStatus

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[int] = None
    status: Optional[TaskStatus] = None

class TaskInDB(TaskBase):
    id: int
    status: TaskStatus
    created_at: datetime
    updated_at: Optional[datetime]
    model_config = ConfigDict(from_attributes=True)


class TaskLog(BaseModel):
    id: int
    task_id: int
    status: TaskStatus
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
    # class Config:
        # orm_mode = True