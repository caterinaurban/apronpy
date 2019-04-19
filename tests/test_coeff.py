"""
APRON Coefficients - Unit Tests
===============================

:Author: Caterina Urban
"""
import unittest
from copy import deepcopy

from apronpy.coeff import PyDoubleScalarCoeff, PyMPQScalarCoeff, PyMPFRScalarCoeff, \
    PyDoubleIntervalCoeff, PyMPQIntervalCoeff, PyMPFRIntervalCoeff


class TestPyDoubleScalarCoeff(unittest.TestCase):
    
    def test_init(self):
        self.assertEqual(str(PyDoubleScalarCoeff()), '0.0')

    def test_deepcopy(self):
        c0 = PyDoubleScalarCoeff()
        c1 = deepcopy(c0)
        c2 = c0
        self.assertNotEqual(id(c0), id(c1))
        self.assertEqual(id(c0), id(c2))

    def test_cmp(self):
        self.assertTrue(PyDoubleScalarCoeff(-0.5) < PyDoubleScalarCoeff())
        self.assertFalse(PyDoubleScalarCoeff() < PyDoubleScalarCoeff(-0.5))
        self.assertTrue(PyDoubleScalarCoeff() == PyDoubleScalarCoeff(0))
        self.assertFalse(PyDoubleScalarCoeff() == PyDoubleScalarCoeff(-0.5))
        self.assertTrue(PyDoubleScalarCoeff() > PyDoubleScalarCoeff(-0.5))
        self.assertFalse(PyDoubleScalarCoeff(-0.5) > PyDoubleScalarCoeff())

    def test_neg(self):
        self.assertEqual(-PyDoubleScalarCoeff(-0.5), PyDoubleScalarCoeff(0.5))
        self.assertEqual(-PyDoubleScalarCoeff(0), PyDoubleScalarCoeff(0))
        self.assertEqual(-PyDoubleScalarCoeff(0.5), PyDoubleScalarCoeff(-0.5))


class TestPyMPQScalarCoeff(unittest.TestCase):

    def test_init(self):
        self.assertEqual(str(PyMPQScalarCoeff()), '0')

    def test_deepcopy(self):
        c0 = PyMPQScalarCoeff()
        c1 = deepcopy(c0)
        c2 = c0
        self.assertNotEqual(id(c0), id(c1))
        self.assertEqual(id(c0), id(c2))

    def test_cmp(self):
        self.assertTrue(PyMPQScalarCoeff(-1, 2) < PyMPQScalarCoeff())
        self.assertFalse(PyMPQScalarCoeff() < PyMPQScalarCoeff(-1, 2))
        self.assertTrue(PyMPQScalarCoeff() == PyMPQScalarCoeff(0))
        self.assertFalse(PyMPQScalarCoeff() == PyMPQScalarCoeff(-1, 2))
        self.assertTrue(PyMPQScalarCoeff() > PyMPQScalarCoeff(-1, 2))
        self.assertFalse(PyMPQScalarCoeff(-1, 2) > PyMPQScalarCoeff())

    def test_neg(self):
        self.assertEqual(-PyMPQScalarCoeff(-1, 2), PyMPQScalarCoeff(1, 2))
        self.assertEqual(-PyMPQScalarCoeff(0), PyMPQScalarCoeff(0))
        self.assertEqual(-PyMPQScalarCoeff(1, 2), PyMPQScalarCoeff(-1, 2))


class TestPyMPFRScalarCoeff(unittest.TestCase):

    def test_init(self):
        self.assertEqual(str(PyMPFRScalarCoeff(0)), '0.0')

    def test_deepcopy(self):
        c0 = PyMPFRScalarCoeff(0)
        c1 = deepcopy(c0)
        c2 = c0
        self.assertNotEqual(id(c0), id(c1))
        self.assertEqual(id(c0), id(c2))

    def test_cmp(self):
        self.assertTrue(PyMPFRScalarCoeff(-0.5) < PyMPFRScalarCoeff(0))
        self.assertFalse(PyMPFRScalarCoeff(0) < PyMPFRScalarCoeff(-0.5))
        self.assertTrue(PyMPFRScalarCoeff(0) == PyMPFRScalarCoeff(0))
        self.assertFalse(PyMPFRScalarCoeff(0) == PyMPFRScalarCoeff(-0.5))
        self.assertTrue(PyMPFRScalarCoeff(0) > PyMPFRScalarCoeff(-0.5))
        self.assertFalse(PyMPFRScalarCoeff(-0.5) > PyMPFRScalarCoeff(0))

    def test_neg(self):
        self.assertEqual(-PyMPFRScalarCoeff(-0.5), PyMPFRScalarCoeff(0.5))
        self.assertEqual(-PyMPFRScalarCoeff(0), PyMPFRScalarCoeff(0))
        self.assertEqual(-PyMPFRScalarCoeff(0.5), PyMPFRScalarCoeff(-0.5))


