"""
APRON Scalar Numbers - Unit Tests
=================================

:Author: Caterina Urban
"""
import unittest
from ctypes import c_double
from apronpy.mpq import PyMPQ
from apronpy.scalar import PyDoubleScalar, PyMPQScalar


class TestDoubleScalar(unittest.TestCase):

    def test_init(self):
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


class TestMPQScalar(unittest.TestCase):

    def test_initialization(self):
        self.assertEqual(str(PyMPQScalar(-9)), '-9/1')
        self.assertEqual(str(PyMPQScalar(PyMPQ(-9))), '-9/1')
        self.assertEqual(str(PyMPQScalar(9)), '9/1')
        self.assertEqual(str(PyMPQScalar(PyMPQ(9))), '9/1')
        self.assertEqual(str(PyMPQScalar(1, 2)), '1/2')
        self.assertEqual(str(PyMPQScalar(PyMPQ(1, 2))), '1/2')
        self.assertEqual(str(PyMPQScalar.init_infty(-9)), '-9/0')
        self.assertEqual(str(PyMPQScalar.init_infty(0)), '0/1')
        self.assertEqual(str(PyMPQScalar.init_infty(9)), '9/0')
    
    def test_infty(self):
        self.assertEqual(PyMPQScalar(9).infty(), 0)
        self.assertEqual(PyMPQScalar.init_infty(-9).infty(), -1)
        self.assertEqual(PyMPQScalar.init_infty(0).infty(), 0)
        self.assertEqual(PyMPQScalar.init_infty(9).infty(), 1)

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


if __name__ == '__main__':
    unittest.main()
