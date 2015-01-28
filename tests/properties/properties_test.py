import doctest
import unittest

import typeschema
import typeschema.properties as ty


class TestCase(unittest.TestCase):
    def test_properties_doc(self):
        fails, tested = doctest.testmod(ty)
        if fails > 0:
            self.fail('Doctest failed!')

    def test_mutable_default(self):
        l = [1, 2, 3]

        class MyClass(object):
            my_attr = ty.property('my_attr', {'type': 'array'}, default=l)

        a = MyClass()
        b = MyClass()

        a.my_attr.append(4)
        self.assertEqual(a.my_attr, [1, 2, 3, 4])
        self.assertEqual(b.my_attr, [1, 2, 3])
