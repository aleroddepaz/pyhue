#!/usr/bin/env python

from distutils.core import setup


long_description = '''
pyhue
=====

Python library for the Philips Hue personal lighting system.

Installation
------------

.. raw:: html

    <p>
    You can install pyhue with <code>pip install pyhue</code> or
    <a href="http://raw.github.com/alexrdp90/pyhue/master/src/pyhue.py">download <code>pyhue.py</code></a>
    and place it in your project directory.
    </p>


Example
-------

::

    import pyhue
    
    bridge = pyhue.Bridge('my_ip_address', 'my_username')
    for light in bridge.lights:
        light.on = True
        light.hue = 0


Features
--------

- Object-oriented mapping of the RESTful interface.
- Major support of the v1.0 of the API: Lights_, Groups_, Schedules_.
- Conversion of basic color models.


See the complete documentation of the Philips Hue personal lighting system on http://developers.meethue.com.

.. _download ``pyhue.py``: <>
.. _Lights: http://developers.meethue.com/1_lightsapi.html
.. _Groups: http://developers.meethue.com/2_groupsapi.html
.. _Schedules: http://developers.meethue.com/3_schedulesapi.html

'''


setup(
    name = 'pyhue',
    version = '0.5',
    license = 'GPLv3',
    description = 'Python library for the Philips Hue personal lighting system',
    long_description = long_description,
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