from fastapi import APIRouter, status
from pydantic import BaseModel
from uuid import uuid4

router = APIRouter(prefix="/tasks", tags=["tasks"])

# temporary in-memory store
tasks = {}


class TaskRequest(BaseModel):
    type: str
    data: dict


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
def create_task(request: TaskRequest):
    task_id = str(uuid4())

    tasks[task_id] = {"status": "pending", "type": request.type, "data": request.data}

    return {
        "task_id": task_id,
        "status": "pending",
        "type": request.type,
        "links": {
            "status": f"/tasks/{task_id}/status",
            "result": f"/tasks/{task_id}/result",
        },
    }
