"""
GMP Multi-Precision Rationals - Unit Tests
==========================================

:Author: Caterina Urban
"""
import unittest
from copy import deepcopy

from apronpy.mpq import PyMPQ


class TestPyMPQ(unittest.TestCase):

    def test_initialization_assignment_conversion(self):
        self.assertEqual(str(PyMPQ()), '0')
        self.assertEqual(str(PyMPQ(0)), '0')
        self.assertEqual(str(PyMPQ(0.5)), '1/2')
        self.assertEqual(str(PyMPQ(0, 1)), '0')
        self.assertEqual(str(PyMPQ(1, 2)), '1/2')
        self.assertEqual(str(PyMPQ(2, 4)), '1/2')

    def test_deepcopy(self):
        q0 = PyMPQ(1, 2)
        q1 = deepcopy(q0)
        q2 = q0
        self.assertNotEqual(id(q0), id(q1))
        self.assertEqual(id(q0), id(q2))

    def test_arithmetic(self):
        self.assertEqual(PyMPQ(1, 2) + PyMPQ(1, 4), PyMPQ(3, 4))
        self.assertEqual(PyMPQ(1, 2) - PyMPQ(1, 4), PyMPQ(1, 4))
        self.assertEqual(PyMPQ(1, 2) * PyMPQ(1, 4), PyMPQ(1, 8))
        self.assertEqual(-PyMPQ(1, 2), PyMPQ(-1, 2))
        self.assertEqual(-PyMPQ(2, 4), PyMPQ(-1, 2))
        self.assertEqual(abs(PyMPQ(-1, 2)), PyMPQ(abs(-1), abs(2)))

    def test_comparison(self):
        self.assertTrue(PyMPQ(1, 4) < PyMPQ(1, 2))
        self.assertTrue(PyMPQ(1, 4) <= PyMPQ(1, 2))
        self.assertTrue(PyMPQ(1, 2) <= PyMPQ(1, 2))
        self.assertTrue(PyMPQ(1, 2) == PyMPQ(1, 2))
        self.assertTrue(PyMPQ(1, 4) != PyMPQ(1, 2))
        self.assertTrue(PyMPQ(1, 2) >= PyMPQ(1, 2))
        self.assertTrue(PyMPQ(1, 2) >= PyMPQ(1, 4))
        self.assertTrue(PyMPQ(1, 2) > PyMPQ(1, 4))


if __name__ == '__main__':
    unittest.main()
