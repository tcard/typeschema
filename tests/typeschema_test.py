import unittest
import typeschema
import doctest


class TestCase(unittest.TestCase):
    def test_doc(self):
        fails, tested = doctest.testmod(typeschema.typeschema)
        if fails > 0:
            self.fail('Doctest failed!')
