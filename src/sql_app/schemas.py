import datetime
from typing import Optional

from pydantic import BaseModel

from src.sql_app.models import TaskStatusEnum


class Task(BaseModel):
    task_id: str
    status: TaskStatusEnum
    created_at: datetime.datetime
    completed_at: Optional[datetime.datetime] = None
    task_result: Optional[str] = None

    class Config:
        orm_mode = True
