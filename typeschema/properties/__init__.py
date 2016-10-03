"""
typeschema.properties defines some classes than can be used for defining
properties of a class.
"""

import typeschema
import copy

_builtin_property = property
_builtin_float = float


class property(_builtin_property):
    """
    Defines a property for a class whose setter checks the input against a
    JSON schema.

    Args:
        name: Name of the property. The value of the property will be set in
            the object's ``__dict__`` with the name as key.
        schema: A JSON schema as defined in ``typeschema``.
        default: A value It will be copied with ``copy.deepcopy``, so that
            different instances of the class don't share this value.
        check: A ``typeschema.Checker``.

    Returns:
        A ``property`` object.

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

        super(property, self).__init__(self._get_getter(), self._get_setter())

    def _get_getter(self):
        name = self.name
        default = self.default

        def getter(self):
            if default is not None and not name in self.__dict__:
                self.__dict__[name] = copy.deepcopy(default)
            return self.__dict__.get(name, default)

        return getter

    def _get_setter(self):
        schema = self.schema
        name = self.name
        check = self.check

        def setter(self, value):
            check(value, schema)
            self.__dict__[name] = value

        return setter


class nullable(property):
    """
    Defines a nullable property for a class whose setter checks that the input
    is either a ``typeschema`` type or ``None``.

    >>> class MyClass(object):
    ...     my_attr = nullable('my_attr', 'number', default=123.4)
    >>> my = MyClass()
    >>> my.my_attr
    123.4
    >>> my.my_attr = None
    >>> print my.my_attr
    None
    >>> my.my_attr = '123'
    Traceback (most recent call last):
        ...
    ValidationError: '123' is not valid under any of the given schemas
    <BLANKLINE>
    Failed validating 'anyOf' in schema:
        {'anyOf': [{'type': 'number'}, {'type': 'null'}]}
    <BLANKLINE>
    On instance:
        '123'
    """
    def __init__(self, name, internal_type, default=None, check=typeschema.check):
        super(nullable, self).__init__(name, {'anyOf': [
            {'type': internal_type},
            {'type': 'null'}
        ]}, default=default, check=check)


class int(nullable):
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
    def __init__(self, name, default=None):
        super(int, self).__init__(name, 'integer', default=default)


class float(nullable):
    """
    Defines a property for a class whose setter checks that the input is a
    float or None.

    >>> class MyClass(object):
    ...     my_attr = float('my_attr', default=0.99)
    >>> my = MyClass()
    >>> my.my_attr
    0.99
    >>> my.my_attr = 1
    >>> my.my_attr
    1.0
    >>> my.my_attr = '0.99'
    Traceback (most recent call last):
        ...
    ValidationError: '0.99' is not valid under any of the given schemas
    <BLANKLINE>
    Failed validating 'anyOf' in schema:
        {'anyOf': [{'type': 'number'}, {'type': 'null'}]}
    <BLANKLINE>
    On instance:
        '0.99'
    """
    def __init__(self, name, default=None):
        super(float, self).__init__(name, 'number', default=default)

    def _get_setter(self):
        parent_setter = super(float, self)._get_setter()
        name = self.name

        def setter(self, value):
            # call the parent, let them do the checks
            # cast to float if the check is passed
            parent_setter(self, value)
            self.__dict__[name] = _builtin_float(self.__dict__[name])

        return setter


class string(nullable):
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
    def __init__(self, name, default=None):
        super(string, self).__init__(name, 'string', default=default)


class bool(nullable):
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
    def __init__(self, name, default=None):
        super(bool, self).__init__(name, 'boolean', default=default)


class list(nullable):
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
    def __init__(self, name, default=None):
        super(list, self).__init__(name, 'array', default=default)


class enum(property):
    """
    Defines a property for a class whose setter checks that the input is in
    a list of possible values or None.

    >>> class MyClass(object):
    ...     my_attr = enum('my_attr', ['a', 'b', 'C'])
    >>> my = MyClass()
    >>> my.my_attr
    >>> my.my_attr = 'c'
    Traceback (most recent call last):
        ...
    ValidationError: 'c' is not valid under any of the given schemas
    <BLANKLINE>
    Failed validating 'anyOf' in schema:
        {'anyOf': [{'enum': ['a', 'b', 'C']}, {'type': 'null'}]}
    <BLANKLINE>
    On instance:
        'c'
    >>> my.my_attr = None
    >>> my.my_attr
    >>> my.my_attr = 'C'
    >>> my.my_attr
    'C'
    """
    def __init__(self, name, values, default=None):
        super(enum, self).__init__(name, {'anyOf': [
            {'enum': values},
            {'type': 'null'}
        ]}, default=default)
