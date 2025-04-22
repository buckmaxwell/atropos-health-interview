from sqlmodel import Session, SQLModel
from typing import TypeVar
from atropos.db import engine
from atropos.api.services.base import Service

T = TypeVar("T", bound=SQLModel)


class CreateRecord(Service):
    def __call__(self, record: T) -> T:
        with Session(engine) as session:
            session.add(record)
            session.commit()
            session.refresh(record)
        return record
