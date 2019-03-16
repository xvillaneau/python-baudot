
from abc import ABC, abstractmethod
from collections.abc import Iterator


class BaudotReader(Iterator, ABC):
    pass


class BaudotWriter(ABC):

    @abstractmethod
    def write(self, code: int):
        pass
