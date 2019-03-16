"""
Core utilities for Baudot input/output handlers
"""

from abc import ABC, abstractmethod


class BaudotReader(ABC):
    """Abstract Base Class for a reader"""

    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self):
        pass


class BaudotWriter(ABC):
    """Abstract Base Class for a writer"""

    @abstractmethod
    def write(self, code: int):
        """Write a single code to the output"""
