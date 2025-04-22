from sqlmodel import Session
from atropos.api.models.task import Task
from atropos.api.services.base import Service
from atropos.api.services.get_record_by_id import GetRecordById


class GetTaskById(Service):
    def __init__(self, get_record_by_id: GetRecordById = GetRecordById()):
        self.get_record_by_id = get_record_by_id

    def __call__(self, task_id: str, session: Session) -> Task:
        return self.get_record_by_id(Task, task_id, session)
