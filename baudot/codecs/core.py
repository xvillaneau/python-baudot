
"""
Core codec base classes and logic.

These tools handle encoding and decoding *per character*;
the core logic of stateful encoding is in ``baudot.core``
"""

from abc import ABC, abstractmethod
from collections import namedtuple, defaultdict
from typing import List, Dict, Union, Tuple, Set, Optional

from ..exceptions import IncoherentTable, DecodingError, EncodingError

__all__ = ['Shift', 'BaudotCodec', 'SimpleTabledCodec']

Shift = namedtuple('Shift', ('name',))

Value = Union[str, Shift]
Table = List[Value]


class BaudotCodec(ABC):
    """
    Abstract Base Class for a Codec

    Subclasses must implement :py:meth:`encode` and :py:meth:`decode`
    """

    @abstractmethod
    def encode(self, value: Value, state: Shift) -> Tuple[int, Shift]:
        """
        Abstract method for encoding a single character or state shift
        """

    @abstractmethod
    def decode(self, code: int, state: Shift) -> Union[str, Shift]:
        """
        Abstract method for decoding a single code.
        """


class SimpleTabledCodec(BaudotCodec):
    """
    Creates a codec based on a character table.

    The input format must be a dictionary of which the keys are the
    possible states (instances of ``Shift``) and the values are lists
    of length 32 exactly, containing characters or shifts.

    The ``Shift`` instances are the only control characters this
    library knows of. Any other must be taken from ASCII/Unicode.
    """

    __slots__ = ['name', 'shifts', 'alphabet', 'decoding_table',
                 'encoding_single', 'encoding_any', 'encoding_others']

    def __init__(self, name: str, tables: Dict[Shift, Table]):

        _verify_tables(tables)
        enc_single, enc_any, enc_others = _make_simple_encoding_table(tables)

        self.name: str = name
        self.shifts: Set[Shift] = set(tables.keys())
        self.alphabet: Set[str] = set(value
                                      for table in tables.values()
                                      for value in table
                                      if isinstance(value, str))
        self.decoding_table: Dict[Shift, Table] = tables
        self.encoding_single: Dict[Value, Tuple[int, Shift]] = enc_single
        self.encoding_any: Dict[Value, int] = enc_any
        self.encoding_others: Dict[Value, Set[Tuple[int, Shift]]] = enc_others

    def encode(self, value: Value, state: Shift) -> Tuple[int, Shift]:
        """
        Get the code of the given character of Shift for this codec.

        Actually, this logic returns not only the code but also the
        state required for this code. The current state should also
        be passed so that more complicated cases can be solved.

        :param value: Value (character or state shift) to encode
        :param state: Current state of encoding
        :return: Code for this value, and required state
        """

        # If this value exists (with the same code) in all states,
        # return its code and the state unchanged
        if value in self.encoding_any:
            return self.encoding_any[value], state

        # If the value unambiguously exists in only one state,
        # return its code and the corresponding state
        if value in self.encoding_single:
            return self.encoding_single[value]

        if value not in self.encoding_others:
            raise EncodingError(f"Unsupported value {value}")

        # The logic below handles other cases. This will need more work.

        # TODO: Allow char with codes in two states but not in a third
        # TODO: Allow char that appears twice in a single state
        matches = self.encoding_others[value]
        try:
            # This logic handles the case where a same character exists
            # in multiple states but with different codes. Just return
            # the code that works with the current state.
            return next((code, st) for code, st in matches if st == state)
        except StopIteration:
            raise NotImplementedError("This char encodes in a weird way.")

    def decode(self, code: int, state: Optional[Shift]) -> Value:
        """
        Get the character or state shift corresponding to a given
        code in a given state.

        :param code: Code to look up
        :param state: State to apply. This may be `None`, so that a
            the state can be initialized.
        :return: Decoded character or state shift
        """

        if not 0 <= code < 32:
            raise DecodingError(f"Invalid code: {code}")

        # Allow state initialization by looking up unambiguous values
        if state is None and code in self.encoding_any.values():
            return next(val for val, c in self.encoding_any.items() if c == code)

        if state not in self.decoding_table:
            raise DecodingError(f"Unrecognized state: {state}")

        return self.decoding_table[state][code]


def _verify_tables(tables: Dict[Shift, Table]):
    """
    Function for verifying that a given input table is correct
    """

    if not tables:
        raise IncoherentTable('A coding table cannot be empty')

    if not all(len(t) == 32 for t in tables.values()):
        raise IncoherentTable('All tables MUST have 32 entries')

    shifts_in_keys = set(tables.keys())
    shifts_in_table = set(shift
                          for table in tables.values()
                          for shift in table
                          if isinstance(shift, Shift))

    if shifts_in_keys != shifts_in_table:
        raise IncoherentTable("Shifts in the tables don't match their keys")


def _make_simple_encoding_table(tables: Dict[Shift, Table]):
    """
    Generates the encoding tables by reversing the decoding table
    """

    matches: Dict[Value, Set[Tuple[int, Shift]]] = defaultdict(set)
    for shift, table in tables.items():
        for i, value in enumerate(table):
            matches[value].add((i, shift))

    single_match, any_matches, others = {}, {}, {}

    for value, match in matches.items():

        if len(match) == 1:
            single_match[value] = match.pop()
            continue

        codes = set(code for code, _ in match)
        if len(codes) == 1 and len(match) == len(tables):
            any_matches[value] = codes.pop()
            continue

        others[value] = match

    return single_match, any_matches, others
