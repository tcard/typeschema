"""
location related types:

* country: the city is a string contained in the following list: http://en.wikipedia.org/wiki/List_of_sovereign_states_and_dependent_territories_by_continent_(data_file)
* city: is a dict with name key and country key. The name could be any string.

>>> from typeschema import Checker
>>> import typeschema.types.location
>>> checker = Checker()
>>> checker.extend(typeschema.types.location.types)
>>> checker.check("China", {'type': 'country'})
>>> checker.check(City('Madrid', 'Spain'), {'type': 'city'})
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

>>> checker.check(City('Madrid', 'Foo'), {'type': 'city'})
Traceback (most recent call last):
    ...
ValidationError: ['Madrid', 'Foo'] is not of type 'city'
<BLANKLINE>
Failed validating 'type' in schema:
    {'type': 'city'}
<BLANKLINE>
On instance:
    ['Madrid', 'Foo']
"""

import collections
import incf.countryutils.datatypes as datatypes


class City(collections.namedtuple('City', ['name', 'country'])):
    @property
    def country(self):
        return datatypes.Country(self[1])

    def to_validate(self):
        return list(self)


def is_country(value):
    if not isinstance(value, str):
        return False

    return datatypes.Country(value)


def is_city(value):
    if len(value) != 2:
        return False

    return is_country(value[1])


types = {
    'country': is_country,
    'city': is_city,
}
