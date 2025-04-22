from fastapi import APIRouter
from typing import List

from atropos.api.schemas.task_type import TaskType
from atropos.api.services.get_task_types import GetTaskTypes

router = APIRouter(prefix="/task-types", tags=["task-types"])


@router.get("/", response_model=List[TaskType])
def get_task_types():
    """
    Return all supported task types and their input schemas.
    """
    return GetTaskTypes()()
