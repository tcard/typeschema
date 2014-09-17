import unittest
import typeschema


class TestCase(unittest.TestCase):
    def test_doc(self):
        import doctest
        fails, tested = doctest.testmod(typeschema)
        if fails > 0:
            self.fail('Doctest failed!')
