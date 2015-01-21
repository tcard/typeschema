"""
networking related types:

>>> from typeschema import Checker
>>> checker = Checker()
>>> checker.extend(typeschema.types.network)
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
import struct


def is_ip(value, definition):
    try:
        struct.unpack("!L", socket.inet_aton(value))[0]
    except:
        raise typeschema.ValidationError("Invalid IP address")


types = {
    'ip': [{}, is_ip]
}
