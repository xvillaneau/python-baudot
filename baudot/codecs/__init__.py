
"""
Codecs are the tools used to convert encoded-data (5-bit digits)
into Unicode characters and back.
"""

from .core import BaudotCodec, SimpleTabledCodec, Shift
from .ita1_baudot import ITA1_CONTINENTAL, ITA1_UK
from .ita2_baudot_murray import ITA2_STANDARD, ITA2_US
