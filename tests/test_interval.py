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
        self.assertEqual(str(PyDoubleInterval.init_top()), '[-inf,inf]')
        self.assertEqual(str(PyDoubleInterval.init_bottom()), '[1.0,-1.0]')

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
        self.assertFalse(PyDoubleInterval.init_top().is_bottom())
        self.assertTrue(PyDoubleInterval.init_bottom().is_bottom())
    
    def test_cmp(self):
        self.assertTrue(PyDoubleInterval.init_bottom() < PyDoubleInterval())
        self.assertFalse(PyDoubleInterval() < PyDoubleInterval.init_bottom())
        self.assertTrue(PyDoubleInterval() < PyDoubleInterval(-0.5, 0.5))
        self.assertFalse(PyDoubleInterval(-0.5, 0.5) < PyDoubleInterval())
        self.assertTrue(PyDoubleInterval(-0.5, 0.5) < PyDoubleInterval.init_top())
        self.assertFalse(PyDoubleInterval.init_top() < PyDoubleInterval(-0.5, 0.5))
        self.assertFalse(PyDoubleInterval.init_bottom() == PyDoubleInterval())
        self.assertTrue(PyDoubleInterval() == PyDoubleInterval(0, 0))
        self.assertFalse(PyDoubleInterval() == PyDoubleInterval(-0.5, 0.5))
        self.assertTrue(
            PyDoubleInterval(-0.5, 0.5) == PyDoubleInterval(c_double(-0.5), c_double(0.5))
        )
        self.assertFalse(PyDoubleInterval(-0.5, 0.5) == PyDoubleInterval.init_top())
        self.assertFalse(PyDoubleInterval.init_bottom() > PyDoubleInterval())
        self.assertTrue(PyDoubleInterval() > PyDoubleInterval.init_bottom())
        self.assertFalse(PyDoubleInterval() > PyDoubleInterval(-0.5, 0.5))
        self.assertTrue(PyDoubleInterval(-0.5, 0.5) > PyDoubleInterval())
        self.assertFalse(PyDoubleInterval(-0.5, 0.5) > PyDoubleInterval.init_top())
        self.assertTrue(PyDoubleInterval.init_top() > PyDoubleInterval(-0.5, 0.5))
    
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
        self.assertTrue(PyDoubleInterval.init_top().is_top())
        self.assertFalse(PyDoubleInterval.init_bottom().is_top())

    def test_neg(self):
        self.assertEqual(-PyDoubleInterval.init_bottom(), PyDoubleInterval.init_bottom())
        self.assertEqual(-PyDoubleInterval(-1, 2), PyDoubleInterval(-2, 1))
        self.assertEqual(-PyDoubleInterval(), PyDoubleInterval(0, 0))
        self.assertEqual(
            -PyDoubleInterval(-0.5, 0.5), PyDoubleInterval(c_double(-0.5), c_double(0.5))
        )
        self.assertEqual(-PyDoubleInterval(1, 2), PyDoubleInterval(-2, -1))
        self.assertEqual(-PyDoubleInterval.init_top(), PyDoubleInterval.init_top())


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
        self.assertEqual(str(PyMPQInterval.init_top()), '[-1/0,1/0]')
        self.assertEqual(str(PyMPQInterval.init_bottom()), '[1,-1]')

    def test_is_bottom(self):
        self.assertFalse(PyMPQInterval().is_bottom())
        self.assertFalse(PyMPQInterval(0, 0).is_bottom())
        self.assertFalse(PyMPQInterval(0, 0, 1, 1).is_bottom())
        self.assertFalse(PyMPQInterval(PyMPQScalar(0), PyMPQScalar(0)).is_bottom())
        self.assertFalse(PyMPQInterval(PyMPQScalar(0, 1), PyMPQScalar(0, 1)).is_bottom())
        self.assertFalse(PyMPQInterval(-1, 1, 2, 2).is_bottom())
        self.assertFalse(PyMPQInterval(PyMPQ(-1, 2), PyMPQ(1, 2)).is_bottom())
        self.assertFalse(PyMPQInterval(PyMPQScalar(-1, 2), PyMPQScalar(1, 2)).is_bottom())
        self.assertFalse(PyMPQInterval.init_top().is_bottom())
        self.assertTrue(PyMPQInterval.init_bottom().is_bottom())

    def test_cmp(self):
        self.assertTrue(PyMPQInterval.init_bottom() < PyMPQInterval())
        self.assertFalse(PyMPQInterval() < PyMPQInterval.init_bottom())
        self.assertTrue(PyMPQInterval() < PyMPQInterval(-1, 1, 2, 2))
        self.assertFalse(PyMPQInterval(-1, 1, 2, 2) < PyMPQInterval())
        self.assertTrue(PyMPQInterval(-1, 1, 2, 2) < PyMPQInterval.init_top())
        self.assertFalse(PyMPQInterval.init_top() < PyMPQInterval(-1, 1, 2, 2))
        self.assertFalse(PyMPQInterval.init_bottom() == PyMPQInterval())
        self.assertTrue(PyMPQInterval() == PyMPQInterval(0, 0))
        self.assertFalse(PyMPQInterval() == PyMPQInterval(-1, 1, 2, 2))
        self.assertTrue(PyMPQInterval(-1, 1, 2, 2) == PyMPQInterval(PyMPQ(-1, 2), PyMPQ(1, 2)))
        self.assertFalse(PyMPQInterval(-1, 1, 2, 2) == PyMPQInterval.init_top())
        self.assertFalse(PyMPQInterval.init_bottom() > PyMPQInterval())
        self.assertTrue(PyMPQInterval() > PyMPQInterval.init_bottom())
        self.assertFalse(PyMPQInterval() > PyMPQInterval(-1, 1, 2, 2))
        self.assertTrue(PyMPQInterval(-1, 1, 2, 2) > PyMPQInterval())
        self.assertFalse(PyMPQInterval(-1, 1, 2, 2) > PyMPQInterval.init_top())
        self.assertTrue(PyMPQInterval.init_top() > PyMPQInterval(-1, 1, 2, 2))
    
    def test_is_top(self):
        self.assertFalse(PyMPQInterval().is_top())
        self.assertFalse(PyMPQInterval(0, 0).is_top())
        self.assertFalse(PyMPQInterval(0, 0, 1, 1).is_top())
        self.assertFalse(PyMPQInterval(PyMPQScalar(0), PyMPQScalar(0)).is_top())
        self.assertFalse(PyMPQInterval(PyMPQScalar(0, 1), PyMPQScalar(0, 1)).is_top())
        self.assertFalse(PyMPQInterval(-1, 1, 2, 2).is_top())
        self.assertFalse(PyMPQInterval(PyMPQ(-1, 2), PyMPQ(1, 2)).is_top())
        self.assertFalse(PyMPQInterval(PyMPQScalar(-1, 2), PyMPQScalar(1, 2)).is_top())
        self.assertTrue(PyMPQInterval.init_top().is_top())
        self.assertFalse(PyMPQInterval.init_bottom().is_top())
    
    def test_neg(self):
        self.assertEqual(-PyMPQInterval.init_bottom(), PyMPQInterval.init_bottom())
        self.assertEqual(-PyMPQInterval(-1, 2), PyMPQInterval(-2, 1))
        self.assertEqual(-PyMPQInterval(), PyMPQInterval(0, 0))
        self.assertEqual(-PyMPQInterval(-1, 1, 2, 2), PyMPQInterval(-PyMPQ(1, 2), PyMPQ(1, 2)))
        self.assertEqual(-PyMPQInterval(1, 1, 2, 2), PyMPQInterval(-PyMPQ(1, 2), -PyMPQ(1, 2)))
        self.assertEqual(-PyMPQInterval(1, 1, 2, 2), PyMPQInterval(PyMPQ(-1, 2), PyMPQ(-1, 2)))
        self.assertEqual(-PyMPQInterval(1, 2), PyMPQInterval(-2, -1))
        self.assertEqual(-PyMPQInterval.init_top(), PyMPQInterval.init_top())


