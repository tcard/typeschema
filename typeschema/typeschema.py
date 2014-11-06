"""
typeschema is a wrapper for jsonschema that provides some helpers, a simpler
interface, and lets the user define its own types.
"""

import jsonschema as js

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

        if "to_validate" in dir(value):
            value = value.to_validate()

        self.validator(schema).validate(value)

    def define(self, name, definition, checker=None):
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
            return

        if not checker:
            checker = self.check

        # The jsonschema library only lets you define custom types with
        # Python types, that is, you have to pass a class or a type.
        # But we want to define new types with JSON schemas.
        # This creates a dummy type that overrides isinstance so that
        # when jsonschema checks if a value is an instance of this type,
        # a normal check happens with that value against the provided
        # schema.
        # Sorry for the black magic.

        class DefinedTypeMeta(type):
            def __instancecheck__(self, value):
                try:
                    checker(value, definition)
                    return True
                except:
                    return False

        class DefinedType(object):
            __metaclass__ = DefinedTypeMeta

        self.validator.DEFAULT_TYPES[unicode(name)] = DefinedType

    def extend(self, module):
        """
        Extends the checker defining the types from the module.

        >>> class MyModule:
        ...     types = {'foo': [{'type': 'integer', 'minimum': 10}]}
        >>> checker = Checker()
        >>> checker.extend(MyModule)
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

        Args:
            module: module with property types
        """

        for k in module.types.keys():
            self.define(k, *module.types[k])


class FrozenChecker(Checker):
    """
    A Checker that doesn't allow any further type definition.
    """
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
