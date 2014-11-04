import typeschema.properties
import typeschema.types.location
import incf.countryutils.datatypes as datatypes


checker = typeschema.Checker()
checker.extend(typeschema.types.location)
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


class city(typeschema.properties.nullable):
    """
    Defines a property for a class whose setter checks that the input is an
    city (check typeschema.types.location for reference) or None.

    >>> class MyClass(object):
    ...     my_attr = city('my_attr', default={'name': 'Madrid', 'country': 'Spain'})
    >>> my = MyClass()
    >>> my.my_attr['name']
    'Madrid'
    >>> my.my_attr['country'].name
    'Spain'
    >>> my.my_attr['country'].continent.name
    'Europe'
    >>> my.my_attr = {'name': 'Madrid', 'country': 'Foo'}
    Traceback (most recent call last):
        ...
    ValidationError: {'country': 'Foo', 'name': 'Madrid'} is not valid under any of the given schemas
    <BLANKLINE>
    Failed validating 'anyOf' in schema:
        {'anyOf': [{'type': 'city'}, {'type': 'null'}]}
    <BLANKLINE>
    On instance:
        {'country': 'Foo', 'name': 'Madrid'}
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

            return {
                "name": city['name'],
                "country": datatypes.Country(city['country'])
            }

        return getter

