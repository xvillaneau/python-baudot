# Baudot – A 5-bit Stateful Codec Python Library

`baudot` is a Python 3 library for reading and writing 5-bit stateful encoding.

This library is named after [Jean-Maurice-Émile Baudot (1845-1903)][wiki-emile],
the French engineer who invented this code.
The [Baudot code][wiki-baudot] was the first practical binary character
encoding, and is an ancestor of the ASCII code we are familiar with today.

[wiki-emile]: https://en.wikipedia.org/wiki/%C3%89mile_Baudot
[wiki-baudot]: https://en.wikipedia.org/wiki/Baudot_code

## Examples

### Encoding example

```python
from io import StringIO
from baudot import encode_str, codecs, handlers

input_str = 'HELLO WORLD!'
with StringIO() as output_buffer:
    writer = handlers.TapeWriter(output_buffer)
    encode_str(input_str, codecs.ITA2_STANDARD, writer)
    print(output_buffer.getvalue())
```

This would output the following:

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

### Decoding example

```python
from io import BytesIO
from baudot import decode_to_str, codecs, handlers

code = b'1f14011212180413180a12091b0d'
with BytesIO(code) as code_stream:
    reader = handlers.HexBytesReader(code_stream)
    print(decode_to_str(reader, codecs.ITA2_US))
```

Should print:

    HELLO WORLD!

## Installation

Pip is the simplest way to install Baudot:

    pip install baudot

This library works with Python 3.6 and up.
It does not have any external requirement.

## Docs

Coming soon
