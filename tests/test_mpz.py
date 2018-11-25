"""
GMP Multi-Precision Integers - Unit Tests
=========================================

:Author: Caterina Urban
"""
import unittest
from apronpy.mpz import PyMPZ


class TestMPZ(unittest.TestCase):

    def test_initialization_assignment_conversion(self):
        self.assertEqual(str(PyMPZ()), '0')
        self.assertEqual(str(PyMPZ(0.0)), '0')
        self.assertEqual(str(PyMPZ(9)), '9')

    def test_arithmetic(self):
        self.assertEqual(PyMPZ(9) + PyMPZ(3), PyMPZ(9 + 3))
        self.assertEqual(PyMPZ(9) - PyMPZ(3), PyMPZ(9 - 3))
        self.assertEqual(PyMPZ(9) * PyMPZ(3), PyMPZ(9 * 3))
        self.assertEqual(-PyMPZ(9), PyMPZ(-9))
        self.assertEqual(abs(PyMPZ(-9)), PyMPZ(abs(-9)))

    def test_comparison(self):
        self.assertTrue(PyMPZ(3) < PyMPZ(9))
        self.assertTrue(PyMPZ(3) <= PyMPZ(9))
        self.assertTrue(PyMPZ(9) <= PyMPZ(9))
        self.assertTrue(PyMPZ(9) == PyMPZ(9))
        self.assertTrue(PyMPZ(3) != PyMPZ(9))
        self.assertTrue(PyMPZ(9) >= PyMPZ(9))
        self.assertTrue(PyMPZ(9) >= PyMPZ(3))
        self.assertTrue(PyMPZ(9) > PyMPZ(3))


if __name__ == '__main__':
    unittest.main()
