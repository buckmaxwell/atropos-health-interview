from pydantic import BaseModel
from typing import Literal


class TaskResponseLinks(BaseModel):
    status: str
    result: str


class TaskResponse(BaseModel):
    task_id: str
    status: Literal["pending"]
    type: str
    links: TaskResponseLinks

    @classmethod
    def from_task(cls, task_id: str, task_type: str) -> "TaskResponse":
        return cls(
            task_id=task_id,
            status="pending",
            type=task_type,
            links=TaskResponseLinks(
                status=f"/tasks/{task_id}/status", result=f"/tasks/{task_id}/result"
            ),
        )
