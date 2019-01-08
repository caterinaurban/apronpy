"""
APRON Boxes - Unit Tests
========================

:Author: Caterina Urban
"""
import unittest

from apronpy.box import PyBoxD, PyBoxMPQ, PyBoxMPFR
from apronpy.environment import PyEnvironment
from apronpy.interval import PyDoubleInterval, PyMPQInterval, PyMPFRInterval
from apronpy.var import PyVar


class TestPyBoxD(unittest.TestCase):

    def test_bottom(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        self.assertTrue(PyBoxD.bottom(e).is_bottom())
        b1 = PyBoxD(e, variables=[PyVar('x')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBoxD(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBoxD(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(PyBoxD.top(e).is_bottom())

    def test_top(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        self.assertFalse(PyBoxD.bottom(e).is_top())
        b1 = PyBoxD(e, variables=[PyVar('x')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBoxD(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBoxD(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertTrue(PyBoxD.top(e).is_top())

    def test_default(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        b1 = PyBoxD(e, variables=[PyVar('x')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        self.assertFalse(b1.is_top())
        b2 = PyBoxD(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        self.assertFalse(b2.is_top())
        b3 = PyBoxD(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(b3.is_top())


class TestPyBoxMPQ(unittest.TestCase):

    def test_bottom(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        self.assertTrue(PyBoxMPQ.bottom(e).is_bottom())
        b1 = PyBoxMPQ(e, variables=[PyVar('x')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBoxMPQ(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBoxMPQ(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(PyBoxMPQ.top(e).is_bottom())

    def test_top(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        self.assertFalse(PyBoxMPQ.bottom(e).is_top())
        b1 = PyBoxMPQ(e, variables=[PyVar('x')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBoxMPQ(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBoxMPQ(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertTrue(PyBoxMPQ.top(e).is_top())

    def test_default(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        b1 = PyBoxMPQ(e, variables=[PyVar('x')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        self.assertFalse(b1.is_top())
        b2 = PyBoxMPQ(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        self.assertFalse(b2.is_top())
        b3 = PyBoxMPQ(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(b3.is_top())
        

class TestPyBoxMPFR(unittest.TestCase):

    def test_bottom(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        self.assertTrue(PyBoxMPFR.bottom(e).is_bottom())
        b1 = PyBoxMPFR(e, variables=[PyVar('x')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBoxMPFR(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBoxMPFR(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(PyBoxMPFR.top(e).is_bottom())

    def test_top(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        self.assertFalse(PyBoxMPFR.bottom(e).is_top())
        b1 = PyBoxMPFR(e, variables=[PyVar('x')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBoxMPFR(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBoxMPFR(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertTrue(PyBoxMPFR.top(e).is_top())

    def test_default(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        b1 = PyBoxMPFR(e, variables=[PyVar('x')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        self.assertFalse(b1.is_top())
        b2 = PyBoxMPFR(e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        self.assertFalse(b2.is_top())
        b3 = PyBoxMPFR(e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(b3.is_top())


if __name__ == '__main__':
    unittest.main()
