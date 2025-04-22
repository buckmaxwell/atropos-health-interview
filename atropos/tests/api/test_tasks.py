from unittest.mock import patch, MagicMock
from atropos.api.models.task import Task


@patch("atropos.api.tasks.CreateTaskRecord")
@patch("atropos.api.tasks.EnqueueTask")
def test_post_tasks_creates_task_and_queues_it(
    mock_enqueue_cls, mock_create_cls, client
):
    task = Task(id="abc123", type="data-processing")
    mock_create = MagicMock(return_value=task)
    mock_enqueue = MagicMock()

    mock_create_cls.return_value = mock_create
    mock_enqueue_cls.return_value = mock_enqueue

    response = client.post(
        "/tasks",
        json={
            "type": "data-processing",
            "data": {"file_url": "https://example.com/my.csv"},
        },
    )

    assert response.status_code == 202
    body = response.json()
    assert body["task_id"] == "abc123"
    assert body["status"] == "pending"
    assert "status" in body["links"]
    assert "result" in body["links"]

    mock_create.assert_called_once()
    mock_enqueue.assert_called_once()
