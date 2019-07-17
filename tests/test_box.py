"""
APRON Boxes - Unit Tests
========================

:Author: Caterina Urban
"""
import unittest
from copy import deepcopy

from apronpy.box import PyBoxD, PyBoxMPQ, PyBoxMPFR
from apronpy.environment import PyEnvironment
from apronpy.interval import PyDoubleInterval, PyMPQInterval, PyMPFRInterval
from apronpy.var import PyVar


class TestPyBoxD(unittest.TestCase):

    def test_bottom(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        self.assertTrue(PyBoxD.bottom(e).is_bottom())
        b1 = PyBoxD(e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBoxD(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBoxD(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(PyBoxD.top(e).is_bottom())

    def test_default(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        b1 = PyBoxD(e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        self.assertFalse(b1.is_top())
        b2 = PyBoxD(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        self.assertFalse(b2.is_top())
        b3 = PyBoxD(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(b3.is_top())

    def test_top(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        self.assertFalse(PyBoxD.bottom(e).is_top())
        b1 = PyBoxD(e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBoxD(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBoxD(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertTrue(PyBoxD.top(e).is_top())

    def test_deepcopy(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        b0 = PyBoxD(e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        b1 = deepcopy(b0)
        b2 = b0
        self.assertNotEqual(id(b0), id(b1))
        self.assertEqual(id(b0), id(b2))

    def test_meet(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        b0 = PyBoxD.bottom(e)
        b1d = PyBoxD(e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 0.0)])
        b1q = PyBoxD(e, variables=[PyVar('x0')], intervals=[PyMPQInterval(-5, 0, 2, 1)])
        b1f = PyBoxD(e, variables=[PyVar('x0')], intervals=[PyMPFRInterval(-2.5, 0.0)])
        b2d = PyBoxD(e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(0.0, 2.5)])
        b2q = PyBoxD(e, variables=[PyVar('x0')], intervals=[PyMPQInterval(0, 5, 1, 2)])
        b2f = PyBoxD(e, variables=[PyVar('x0')], intervals=[PyMPFRInterval(0.0, 2.5)])
        b3d = PyBoxD(e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(0.0, 0.0)])
        b3q = PyBoxD(e, variables=[PyVar('x0')], intervals=[PyMPQInterval(0, 0, 1, 1)])
        b3f = PyBoxD(e, variables=[PyVar('x0')], intervals=[PyMPFRInterval(0.0, 0.0)])
        b4 = PyBoxD.top(e)
        self.assertTrue(b0.meet(b1d) == b0)
        self.assertTrue(b0.meet(b1q) == b0)
        self.assertTrue(b0.meet(b1f) == b0)
        self.assertTrue(b0.meet(b2d) == b0)
        self.assertTrue(b0.meet(b2q) == b0)
        self.assertTrue(b0.meet(b2f) == b0)
        self.assertTrue(b0.meet(b3d) == b0)
        self.assertTrue(b0.meet(b3q) == b0)
        self.assertTrue(b0.meet(b3f) == b0)
        self.assertTrue(b1d.meet(b2d) == b3d)
        self.assertTrue(b1d.meet(b3d) == b3d)
        self.assertTrue(b2d.meet(b3d) == b3d)
        self.assertTrue(b1q.meet(b2q) == b3q)
        self.assertTrue(b1q.meet(b3q) == b3q)
        self.assertTrue(b2q.meet(b3q) == b3q)
        self.assertTrue(b1f.meet(b2f) == b3f)
        self.assertTrue(b1f.meet(b3f) == b3f)
        self.assertTrue(b2f.meet(b3f) == b3f)
        self.assertTrue(b1d.meet(b4) == b1d)
        self.assertTrue(b1q.meet(b4) == b1q)
        self.assertTrue(b1f.meet(b4) == b1f)
        self.assertTrue(b2d.meet(b4) == b2d)
        self.assertTrue(b2q.meet(b4) == b2q)
        self.assertTrue(b2f.meet(b4) == b2f)
        self.assertTrue(b3d.meet(b4) == b3d)
        self.assertTrue(b3q.meet(b4) == b3q)
        self.assertTrue(b3f.meet(b4) == b3f)


class TestPyBoxMPQ(unittest.TestCase):

    def test_bottom(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        self.assertTrue(PyBoxMPQ.bottom(e).is_bottom())
        b1 = PyBoxMPQ(e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBoxMPQ(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBoxMPQ(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(PyBoxMPQ.top(e).is_bottom())

    def test_default(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        b1 = PyBoxMPQ(e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        self.assertFalse(b1.is_top())
        b2 = PyBoxMPQ(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        self.assertFalse(b2.is_top())
        b3 = PyBoxMPQ(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(b3.is_top())

    def test_top(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        self.assertFalse(PyBoxMPQ.bottom(e).is_top())
        b1 = PyBoxMPQ(e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBoxMPQ(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBoxMPQ(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertTrue(PyBoxMPQ.top(e).is_top())

    def test_bound_variable(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        variables = [PyVar('x0'), PyVar('y')]
        intervals = [PyMPQInterval(-3, 2), PyMPQInterval(-2, 2, 1, 1)]
        b = PyBoxMPQ(e, variables=variables, intervals=intervals)
        self.assertEqual(str(b.bound_variable(PyVar('y'))), '[-2,2]')

    def test_forget(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        variables = [PyVar('x0'), PyVar('y')]
        intervals = [PyMPQInterval(-3, 2), PyMPQInterval(-2, 2, 1, 1)]
        b = PyBoxMPQ(e, variables=variables, intervals=intervals)
        self.assertEqual(str(b.forget([PyVar('y')])), '1·x0 + 3 >= 0 ∧ -1·x0 + 2 >= 0')


class TestPyBoxMPFR(unittest.TestCase):

    def test_bottom(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        self.assertTrue(PyBoxMPFR.bottom(e).is_bottom())
        b1 = PyBoxMPFR(e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBoxMPFR(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBoxMPFR(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(PyBoxMPFR.top(e).is_bottom())

    def test_default(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        b1 = PyBoxMPFR(e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        self.assertFalse(b1.is_top())
        b2 = PyBoxMPFR(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        self.assertFalse(b2.is_top())
        b3 = PyBoxMPFR(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(b3.is_top())

    def test_top(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        self.assertFalse(PyBoxMPFR.bottom(e).is_top())
        b1 = PyBoxMPFR(e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBoxMPFR(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBoxMPFR(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertTrue(PyBoxMPFR.top(e).is_top())


if __name__ == '__main__':
    unittest.main()
