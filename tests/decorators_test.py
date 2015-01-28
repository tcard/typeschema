import doctest
import unittest

import typeschema.decorators


class TestCase(unittest.TestCase):
    def test_decorators_doc(self):
        fails, tested = doctest.testmod(typeschema.decorators)
        if fails > 0:
            self.fail('Doctest failed!')
