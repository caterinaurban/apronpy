"""
APRON Environments - Unit Tests
===============================

:Author: Caterina Urban
"""
import unittest
from copy import deepcopy

from apronpy.environment import PyEnvironment
from apronpy.var import PyVar


class TestPyEnvironment(unittest.TestCase):

    def test_init(self):
        self.assertEqual(str(PyEnvironment([PyVar('x')], [PyVar('y'), PyVar('z')])), '{x|y,z}')
        self.assertEqual(str(PyEnvironment([], [PyVar('y'), PyVar('z')])), '{|y,z}')
        self.assertEqual(str(PyEnvironment(real_vars=[PyVar('y'), PyVar('z')])), '{|y,z}')
        self.assertEqual(str(PyEnvironment([PyVar('x')], [])), '{x|}')
        self.assertEqual(str(PyEnvironment([PyVar('x')])), '{x|}')
        self.assertRaises(ValueError, PyEnvironment, [PyVar('x')], [PyVar('x'), PyVar('y')])

    def test_deepcopy(self):
        e0 = PyEnvironment([PyVar('x')], [PyVar('y'), PyVar('z')])
        e1 = deepcopy(e0)
        e2 = e0
        self.assertEqual(id(e0), id(e1))
        self.assertEqual(id(e0), id(e2))

    def test_len(self):
        self.assertEqual(len(PyEnvironment([PyVar('x')], [PyVar('y'), PyVar('z')])), 3)
        self.assertEqual(len(PyEnvironment([], [PyVar('y'), PyVar('z')])), 2)
        self.assertEqual(len(PyEnvironment(real_vars=[PyVar('y'), PyVar('z')])), 2)
        self.assertEqual(len(PyEnvironment([PyVar('x')], [])), 1)
        self.assertEqual(len(PyEnvironment([PyVar('x')])), 1)
        self.assertEqual(len(PyEnvironment()), 0)

    def test_add(self):
        e1 = PyEnvironment([PyVar('x')], [PyVar('y'), PyVar('z')])
        e2 = PyEnvironment([PyVar('x')], [PyVar('y')])
        self.assertEqual(str(e1), str(e2.add(real_vars=[PyVar('z')])))
        self.assertRaises(ValueError, e1.add, [PyVar('x')])

    def test_remove(self):
        e1 = PyEnvironment([PyVar('x')], [PyVar('y'), PyVar('z')])
        e2 = PyEnvironment([], [PyVar('y'), PyVar('z')])
        self.assertEqual(str(e1.remove([PyVar('x')])), str(e2))
        self.assertRaises(ValueError, e1.remove, [PyVar('w')])

    def test_contains(self):
        self.assertTrue(PyVar('x') in PyEnvironment([PyVar('x')], [PyVar('y')]))
        self.assertFalse(PyVar('y') in PyEnvironment([PyVar('x')]))
        self.assertFalse(PyVar('x') not in PyEnvironment([PyVar('x')], [PyVar('y')]))
        self.assertTrue(PyVar('y') not in PyEnvironment([PyVar('x')]))

    def test_cmp(self):
        self.assertTrue(PyEnvironment([PyVar('x')]) < PyEnvironment([PyVar('x')], [PyVar('y')]))
        self.assertFalse(PyEnvironment([PyVar('x')]) > PyEnvironment([PyVar('x')]))
        self.assertTrue(PyEnvironment([PyVar('x')]) == PyEnvironment([PyVar('x')], []))
        self.assertFalse(PyEnvironment([PyVar('x')]) == PyEnvironment([PyVar('x')], [PyVar('y')]))
        self.assertTrue(PyEnvironment([PyVar('x')]) > PyEnvironment())
        self.assertFalse(PyEnvironment([PyVar('x')]) < PyEnvironment())
        self.assertTrue(PyEnvironment().add([PyVar('x')]) == PyEnvironment([PyVar('x')]))
        self.assertTrue(PyEnvironment([PyVar('x')]).remove([PyVar('x')]) == PyEnvironment())

    def test_union(self):
        e1 = PyEnvironment([PyVar('x')], [PyVar('y')])
        self.assertEqual(e1, PyEnvironment([PyVar('x')]).union(PyEnvironment([], [PyVar('y')])))
        e2 = PyEnvironment([], [PyVar('y'), PyVar('z')])
        self.assertEqual(e2, PyEnvironment([], [PyVar('y')]) | PyEnvironment([], [PyVar('z')]))
        e3 = PyEnvironment([PyVar('x')], [])
        self.assertEqual(PyEnvironment() | PyEnvironment([PyVar('x')], []), e3)
        self.assertEqual(PyEnvironment([PyVar('x')], []) | PyEnvironment(), e3)
        e4 = PyEnvironment([PyVar('x')], [])
        self.assertRaises(ValueError, e4.union, PyEnvironment([], [PyVar('x')]))

    def test_rename(self):
        e1 = PyEnvironment([PyVar('x')], [PyVar('y')])
        e2 = PyEnvironment([PyVar('x')], [PyVar('z')])
        self.assertEqual(e1.rename([PyVar('y')], [PyVar('z')]), e2)
        self.assertRaises(ValueError, e2.rename, [PyVar('x')], [PyVar('z')])


if __name__ == '__main__':
    unittest.main()