class TestPyMPFRInterval(unittest.TestCase):

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

    def test_is_bottom(self):
        self.assertFalse(PyMPFRInterval(0, 0).is_bottom())
        self.assertFalse(PyMPFRInterval(0.0, 0.0).is_bottom())
        self.assertFalse(PyMPFRInterval(PyMPFRScalar(0), PyMPFRScalar(0)).is_bottom())
        self.assertFalse(PyMPFRInterval(PyMPFRScalar(0.0), PyMPFRScalar(0.0)).is_bottom())
        self.assertFalse(PyMPFRInterval(-0.5, 0.5).is_bottom())
        self.assertFalse(PyMPFRInterval(PyMPFR(-0.5), PyMPFR(0.5)).is_bottom())
        self.assertFalse(PyMPFRInterval(PyMPFRScalar(-0.5), PyMPFRScalar(0.5)).is_bottom())
        self.assertFalse(PyMPFRInterval.init_top().is_bottom())
        self.assertTrue(PyMPFRInterval.init_bottom().is_bottom())
        
    def test_cmp(self):
        self.assertTrue(PyMPFRInterval.init_bottom() < PyMPFRInterval(0, 0))
        self.assertFalse(PyMPFRInterval(0, 0) < PyMPFRInterval.init_bottom())
        self.assertTrue(PyMPFRInterval(0, 0) < PyMPFRInterval(-0.5, 0.5))
        self.assertFalse(PyMPFRInterval(-0.5, 0.5) < PyMPFRInterval(0, 0))
        self.assertTrue(PyMPFRInterval(-0.5, 0.5) < PyMPFRInterval.init_top())
        self.assertFalse(PyMPFRInterval.init_top() < PyMPFRInterval(-0.5, 0.5))
        self.assertFalse(PyMPFRInterval.init_bottom() == PyMPFRInterval(0, 0))
        self.assertTrue(PyMPFRInterval(0, 0) == PyMPFRInterval(0, 0))
        self.assertFalse(PyMPFRInterval(0, 0) == PyMPFRInterval(-0.5, 0.5))
        self.assertTrue(PyMPFRInterval(-0.5, 0.5) == PyMPFRInterval(PyMPFR(-0.5), PyMPFR(0.5)))
        self.assertFalse(PyMPFRInterval(-0.5, 0.5) == PyMPFRInterval.init_top())
        self.assertFalse(PyMPFRInterval.init_bottom() > PyMPFRInterval(0, 0))
        self.assertTrue(PyMPFRInterval(0, 0) > PyMPFRInterval.init_bottom())
        self.assertFalse(PyMPFRInterval(0, 0) > PyMPFRInterval(-0.5, 0.5))
        self.assertTrue(PyMPFRInterval(-0.5, 0.5) > PyMPFRInterval(0, 0))
        self.assertFalse(PyMPFRInterval(-0.5, 0.5) > PyMPFRInterval.init_top())
        self.assertTrue(PyMPFRInterval.init_top() > PyMPFRInterval(-0.5, 0.5))
        
    def test_is_top(self):
        self.assertFalse(PyMPFRInterval(0, 0).is_top())
        self.assertFalse(PyMPFRInterval(0.0, 0.0).is_top())
        self.assertFalse(PyMPFRInterval(PyMPFRScalar(0), PyMPFRScalar(0)).is_top())
        self.assertFalse(PyMPFRInterval(PyMPFRScalar(0.0), PyMPFRScalar(0.0)).is_top())
        self.assertFalse(PyMPFRInterval(-0.5, 0.5).is_top())
        self.assertFalse(PyMPFRInterval(PyMPFR(-0.5), PyMPFR(0.5)).is_top())
        self.assertFalse(PyMPFRInterval(PyMPFRScalar(-0.5), PyMPFRScalar(0.5)).is_top())
        self.assertTrue(PyMPFRInterval.init_top().is_top())
        self.assertFalse(PyMPFRInterval.init_bottom().is_top())
    
    def test_neg(self):
        self.assertEqual(-PyMPFRInterval.init_bottom(), PyMPFRInterval.init_bottom())
        self.assertEqual(-PyMPFRInterval(-1, 2), PyMPFRInterval(-2, 1))
        self.assertEqual(-PyMPFRInterval(0, 0), PyMPFRInterval(0, 0))
        self.assertEqual(-PyMPFRInterval(-0.5, 0.5), PyMPFRInterval(PyMPFR(-0.5), PyMPFR(0.5)))
        self.assertEqual(-PyMPFRInterval(1, 2), PyMPFRInterval(-2, -1))
        self.assertEqual(-PyMPFRInterval.init_top(), PyMPFRInterval.init_top())


if __name__ == '__main__':
    unittest.main()
