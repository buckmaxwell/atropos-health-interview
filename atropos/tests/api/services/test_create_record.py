from sqlmodel import Session, select
from atropos.db import engine

from atropos.api.models.task import Task

from atropos.api.services.create_record import CreateRecord

TEST_TASK_TYPE = "test_task_type"


def clear_test_tasks():
    with Session(engine) as session:
        session.exec(Task.__table__.delete().where(Task.type == TEST_TASK_TYPE))
        session.commit()


def test_create_record_creates_record_in_db():
    clear_test_tasks()

    create_record = CreateRecord()
    create_record(Task(type=TEST_TASK_TYPE))

    with Session(engine) as session:
        task = session.exec(select(Task).where(Task.type == TEST_TASK_TYPE)).first()
        assert task is not None
        assert task.type == TEST_TASK_TYPE
        assert task.id is not None

    clear_test_tasks()
