import unittest
import typeschema.properties.ip
import doctest


class TestCase(unittest.TestCase):
    def test_properties_location_doc(self):
        fails, tested = doctest.testmod(typeschema.properties.ip)
        if fails > 0:
            self.fail('Doctest failed!')
