from unittest.mock import patch, create_autospec

from atropos.api.models.task import Task
from atropos.api.services.get_task_by_id import GetTaskById


from atropos.tests.fakes.task_services import (
    FakeCreateTaskRecord,
    FakeDispatchTask,
    FakeGetTaskById,
    FakeGetTaskByIdRaises,
)


@patch("atropos.api.tasks.DispatchTask")
@patch("atropos.api.tasks.CreateTaskRecord")
def test_post_tasks_creates_task_and_dispatches(
    mock_create_cls, mock_dispatch_cls, client
):
    task = Task(
        id="abc123",
        type="data-processing",
        status="pending",
        download_url=None,
    )

    fake_create = FakeCreateTaskRecord(return_value=task)
    fake_dispatch = FakeDispatchTask()

    mock_create_cls.return_value = fake_create
    mock_dispatch_cls.return_value = fake_dispatch

    response = client.post(
        "/tasks",
        json={
            "type": "data-processing",
            "data": {"file_url": "https://example.com/my.csv"},
        },
    )

    # Validate response
    assert response.status_code == 202
    body = response.json()
    assert body["task_id"] == "abc123"
    assert body["status"] == "pending"
    assert body["type"] == "data-processing"
    assert "download_url" in body

    # Validate fake services were used
    assert len(fake_create.called_with) == 1
    assert fake_create.called_with[0][0] == "data-processing"
    assert fake_create.called_with[0][1] is not None

    assert len(fake_dispatch.called_with) == 1
    assert fake_dispatch.called_with[0] == (
        "abc123",
        "data-processing",
        {"file_url": "https://example.com/my.csv"},
    )


@patch("atropos.api.tasks.GetTaskById", spec=GetTaskById)
def test_get_existing_task_returns_task(mock_get_cls, client):
    task = Task(
        id="abc123",
        type="data-processing",
        status="succeeded",
        download_url="https://example.com/file.zip",
    )

    # Safe autospec on the class (no instance=True)
    mock_get = create_autospec(GetTaskById)
    mock_get.side_effect = lambda task_id: task  # simulate __call__
    mock_get_cls.return_value = mock_get

    response = client.get("/tasks/abc123")

    assert response.status_code == 200
    body = response.json()
    assert body["task_id"] == "abc123"
    assert body["status"] == "succeeded"
    assert body["download_url"] == "https://example.com/file.zip"
    assert body["type"] == "data-processing"

    mock_get.assert_called_once_with("abc123")


@patch("atropos.api.tasks.GetTaskById")
def test_get_existing_task_returns_task(mock_get_cls, client):
    # Real task to be returned
    task = Task(
        id="abc123",
        type="data-processing",
        status="succeeded",
        download_url="https://example.com/file.zip",
    )

    # Use a real fake instead of a mock
    fake_service = FakeGetTaskById(task)
    mock_get_cls.return_value = fake_service

    response = client.get("/tasks/abc123")

    assert response.status_code == 200
    body = response.json()
    assert body["task_id"] == "abc123"
    assert body["status"] == "succeeded"
    assert body["download_url"] == "https://example.com/file.zip"
    assert body["type"] == "data-processing"

    # Verify the call
    assert len(fake_service.called_with) == 1
    called_task_id, called_session = fake_service.called_with[0]
    assert called_task_id == "abc123"
    assert called_session is not None


@patch("atropos.api.tasks.GetTaskById")
def test_get_nonexistent_task_returns_404(mock_get_cls, client):
    fake_service = FakeGetTaskByIdRaises()
    mock_get_cls.return_value = fake_service

    response = client.get("/tasks/not-a-real-id")

    assert response.status_code == 404
    body = response.json()
    assert body["error"] == "not found"

    # Validate the call happened
    assert len(fake_service.called_with) == 1
    called_task_id, called_session = fake_service.called_with[0]
    assert called_task_id == "not-a-real-id"
    assert called_session is not None


def test_post_with_invalid_task_type_returns_422(client):
    response = client.post(
        "/tasks",
        json={"type": "invalid-type", "data": {"foo": "bar"}},
    )

    assert response.status_code == 422
    assert (
        response.json()["detail"][0]["msg"] == "Unsupported task type: 'invalid-type'"
    )
