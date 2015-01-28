import doctest
import unittest

import typeschema.types.network


class TestCase(unittest.TestCase):
    def test_types_location_doc(self):
        fails, tested = doctest.testmod(typeschema.types.network)
        if fails > 0:
            self.fail('Doctest failed!')
