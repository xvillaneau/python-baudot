"""
Handler for reading and writing to pretty tape-like formatted text

For example, the tape might look like:::

    ***.**
    * *.
       . *
    *  .*
    *  .*
    ** .
      *.
    *  .**
    ** .
     * .*
    *  .*
     * . *
    ** .**
     **. *

(Which reads 'HELLO WORLD!')
"""

from collections import namedtuple
from io import TextIOBase

from .core import BaudotReader, BaudotWriter
from ..exceptions import WriteError

TapeConfig = namedtuple('TapeConfig', ('punch', 'blank', 'sep'))
TapeConfig.__doc__ = """
Object for storing a tape representation format.
"""

DEFAULT_TAPE = TapeConfig('*', ' ', '.')

MSB_FIRST = [1 << (4-n) for n in range(5)]


class TapeReader(BaudotReader):
    """
    Reader class for tape-like data.
    """

    def __init__(self, stream: TextIOBase, config: TapeConfig = DEFAULT_TAPE):
        self.stream = stream
        self.config = config

    def __next__(self) -> int:
        line = next(self.stream)
        pairs = zip(line.replace(self.config.sep, ''), MSB_FIRST)
        return sum(n for c, n in pairs if c == self.config.punch)


class TapeWriter(BaudotWriter):
    """
    Writer class for tape-like data.
    """

    def __init__(self, stream: TextIOBase, config: TapeConfig = DEFAULT_TAPE):
        self.stream = stream
        self.config = config

    def write(self, code: int):
        """Writes a code to tape"""
        if not 0 <= code < 32:
            raise WriteError('Invalid 5-bit character code')

        chars = ''.join(self.config.punch if c == '1' else self.config.blank
                        for c in f'{code:05b}')
        self.stream.write(f"{chars[:3]}{self.config.sep}{chars[3:]}\n")
