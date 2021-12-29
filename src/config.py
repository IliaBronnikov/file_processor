import os
import tempfile

ACCESS_TOKEN = os.getenv("ACCESS_TOKEN", "token")

DB_NAME = os.getenv("DB_NAME", "postgres")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "sqlite:///./sql_app.db")

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://localhost:5672")

TEMP_DIR = tempfile.gettempdir()
