import json
import os

from redis import Redis
from atropos.api.services.base import Service


class EnqueueTask(Service):
    def __init__(self, task_queue="task:queue"):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis = Redis.from_url(redis_url)
        self.task_queue = task_queue

    def __call__(self, task_id: str, task_type: str, data: dict):
        payload = {"task_id": task_id, "type": task_type, "data": data}
        self.redis.rpush(self.task_queue, json.dumps(payload))
