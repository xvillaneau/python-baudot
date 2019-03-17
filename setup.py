
from setuptools import setup, find_packages

LONG_DESC = """
Baudot is a Python library for encoding and decoding 5-bit stateful encoding.

This library is named after `Jean-Maurice-Émile Baudot`_ (1845-1903), the French
engineer who invented this code. The `Baudot code`_ was the first practical and
widely used binary character encoding, and is an ancestor of the ASCII code we
are familiar with today.

This library accomplishes two tasks (and their inverse):

1. reading 5-bit codes from custom input formats,
2. converting 5-bit codes to unicode characters.

This library provides support for several common encodings, as well as support
for reading tape-like files and hexadecimal data.

Please keep in mind that this project is very young, and that its API is most
likely ill-designed at this point. Suggestions are welcome!

.. _`Jean-Maurice-Émile Baudot`: https://en.wikipedia.org/wiki/%C3%89mile_Baudot
.. _`Baudot code`: https://en.wikipedia.org/wiki/Baudot_code

"""

setup(
    name='baudot',
    version='0.1.1.post2',
    description='Tools for handling stateful 5-bit encoding',
    long_description=LONG_DESC,
    author='Xavier Villaneau',
    author_email='xvillaneau+baudot@gmail.com',
    url='https://github.com/xvillaneau/python-baudot',
    license='LGPLv3',
    python_requires='>=3.6.0',
    packages=find_packages(exclude=('tests',)),
    test_requires=["pytest", "hypothesis", "coverage", "pylint"],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications',
    ],
)
