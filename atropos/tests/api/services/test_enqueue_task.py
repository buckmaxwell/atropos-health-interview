from unittest.mock import patch
from atropos.api.services.dispatch_task import DispatchTask


@patch("atropos.api.services.dispatch_task.dispatch_task_helper")
def test_dispatch_task_calls_celery_delay(mock_dispatch_task):
    task_id = "test-task-id"
    task_type = "data-processing"
    data = {"foo": "bar"}

    dispatcher = DispatchTask()
    dispatcher(task_id, task_type, data)

    mock_dispatch_task.delay.assert_called_once_with(task_id, task_type, data)
