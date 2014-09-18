import os
import re
from setuptools import setup


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
    maintainer='Tyba',
    maintainer_email='development@tyba.com',
    version=get_version_from_init(),
    url='https://github.com/Tyba/typeschema',
    packages=[
        'typeschema',
        'typeschema.properties'
    ],
    install_requires=[
        'jsonschema == 2.4.0'  # test
    ]
)
