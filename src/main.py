from fastapi import FastAPI, UploadFile, File, Depends
from sqlalchemy.orm import Session

from src.services import save_file
from src.sql_app import models
from src.sql_app import schemas
from src.sql_app.database import SessionLocal, engine
from src.sql_app.repo import create_task, get_task
from src.tasks import process_file
from fastapi.security import OAuth2PasswordBearer

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/", response_model=schemas.Task)
async def process(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    file_path = await save_file(file=file)
    celery_task = process_file.s(file_path)
    celery_task.freeze()
    task = create_task(db=db, task_id=celery_task.id)

    celery_task.delay()
    return schemas.Task.from_orm(task)


@app.get("/status", response_model=schemas.Task)
async def status(
    task_id: str, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> schemas.Task:
    task = get_task(db=db, task_id=task_id)
    return schemas.Task.from_orm(task)
