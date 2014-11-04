import typeschema.properties
import typeschema.types.location

checker = typeschema.Checker()
checker.extend(typeschema.types.location)
check = checker.check


class country(typeschema.properties.nullable):
    """
    Defines a property for a class whose setter checks that the input is an
    country or None.

    >>> class MyClass(object):
    ...     my_attr = country('my_attr', default='Spain')
    >>> my = MyClass()
    >>> my.my_attr
    'Spain'
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


class city(typeschema.properties.nullable):
    """
    Defines a property for a class whose setter checks that the input is an
    city or None.

    >>> class MyClass(object):
    ...     my_attr = city('my_attr', default=['Madrid', 'Spain'])
    >>> my = MyClass()
    >>> my.my_attr
    ['Madrid', 'Spain']
    >>> my.my_attr = ['Madrid', 'Foo']
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
