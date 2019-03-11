
from abc import ABC, abstractmethod
from collections import namedtuple, defaultdict
from typing import List, Dict, Union, Tuple, Set, Optional

from ..exceptions import IncoherentTable, DecodingError, EncodingError

__all__ = ['Shift', 'BaudotCodec', 'SimpleTabledCodec']

Shift = namedtuple('Shift', ('name',))

Value = Union[str, Shift]
Table = List[Value]


class BaudotCodec(ABC):

    @abstractmethod
    def encode(self, value: Value, state: Shift) -> Tuple[int, Shift]:
        pass

    @abstractmethod
    def decode(self, code: int, state: Shift) -> Union[str, Shift]:
        pass


class SimpleTabledCodec(BaudotCodec):

    __slots__ = ['name', 'shifts', 'alphabet', 'decoding_table'
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

        if value in self.encoding_any:
            return self.encoding_any[value], state

        if value in self.encoding_single:
            return self.encoding_single[value]

        if value not in self.encoding_others:
            raise EncodingError(f"Unsupported value {value}")

        matches = self.encoding_others[value]
        try:
            return next((code, st) for code, st in matches if st == state)
        except StopIteration:
            # TODO: Allow custom logic, needed for Russian MTK-2 support
            raise NotImplementedError("This char encodes in a weird way.")

    def decode(self, code: int, state: Optional[Shift]) -> Value:

        if not 0 <= code < 32:
            raise DecodingError(f"Invalid code: {code}")

        # Allow state initialization by looking up unambiguous values
        if state is None and code in self.encoding_any.values():
            return next(val for val, c in self.encoding_any.items() if c == code)

        if state not in self.decoding_table:
            raise DecodingError(f"Unrecognized state: {state}")

        return self.decoding_table[state][code]


def _verify_tables(tables: Dict[Shift, Table]):

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
