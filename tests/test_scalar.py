"""
APRON Scalar Numbers - Unit Tests
=================================

:Author: Caterina Urban
"""
import unittest
from copy import deepcopy
from ctypes import c_double

from apronpy.mpfr import PyMPFR
from apronpy.mpq import PyMPQ
from apronpy.scalar import PyDoubleScalar, PyMPQScalar, PyMPFRScalar


class TestPyDoubleScalar(unittest.TestCase):

    def test_init(self):
        self.assertEqual(str(PyDoubleScalar()), '0.0')
        self.assertEqual(str(PyDoubleScalar(0)), '0.0')
        self.assertEqual(str(PyDoubleScalar(0.0)), '0.0')
        self.assertEqual(str(PyDoubleScalar(c_double(0))), '0.0')
        self.assertEqual(str(PyDoubleScalar(c_double(0.0))), '0.0')
        self.assertEqual(str(PyDoubleScalar(-9)), '-9.0')
        self.assertEqual(str(PyDoubleScalar(c_double(-9))), '-9.0')
        self.assertEqual(str(PyDoubleScalar(9)), '9.0')
        self.assertEqual(str(PyDoubleScalar(c_double(9))), '9.0')
        self.assertEqual(str(PyDoubleScalar(0.5)), '0.5')
        self.assertEqual(str(PyDoubleScalar(c_double(0.5))), '0.5')
        self.assertEqual(str(PyDoubleScalar.init_infty(-9)), '-inf')
        self.assertEqual(str(PyDoubleScalar.init_infty(0)), '0.0')
        self.assertEqual(str(PyDoubleScalar.init_infty(9)), 'inf')

    def test_infty(self):
        self.assertEqual(PyDoubleScalar(9).infty(), 0)
        self.assertEqual(PyDoubleScalar.init_infty(-9).infty(), -1)
        self.assertEqual(PyDoubleScalar.init_infty(0).infty(), 0)
        self.assertEqual(PyDoubleScalar.init_infty(9).infty(), 1)

    def test_deepcopy(self):
        s0 = PyDoubleScalar(9)
        s1 = deepcopy(s0)
        s2 = s0
        self.assertNotEqual(id(s0), id(s1))
        self.assertEqual(id(s0), id(s2))

    def test_cmp(self):
        self.assertTrue(PyDoubleScalar(0.5) < PyDoubleScalar(9))
        self.assertTrue(PyDoubleScalar(9) == PyDoubleScalar(9))
        self.assertTrue(PyDoubleScalar(9) > PyDoubleScalar(0.5))

    def test_sign(self):
        self.assertEqual(PyDoubleScalar(-9).sign(), -1)
        self.assertEqual(PyDoubleScalar(c_double(-9)).sign(), -1)
        self.assertEqual(PyDoubleScalar(9).sign(), 1)
        self.assertEqual(PyDoubleScalar(c_double(9)).sign(), 1)
        self.assertEqual(PyDoubleScalar(0).sign(), 0)
        self.assertEqual(PyDoubleScalar(c_double(0)).sign(), 0)
        self.assertEqual(PyDoubleScalar.init_infty(-9).sign(), -1)
        self.assertEqual(PyDoubleScalar.init_infty(0).sign(), 0)
        self.assertEqual(PyDoubleScalar.init_infty(9).sign(), 1)

    def test_neg(self):
        self.assertEqual(-PyDoubleScalar(-9), PyDoubleScalar(9))
        self.assertEqual(-PyDoubleScalar(c_double(-9)), PyDoubleScalar(c_double(9)))
        self.assertEqual(-PyDoubleScalar(9), PyDoubleScalar(-9))
        self.assertEqual(-PyDoubleScalar(c_double(9)), PyDoubleScalar(c_double(-9)))
        self.assertEqual(-PyDoubleScalar(0), PyDoubleScalar(0))
        self.assertEqual(-PyDoubleScalar(c_double(0)), PyDoubleScalar(c_double(0)))
        self.assertEqual(-PyDoubleScalar.init_infty(-9), PyDoubleScalar.init_infty(9))
        self.assertEqual(-PyDoubleScalar.init_infty(0), PyDoubleScalar.init_infty(0))
        self.assertEqual(-PyDoubleScalar.init_infty(9), PyDoubleScalar.init_infty(-9))


