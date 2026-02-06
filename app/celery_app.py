import os
from celery import Celery
from kombu import Queue

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery(
    "worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks.image_processing"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Priority Queue Scaffolding
    task_default_queue="default",
    task_queues=(
        Queue("high_priority", routing_key="high_priority"),
        Queue("default", routing_key="default"),
        Queue("low_priority", routing_key="low_priority"),
    ),
)
