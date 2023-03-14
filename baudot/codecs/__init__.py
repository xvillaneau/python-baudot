"""
Codecs are the tools used to convert encoded-data (5-bit digits)
into Unicode characters and back.
"""

from .core import BaudotCodec, Shift, SimpleTabledCodec
from .ita1_baudot import ITA1_CONTINENTAL, ITA1_UK
from .ita2_baudot_murray import ITA2_STANDARD, ITA2_US

__all__ = [
    "BaudotCodec",
    "SimpleTabledCodec",
    "Shift",
    "ITA1_CONTINENTAL",
    "ITA1_UK",
    "ITA2_STANDARD",
    "ITA2_US",
]
