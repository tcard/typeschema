import unittest
import typeschema.types.time
import doctest


class TestCase(unittest.TestCase):
    def test_types_time_doc(self):
        fails, tested = doctest.testmod(typeschema.types.time,
                                        optionflags=doctest.ELLIPSIS)
        if fails > 0:
            self.fail('Doctest failed!')
