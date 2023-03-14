"""
Baudot – Tools for handling stateful 5-bit encoding
"""

from .core import decode, decode_to_str, encode, encode_str

__all__ = [
    "encode",
    "encode_str",
    "decode",
    "decode_to_str",
]
