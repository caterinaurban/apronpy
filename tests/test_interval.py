"""
APRON Intervals on Scalars - Unit Tests
=======================================

:Author: Caterina Urban
"""
import unittest
from copy import deepcopy
from ctypes import c_double

from apronpy.interval import PyDoubleInterval, PyMPQInterval, PyMPFRInterval
from apronpy.mpfr import PyMPFR
from apronpy.mpq import PyMPQ
from apronpy.scalar import PyDoubleScalar, PyMPQScalar, PyMPFRScalar


class TestPyDoubleInterval(unittest.TestCase):

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
        self.assertEqual(str(PyDoubleInterval.top()), '[-inf,inf]')
        self.assertEqual(str(PyDoubleInterval.bottom()), '[1.0,-1.0]')

    def test_deepcopy(self):
        i0 = PyDoubleInterval(0, 0)
        i1 = deepcopy(i0)
        i2 = i0
        self.assertNotEqual(id(i0), id(i1))
        self.assertEqual(id(i0), id(i2))

    def test_is_bottom(self):
        self.assertFalse(PyDoubleInterval().is_bottom())
        self.assertFalse(PyDoubleInterval(0, 0).is_bottom())
        self.assertFalse(PyDoubleInterval(0.0, 0.0).is_bottom())
        self.assertFalse(PyDoubleInterval(c_double(0), c_double(0)).is_bottom())
        self.assertFalse(PyDoubleInterval(c_double(0.0), c_double(0.0)).is_bottom())
        self.assertFalse(PyDoubleInterval(PyDoubleScalar(0), PyDoubleScalar(0)).is_bottom())
        self.assertFalse(PyDoubleInterval(PyDoubleScalar(0.0), PyDoubleScalar(0.0)).is_bottom())
        self.assertFalse(PyDoubleInterval(-0.5, 0.5).is_bottom())
        self.assertFalse(PyDoubleInterval(c_double(-0.5), c_double(0.5)).is_bottom())
        self.assertFalse(PyDoubleInterval(PyDoubleScalar(-0.5), PyDoubleScalar(0.5)).is_bottom())
        self.assertFalse(PyDoubleInterval.top().is_bottom())
        self.assertTrue(PyDoubleInterval.bottom().is_bottom())
    
    def test_cmp(self):
        self.assertTrue(PyDoubleInterval.bottom() < PyDoubleInterval())
        self.assertFalse(PyDoubleInterval() < PyDoubleInterval.bottom())
        self.assertTrue(PyDoubleInterval() < PyDoubleInterval(-0.5, 0.5))
        self.assertFalse(PyDoubleInterval(-0.5, 0.5) < PyDoubleInterval())
        self.assertTrue(PyDoubleInterval(-0.5, 0.5) < PyDoubleInterval.top())
        self.assertFalse(PyDoubleInterval.top() < PyDoubleInterval(-0.5, 0.5))
        self.assertFalse(PyDoubleInterval.bottom() == PyDoubleInterval())
        self.assertTrue(PyDoubleInterval() == PyDoubleInterval(0, 0))
        self.assertFalse(PyDoubleInterval() == PyDoubleInterval(-0.5, 0.5))
        self.assertTrue(
            PyDoubleInterval(-0.5, 0.5) == PyDoubleInterval(c_double(-0.5), c_double(0.5))
        )
        self.assertFalse(PyDoubleInterval(-0.5, 0.5) == PyDoubleInterval.top())
        self.assertFalse(PyDoubleInterval.bottom() > PyDoubleInterval())
        self.assertTrue(PyDoubleInterval() > PyDoubleInterval.bottom())
        self.assertFalse(PyDoubleInterval() > PyDoubleInterval(-0.5, 0.5))
        self.assertTrue(PyDoubleInterval(-0.5, 0.5) > PyDoubleInterval())
        self.assertFalse(PyDoubleInterval(-0.5, 0.5) > PyDoubleInterval.top())
        self.assertTrue(PyDoubleInterval.top() > PyDoubleInterval(-0.5, 0.5))
        self.assertTrue(PyDoubleInterval(-3, -1) <= PyDoubleInterval(PyDoubleScalar.init_infty(-1), PyDoubleScalar(-1)))
    
    def test_is_top(self):
        self.assertFalse(PyDoubleInterval().is_top())
        self.assertFalse(PyDoubleInterval(0, 0).is_top())
        self.assertFalse(PyDoubleInterval(0.0, 0.0).is_top())
        self.assertFalse(PyDoubleInterval(c_double(0), c_double(0)).is_top())
        self.assertFalse(PyDoubleInterval(c_double(0.0), c_double(0.0)).is_top())
        self.assertFalse(PyDoubleInterval(PyDoubleScalar(0), PyDoubleScalar(0)).is_top())
        self.assertFalse(PyDoubleInterval(PyDoubleScalar(0.0), PyDoubleScalar(0.0)).is_top())
        self.assertFalse(PyDoubleInterval(-0.5, 0.5).is_top())
        self.assertFalse(PyDoubleInterval(c_double(-0.5), c_double(0.5)).is_top())
        self.assertFalse(PyDoubleInterval(PyDoubleScalar(-0.5), PyDoubleScalar(0.5)).is_top())
        self.assertTrue(PyDoubleInterval.top().is_top())
        self.assertFalse(PyDoubleInterval.bottom().is_top())

    def test_neg(self):
        self.assertEqual(-PyDoubleInterval.bottom(), PyDoubleInterval.bottom())
        self.assertEqual(-PyDoubleInterval(-1, 2), PyDoubleInterval(-2, 1))
        self.assertEqual(-PyDoubleInterval(), PyDoubleInterval(0, 0))
        self.assertEqual(
            -PyDoubleInterval(-0.5, 0.5), PyDoubleInterval(c_double(-0.5), c_double(0.5))
        )
        self.assertEqual(-PyDoubleInterval(1, 2), PyDoubleInterval(-2, -1))
        self.assertEqual(-PyDoubleInterval.top(), PyDoubleInterval.top())


