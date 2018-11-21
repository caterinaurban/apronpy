"""
GMP Multi-Precision Rationals - Unit Tests
==========================================

:Author: Caterina Urban
"""
import unittest
from apronpy.mpq import PyMPQ


class TestMPQ(unittest.TestCase):

    def test_initialization_assignment_conversion(self):
        self.assertEqual(str(PyMPQ(0.5)), '1/2')

    def test_arithmetic(self):
        self.assertEqual(PyMPQ(0.5) + PyMPQ(0.25), PyMPQ(0.5 + 0.25))
        self.assertEqual(PyMPQ(0.5) - PyMPQ(0.25), PyMPQ(0.5 - 0.25))
        self.assertEqual(PyMPQ(0.5) * PyMPQ(0.25), PyMPQ(0.5 * 0.25))
        self.assertEqual(-PyMPQ(0.5), PyMPQ(-0.5))
        self.assertEqual(abs(PyMPQ(-0.5)), PyMPQ(abs(-0.5)))

    def test_comparison(self):
        self.assertTrue(PyMPQ(0.25) < PyMPQ(0.5))
        self.assertTrue(PyMPQ(0.25) <= PyMPQ(0.5))
        self.assertTrue(PyMPQ(0.5) <= PyMPQ(0.5))
        self.assertTrue(PyMPQ(0.5) == PyMPQ(0.5))
        self.assertTrue(PyMPQ(0.25) != PyMPQ(0.5))
        self.assertTrue(PyMPQ(0.5) >= PyMPQ(0.5))
        self.assertTrue(PyMPQ(0.5) >= PyMPQ(0.25))
        self.assertTrue(PyMPQ(0.5) > PyMPQ(0.25))


if __name__ == '__main__':
    unittest.main()
