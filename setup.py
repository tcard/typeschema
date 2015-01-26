#! /usr/bin/env python

import os
import re
from setuptools import setup, find_packages


def get_version_from_init():
    file = open(os.path.join(
        os.path.dirname(__file__),
        'typeschema',
        '__init__.py'
    ))

    regexp = re.compile(r".*__version__ = '(.*?)'", re.S)
    version = regexp.match(file.read()).group(1)
    file.close()

    return version

setup(
    name='typeschema',
    description='A simpler type validator based on jsonschema.',
    maintainer='Tyba',
    maintainer_email='development@tyba.com',
    version=get_version_from_init(),
    url='https://github.com/tyba/typeschema',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'jsonschema == 2.4.0',
        'incf.countryutils == 1.0'
    ]
)
