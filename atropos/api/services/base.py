# atropos/services/base.py

from abc import ABC, abstractmethod


class Service(ABC):
    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError
