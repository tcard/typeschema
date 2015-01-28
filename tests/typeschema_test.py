import doctest
import unittest

import typeschema


class TestCase(unittest.TestCase):
    def test_doc(self):
        fails, tested = doctest.testmod(typeschema.typeschema)
        if fails > 0:
            self.fail('Doctest failed!')
