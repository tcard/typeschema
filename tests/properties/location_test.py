import unittest
import typeschema.properties.location
import doctest


class TestCase(unittest.TestCase):
    def test_properties_location_doc(self):
        fails, tested = doctest.testmod(typeschema.properties.location)
        if fails > 0:
            self.fail('Doctest failed!')
