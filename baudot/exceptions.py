
"""
Custom exceptions for the Baudot library
"""


class BaudotException(Exception):
    """Core exception class for this library"""


class IncoherentTable(BaudotException):
    """Raised when an encoding/decoding table is not valid"""


class DecodingError(BaudotException):
    """Raised on decoding error"""


class EncodingError(BaudotException):
    """Raised on encoding error"""


class ReadError(BaudotException):
    """Raised when reading a 5-bit stream fails"""


class WriteError(BaudotException):
    """Raised when writing a 5-bit stream fails"""