class TestPyMPQInterval(unittest.TestCase):

    def test_init(self):
        self.assertEqual(str(PyMPQInterval()), '[0,0]')
        self.assertEqual(str(PyMPQInterval(0, 0)), '[0,0]')
        self.assertEqual(str(PyMPQInterval(0, 0, 1, 1)), '[0,0]')
        self.assertEqual(str(PyMPQInterval(PyMPQScalar(0), PyMPQScalar(0))), '[0,0]')
        self.assertEqual(str(PyMPQInterval(PyMPQScalar(0, 1), PyMPQScalar(0, 1))), '[0,0]')
        self.assertEqual(str(PyMPQInterval(-1, 1, 2, 2)), '[-1/2,1/2]')
        self.assertEqual(str(PyMPQInterval(PyMPQ(-1, 2), PyMPQ(1, 2))), '[-1/2,1/2]')
        self.assertEqual(str(PyMPQInterval(PyMPQScalar(-1, 2), PyMPQScalar(1, 2))), '[-1/2,1/2]')
        self.assertEqual(str(PyMPQInterval.top()), '[-1/0,1/0]')
        self.assertEqual(str(PyMPQInterval.bottom()), '[1,-1]')

    def test_deepcopy(self):
        i0 = PyMPQInterval(0, 0)
        i1 = deepcopy(i0)
        i2 = i0
        self.assertNotEqual(id(i0), id(i1))
        self.assertEqual(id(i0), id(i2))

    def test_is_bottom(self):
        self.assertFalse(PyMPQInterval().is_bottom())
        self.assertFalse(PyMPQInterval(0, 0).is_bottom())
        self.assertFalse(PyMPQInterval(0, 0, 1, 1).is_bottom())
        self.assertFalse(PyMPQInterval(PyMPQScalar(0), PyMPQScalar(0)).is_bottom())
        self.assertFalse(PyMPQInterval(PyMPQScalar(0, 1), PyMPQScalar(0, 1)).is_bottom())
        self.assertFalse(PyMPQInterval(-1, 1, 2, 2).is_bottom())
        self.assertFalse(PyMPQInterval(PyMPQ(-1, 2), PyMPQ(1, 2)).is_bottom())
        self.assertFalse(PyMPQInterval(PyMPQScalar(-1, 2), PyMPQScalar(1, 2)).is_bottom())
        self.assertFalse(PyMPQInterval.top().is_bottom())
        self.assertTrue(PyMPQInterval.bottom().is_bottom())

    def test_cmp(self):
        self.assertTrue(PyMPQInterval.bottom() < PyMPQInterval())
        self.assertFalse(PyMPQInterval() < PyMPQInterval.bottom())
        self.assertTrue(PyMPQInterval() < PyMPQInterval(-1, 1, 2, 2))
        self.assertFalse(PyMPQInterval(-1, 1, 2, 2) < PyMPQInterval())
        self.assertTrue(PyMPQInterval(-1, 1, 2, 2) < PyMPQInterval.top())
        self.assertFalse(PyMPQInterval.top() < PyMPQInterval(-1, 1, 2, 2))
        self.assertFalse(PyMPQInterval.bottom() == PyMPQInterval())
        self.assertTrue(PyMPQInterval() == PyMPQInterval(0, 0))
        self.assertFalse(PyMPQInterval() == PyMPQInterval(-1, 1, 2, 2))
        self.assertTrue(PyMPQInterval(-1, 1, 2, 2) == PyMPQInterval(PyMPQ(-1, 2), PyMPQ(1, 2)))
        self.assertFalse(PyMPQInterval(-1, 1, 2, 2) == PyMPQInterval.top())
        self.assertFalse(PyMPQInterval.bottom() > PyMPQInterval())
        self.assertTrue(PyMPQInterval() > PyMPQInterval.bottom())
        self.assertFalse(PyMPQInterval() > PyMPQInterval(-1, 1, 2, 2))
        self.assertTrue(PyMPQInterval(-1, 1, 2, 2) > PyMPQInterval())
        self.assertFalse(PyMPQInterval(-1, 1, 2, 2) > PyMPQInterval.top())
        self.assertTrue(PyMPQInterval.top() > PyMPQInterval(-1, 1, 2, 2))
        self.assertTrue(PyMPQInterval(-3, -1) <= PyMPQInterval(PyMPQScalar.init_infty(-1), PyMPQScalar(-1)))
    
    def test_is_top(self):
        self.assertFalse(PyMPQInterval().is_top())
        self.assertFalse(PyMPQInterval(0, 0).is_top())
        self.assertFalse(PyMPQInterval(0, 0, 1, 1).is_top())
        self.assertFalse(PyMPQInterval(PyMPQScalar(0), PyMPQScalar(0)).is_top())
        self.assertFalse(PyMPQInterval(PyMPQScalar(0, 1), PyMPQScalar(0, 1)).is_top())
        self.assertFalse(PyMPQInterval(-1, 1, 2, 2).is_top())
        self.assertFalse(PyMPQInterval(PyMPQ(-1, 2), PyMPQ(1, 2)).is_top())
        self.assertFalse(PyMPQInterval(PyMPQScalar(-1, 2), PyMPQScalar(1, 2)).is_top())
        self.assertTrue(PyMPQInterval.top().is_top())
        self.assertFalse(PyMPQInterval.bottom().is_top())
    
    def test_neg(self):
        self.assertEqual(-PyMPQInterval.bottom(), PyMPQInterval.bottom())
        self.assertEqual(-PyMPQInterval(-1, 2), PyMPQInterval(-2, 1))
        self.assertEqual(-PyMPQInterval(), PyMPQInterval(0, 0))
        self.assertEqual(-PyMPQInterval(-1, 1, 2, 2), PyMPQInterval(-PyMPQ(1, 2), PyMPQ(1, 2)))
        self.assertEqual(-PyMPQInterval(1, 1, 2, 2), PyMPQInterval(-PyMPQ(1, 2), -PyMPQ(1, 2)))
        self.assertEqual(-PyMPQInterval(1, 1, 2, 2), PyMPQInterval(PyMPQ(-1, 2), PyMPQ(-1, 2)))
        self.assertEqual(-PyMPQInterval(1, 2), PyMPQInterval(-2, -1))
        self.assertEqual(-PyMPQInterval.top(), PyMPQInterval.top())


