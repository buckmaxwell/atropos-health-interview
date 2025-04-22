from fastapi import APIRouter


router = APIRouter(prefix="/task-types", tags=["task-types"])


@router.get("/task-types")
def get_task_types():
    """
    Get all task types.
    """
    return {
        "task_types": [
            "task_type_1",
            "task_type_2",
            "task_type_3",
        ]
    }
