from sqlmodel import Session
from typing import Optional
from atropos.api.models.task import Task
from atropos.api.services.base import Service
from atropos.api.services.create_record import CreateRecord
from atropos.api.schemas.task_type import ALL_TASK_TYPES
from atropos.api.errors import InvalidTaskTypeError


class CreateTaskRecord(Service):
    def __init__(self, create_record: Optional[CreateRecord] = None):
        self.create_record = create_record or CreateRecord()

    def __call__(self, task_type: str, session: Session) -> Task:
        valid_task_types = {cls().type for cls in ALL_TASK_TYPES}

        if task_type not in valid_task_types:
            raise InvalidTaskTypeError(task_type, sorted(valid_task_types))

        task = Task(type=task_type)
        return self.create_record(task, session)
