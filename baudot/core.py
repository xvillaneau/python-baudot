
from io import TextIOBase, StringIO
from typing import Optional

from .handlers import BaudotReader, BaudotWriter
from .codecs import BaudotCodec, Shift


def encode(stream: TextIOBase, codec: BaudotCodec, writer: BaudotWriter):

    state: Optional[Shift] = None
    buffer = []

    while True:

        char = stream.read(1)
        if not char:
            break

        code, new_state = codec.encode(char, state)
        buffer.append(code)

        if new_state != state:
            state_code, _ = codec.encode(new_state, None)
            buffer.append(state_code)
            state = new_state

        while len(buffer) > 0:
            writer.write(buffer.pop(-1))


def encode_str(chars: str, codec: BaudotCodec, writer: BaudotWriter):

    with StringIO(chars) as stream:
        encode(stream, codec, writer)


def decode(reader: BaudotReader, codec: BaudotCodec, stream: TextIOBase):

    state: Optional[Shift] = None

    for code in reader:

        value = codec.decode(code, state)

        if isinstance(value, Shift):
            state = value
        else:
            stream.write(value)


def decode_to_str(reader: BaudotReader, codec: BaudotCodec):

    with StringIO('') as stream:
        decode(reader, codec, stream)
        return stream.getvalue()