class TestPyDoubleIntervalCoeff(unittest.TestCase):

    def test_init(self):
        self.assertEqual(str(PyDoubleIntervalCoeff()), '[0.0,0.0]')

    def test_deepcopy(self):
        c0 = PyDoubleIntervalCoeff()
        c1 = deepcopy(c0)
        c2 = c0
        self.assertNotEqual(id(c0), id(c1))
        self.assertEqual(id(c0), id(c2))
        
    def test_cmp(self):
        self.assertTrue(PyDoubleIntervalCoeff() < PyDoubleIntervalCoeff(-0.5, 0.5))
        self.assertFalse(PyDoubleIntervalCoeff(-0.5, 0.5) < PyDoubleIntervalCoeff())
        self.assertTrue(PyDoubleIntervalCoeff() == PyDoubleIntervalCoeff(0))
        self.assertFalse(PyDoubleIntervalCoeff() == PyDoubleIntervalCoeff(-0.5, 0.5))
        self.assertTrue(PyDoubleIntervalCoeff(-0.5, 0.5) > PyDoubleIntervalCoeff())
        self.assertFalse(PyDoubleIntervalCoeff() > PyDoubleIntervalCoeff(-0.5, 0.5))

    def test_neg(self):
        self.assertEqual(-PyDoubleIntervalCoeff(-1, 2), PyDoubleIntervalCoeff(-2, 1))
        self.assertEqual(-PyDoubleIntervalCoeff(), PyDoubleIntervalCoeff(0, 0))
        self.assertEqual(-PyDoubleIntervalCoeff(1, 2), PyDoubleIntervalCoeff(-2, -1))


class TestPyMPQIntervalCoeff(unittest.TestCase):

    def test_init(self):
        self.assertEqual(str(PyMPQIntervalCoeff()), '[0,0]')

    def test_deepcopy(self):
        c0 = PyMPQIntervalCoeff()
        c1 = deepcopy(c0)
        c2 = c0
        self.assertNotEqual(id(c0), id(c1))
        self.assertEqual(id(c0), id(c2))
        
    def test_cmp(self):
        self.assertTrue(PyMPQIntervalCoeff() < PyMPQIntervalCoeff(-1, 1, 2, 2))
        self.assertFalse(PyMPQIntervalCoeff(-1, 1, 2, 2) < PyMPQIntervalCoeff())
        self.assertTrue(PyMPQIntervalCoeff() == PyMPQIntervalCoeff(0, 0))
        self.assertFalse(PyMPQIntervalCoeff() == PyMPQIntervalCoeff(-1, 1, 2, 2))
        self.assertTrue(PyMPQIntervalCoeff(-1, 1, 2, 2) > PyMPQIntervalCoeff())
        self.assertFalse(PyMPQIntervalCoeff() > PyMPQIntervalCoeff(-1, 1, 2, 2))

    def test_neg(self):
        self.assertEqual(-PyMPQIntervalCoeff(-1, 2), PyMPQIntervalCoeff(-2, 1))
        self.assertEqual(-PyMPQIntervalCoeff(), PyMPQIntervalCoeff(0, 0))
        self.assertEqual(-PyMPQIntervalCoeff(1, 2), PyMPQIntervalCoeff(-2, -1))


class TestPyMPFRIntervalCoeff(unittest.TestCase):

    def test_init(self):
        self.assertEqual(str(PyMPFRIntervalCoeff(0, 0)), '[0.0,0.0]')

    def test_deepcopy(self):
        c0 = PyMPFRIntervalCoeff(0, 0)
        c1 = deepcopy(c0)
        c2 = c0
        self.assertNotEqual(id(c0), id(c1))
        self.assertEqual(id(c0), id(c2))
        
    def test_cmp(self):
        self.assertTrue(PyMPFRIntervalCoeff(0, 0) < PyMPFRIntervalCoeff(-0.5, 0.5))
        self.assertFalse(PyMPFRIntervalCoeff(-0.5, 0.5) < PyMPFRIntervalCoeff(0, 0))
        self.assertTrue(PyMPFRIntervalCoeff(0, 0) == PyMPFRIntervalCoeff(0.0, 0.0))
        self.assertFalse(PyMPFRIntervalCoeff(0, 0) == PyMPFRIntervalCoeff(-0.5, 0.5))
        self.assertTrue(PyMPFRIntervalCoeff(-0.5, 0.5) > PyMPFRIntervalCoeff(0, 0))
        self.assertFalse(PyMPFRIntervalCoeff(0, 0) > PyMPFRIntervalCoeff(-0.5, 0.5))

    def test_neg(self):
        self.assertEqual(-PyMPFRIntervalCoeff(-1, 2), PyMPFRIntervalCoeff(-2, 1))
        self.assertEqual(-PyMPFRIntervalCoeff(0, 0), PyMPFRIntervalCoeff(0, 0))
        self.assertEqual(-PyMPFRIntervalCoeff(1, 2), PyMPFRIntervalCoeff(-2, -1))


if __name__ == '__main__':
    unittest.main()
