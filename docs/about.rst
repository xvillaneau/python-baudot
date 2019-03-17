
About this library and the Baudot code
======================================

What is the Baudot code?
------------------------

The Baudot code was the first (or at least the first practical) fixed-length
character encoding to be used widely in the telecommunications industry.
This system, invented and patented by the French engineer Jean-Maurice-Émile
Baudot in 1870, was intended as a replacement for Morse code when sending
telegraph messages. It allowed the use of a machine (also patented) to read
the messages automatically.

However the code still had to be composed manually; in 1901 the process was
refined by the American engineer Donald Murray, so that it could be easily
composed on a typewriter-like machine. The code was also modified to reduce and
optimize the wear on the tape-punching mechanism. This system, known as the
Baudot-Murray code or ITA2, was even more widely adopted and vastly used
through World War II.

This new standard was eventually one of the bases for the design of the ASCII
encoding that we are now familiar with. In retrospective, the legacy of the
Baudot and Murray codes is immense, though they are rarely used today.

How did it work?
----------------

The Baudot code (and Baudot-Murray afterward) is a 5-bit stateful binary code.
This is a modern description though, since at the time these "bits" would have
just been holes in paper tapes.

Because each line of tape can hold five holes/bits, that means that the code
allows 32 possible combinations per character. This however is obviously not
enough to hold the 26 letters of the alphabet plus ten digits, let alone other
symbols. Baudot's solution was to use special "shift" characters, which would
indicate whether the following codes (until the next shift) were letters or
numbers (and symbols). Hence why it is called a "stateful" encoding. This is
unlike ASCII and its successors, where each character has its unique code.

The Baudot-Murray code extends on the idea of control characters, introducing
codes such as "Carriage Return", "Line Feed", "Enquiry" and "Bell". There even
exists a variant of ITA2 for Russian use, which introduces a third shift that
exposes a table of cyrillic characters.

So, why this library?
---------------------

I got interested in 5-bit encoding while learning about the now famous code
breaking efforts lead by the United Kingdom during WWII. Such tapes were even
an essential component of `Colossus`_, the first electronic computer which was
designed for decrypting the German Lorenz cipher.

At first I thought decoding this could be a fun exercise, then discovered that
I could not find any Python library on PyPi for doing that. So here I am, doing
this for fun (and so that I could call dibs on the "baudot" name).

Quite honestly, I cannot think of many good use cases for this library.
Reportedly, ITA2 is still commonly used in the radio amateur community, so that
could be a potential one. Or this could be used to make a simulation of the
Colossus computer.

More resources
--------------

* `Baudot Code - Wikipedia`_
* `5 Hole Paper Tape - Computerphile`_

.. _`Baudot Code - Wikipedia`: https://en.wikipedia.org/wiki/Baudot_code
.. _`5 Hole Paper Tape - Computerphile`: https://youtu.be/JafQYA7vV6s
.. _`Colossus`: https://en.wikipedia.org/wiki/Colossus_computer