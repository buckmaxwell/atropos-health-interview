from unittest.mock import patch, MagicMock
from atropos.api.services.create_task_record import CreateTaskRecord
from atropos.api.errors import InvalidTaskTypeError
from atropos.api.models.task import Task
import pytest

TEST_TASK_TYPE = "test_task_type"


class FakeTaskType:
    def __init__(self):
        self.type = TEST_TASK_TYPE


@patch("atropos.api.services.create_task_record.ALL_TASK_TYPES", new=(FakeTaskType,))
@patch("atropos.api.services.create_task_record.CreateRecord")
def test_create_task_record_delegates_to_create_record(mock_create_record_cls):
    mock_create = MagicMock()
    mock_create_record_cls.return_value = mock_create

    expected_task = Task(type=TEST_TASK_TYPE)
    mock_create.return_value = expected_task

    mock_session = MagicMock()

    service = CreateTaskRecord(create_record=mock_create)
    result = service(TEST_TASK_TYPE, mock_session)

    mock_create.assert_called_once()
    called_task = mock_create.call_args[0][0]
    assert isinstance(called_task, Task)
    assert called_task.type == TEST_TASK_TYPE
    assert result == expected_task


@patch("atropos.api.services.create_task_record.ALL_TASK_TYPES", new=(FakeTaskType,))
def test_create_task_record_raises_on_invalid_task_type():
    mock_session = MagicMock()
    service = CreateTaskRecord()

    with pytest.raises(InvalidTaskTypeError) as exc:
        service("unsupported-task-type", mock_session)
