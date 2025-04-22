from atropos.api.services.base import Service
from atropos.api.schemas.task_type import ALL_TASK_TYPES, TaskType


class GetTaskTypes(Service):
    def __call__(self) -> list[TaskType]:
        return [task_type() for task_type in ALL_TASK_TYPES]
