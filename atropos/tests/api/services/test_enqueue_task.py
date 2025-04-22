from atropos.api.services.enqueue_task import EnqueueTask
from atropos.tests.conftest import (
    get_redis_client,
    TEST_TASK_QUEUE,
)


def test_enqueue_task_adds_task_to_redis():
    task_id = "test_task_id"
    task_type = "test_task_type"
    data = {"key": "value"}

    enqueue_task_service = EnqueueTask(task_queue=TEST_TASK_QUEUE)
    enqueue_task_service(task_id, task_type, data)

    redis_client = get_redis_client()
    queue_length = redis_client.llen(TEST_TASK_QUEUE)

    assert queue_length == 1
