from sqlmodel import Session, SQLModel, select
from typing import Type, TypeVar
from atropos.api.errors import RecordNotFoundError
from atropos.api.services.base import Service
from sqlalchemy.exc import NoResultFound

T = TypeVar("T", bound=SQLModel)


class GetRecordById(Service):
    def __call__(self, model_cls: Type[T], record_id: str, session: Session) -> T:
        try:
            return session.exec(
                select(model_cls).where(model_cls.id == record_id)
            ).one()
        except NoResultFound:
            raise RecordNotFoundError(
                f"Record with id {record_id} not found in {model_cls.__name__}"
            )
