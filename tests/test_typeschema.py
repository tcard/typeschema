import unittest
import typeschema
import typeschema.properties
import doctest


class TestCase(unittest.TestCase):
    def test_doc(self):
        fails, tested = doctest.testmod(typeschema)
        if fails > 0:
            self.fail('Doctest failed!')

    def test_properties_doc(self):
        fails, tested = doctest.testmod(typeschema.properties)
        if fails > 0:
            self.fail('Doctest failed!')
