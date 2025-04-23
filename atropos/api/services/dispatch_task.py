from atropos.api.services.base import Service
from atropos.api.errors import UnregisteredTaskTypeError
from atropos.api.services.handle_process_data import HandleProcessData
from atropos.celery_app import celery_app


TASK_TYPE_HANDLERS = {
    "data-processing": HandleProcessData(),
}


@celery_app.task(name="dispatch_task_by_type")
def dispatch_task_helper(task_id: str, task_type: str, data: dict):
    handler = TASK_TYPE_HANDLERS.get(task_type)
    if not handler:
        raise UnregisteredTaskTypeError

    handler(task_id, data)


class DispatchTask(Service):
    def __call__(self, task_id: str, task_type: str, data: dict) -> None:
        dispatch_task_helper.delay(task_id, task_type, data)
