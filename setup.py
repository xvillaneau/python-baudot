
from setuptools import setup, find_packages

setup(
    name='baudot',
    version='0.1.0',
    description='Tools for handling stateful 5-bit encoding',
    author='Xavier Villaneau',
    author_email='xvillaneau+baudot@gmail.com',
    license='LGPLv3',
    python_requires='>=3.6.0',
    packages=find_packages(exclude=('tests',)),
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Topic :: Communications',
    ],
)
