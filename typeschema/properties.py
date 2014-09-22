"""
typeschema.properties defines some classes than can be used for defining
properties of a class.
"""

import typeschema

_builtin_property = property


class property(_builtin_property):
    """
    Defines a property for a class whose setter checks the input.

    >>> class MyClass(object):
    ...     my_attr = property('my_attr', {'type': 'integer'})
    ...
    >>> my = MyClass()
    >>> my.my_attr = 123
    >>> my.my_attr
    123
    >>> my.my_attr = '123'
    Traceback (most recent call last):
        ...
    ValidationError: '123' is not of type 'integer'
    <BLANKLINE>
    Failed validating 'type' in schema:
        {'type': 'integer'}
    <BLANKLINE>
    On instance:
        '123'
    >>> MyClass.my_attr.schema
    {'type': 'integer'}
    """
    def __init__(self, name, schema, default=None, check=typeschema.check):
        self.name = name
        self.schema = schema
        self.default = default
        self.check = check
        if default is not None:
            check(default, schema)

        def getter(self):
            return self.__dict__.get(name, default)

        def setter(self, value):
            check(value, schema)
            self.__dict__[name] = value

        super(property, self).__init__(getter, setter)


def int(name, default=None):
    """
    Defines a property for a class whose setter checks that the input is an
    integer or None.

    >>> class MyClass(object):
    ...     my_attr = int('my_attr', default=123)
    >>> my = MyClass()
    >>> my.my_attr
    123
    >>> my.my_attr = '123'
    Traceback (most recent call last):
        ...
    ValidationError: '123' is not valid under any of the given schemas
    <BLANKLINE>
    Failed validating 'anyOf' in schema:
        {'anyOf': [{'type': 'integer'}, {'type': 'null'}]}
    <BLANKLINE>
    On instance:
        '123'
    """
    return property(name, {'anyOf': [
                    {'type': 'integer'},
                    {'type': 'null'}
                    ]}, default=default)


def string(name, default=None):
    """
    Defines a property for a class whose setter checks that the input is a
    string or None.

    >>> class MyClass(object):
    ...     my_attr = string('my_attr', default='foo')
    >>> my = MyClass()
    >>> my.my_attr
    'foo'
    >>> my.my_attr = 123
    Traceback (most recent call last):
        ...
    ValidationError: 123 is not valid under any of the given schemas
    <BLANKLINE>
    Failed validating 'anyOf' in schema:
        {'anyOf': [{'type': 'string'}, {'type': 'null'}]}
    <BLANKLINE>
    On instance:
        123
    """
    return property(name, {'anyOf': [
                    {'type': 'string'},
                    {'type': 'null'}
                    ]}, default=default)


def bool(name, default=None):
    """
    Defines a property for a class whose setter checks that the input is a
    boolean or None.

    >>> class MyClass(object):
    ...     my_attr = bool('my_attr', default=True)
    >>> my = MyClass()
    >>> my.my_attr
    True
    >>> my.my_attr = 123
    Traceback (most recent call last):
        ...
    ValidationError: 123 is not valid under any of the given schemas
    <BLANKLINE>
    Failed validating 'anyOf' in schema:
        {'anyOf': [{'type': 'boolean'}, {'type': 'null'}]}
    <BLANKLINE>
    On instance:
        123
    """
    return property(name, {'anyOf': [
                    {'type': 'boolean'},
                    {'type': 'null'}
                    ]}, default=default)


def list(name, default=None):
    """
    Defines a property for a class whose setter checks that the input is a
    list or None.

    >>> class MyClass(object):
    ...     my_attr = list('my_attr', default=[])
    >>> my = MyClass()
    >>> my.my_attr
    []
    >>> my.my_attr = [1, 2]
    >>> my.my_attr.append(3)
    >>> my.my_attr
    [1, 2, 3]
    >>> my.my_attr = '123'
    Traceback (most recent call last):
        ...
    ValidationError: '123' is not valid under any of the given schemas
    <BLANKLINE>
    Failed validating 'anyOf' in schema:
        {'anyOf': [{'type': 'array'}, {'type': 'null'}]}
    <BLANKLINE>
    On instance:
        '123'
    """
    return property(name, {'anyOf': [
                    {'type': 'array'},
                    {'type': 'null'}
                    ]}, default=default)
