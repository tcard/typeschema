import typeschema.properties
from typeschema.types.network import types


_checker = typeschema.Checker()
_checker.extend(types)
checker = _checker.frozen()
check = checker.check


class ip(typeschema.properties.nullable):
    """
    Defines a property for a class whose setter checks that the input is a
    valid ipv4 or None.

    >>> class MyClass(object):
    ...     my_attr = ip('my_attr', default='127.0.0.1')
    >>> my = MyClass()
    >>> my.my_attr
    '127.0.0.1'
    >>> my.my_attr = '8.8.8.8'
    >>> my.my_attr
    '8.8.8.8'
    >>> my.my_attr = 'Foo'
    Traceback (most recent call last):
        ...
    ValidationError: 'Foo' is not valid under any of the given schemas
    <BLANKLINE>
    Failed validating 'anyOf' in schema:
        {'anyOf': [{'type': 'ip'}, {'type': 'null'}]}
    <BLANKLINE>
    On instance:
        'Foo'
    """
    def __init__(self, name, default=None):
        super(ip, self).__init__(name, 'ip', default=default, check=check)
