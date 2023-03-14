"""
Core utilities for Baudot input/output handlers
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator


class BaudotReader(ABC):
    """Abstract Base Class for a reader"""

    def __iter__(self) -> Iterator[int]:
        return self

    @abstractmethod
    def __next__(self) -> int:
        pass


class BaudotWriter(ABC):
    """Abstract Base Class for a writer"""

    @abstractmethod
    def write(self, code: int) -> None:
        """Write a single code to the output"""
