"""
APRON (String) Variables - Unit Tests
=====================================

:Author: Caterina Urban
"""
import unittest
from copy import deepcopy

from apronpy.var import PyVar


class TestPyVar(unittest.TestCase):

    def test_init(self):
        self.assertEqual(str(PyVar('x0')), 'x0')
        self.assertEqual(str(PyVar('X')), 'X')

    def test_deepcopy(self):
        x0 = PyVar('X')
        x1 = deepcopy(x0)
        x2 = x0
        self.assertNotEqual(id(x0), id(x1))
        self.assertEqual(id(x0), id(x2))

    def test_cmp(self):
        self.assertTrue(PyVar('X') < PyVar('x0'))
        self.assertFalse(PyVar('X') == PyVar('x0'))
        self.assertTrue(PyVar('x0') == PyVar('x0'))
        self.assertFalse(PyVar('X') > PyVar('x0'))
        self.assertTrue(PyVar('y') > PyVar('x0'))


if __name__ == '__main__':
    unittest.main()
