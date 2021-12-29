import datetime
import enum

from sqlalchemy import Column, Integer, String, DateTime, Enum

from .database import Base


class TaskStatusEnum(enum.Enum):
    created = "created"
    processing = "processing"
    completed = "completed"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True, default=None)
    status = Column(Enum(TaskStatusEnum), default=TaskStatusEnum.created)
    task_result = Column(String, default=None)
