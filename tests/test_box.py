"""
APRON Boxes - Unit Tests
========================

:Author: Caterina Urban
"""
import unittest
from copy import deepcopy

from apronpy.box import PyBox, PyBoxDManager, PyBoxMPQManager, PyBoxMPFRManager
from apronpy.environment import PyEnvironment
from apronpy.interval import PyDoubleInterval, PyMPQInterval, PyMPFRInterval
from apronpy.manager import PyManager
from apronpy.texpr0 import TexprOp, TexprRtype, TexprRdir
from apronpy.texpr1 import PyTexpr1
from apronpy.var import PyVar


class TestPyDBox(unittest.TestCase):

    def test_bottom(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        man: PyManager = PyBoxDManager()
        self.assertTrue(PyBox.bottom(man, e).is_bottom())
        b1 = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBox(man, e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBox(man, e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(PyBox.top(man, e).is_bottom())

    def test_default(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        man: PyManager = PyBoxDManager()
        b1 = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        self.assertFalse(b1.is_top())
        b2 = PyBox(man, e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        self.assertFalse(b2.is_top())
        b3 = PyBox(man, e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(b3.is_top())

    def test_top(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        man: PyManager = PyBoxDManager()
        self.assertFalse(PyBox.bottom(man, e).is_top())
        b1 = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBox(man, e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBox(man, e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertTrue(PyBox.top(man, e).is_top())

    def test_deepcopy(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        man: PyManager = PyBoxDManager()
        b0 = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        b1 = deepcopy(b0)
        b2 = b0
        self.assertNotEqual(id(b0), id(b1))
        self.assertEqual(id(b0), id(b2))

    def test_meet(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        man: PyManager = PyBoxDManager()
        b0 = PyBox.bottom(man, e)
        b1d = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 0.0)])
        b1q = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyMPQInterval(-5, 0, 2, 1)])
        b1f = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyMPFRInterval(-2.5, 0.0)])
        b2d = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(0.0, 2.5)])
        b2q = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyMPQInterval(0, 5, 1, 2)])
        b2f = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyMPFRInterval(0.0, 2.5)])
        b3d = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(0.0, 0.0)])
        b3q = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyMPQInterval(0, 0, 1, 1)])
        b3f = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyMPFRInterval(0.0, 0.0)])
        b4 = PyBox.top(man, e)
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


class TestPyMPQBox(unittest.TestCase):

    def test_bottom(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        man: PyManager = PyBoxMPQManager()
        self.assertTrue(PyBox.bottom(man, e).is_bottom())
        b1 = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBox(man, e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBox(man, e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(PyBox.top(man, e).is_bottom())

    def test_default(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        man: PyManager = PyBoxMPQManager()
        b1 = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        self.assertFalse(b1.is_top())
        b2 = PyBox(man, e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        self.assertFalse(b2.is_top())
        b3 = PyBox(man, e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(b3.is_top())

    def test_top(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        man: PyManager = PyBoxMPQManager()
        self.assertFalse(PyBox.bottom(man, e).is_top())
        b1 = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBox(man, e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBox(man, e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertTrue(PyBox.top(man, e).is_top())

    def test_bound_variable(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        man: PyManager = PyBoxMPQManager()
        variables = [PyVar('x0'), PyVar('y')]
        intervals = [PyMPQInterval(-3, 2), PyMPQInterval(-2, 2, 1, 1)]
        b = PyBox(man, e, variables=variables, intervals=intervals)
        self.assertEqual(str(b.bound_variable(PyVar('y'))), '[-2,2]')

    def test_bound_texpr(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        man: PyManager = PyBoxMPQManager()
        variables = [PyVar('x0'), PyVar('y')]
        intervals = [PyMPQInterval(-3, 2), PyMPQInterval(-2, 2, 1, 1)]
        b = PyBox(man, e, variables=variables, intervals=intervals)
        x0 = PyTexpr1.var(e, PyVar('x0'))
        x1 = PyTexpr1.var(e, PyVar('y'))
        add = PyTexpr1.binop(TexprOp.AP_TEXPR_ADD, x0, x1, TexprRtype.AP_RTYPE_REAL, TexprRdir.AP_RDIR_RND)
        self.assertEqual(str(b.bound_texpr(add)), '[-5,4]')

    def test_forget(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        man: PyManager = PyBoxMPQManager()
        variables = [PyVar('x0'), PyVar('y')]
        intervals = [PyMPQInterval(-3, 2), PyMPQInterval(-2, 2, 1, 1)]
        b = PyBox(man, e, variables=variables, intervals=intervals)
        self.assertEqual(str(b.forget([PyVar('y')])), '1·x0 + 3 >= 0 ∧ -1·x0 + 2 >= 0')


class TestPyMPFRBox(unittest.TestCase):

    def test_bottom(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        man: PyManager = PyBoxMPFRManager()
        self.assertTrue(PyBox.bottom(man, e).is_bottom())
        b1 = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBox(man, e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBox(man, e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(PyBox.top(man, e).is_bottom())

    def test_default(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        man: PyManager = PyBoxMPFRManager()
        b1 = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        self.assertFalse(b1.is_top())
        b2 = PyBox(man, e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        self.assertFalse(b2.is_top())
        b3 = PyBox(man, e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertFalse(b3.is_top())

    def test_top(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        man: PyManager = PyBoxMPFRManager()
        self.assertFalse(PyBox.bottom(man, e).is_top())
        b1 = PyBox(man, e, variables=[PyVar('x0')], intervals=[PyDoubleInterval(-2.5, 2.5)])
        self.assertFalse(b1.is_bottom())
        b2 = PyBox(man, e, variables=[PyVar('y')], intervals=[PyMPQInterval(-5, 5, 2, 2)])
        self.assertFalse(b2.is_bottom())
        b3 = PyBox(man, e, variables=[PyVar('z')], intervals=[PyMPFRInterval(-2.5, 2.5)])
        self.assertFalse(b3.is_bottom())
        self.assertTrue(PyBox.top(man, e).is_top())


if __name__ == '__main__':
    unittest.main()
