"""
Codec definitions for second-generation Baudot codes
(a.k.a. Baudot-Murray or ITA2)
"""
# pylint: disable=invalid-name

from .core import Shift, SimpleTabledCodec

Letters = Shift('Letters')
Figures = Shift('Figures')

STANDARD_TABLE = {
    Letters: [
        '\x00', 'E', '\n', 'A', ' ', 'S', 'I', 'U',
        '\r', 'D', 'R', 'J', 'N', 'F', 'C', 'K',
        'T', 'Z', 'L', 'W', 'H', 'Y', 'P', 'Q',
        'O', 'B', 'G', Figures, 'M', 'X', 'V', Letters
    ],
    Figures: [
        '\x00', '3', '\n', '-', ' ', "'", '8', '7',
        '\r', '\x05', '4', '\x07', ',', '!', ':', '(',
        '5', '+', ')', '2', '£', '6', '0', '1',
        '9', '?', '&', Figures, '.', '/', '=', Letters
    ],
}

US_TABLE = {
    Letters: STANDARD_TABLE[Letters].copy(),
    Figures: [
        '\x00', '3', '\n', '-', ' ', '\x07', '8', '7',
        '\r', '$', '4', "'", ',', '!', ':', '(',
        '5', '"', ')', '2', '#', '6', '0', '1',
        '9', '?', '&', Figures, '.', '/', ';', Letters
    ],
}

ITA2_STANDARD = SimpleTabledCodec(
    'Baudot-Murray code (ITA2), Standard',
    STANDARD_TABLE)
ITA2_US = SimpleTabledCodec(
    'Baudot-Murray code (ITA2), US variant',
    US_TABLE)
