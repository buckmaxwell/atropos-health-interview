from typing import Any
from atropos.api.models.task import Task
from atropos.api.errors import RecordNotFoundError


class FakeCreateTaskRecord:
    def __init__(self, return_value: Task):
        self.return_value = return_value
        self.called_with = []

    def __call__(self, task_type: str, session: Any) -> Task:
        self.called_with.append((task_type, session))
        return self.return_value


class FakeDispatchTask:
    def __init__(self):
        self.called_with = []

    def __call__(self, task_id: str, task_type: str, data: dict):
        self.called_with.append((task_id, task_type, data))


class FakeGetTaskById:
    def __init__(self, task: Task):
        self.task = task
        self.called_with = []

    def __call__(self, task_id: str, session: Any) -> Task:
        self.called_with.append((task_id, session))
        return self.task


class FakeGetTaskByIdRaises:
    def __init__(self):
        self.called_with = []

    def __call__(self, task_id: str, session: Any):
        self.called_with.append((task_id, session))
        raise RecordNotFoundError("not found")
