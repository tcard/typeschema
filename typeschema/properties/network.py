import typeschema.properties
import typeschema.types.location
import socket
import struct


checker = typeschema.Checker()
checker.extend(typeschema.types.location)
check = checker.check


class ip(typeschema.properties.int):
    """
    Defines a property for a class whose setter checks that the input is a
    valid ipv4 or None.

    >>> class MyClass(object):
    ...     my_attr = ip('my_attr', default='127.0.0.1')
    >>> my = MyClass()
    >>> my.my_attr
    '127.0.0.1'
    >>> my.my_attr = '8.8.8.8'
    >>> my.my_attr
    '8.8.8.8'
    >>> my.my_attr = 'Foo'
    Traceback (most recent call last):
        ...
    error: illegal IP address string passed to inet_aton
    """
    def __init__(self, name, default=None):
        super(typeschema.properties.int, self).__init__(
            name, 'ip', default=self._ip2log(default)
        )

    def _get_getter(self):
        name = self.name
        default = self.default

        def getter(self):
            long = self.__dict__.get(name, default)
            if not long:
                return None

            return socket.inet_ntoa(struct.pack('!L', long))

        return getter

    def _get_setter(self):
        parent = self
        parent_setter = super(ip, self)._get_setter()

        def setter(self, value):
            if value:
                value = parent._ip2log(value)

            parent_setter(self, value)

        return setter

    def _ip2log(self, ip):
        if ip:
            return struct.unpack("!L", socket.inet_aton(ip))[0]
