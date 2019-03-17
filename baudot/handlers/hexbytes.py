"""
Handler for reading and writing 5-bit codes as a hexadecimal bit stream.
"""

from io import BufferedIOBase

from .core import BaudotReader, BaudotWriter
from ..exceptions import ReadError, WriteError


class HexBytesReader(BaudotReader):
    """
    Reader for hexadecimal 5-bit streams
    """

    def __init__(self, stream: BufferedIOBase):
        self.stream = stream

    def __next__(self):
        hex_byte = self.stream.read(2)
        if not hex_byte:
            raise StopIteration()
        try:
            code = int(hex_byte, 16)
        except ValueError:
            str_repr = hex_byte.decode(errors='backslashreplace')
            raise ReadError(f'Invalid hexadecimal byte: {str_repr}')
        if not 0 <= code < 32:
            raise ReadError(f'Code value {code} is not a valid 5-bit value')
        return code


class HexBytesWriter(BaudotWriter):
    """
    Writer for hexadecimal 5-bit stream
    """

    def __init__(self, stream: BufferedIOBase):
        self.stream = stream

    def write(self, code: int):
        """Writes a code as an hexadecimal value"""
        if not 0 <= code < 32:
            raise WriteError('Invalid 5-bit character code')

        self.stream.write(f'{code:02x}'.encode())
