"""
Codec definitions for first-generation Baudot codes (a.k.a. ITA1)
"""
# pylint: disable=invalid-name

from .core import Shift, SimpleTabledCodec

Figures = Shift('Figures')
Letters = Shift('Letters')

CONTINENTAL_TABLE = {
    Letters: [
        ' ', 'A', 'E', 'É', 'Y', 'U', 'I', 'O',
        Figures, 'J', 'G', 'H', 'B', 'C', 'F', 'D',
        Letters, 't', 'X', 'Z', 'S', 'T', 'W', 'V',
        '\x08', 'K', 'M', 'L', 'R', 'Q', 'N', 'P'
    ],
    Figures: [
        ' ', '1', '2', '&', '3', '4', 'o', '5',
        Figures, '6', '7', 'h', '8', '9', 'f', '0',
        Letters, '.', ',', ':', ';', '!', '?', "'",
        '\x08', '(', ')', '=', '-', '/', '№', '%'
    ],
}

UK_TABLE = {
    Letters: [
        ' ', 'A', 'E', '/', 'Y', 'U', 'I', 'O',
        Figures, 'J', 'G', 'H', 'B', 'C', 'F', 'D',
        Letters, '-', 'X', 'Z', 'S', 'T', 'W', 'V',
        '\x08', 'K', 'M', 'L', 'R', 'Q', 'N', 'P'
    ],
    Figures: [
        ' ', '1', '2', '¹⁄', '3', '4', '³⁄', '5',
        Figures, '6', '7', '¹', '8', '9', '⁵⁄', '0',
        Letters, '.', '⁹⁄', ':', '⁷⁄', '²', '?', "'",
        '\x08', '(', ')', '=', '-', '/', '£', '+'
    ],
}

ITA1_CONTINENTAL = SimpleTabledCodec(
    'Baudot code (ITA1), Continental version',
    CONTINENTAL_TABLE)

ITA1_UK = SimpleTabledCodec(
    'Baudot code (ITA1), UK version',
    UK_TABLE)
