import pytest
from atropos.api.models.task import Task
from atropos.api.services.get_record_by_id import GetRecordById, RecordNotFoundError
from atropos.api.services.create_record import CreateRecord


def test_get_record_by_id_returns_task(db_session):
    task_id = "abc123"
    task = Task(id=task_id, type="data-processing")

    CreateRecord()(task, db_session)

    result = GetRecordById()(Task, task_id, db_session)

    assert result.id == task_id
    assert result.type == "data-processing"


def test_get_record_by_id_raises_not_found(db_session):
    with pytest.raises(RecordNotFoundError) as exc:
        GetRecordById()(Task, "nonexistent-id", db_session)

    assert "nonexistent-id" in str(exc.value)
