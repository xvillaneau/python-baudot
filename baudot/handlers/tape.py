
from collections import namedtuple
from io import TextIOBase

from .core import BaudotReader, BaudotWriter

TapeConfig = namedtuple('PrettyConfig', ('punch', 'blank', 'sep'))

MSB_FIRST = [1 << (4-n) for n in range(5)]


class TapeReader(BaudotReader):

    def __init__(self, stream: TextIOBase, config: TapeConfig):
        self.stream = stream
        self.config = config

    def __next__(self) -> int:
        line = next(self.stream)
        pairs = zip(line.replace(self.config.sep, ''), MSB_FIRST)
        return sum(n for c, n in pairs if c == self.config.punch)


class TapeWriter(BaudotWriter):

    def __init__(self, stream: TextIOBase, config: TapeConfig, flush=False):
        self.stream = stream
        self.config = config
        self.flush = flush

    def write(self, code: int):
        if not 0 <= code < 32:
            raise ValueError('Invalid 5-bit character code')

        chars = ''.join(self.config.punch if c == '1' else self.config.blank
                        for c in f'{code:05b}')
        self.stream.write(f"{chars[:3]}{self.config.sep}{chars[3:]}\n")

        if self.flush:
            self.stream.flush()