class TestPyMPQScalar(unittest.TestCase):

    def test_initialization(self):
        self.assertEqual(str(PyMPQScalar()), '0')
        self.assertEqual(str(PyMPQScalar(0)), '0')
        self.assertEqual(str(PyMPQScalar(0, 1)), '0')
        self.assertEqual(str(PyMPQScalar(PyMPQ(0))), '0')
        self.assertEqual(str(PyMPQScalar(PyMPQ(0, 1))), '0')
        self.assertEqual(str(PyMPQScalar(-9)), '-9')
        self.assertEqual(str(PyMPQScalar(PyMPQ(-9))), '-9')
        self.assertEqual(str(PyMPQScalar(9)), '9')
        self.assertEqual(str(PyMPQScalar(PyMPQ(9))), '9')
        self.assertEqual(str(PyMPQScalar(1, 2)), '1/2')
        self.assertEqual(str(PyMPQScalar(PyMPQ(1, 2))), '1/2')
        self.assertEqual(str(PyMPQScalar.init_infty(-9)), '-9/0')
        self.assertEqual(str(PyMPQScalar.init_infty(0)), '0')
        self.assertEqual(str(PyMPQScalar.init_infty(9)), '9/0')
    
    def test_infty(self):
        self.assertEqual(PyMPQScalar(9).infty(), 0)
        self.assertEqual(PyMPQScalar.init_infty(-9).infty(), -1)
        self.assertEqual(PyMPQScalar.init_infty(0).infty(), 0)
        self.assertEqual(PyMPQScalar.init_infty(9).infty(), 1)

    def test_deepcopy(self):
        s0 = PyMPQScalar(9)
        s1 = deepcopy(s0)
        s2 = s0
        self.assertNotEqual(id(s0), id(s1))
        self.assertEqual(id(s0), id(s2))

    def test_cmp(self):
        self.assertTrue(PyMPQScalar(1, 2) < PyMPQScalar(9))
        self.assertTrue(PyMPQScalar(9) == PyMPQScalar(9))
        self.assertTrue(PyMPQScalar(9) > PyMPQScalar(1, 2))

    def test_sign(self):
        self.assertEqual(PyMPQScalar(-9).sign(), -1)
        self.assertEqual(PyMPQScalar(PyMPQ(-9)).sign(), -1)
        self.assertEqual(PyMPQScalar(9).sign(), 1)
        self.assertEqual(PyMPQScalar(PyMPQ(9)).sign(), 1)
        self.assertEqual(PyMPQScalar(0).sign(), 0)
        self.assertEqual(PyMPQScalar(PyMPQ(0)).sign(), 0)
        self.assertEqual(PyMPQScalar.init_infty(-9).sign(), -1)
        self.assertEqual(PyMPQScalar.init_infty(0).sign(), 0)
        self.assertEqual(PyMPQScalar.init_infty(9).sign(), 1)


class TestPyMPFRScalar(unittest.TestCase):

    def test_init(self):
        self.assertEqual(str(PyMPFRScalar(0)), '0.0')
        self.assertEqual(str(PyMPFRScalar(0.0)), '0.0')
        self.assertEqual(str(PyMPFRScalar(PyMPFR(0))), '0.0')
        self.assertEqual(str(PyMPFRScalar(PyMPFR(0.0))), '0.0')
        self.assertEqual(str(PyMPFRScalar(-9)), '-9.0')
        self.assertEqual(str(PyMPFRScalar(PyMPFR(-9))), '-9.0')
        self.assertEqual(str(PyMPFRScalar(9)), '9.0')
        self.assertEqual(str(PyMPFRScalar(PyMPFR(9))), '9.0')
        self.assertEqual(str(PyMPFRScalar(0.5)), '0.5')
        self.assertEqual(str(PyMPFRScalar(PyMPFR(0.5))), '0.5')
        self.assertEqual(str(PyMPFRScalar.init_infty(-9)), '-inf')
        self.assertEqual(str(PyMPFRScalar.init_infty(0)), 'inf')  # !
        self.assertEqual(str(PyMPFRScalar.init_infty(9)), 'inf')

    def test_infty(self):
        self.assertEqual(PyMPFRScalar(9).infty(), 0)
        self.assertEqual(PyMPFRScalar.init_infty(-9).infty(), -1)
        self.assertEqual(PyMPFRScalar.init_infty(0).infty(), 1)  # !
        self.assertEqual(PyMPFRScalar.init_infty(9).infty(), 1)

    def test_deepcopy(self):
        s0 = PyMPFRScalar(9)
        s1 = deepcopy(s0)
        s2 = s0
        self.assertNotEqual(id(s0), id(s1))
        self.assertEqual(id(s0), id(s2))

    def test_cmp(self):
        self.assertTrue(PyMPFRScalar(0.5) < PyMPFRScalar(9))
        self.assertTrue(PyMPFRScalar(9) == PyMPFRScalar(9))
        self.assertTrue(PyMPFRScalar(9) > PyMPFRScalar(0.5))

    def test_sign(self):
        self.assertEqual(PyMPFRScalar(-9).sign(), -1)
        self.assertEqual(PyMPFRScalar(PyMPFR(-9)).sign(), -1)
        self.assertEqual(PyMPFRScalar(9).sign(), 1)
        self.assertEqual(PyMPFRScalar(PyMPFR(9)).sign(), 1)
        self.assertEqual(PyMPFRScalar(0).sign(), 0)
        self.assertEqual(PyMPFRScalar(PyMPFR(0)).sign(), 0)
        self.assertEqual(PyMPFRScalar.init_infty(-9).sign(), -1)
        self.assertEqual(PyMPFRScalar.init_infty(0).sign(), 1)  # !
        self.assertEqual(PyMPFRScalar.init_infty(9).sign(), 1)

    def test_neg(self):
        self.assertEqual(-PyMPFRScalar(-9), PyMPFRScalar(9))
        self.assertEqual(-PyMPFRScalar(PyMPFR(-9)), PyMPFRScalar(PyMPFR(9)))
        self.assertEqual(-PyMPFRScalar(9), PyMPFRScalar(-9))
        self.assertEqual(-PyMPFRScalar(PyMPFR(9)), PyMPFRScalar(PyMPFR(-9)))
        self.assertEqual(-PyMPFRScalar(0), PyMPFRScalar(0))
        self.assertEqual(-PyMPFRScalar(PyMPFR(0)), PyMPFRScalar(PyMPFR(0)))
        self.assertEqual(-PyMPFRScalar.init_infty(-9), PyMPFRScalar.init_infty(9))
        self.assertNotEqual(-PyMPFRScalar.init_infty(0), PyMPFRScalar.init_infty(0))  # !
        self.assertEqual(-PyMPFRScalar.init_infty(9), PyMPFRScalar.init_infty(-9))


if __name__ == '__main__':
    unittest.main()
