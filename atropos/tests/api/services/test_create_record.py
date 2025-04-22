from atropos.api.models.task import Task
from atropos.api.services.create_record import CreateRecord
from atropos.api.services.get_record_by_id import GetRecordById

TEST_TASK_TYPE = "test_task_type"


def test_create_record_creates_record_in_db(db_session):
    task = Task(type=TEST_TASK_TYPE)

    # Use session-aware services
    CreateRecord()(task, db_session)

    result = GetRecordById()(Task, task.id, db_session)

    assert result is not None
    assert result.id == task.id
    assert result.type == TEST_TASK_TYPE
