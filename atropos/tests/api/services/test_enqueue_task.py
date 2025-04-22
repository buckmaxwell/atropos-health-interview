import os

from redis import Redis
from atropos.api.services.enqueue_task import EnqueueTask


TEST_TASK_QUEUE = "test:task:queue"


def get_redis_client():
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis = Redis.from_url(redis_url)
    return redis


def clear_test_test_queue():
    redis_client = get_redis_client()
    redis_client.delete(TEST_TASK_QUEUE)


def test_enqueue_task_adds_task_to_redis():
    clear_test_test_queue()

    task_id = "test_task_id"
    task_type = "test_task_type"
    data = {"key": "value"}

    enqueue_task_service = EnqueueTask(task_queue=TEST_TASK_QUEUE)
    enqueue_task_service(task_id, task_type, data)

    redis_client = get_redis_client()

    queue_length = redis_client.llen(TEST_TASK_QUEUE)

    assert queue_length == 1

    clear_test_test_queue()
