from abc import abstractmethod
from atropos.api.services.base import Service


class HandleTask(Service):
    @abstractmethod
    def __call__(self, task_id: str, data: dict) -> None:
        raise NotImplementedError
