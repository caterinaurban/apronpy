"""
APRON Intervals on Scalars - Unit Tests
=======================================

:Author: Caterina Urban
"""
import unittest
from ctypes import c_double

from apronpy.interval import PyDoubleInterval, PyMPQInterval, PyMPFRInterval
from apronpy.mpfr import PyMPFR
from apronpy.mpq import PyMPQ
from apronpy.scalar import PyDoubleScalar, PyMPQScalar, PyMPFRScalar


class TestDoubleInterval(unittest.TestCase):

    def test_init(self):
        self.assertEqual(str(PyDoubleInterval()), '[0.0,0.0]')
        self.assertEqual(str(PyDoubleInterval(0, 0)), '[0.0,0.0]')
        self.assertEqual(str(PyDoubleInterval(0.0, 0.0)), '[0.0,0.0]')
        self.assertEqual(str(PyDoubleInterval(c_double(0), c_double(0))), '[0.0,0.0]')
        self.assertEqual(str(PyDoubleInterval(c_double(0.0), c_double(0.0))), '[0.0,0.0]')
        self.assertEqual(str(PyDoubleInterval(PyDoubleScalar(0), PyDoubleScalar(0))), '[0.0,0.0]')
        self.assertEqual(
            str(PyDoubleInterval(PyDoubleScalar(0.0), PyDoubleScalar(0.0))), '[0.0,0.0]'
        )
        self.assertEqual(str(PyDoubleInterval(-0.5, 0.5)), '[-0.5,0.5]')
        self.assertEqual(str(PyDoubleInterval(c_double(-0.5), c_double(0.5))), '[-0.5,0.5]')
        self.assertEqual(
            str(PyDoubleInterval(PyDoubleScalar(-0.5), PyDoubleScalar(0.5))), '[-0.5,0.5]'
        )
        self.assertEqual(str(PyDoubleInterval.init_top()), '[-inf,inf]')
        self.assertEqual(str(PyDoubleInterval.init_bottom()), '[1.0,-1.0]')

    # def test_infty(self):
    #     self.assertEqual(PyDoubleScalar(9).infty(), 0)
    #     self.assertEqual(PyDoubleScalar.init_infty(-9).infty(), -1)
    #     self.assertEqual(PyDoubleScalar.init_infty(0).infty(), 0)
    #     self.assertEqual(PyDoubleScalar.init_infty(9).infty(), 1)
    #
    # def test_cmp(self):
    #     self.assertTrue(PyDoubleScalar(0.5) < PyDoubleScalar(9))
    #     self.assertTrue(PyDoubleScalar(9) == PyDoubleScalar(9))
    #     self.assertTrue(PyDoubleScalar(9) > PyDoubleScalar(0.5))
    #
    # def test_sign(self):
    #     self.assertEqual(PyDoubleScalar(-9).sign(), -1)
    #     self.assertEqual(PyDoubleScalar(c_double(-9)).sign(), -1)
    #     self.assertEqual(PyDoubleScalar(9).sign(), 1)
    #     self.assertEqual(PyDoubleScalar(c_double(9)).sign(), 1)
    #     self.assertEqual(PyDoubleScalar(0).sign(), 0)
    #     self.assertEqual(PyDoubleScalar(c_double(0)).sign(), 0)
    #     self.assertEqual(PyDoubleScalar.init_infty(-9).sign(), -1)
    #     self.assertEqual(PyDoubleScalar.init_infty(0).sign(), 0)
    #     self.assertEqual(PyDoubleScalar.init_infty(9).sign(), 1)
    #
    # def test_neg(self):
    #     self.assertEqual(-PyDoubleScalar(-9), PyDoubleScalar(9))
    #     self.assertEqual(-PyDoubleScalar(c_double(-9)), PyDoubleScalar(c_double(9)))
    #     self.assertEqual(-PyDoubleScalar(9), PyDoubleScalar(-9))
    #     self.assertEqual(-PyDoubleScalar(c_double(9)), PyDoubleScalar(c_double(-9)))
    #     self.assertEqual(-PyDoubleScalar(0), PyDoubleScalar(0))
    #     self.assertEqual(-PyDoubleScalar(c_double(0)), PyDoubleScalar(c_double(0)))
    #     self.assertEqual(-PyDoubleScalar.init_infty(-9), PyDoubleScalar.init_infty(9))
    #     self.assertEqual(-PyDoubleScalar.init_infty(0), PyDoubleScalar.init_infty(0))
    #     self.assertEqual(-PyDoubleScalar.init_infty(9), PyDoubleScalar.init_infty(-9))