class TestPyMPFRInterval(unittest.TestCase):

    def test_init(self):
        self.assertEqual(str(PyMPFRInterval(0, 0)), '[0.0,0.0]')
        self.assertEqual(str(PyMPFRInterval(0.0, 0.0)), '[0.0,0.0]')
        self.assertEqual(str(PyMPFRInterval(PyMPFRScalar(0), PyMPFRScalar(0))), '[0.0,0.0]')
        self.assertEqual(str(PyMPFRInterval(PyMPFRScalar(0.0), PyMPFRScalar(0.0))), '[0.0,0.0]')
        self.assertEqual(str(PyMPFRInterval(-0.5, 0.5)), '[-0.5,0.5]')
        self.assertEqual(str(PyMPFRInterval(PyMPFR(-0.5), PyMPFR(0.5))), '[-0.5,0.5]')
        self.assertEqual(str(PyMPFRInterval(PyMPFRScalar(-0.5), PyMPFRScalar(0.5))), '[-0.5,0.5]')
        self.assertEqual(str(PyMPFRInterval.top()), '[-inf,inf]')
        self.assertEqual(str(PyMPFRInterval.bottom()), '[1.0,-1.0]')

    def test_deepcopy(self):
        i0 = PyMPFRInterval(0, 0)
        i1 = deepcopy(i0)
        i2 = i0
        self.assertNotEqual(id(i0), id(i1))
        self.assertEqual(id(i0), id(i2))

    def test_is_bottom(self):
        self.assertFalse(PyMPFRInterval(0, 0).is_bottom())
        self.assertFalse(PyMPFRInterval(0.0, 0.0).is_bottom())
        self.assertFalse(PyMPFRInterval(PyMPFRScalar(0), PyMPFRScalar(0)).is_bottom())
        self.assertFalse(PyMPFRInterval(PyMPFRScalar(0.0), PyMPFRScalar(0.0)).is_bottom())
        self.assertFalse(PyMPFRInterval(-0.5, 0.5).is_bottom())
        self.assertFalse(PyMPFRInterval(PyMPFR(-0.5), PyMPFR(0.5)).is_bottom())
        self.assertFalse(PyMPFRInterval(PyMPFRScalar(-0.5), PyMPFRScalar(0.5)).is_bottom())
        self.assertFalse(PyMPFRInterval.top().is_bottom())
        self.assertTrue(PyMPFRInterval.bottom().is_bottom())
        
    def test_cmp(self):
        self.assertTrue(PyMPFRInterval.bottom() < PyMPFRInterval(0, 0))
        self.assertFalse(PyMPFRInterval(0, 0) < PyMPFRInterval.bottom())
        self.assertTrue(PyMPFRInterval(0, 0) < PyMPFRInterval(-0.5, 0.5))
        self.assertFalse(PyMPFRInterval(-0.5, 0.5) < PyMPFRInterval(0, 0))
        self.assertTrue(PyMPFRInterval(-0.5, 0.5) < PyMPFRInterval.top())
        self.assertFalse(PyMPFRInterval.top() < PyMPFRInterval(-0.5, 0.5))
        self.assertFalse(PyMPFRInterval.bottom() == PyMPFRInterval(0, 0))
        self.assertTrue(PyMPFRInterval(0, 0) == PyMPFRInterval(0, 0))
        self.assertFalse(PyMPFRInterval(0, 0) == PyMPFRInterval(-0.5, 0.5))
        self.assertTrue(PyMPFRInterval(-0.5, 0.5) == PyMPFRInterval(PyMPFR(-0.5), PyMPFR(0.5)))
        self.assertFalse(PyMPFRInterval(-0.5, 0.5) == PyMPFRInterval.top())
        self.assertFalse(PyMPFRInterval.bottom() > PyMPFRInterval(0, 0))
        self.assertTrue(PyMPFRInterval(0, 0) > PyMPFRInterval.bottom())
        self.assertFalse(PyMPFRInterval(0, 0) > PyMPFRInterval(-0.5, 0.5))
        self.assertTrue(PyMPFRInterval(-0.5, 0.5) > PyMPFRInterval(0, 0))
        self.assertFalse(PyMPFRInterval(-0.5, 0.5) > PyMPFRInterval.top())
        self.assertTrue(PyMPFRInterval.top() > PyMPFRInterval(-0.5, 0.5))
        
    def test_is_top(self):
        self.assertFalse(PyMPFRInterval(0, 0).is_top())
        self.assertFalse(PyMPFRInterval(0.0, 0.0).is_top())
        self.assertFalse(PyMPFRInterval(PyMPFRScalar(0), PyMPFRScalar(0)).is_top())
        self.assertFalse(PyMPFRInterval(PyMPFRScalar(0.0), PyMPFRScalar(0.0)).is_top())
        self.assertFalse(PyMPFRInterval(-0.5, 0.5).is_top())
        self.assertFalse(PyMPFRInterval(PyMPFR(-0.5), PyMPFR(0.5)).is_top())
        self.assertFalse(PyMPFRInterval(PyMPFRScalar(-0.5), PyMPFRScalar(0.5)).is_top())
        self.assertTrue(PyMPFRInterval.top().is_top())
        self.assertFalse(PyMPFRInterval.bottom().is_top())
    
    def test_neg(self):
        self.assertEqual(-PyMPFRInterval.bottom(), PyMPFRInterval.bottom())
        self.assertEqual(-PyMPFRInterval(-1, 2), PyMPFRInterval(-2, 1))
        self.assertEqual(-PyMPFRInterval(0, 0), PyMPFRInterval(0, 0))
        self.assertEqual(-PyMPFRInterval(-0.5, 0.5), PyMPFRInterval(PyMPFR(-0.5), PyMPFR(0.5)))
        self.assertEqual(-PyMPFRInterval(1, 2), PyMPFRInterval(-2, -1))
        self.assertEqual(-PyMPFRInterval.top(), PyMPFRInterval.top())


if __name__ == '__main__':
    unittest.main()
