from fastapi import APIRouter, status

from sqlmodel import Session
from atropos.db import engine

from atropos.api.schemas.task import TaskRequest, TaskResponse
from atropos.api.services.create_task_record import CreateTaskRecord
from atropos.api.services.enqueue_task import EnqueueTask
from atropos.api.services.get_task_by_id import GetTaskById


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", status_code=status.HTTP_202_ACCEPTED, response_model=TaskResponse)
def create_task(request: TaskRequest):
    with Session(engine) as session:
        task = CreateTaskRecord()(request.type, session)
    EnqueueTask()(task.id, task.type, request.data)
    return TaskResponse.from_task(task)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str):
    with Session(engine) as session:
        task = GetTaskById()(task_id, session)
    return TaskResponse.from_task(task)
