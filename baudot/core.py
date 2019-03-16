"""
Core encoding/decoding logic of the library
"""

from io import TextIOBase, StringIO
from typing import Optional

from .handlers import BaudotReader, BaudotWriter
from .codecs import BaudotCodec, Shift


def encode(stream: TextIOBase, codec: BaudotCodec, writer: BaudotWriter):
    """
    Encode unicode characters from an input stream to an output writer,
    using the given codec.

    :param stream: Unicode character stream to encode (can be a file)
    :param codec: Codec to use for encoding
    :param writer: Writer instance for the wanted output format
    """
    state: Optional[Shift] = None
    buffer = []

    while True:
        char = stream.read(1)
        if not char:  # TextIOBase returns empty character on EOF
            break

        code, new_state = codec.encode(char, state)
        buffer.append(code)

        if new_state != state:
            state_code, _ = codec.encode(new_state, None)
            buffer.append(state_code)
            state = new_state

        while buffer:
            writer.write(buffer.pop(-1))


def encode_str(chars: str, codec: BaudotCodec, writer: BaudotWriter):
    """
    Encode unicode characters from an input string to an output writer,
    using the given codec.

    :param chars: Unicode string to encode
    :param codec: Codec to use for encoding
    :param writer: Writer instance for the wanted output format
    """
    with StringIO(chars) as stream:
        encode(stream, codec, writer)


def decode(reader: BaudotReader, codec: BaudotCodec, stream: TextIOBase):
    """
    Decode a baudot code stream from a reader to a unicode stream,
    using a given codec.

    :param reader: Reader instance that will read codes from an input
    :param codec: Codec to use for decoding
    :param stream: Unicode stream to write to (can be a file)
    """
    state: Optional[Shift] = None

    for code in reader:
        value = codec.decode(code, state)

        if isinstance(value, Shift):
            state = value
        else:
            stream.write(value)


def decode_to_str(reader: BaudotReader, codec: BaudotCodec) -> str:
    """
    Decode a baudot code stream from a reader to a unicode string,
    using a given codec.

    :param reader: Reader instance that will read codes from an input
    :param codec: Codec to use for decoding
    :return: Decoded Unicode string
    """
    with StringIO('') as stream:
        decode(reader, codec, stream)
        return stream.getvalue()
