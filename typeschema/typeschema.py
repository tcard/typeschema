"""
typeschema is a wrapper for jsonschema that provides some helpers, a simpler
interface, and lets the user define its own types.
"""

import jsonschema as js


class Checker(object):
    """
    A Checker wraps a jsonschema.Draft4Validator, allowing the user to define
    custom types.
    """

    def __init__(self):
        self._validator = js.validators.extend(js.Draft4Validator, {})

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

        if "to_validate" in dir(value):
            value = value.to_validate()

        self._validator(schema).validate(value)

    def define(self, name, definition):
        """
        Define a custom type for this checker.

        Args:
            name: An identifier for the type.
            definition: Either a JSON schema, a custom Python type (including
                classes), or a function that takes a value and returns `bool`.

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

        You can also pass a type:

        >>> from datetime import datetime
        >>> checker.define('date_time', datetime)
        >>> checker.check(datetime.now(), {'type': 'date_time'})

        Or a function that takes a value and returns ``bool``:

        >>> checker.define('even', lambda x: x % 2 == 0)
        >>> checker.check(2, {'type': 'even'})
        >>> checker.check(3, {'type': 'even'})
        Traceback (most recent call last):
            ...
        ValidationError: 3 is not of type 'even'
        <BLANKLINE>
        Failed validating 'type' in schema:
            {'type': 'even'}
        <BLANKLINE>
        On instance:
            3
        """

        if isinstance(definition, type):
            self._validator.DEFAULT_TYPES[unicode(name)] = definition
            return

        # The jsonschema library only lets you define custom types with
        # Python types, that is, you have to pass a class or a type.
        # But we want to define new types with JSON schemas, and functions.
        # This creates a dummy type that overrides isinstance so that
        # when jsonschema checks if a value is an instance of this type,
        # a normal check happens with that value against the provided
        # schema.
        # Sorry for the black magic.

        check = self.check

        class DefinedTypeMeta(type):
            if callable(definition):
                def __instancecheck__(self, value):
                    try:
                        return True if definition(value) else False
                    except:
                        return False
            else:
                def __instancecheck__(self, value):
                    try:
                        check(value, definition)
                        return True
                    except:
                        return False

        class DefinedType(object):
            __metaclass__ = DefinedTypeMeta

        self._validator.DEFAULT_TYPES[unicode(name)] = DefinedType

    def extend(self, types):
        """
        Defines several types at once.

        Args:
            types: A dictionary of type definitions indexed by name.

        >>> class MyModule:
        ...     types = {'foo': {'type': 'integer', 'minimum': 10}}
        >>> checker = Checker()
        >>> checker.extend(MyModule.types)
        >>> checker.check(20, {'type': 'foo'})
        >>> checker.check(5, {'type': 'foo'})
        Traceback (most recent call last):
            ...
        ValidationError: 5 is not of type 'foo'
        <BLANKLINE>
        Failed validating 'type' in schema:
            {'type': 'foo'}
        <BLANKLINE>
        On instance:
            5
        """

        for name, definition in types.iteritems():
            self.define(name, definition)

    def frozen(self):
        return FrozenChecker.from_checker(self)


class FrozenChecker(Checker):
    """
    A Checker that doesn't allow any further type definition.
    """

    @staticmethod
    def from_checker(other):
        frozen = FrozenChecker()
        for type, definition in other._validator.DEFAULT_TYPES.items():
            super(FrozenChecker, frozen).define(type, definition)
        return frozen

    def define(self, name, schema, check=None):
        raise Exception("can't add types to a frozen checker.")

checker = FrozenChecker()


def check(value, schema):
    """
    Wrapper for a default Checker().check(value, schema).
    """
    checker.check(value, schema)


ValidationError = js.ValidationError
SchemaError = js.SchemaError
FormatError = js.FormatError
UnknownType = js.validators.UnknownType
