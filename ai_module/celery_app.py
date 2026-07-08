import os
from celery import Celery

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

app = Celery(
    "ai_processor",
    broker=redis_url,
    include=["ai_worker"]
)

app.conf.update(
    task_serializer="json",
    accept_content=["json"],  
    worker_prefetch_multiplier=1
)