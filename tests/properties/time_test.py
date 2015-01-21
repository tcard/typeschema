import unittest
import typeschema.properties.time
import doctest


class TestCase(unittest.TestCase):
    def test_properties_datetime_doc(self):
        fails, tested = doctest.testmod(typeschema.properties.time,
                                        optionflags=doctest.ELLIPSIS)
        if fails > 0:
            self.fail('Doctest failed!')
