from unittest.mock import patch

from sqlmodel import Session
from atropos.db import engine

from atropos.api.models.task import Task
from atropos.api.services.create_record import CreateRecord
from atropos.api.services.handle_process_data import HandleProcessData
from atropos.api.services.get_record_by_id import GetRecordById


@patch("atropos.api.services.handle_process_data.sleep", return_value=None)
def test_handle_process_data_transitions_task_status(mock_sleep):

    # We don't use the db_session fixture here because our handler, as a celery task
    # needs to run it's own session (so wrapping everything in a transaction won't work)
    with Session(engine) as session:
        task = CreateRecord()(Task(type="data-processing"), session)

    handler = HandleProcessData()
    handler(task.id, data={"file_url": "https://example.com/file.csv"})

    with Session(engine) as session:
        updated_task = GetRecordById()(Task, task.id, session)
        assert updated_task.status == "succeeded"
        assert updated_task.download_url == "https://example.com/download_link"

    # Delete side effects because we aren't using the db_session fixture
    with Session(engine) as session:
        session.delete(updated_task)
        session.commit()

    # Optionally clean up (not necessary with test DB reset)
