import datetime

from celery import Celery

from src.config import CELERY_BROKER_URL
from src.services import parser_excel
from src.sql_app.database import SessionLocal
from src.sql_app.models import TaskStatusEnum
from src.sql_app.repo import get_task, update_task

celery_app = Celery("tasks", broker=CELERY_BROKER_URL)


@celery_app.task(bind=True)
def process_file(self, file_name: str):
    with SessionLocal() as db:
        task = get_task(db=db, task_id=self.request.id)

        update_task(db=db, task=task, status=TaskStatusEnum.processing)

        process_result = parser_excel(file_name)

        update_task(
            db=db,
            task=task,
            status=TaskStatusEnum.completed,
            completed_at=datetime.datetime.utcnow(),
            task_result=process_result,
        )
        return process_result
