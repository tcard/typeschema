import incf.countryutils.datatypes as datatypes

import typeschema.properties
import typeschema.types.location
from typeschema.types.location import City, types

_checker = typeschema.Checker()
_checker.extend(types)
checker = _checker.frozen()
check = checker.check


class country(typeschema.properties.nullable):
    """
    Defines a property for a class whose setter checks that the input is an
    country (check typeschema.types.location for reference) or None.

    >>> class MyClass(object):
    ...     my_attr = country('my_attr', default='Spain')
    >>> my = MyClass()
    >>> my.my_attr.name
    'Spain'
    >>> my.my_attr.continent.name
    'Europe'
    >>> my.my_attr = 'France'
    >>> my_alt = MyClass()
    >>> my_alt.my_attr = my.my_attr
    >>> my_alt.my_attr.name
    'France'
    >>> my.my_attr = 'Foo'
    Traceback (most recent call last):
        ...
    ValidationError: 'Foo' is not valid under any of the given schemas
    <BLANKLINE>
    Failed validating 'anyOf' in schema:
        {'anyOf': [{'type': 'country'}, {'type': 'null'}]}
    <BLANKLINE>
    On instance:
        'Foo'
    """
    def __init__(self, name, default=None):
        super(country, self).__init__(
            name,
            'country',
            default=default,
            check=check
        )

    def _get_getter(self):
        name = self.name
        default = self.default

        def getter(self):
            country = self.__dict__.get(name, default)
            if not country:
                return None

            return datatypes.Country(country)

        return getter

    def _get_setter(self):
        parent_setter = super(country, self)._get_setter()

        def setter(self, value):
            if isinstance(value, datatypes.Country):
                value = value.name

            parent_setter(self, value)

        return setter


class city(typeschema.properties.nullable):
    """
    Defines a property for a class whose setter checks that the input is an
    city (check typeschema.types.location for reference) or None.

    >>> class MyClass(object):
    ...     my_attr = city('my_attr', default=City('Madrid', 'Spain'))
    >>> my = MyClass()
    >>> my.my_attr.name
    'Madrid'
    >>> my.my_attr.country.name
    'Spain'
    >>> my.my_attr.country.continent.name
    'Europe'
    >>> my.my_attr = ['Roma', 'Italy']
    >>> my.my_attr.country.name
    'Italy'
    >>> my.my_attr = City('Madrid', 'Foo')
    Traceback (most recent call last):
        ...
    ValidationError: ['Madrid', 'Foo'] is not valid under any of the given schemas
    <BLANKLINE>
    Failed validating 'anyOf' in schema:
        {'anyOf': [{'type': 'city'}, {'type': 'null'}]}
    <BLANKLINE>
    On instance:
        ['Madrid', 'Foo']
    """
    def __init__(self, name, default=None):
        super(city, self).__init__(
            name,
            'city',
            default=default,
            check=check
        )

    def _get_getter(self):
        name = self.name
        default = self.default

        def getter(self):
            city = self.__dict__.get(name, default)
            if not city:
                return None

            if not isinstance(city, City):
                return City(*city)

            return city

        return getter
