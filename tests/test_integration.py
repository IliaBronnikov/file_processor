import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app, get_db
from src.sql_app.database import Base
from src.sql_app.repo import create_task


@pytest.fixture()
def test_db():
    try:
        engine = create_engine(
            "sqlite:///./tests/test.db", connect_args={"check_same_thread": False}
        )
        TestingSessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )
        Base.metadata.create_all(bind=engine)
        db = TestingSessionLocal()
        yield db
        Base.metadata.drop_all(bind=engine)
    finally:
        db.close()


@pytest.fixture()
def client():
    return TestClient(app)

app.dependency_overrides[get_db] = test_db

def test_process(client):
    response = client.post(
        "/",
        files={"file": "test.xlsx"},
        headers={"Authorization": "Bearer footokenbar"},
    )

    assert response.status_code == 200
    assert response.json()["task_id"] != None
    assert response.json()["completed_at"] == None
    assert response.json()["status"] == "created"


def test_status_authorization(test_db, client):
    create_task(db=test_db, task_id="test_task")

    response = client.get(
        "/status",
        params={"task_id": "test_task"},
        headers={"Authorization": "Bearer footokenbar"},
    )

    assert response.status_code == 200
    assert response.json()["status"] == "created"


def test_status_not_authorization(test_db):
    create_task(db=test_db, task_id="test_task")

    response = client.get(
        "/status",
        params={"task_id": "test_task"},
    )

    assert response.status_code == 401
