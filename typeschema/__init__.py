"""
typeschema is a wrapper for jsonschema that provides some helpers, a simpler
interface, and lets the user define its own types.
"""

__version__ = '0.0.1'

import jsonschema as js
import inspect

_default_types = {}


class Checker(object):
    """
    A Checker wraps a jsonschema.Draft4Validator, allowing the user to define
    custom types.

    Some custom types above the ones in JSON schema are already defined for
    for every Checker from the _default_types module variable.
    """

    def __init__(self):
        self.validator = js.validators.extend(js.Draft4Validator, {})
        self.validator.DEFAULT_TYPES.update(_default_types)

    def check(self, value, schema):
        """
        Checks that a value complies with a JSON schema.

        >>> checker = Checker()
        >>> checker.check(123, {'type': 'integer'})
        >>> checker.check(123, {'type': 'string'})
        Traceback (most recent call last):
            ...
        ValidationError: 123 is not of type 'string'
        <BLANKLINE>
        Failed validating 'type' in schema:
            {'type': 'string'}
        <BLANKLINE>
        On instance:
            123

        Raises:
                See the jsonschema documentation for validate.
        """
        self.validator(schema).validate(value)

    def define(self, name, definition):
        """
        Define a custom type for this checker.

        >>> checker = Checker()
        >>> checker.define('my_type', {'type': 'integer', 'minimum': 10})
        >>> checker.check(20, {'type': 'my_type'})
        >>> checker.check(5, {'type': 'my_type'})
        Traceback (most recent call last):
            ...
        ValidationError: 5 is not of type 'my_type'
        <BLANKLINE>
        Failed validating 'type' in schema:
            {'type': 'my_type'}
        <BLANKLINE>
        On instance:
            5
        >>> from datetime import datetime
        >>> checker.define('date_time', datetime)
        >>> checker.check(datetime.now(), {'type': 'date_time'})

        Args:
            name: An identifier for the type.
            definition: Either a JSON schema, or a custom Python type
                        (including classes).
        """
        if isinstance(definition, type):
            self.validator.DEFAULT_TYPES[unicode(name)] = definition
        else:
            check = self.check

            # The jsonschema library only lets you define custom types with
            # Python types, that is, you have to pass a class or a type.
            # But we want to define new types with JSON schemas.
            # This creates a dummy type that overrides isinstance so that
            # when jsonschema checks if a value is an instance of this type,
            # a normal check happens with that value against the provided
            # schema.
            # Sorry for the black magic.

            class DefinedTypeMeta(type):
                def __instancecheck__(self, value):
                    try:
                        check(value, definition)
                        return True
                    except:
                        return False

            class DefinedType(object):
                __metaclass__ = DefinedTypeMeta

            self.validator.DEFAULT_TYPES[unicode(name)] = DefinedType


class FrozenChecker(Checker):
    """
    A Checker that doesn't allow any further type definition.
    """
    def define(self, name, schema):
        raise Exception("can't add types to a frozen checker.")

checker = FrozenChecker()


def check(value, schema):
    """
    Wrapper for a default Checker().check(value, schema).
    """
    checker.check(value, schema)


def checked_property(name, schema, check=check):
    """
    Defines a property for a class whose setter checks the input.

    >>> class MyClass(object):
    ...     my_attr = checked_property('my_attr', {'type': 'integer'})
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
    """
    def _ensure_defined(self):
        if not '_' + name in self.__dict__:
            setattr(self, '_' + name, None)

    def getter(self):
        _ensure_defined(self)
        return getattr(self, '_' + name)

    def setter(self, value):
        check(value, schema)
        setattr(self, '_' + name, value)

    return property(getter, setter)


def check_args(schemas, check_function=check):
    """
    Decorate a function, checking the schema of its arguments.

    >>> @check_args({
    ...    'foo': {'type': 'integer'},
    ...     # bar goes unchecked
    ...     'baz': {'type': 'number'},
    ...     'qux': {'type': 'string'}
    ... })
    ... def my_function(foo, bar, baz=123, qux='456'):
    ...     print "foo: %r, bar: %r, baz: %r, qux: %r" % (foo, bar, baz, qux)
    >>> my_function(123, 456)
    foo: 123, bar: 456, baz: 123, qux: '456'
    >>> my_function(123, '456', qux='789')
    foo: 123, bar: '456', baz: 123, qux: '789'
    >>> my_function(123, '456', '789')
    Traceback (most recent call last):
        ...
    ArgValidationError: Value passed to argument 'baz' is not valid.
    '789' is not of type 'number'
    <BLANKLINE>
    Failed validating 'type' in schema:
        {'type': 'number'}
    <BLANKLINE>
    On instance:
        '789'
    """

    def _check_if_in_schemas(arg_name, value):
        if arg_name in schemas:
            try:
                check(value, schemas[arg_name])
            except js.ValidationError as e:
                raise ArgValidationError(arg_name, e)

    def check_wrapped(wrapped):
        arg_names = inspect.getargspec(wrapped)

        # Check if every arg in the schema corresponds to an actual arg in the
        # function.
        for arg_name in schemas:
            if arg_name not in arg_names.args:
                raise Exception("defined schema for inexistent argument: " +
                                arg_name)

        # Check the types of the default values of the function.
        defaulted_args = arg_names.args[-len(arg_names.defaults):]
        i = 0
        while i < len(defaulted_args):
            arg_name, def_value = defaulted_args[i], arg_names.defaults[i]
            _check_if_in_schemas(arg_name, def_value)
            i += 1

        def call(*args, **kwargs):
            # Check positional arguments.
            i = 0
            while i < len(args):
                arg_name, value_passed = arg_names.args[i], args[i]
                _check_if_in_schemas(arg_name, value_passed)
                i += 1
            # Check named arguments.
            for arg_name, value_passed in kwargs.items():
                _check_if_in_schemas(arg_name, value_passed)

            return wrapped(*args, **kwargs)

        return call
    return check_wrapped


class ArgValidationError(Exception):
    def __init__(self, arg_name, cause):
        msg = "Value passed to argument '%s' is not valid.\n%s"
        super(ArgValidationError, self).__init__(msg % (arg_name, cause))
        self.cause = cause
