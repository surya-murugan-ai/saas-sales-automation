from celery import Celery
from app.config import settings

# Initialize Celery app for background tasks
celery_app = Celery(
    "sales_automation",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
    include=["app.tasks.leads"]
)

# Configure Celery settings
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)