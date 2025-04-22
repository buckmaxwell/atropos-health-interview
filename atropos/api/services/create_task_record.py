from atropos.api.models.task import Task
from atropos.api.services.base import Service
from atropos.api.services.create_record import CreateRecord


class CreateTaskRecord(Service):
    def __call__(self, task_type: str) -> Task:
        task = Task(type=task_type)
        return CreateRecord()(task)
