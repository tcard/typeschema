"""
networking related types:

>>> from typeschema import Checker
>>> checker = Checker()
>>> checker.extend(typeschema.types.network.types)
>>> checker.check("127.0.0.1", {'type': 'ip'})
>>> checker.check("Foo", {'type': 'ip'})
Traceback (most recent call last):
    ...
ValidationError: 'Foo' is not of type 'ip'
<BLANKLINE>
Failed validating 'type' in schema:
    {'type': 'ip'}
<BLANKLINE>
On instance:
    'Foo'
"""

import typeschema
import socket


def is_ip(value):
    try:
        socket.inet_aton(value)
        return True
    except:
        return False


types = {
    'ip': is_ip
}
