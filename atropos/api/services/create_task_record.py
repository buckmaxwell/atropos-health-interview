from sqlmodel import Session
from atropos.db import engine

from atropos.api.models.task import Task
from atropos.api.services.base import Service


class CreateTaskRecord(Service):
    def __call__(self, task_type: str) -> Task:
        task = Task(type=task_type)
        with Session(engine) as session:
            session.add(task)
            session.commit()
            session.refresh(task)
        return task
