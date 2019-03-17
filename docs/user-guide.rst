User Guide
==========

Library walk-through
--------------------

:py:mod:`baudot.core`
    This module holds the stateful encoding/decoding logic. Its functions are
    directly available in :py:mod:`baudot` for convenience.

:py:mod:`baudot.codecs`
    This package hosts the lookup tables, used for encoding/decoding single
    characters. Standard ITA1 and ITA2 tables are built-in, and the tools for
    making custom codes are also provided.

:py:mod:`baudot.handlers`
    This package provides writer and reader classes for a variety of input and
    output formats.

:py:mod:`baudot.exceptions`
    As its name suggests, this module defines the library's exceptions. All are
    subclasses of :py:exc:`.BaudotException`.

Basic usage
-----------

The core functions for any operation in this library are
:py:func:`baudot.encode` and :py:func:`baudot.decode`.

To work, both require three elements:

1. a text input (for encoding) or output (for decoding) stream
2. a codec object
3. a reader (for decoding) or writer (for encoding) object

This is because overall, :py:mod:`baudot` accomplishes two tasks
(and their inverse):

1. reading 5-bit codes from custom input formats,
2. converting 5-bit codes to unicode characters.

Codec objects are instances of :py:class:`baudot.codecs.BaudotCodec`
(or its sub-classes, to be more specific).
A codec is a static object capable of converting characters to codes and back.
This library includes a few default codecs but others may be user-defined.

Readers and writers are instances of :py:class:`baudot.handlers.BaudotReader`
and :py:class:`baudot.handlers.BaudotWriter` respectively.
Currently, all the handlers in this library require a stream to be passed at
instantiation, that they will read from or write to.
This mimics the way it's done in the standard library module
`csv <https://docs.python.org/3/library/csv.html>`_.

The reason I/O in this library depends on streams is so that many types of
inputs and outputs are natively supported, such as files or ``stdin`` and
``stdout``. Or maybe odd devices that natively support Baudot code!
This however can be inconvenient for small tests, so two helper functions
:py:func:`baudot.encode_str` and :py:func:`baudot.decode_to_str` are available
for using strings as text input. Maybe the handlers could be fitted with a
similar feature in the future.

Please keep in mind that this project is very young, and that its API is most
likely ill-designed at this point. Suggestions are welcome!

Examples
--------

Encoding example
^^^^^^^^^^^^^^^^

.. code-block:: python

    from io import StringIO
    from baudot import encode_str, codecs, handlers

    input_str = 'HELLO WORLD!'
    with StringIO() as output_buffer:
        writer = handlers.TapeWriter(output_buffer)
        encode_str(input_str, codecs.ITA2_STANDARD, writer)
        print(output_buffer.getvalue())

This would output the following:

.. code-block:: none

    ***.**
    * *.
       . *
    *  .*
    *  .*
    ** .
      *.
    *  .**
    ** .
     * .*
    *  .*
     * . *
    ** .**
     **. *

Decoding example
^^^^^^^^^^^^^^^^

.. code-block:: python

    from io import BytesIO
    from baudot import decode_to_str, codecs, handlers

    code = b'1f14011212180413180a12091b0d'
    with BytesIO(code) as code_stream:
        reader = handlers.HexBytesReader(code_stream)
        print(decode_to_str(reader, codecs.ITA2_US))

Should print:

.. code-block:: none

    HELLO WORLD!
