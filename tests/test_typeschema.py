import unittest
import typeschema
import typeschema.properties
import typeschema.properties.location
import typeschema.decorators
import typeschema.types.location
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

    def test_properties_location_doc(self):
        fails, tested = doctest.testmod(typeschema.properties.location)
        if fails > 0:
            self.fail('Doctest failed!')

    def test_decorators_doc(self):
        fails, tested = doctest.testmod(typeschema.decorators)
        if fails > 0:
            self.fail('Doctest failed!')

    def test_types_location_doc(self):
        fails, tested = doctest.testmod(typeschema.types.location)
        if fails > 0:
            self.fail('Doctest failed!')
