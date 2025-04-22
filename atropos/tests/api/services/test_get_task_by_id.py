import pytest
from atropos.api.models.task import Task
from atropos.api.services.get_task_by_id import GetTaskById
from atropos.api.services.create_record import CreateRecord
from atropos.api.services.get_record_by_id import RecordNotFoundError


def test_get_task_by_id_returns_task(db_session):
    task = Task(type="data-processing")
    CreateRecord()(task, db_session)

    result = GetTaskById()(task.id, db_session)

    assert result.id == task.id
    assert result.type == "data-processing"


def test_get_task_by_id_raises_not_found(db_session):
    with pytest.raises(RecordNotFoundError):
        GetTaskById()("nonexistent-id", db_session)
