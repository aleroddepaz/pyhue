#!/usr/bin/env python

from distutils.core import setup

setup(
    name = 'pyhue',
    version = '0.3a',
    license = 'GPLv3',
    description = 'Python library for the Philips Hue personal lighting system',
    author = 'Alejandro Rodas',
    author_email = 'alexrdp90@gmail.com',
    url = 'http://alexrdp90.github.com/pyhue',
    download_url = 'http://pypi.python.org/pypi/pyhue',
    package_dir = {'': 'src'},
    py_modules = ['pyhue'],
    classifiers = [
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)