"""
MPFR Multiprecision Floating-Point Numbers - Unit Tests
=======================================================

:Author: Caterina Urban
"""
import unittest
from copy import deepcopy

from apronpy.mpfr import PyMPFR


class TestPyMPFR(unittest.TestCase):

    def test_initialization_assignment_conversion(self):
        self.assertEqual(str(PyMPFR(9)), '9.0')
        self.assertEqual(str(PyMPFR(-9)), '-9.0')

    def test_deepcopy(self):
        f0 = PyMPFR(9)
        f1 = deepcopy(f0)
        f2 = f0
        self.assertNotEqual(id(f0), id(f1))
        self.assertEqual(id(f0), id(f2))

    def test_arithmetic(self):
        self.assertEqual(PyMPFR(9) + PyMPFR(3), PyMPFR(9 + 3))
        self.assertEqual(PyMPFR(9) - PyMPFR(3), PyMPFR(9 - 3))
        self.assertEqual(PyMPFR(9) * PyMPFR(3), PyMPFR(9 * 3))
        self.assertEqual(-PyMPFR(9), PyMPFR(-9))
        self.assertEqual(abs(PyMPFR(-9)), PyMPFR(abs(-9)))

    def test_comparison(self):
        self.assertTrue(PyMPFR(3) < PyMPFR(9))
        self.assertTrue(PyMPFR(3) <= PyMPFR(9))
        self.assertTrue(PyMPFR(9) <= PyMPFR(9))
        self.assertTrue(PyMPFR(9) == PyMPFR(9))
        self.assertTrue(PyMPFR(3) != PyMPFR(9))
        self.assertTrue(PyMPFR(9) >= PyMPFR(9))
        self.assertTrue(PyMPFR(9) >= PyMPFR(3))
        self.assertTrue(PyMPFR(9) > PyMPFR(3))


if __name__ == '__main__':
    unittest.main()
