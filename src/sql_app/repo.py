from sqlalchemy.orm import Session

from . import models


def get_task(db: Session, task_id: str):
    return db.query(models.Task).filter(models.Task.task_id == task_id).first()


def create_task(db: Session, task_id: str) -> object:
    db_task = models.Task(task_id=task_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task: models.Task, **fields) -> models.Task:
    for field, value in fields.items():
        setattr(task, field, value)
    db.commit()
    return task
