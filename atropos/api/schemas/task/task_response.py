from pydantic import BaseModel
from typing import Literal, Optional
from atropos.api.models import Task as TaskRecord


class TaskResponse(BaseModel):
    task_id: str
    status: Literal["pending", "in-progress", "succeeded", "failed"]
    type: str
    download_url: Optional[str] = None

    @classmethod
    def from_task(cls, task: TaskRecord) -> "TaskResponse":
        return cls(
            task_id=task.id,
            status=task.status,
            type=task.type,
            download_url=task.download_url,
        )
