import json
import os

from redis import Redis
from atropos.api.services.base import Service


class EnqueueTask(Service):
    def __init__(self):
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self.redis = Redis.from_url(redis_url)

    def __call__(self, task_id: str, task_type: str, data: dict):
        payload = {"task_id": task_id, "type": task_type, "data": data}
        self.redis.rpush("task:queue", json.dumps(payload))
