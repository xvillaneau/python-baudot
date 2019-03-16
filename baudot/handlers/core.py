
from abc import ABC, abstractmethod


class BaudotReader(ABC):

    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self):
        pass


class BaudotWriter(ABC):

    @abstractmethod
    def write(self, code: int):
        pass
