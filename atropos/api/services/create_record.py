from sqlmodel import SQLModel, Session
from typing import TypeVar
from atropos.api.services.base import Service

T = TypeVar("T", bound=SQLModel)


class CreateRecord(Service):
    def __call__(self, record: T, session: Session) -> T:
        session.add(record)
        session.commit()
        session.refresh(record)
        return record
