"""
typeschema.decorators provides function decorators based on typeschema.
"""

import inspect
import typeschema


def check_args(schemas, check_function=typeschema.check):
    """
    Decorate a function, checking the schema of its arguments.

    Args:
        schemas: A dictionary <name of the argument>: <JSON schema>.
        check_function: A function that takes a value and a JSON schema and
                        throws a ValidationError.

    Raises:
        typeschema.ValidatonError

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
                check_function(value, schemas[arg_name])
            except typeschema.ValidationError as e:
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
        if arg_names.defaults:
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
