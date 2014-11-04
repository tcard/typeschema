"""
location related types

>>> from typeschema import Checker
>>> checker = Checker()
>>> checker.extend(typeschema.types.location)
>>> checker.check("China", {'type': 'country'})
>>> checker.check({'name': 'Madrid', 'country': 'Spain'}, {'type': 'city'})
>>> checker.check("Foo", {'type': 'country'})
Traceback (most recent call last):
    ...
ValidationError: 'Foo' is not of type 'country'
<BLANKLINE>
Failed validating 'type' in schema:
    {'type': 'country'}
<BLANKLINE>
On instance:
    'Foo'

>>> checker.check({'name':'Madrid', 'country':'Foo'}, {'type': 'city'})
Traceback (most recent call last):
    ...
ValidationError: {'country': 'Foo', 'name': 'Madrid'} is not of type 'city'
<BLANKLINE>
Failed validating 'type' in schema:
    {'type': 'city'}
<BLANKLINE>
On instance:
    {'country': 'Foo', 'name': 'Madrid'}
"""

import typeschema
import incf.countryutils.datatypes as datatypes


def is_country(value, definition):
    if not isinstance(value, str):
        raise typeschema.ValidationError("")

    datatypes.Country(value)


types = {
    'country': [{}, is_country],
    'city': [{
        'type': 'object',
        'properties': {
            "name": {'type': 'string'},
            "country": {'type': 'country'},
        }
    }],
}
