"""
Typeschema types for dates and times.

The type ``datetime`` accepts instances of ``datetime`` from the ``datetime``
module; an ``int`` or a ``float`` with a Unix timestamp in seconds; or a
``str`` conforming to ISO 8601 for UTC times (``yyyy-mm-ddThh:mm:ssZ``).

>>> import typeschema
>>> checker = typeschema.Checker()
>>> checker.extend(typeschema.types.time.types)
>>> checker.check(12345, {'type': 'datetime'})
>>> from datetime import datetime
>>> checker.check(datetime.utcnow(), {'type': 'datetime'})
>>> checker.check('2012-04-23T18:25:43Z', {'type': 'datetime'})
>>> checker.check('Foo', {'type': 'datetime'})
Traceback (most recent call last):
    ...
ValidationError: ...

The type ``date`` accepts instances of ``date`` and ``datetime`` from the
``datetime`` module; or a ``str`` conforming to ISO 8601 for dates
(``yyyy-mm-dd``).

>>> checker.check(datetime.utcnow(), {'type': 'date'})
>>> checker.check(datetime.utcnow().date(), {'type': 'date'})
>>> checker.check('2012-04-23', {'type': 'date'})
>>> checker.check('2012-04-23T18:25:43Z', {'type': 'date'})
Traceback (most recent call last):
    ...
ValidationError: ...
>>> checker.check(datetime.utcnow().time(), {'type': 'date'})
Traceback (most recent call last):
    ...
ValidationError: ...

The type ``time`` accepts instances of ``time`` from the ``datetime`` module;
or a ``str`` conforming to ISO 8601 for UTC times (``hh:mm:ss``).

>>> checker.check(datetime.utcnow(), {'type': 'time'})
Traceback (most recent call last):
    ...
ValidationError: ...
>>> checker.check(datetime.utcnow().time(), {'type': 'time'})
>>> checker.check('18:25:43', {'type': 'time'})
"""

import datetime as dt


def is_datetime(value):
    if any(isinstance(value, t) for t in [int, float, dt.datetime]):
        return True
    try:
        dt.datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
        return True
    except ValueError:
        return False


def is_date(value):
    if any(isinstance(value, t) for t in [dt.date, dt.datetime]):
        return True
    try:
        dt.datetime.strptime(value, '%Y-%m-%d')
        return True
    except ValueError:
        return False


def is_time(value):
    if isinstance(value, dt.time):
        return True
    try:
        dt.datetime.strptime(value, '%H:%M:%S')
        return True
    except ValueError:
        return False

types = {
    'datetime': is_datetime,
    'date': is_date,
    'time': is_time,
}
