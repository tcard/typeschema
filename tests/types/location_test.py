import unittest
import typeschema.types.location
import doctest


class TestCase(unittest.TestCase):
    def test_types_location_doc(self):
        fails, tested = doctest.testmod(typeschema.types.location)
        if fails > 0:
            self.fail('Doctest failed!')
