
class BaudotException(Exception):
    """Core exception class for this library"""


class IncoherentTable(BaudotException):
    """Raised when an encoding/decoding table is not valid"""


class DecodingError(BaudotException):
    """Raised on decoding error"""


class EncodingError(BaudotException):
    """Raised on encoding error"""