class TestMPQInterval(unittest.TestCase):

    def test_init(self):
        self.assertEqual(str(PyMPQInterval()), '[0,0]')
        self.assertEqual(str(PyMPQInterval(0, 0)), '[0,0]')
        self.assertEqual(str(PyMPQInterval(0, 0, 1, 1)), '[0,0]')
        self.assertEqual(str(PyMPQInterval(PyMPQScalar(0), PyMPQScalar(0))), '[0,0]')
        self.assertEqual(str(PyMPQInterval(PyMPQScalar(0, 1), PyMPQScalar(0, 1))), '[0,0]')
        self.assertEqual(str(PyMPQInterval(-1, 1, 2, 2)), '[-1/2,1/2]')
        self.assertEqual(str(PyMPQInterval(PyMPQ(-1, 2), PyMPQ(1, 2))), '[-1/2,1/2]')
        self.assertEqual(str(PyMPQInterval(PyMPQScalar(-1, 2), PyMPQScalar(1, 2))), '[-1/2,1/2]')
        self.assertEqual(str(PyMPQInterval.init_top()), '[-1/0,1/0]')
        self.assertEqual(str(PyMPQInterval.init_bottom()), '[1,-1]')

    # def test_infty(self):
    #     self.assertEqual(PyDoubleScalar(9).infty(), 0)
    #     self.assertEqual(PyDoubleScalar.init_infty(-9).infty(), -1)
    #     self.assertEqual(PyDoubleScalar.init_infty(0).infty(), 0)
    #     self.assertEqual(PyDoubleScalar.init_infty(9).infty(), 1)
    #
    # def test_cmp(self):
    #     self.assertTrue(PyDoubleScalar(0.5) < PyDoubleScalar(9))
    #     self.assertTrue(PyDoubleScalar(9) == PyDoubleScalar(9))
    #     self.assertTrue(PyDoubleScalar(9) > PyDoubleScalar(0.5))
    #
    # def test_sign(self):
    #     self.assertEqual(PyDoubleScalar(-9).sign(), -1)
    #     self.assertEqual(PyDoubleScalar(c_double(-9)).sign(), -1)
    #     self.assertEqual(PyDoubleScalar(9).sign(), 1)
    #     self.assertEqual(PyDoubleScalar(c_double(9)).sign(), 1)
    #     self.assertEqual(PyDoubleScalar(0).sign(), 0)
    #     self.assertEqual(PyDoubleScalar(c_double(0)).sign(), 0)
    #     self.assertEqual(PyDoubleScalar.init_infty(-9).sign(), -1)
    #     self.assertEqual(PyDoubleScalar.init_infty(0).sign(), 0)
    #     self.assertEqual(PyDoubleScalar.init_infty(9).sign(), 1)
    #
    # def test_neg(self):
    #     self.assertEqual(-PyDoubleScalar(-9), PyDoubleScalar(9))
    #     self.assertEqual(-PyDoubleScalar(c_double(-9)), PyDoubleScalar(c_double(9)))
    #     self.assertEqual(-PyDoubleScalar(9), PyDoubleScalar(-9))
    #     self.assertEqual(-PyDoubleScalar(c_double(9)), PyDoubleScalar(c_double(-9)))
    #     self.assertEqual(-PyDoubleScalar(0), PyDoubleScalar(0))
    #     self.assertEqual(-PyDoubleScalar(c_double(0)), PyDoubleScalar(c_double(0)))
    #     self.assertEqual(-PyDoubleScalar.init_infty(-9), PyDoubleScalar.init_infty(9))
    #     self.assertEqual(-PyDoubleScalar.init_infty(0), PyDoubleScalar.init_infty(0))
    #     self.assertEqual(-PyDoubleScalar.init_infty(9), PyDoubleScalar.init_infty(-9))


