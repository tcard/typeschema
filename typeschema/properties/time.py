import typeschema
from typeschema.properties import nullable
from typeschema.types.time import types
import datetime as dt


_checker = typeschema.Checker()
_checker.extend(types)
checker = _checker.frozen()
check = checker.check


class _time_property(nullable):
    def __init__(self, typename, name, default=None):
        super(_time_property, self).__init__(
            name,
            typename,
            default=default,
            check=check
        )
        self.default = self._convert(self.default)

    def _get_setter(self):
        schema = self.schema
        name = self.name
        check = self.check
        _convert = self._convert

        def setter(self, value):
            check(value, schema)
            self.__dict__[name] = _convert(value)

        return setter


class datetime(_time_property):
    """
    Defines a property for a class whose setter checks that the input is a date
    with a time as defined by :py:mod:`typeschema.types.time`.

    The getter always returns a `datetime.datetime`.

    >>> class MyClass(object):
    ...     my_attr = datetime('my_attr')
    >>> my = MyClass()
    >>> my.my_attr = 1358121157
    >>> my.my_attr
    datetime.datetime(2013, 1, ...)
    >>> my.my_attr = "2013-01-13T23:52:37Z"
    >>> my.my_attr
    datetime.datetime(2013, 1, ...)
    """
    def __init__(self, name, default=None):
        super(datetime, self).__init__('datetime', name, default=default)

    def _convert(self, value):
        if isinstance(value, int) or isinstance(value, float):
            value = dt.datetime.fromtimestamp(value)
        elif isinstance(value, basestring):
            value = dt.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        return value


class date(_time_property):
    """
    Defines a property for a class whose setter checks that the input is a date
    as defined by :py:mod:`typeschema.types.time`.

    The getter always returns a `datetime.date`.

    >>> class MyClass(object):
    ...     my_attr = date('my_attr')
    >>> my = MyClass()
    >>> my.my_attr = u"2013-01-13"
    >>> my.my_attr
    datetime.date(2013, 1, ...)
    >>> import datetime as dt
    >>> my.my_attr = dt.datetime.now()
    >>> my.my_attr
    datetime.date(...)
    """
    def __init__(self, name, default=None):
        super(date, self).__init__('date', name, default=default)

    def _convert(self, value):
        if isinstance(value, dt.datetime):
            value = value.date()
        elif isinstance(value, basestring):
            value = dt.datetime.strptime(value, '%Y-%m-%d').date()
        return value


class time(_time_property):
    """
    Defines a property for a class whose setter checks that the input is a time
    as defined by :py:mod:`typeschema.types.time`.

    The getter always returns a `datetime.time`.

    >>> class MyClass(object):
    ...     my_attr = time('my_attr')
    >>> my = MyClass()
    >>> my.my_attr = "23:52:37"
    >>> my.my_attr
    datetime.time(...)
    """
    def __init__(self, name, default=None):
        super(time, self).__init__('time', name, default=default)

    def _convert(self, value):
        if isinstance(value, basestring):
            value = dt.datetime.strptime(value, '%H:%M:%S').time()
        return value
