from fastapi import APIRouter, status

from atropos.api.schemas.task import TaskRequest, TaskResponse
from atropos.api.services.create_task_record import CreateTaskRecord
from atropos.api.services.enqueue_task import EnqueueTask

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_model=TaskResponse)
def create_task(request: TaskRequest):
    task = CreateTaskRecord()(request.type)
    EnqueueTask()(task.id, task.type, request.data)
    return TaskResponse.from_task(task.id, task.type)