class TestMPFRInterval(unittest.TestCase):

    def test_init(self):
        self.assertEqual(str(PyMPFRInterval(0, 0)), '[0.0,0.0]')
        self.assertEqual(str(PyMPFRInterval(0.0, 0.0)), '[0.0,0.0]')
        self.assertEqual(str(PyMPFRInterval(PyMPFRScalar(0), PyMPFRScalar(0))), '[0.0,0.0]')
        self.assertEqual(str(PyMPFRInterval(PyMPFRScalar(0.0), PyMPFRScalar(0.0))), '[0.0,0.0]')
        self.assertEqual(str(PyMPFRInterval(-0.5, 0.5)), '[-0.5,0.5]')
        self.assertEqual(str(PyMPFRInterval(PyMPFR(-0.5), PyMPFR(0.5))), '[-0.5,0.5]')
        self.assertEqual(str(PyMPFRInterval(PyMPFRScalar(-0.5), PyMPFRScalar(0.5))), '[-0.5,0.5]')
        self.assertEqual(str(PyMPFRInterval.init_top()), '[-inf,inf]')
        self.assertEqual(str(PyMPFRInterval.init_bottom()), '[1.0,-1.0]')

    # def test_infty(self):
    #     self.assertEqual(PyDoubleScalar(9).infty(), 0)
    #     self.assertEqual(PyDoubleScalar.init_infty(-9).infty(), -1)
    #     self.assertEqual(PyDoubleScalar.init_infty(0).infty(), 0)
    #     self.assertEqual(PyDoubleScalar.init_infty(9).infty(), 1)
    #
    # def test_cmp(self):
    #     self.assertTrue(PyDoubleScalar(0.5) < PyDoubleScalar(9))
    #     self.assertTrue(PyDoubleScalar(9) == PyDoubleScalar(9))
    #     self.assertTrue(PyDoubleScalar(9) > PyDoubleScalar(0.5))
    #
    # def test_sign(self):
    #     self.assertEqual(PyDoubleScalar(-9).sign(), -1)
    #     self.assertEqual(PyDoubleScalar(c_double(-9)).sign(), -1)
    #     self.assertEqual(PyDoubleScalar(9).sign(), 1)
    #     self.assertEqual(PyDoubleScalar(c_double(9)).sign(), 1)
    #     self.assertEqual(PyDoubleScalar(0).sign(), 0)
    #     self.assertEqual(PyDoubleScalar(c_double(0)).sign(), 0)
    #     self.assertEqual(PyDoubleScalar.init_infty(-9).sign(), -1)
    #     self.assertEqual(PyDoubleScalar.init_infty(0).sign(), 0)
    #     self.assertEqual(PyDoubleScalar.init_infty(9).sign(), 1)
    #
    # def test_neg(self):
    #     self.assertEqual(-PyDoubleScalar(-9), PyDoubleScalar(9))
    #     self.assertEqual(-PyDoubleScalar(c_double(-9)), PyDoubleScalar(c_double(9)))
    #     self.assertEqual(-PyDoubleScalar(9), PyDoubleScalar(-9))
    #     self.assertEqual(-PyDoubleScalar(c_double(9)), PyDoubleScalar(c_double(-9)))
    #     self.assertEqual(-PyDoubleScalar(0), PyDoubleScalar(0))
    #     self.assertEqual(-PyDoubleScalar(c_double(0)), PyDoubleScalar(c_double(0)))
    #     self.assertEqual(-PyDoubleScalar.init_infty(-9), PyDoubleScalar.init_infty(9))
    #     self.assertEqual(-PyDoubleScalar.init_infty(0), PyDoubleScalar.init_infty(0))
    #     self.assertEqual(-PyDoubleScalar.init_infty(9), PyDoubleScalar.init_infty(-9))


if __name__ == '__main__':
    unittest.main()
