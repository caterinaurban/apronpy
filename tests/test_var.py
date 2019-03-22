"""
APRON (String) Variables - Unit Tests
=====================================

:Author: Caterina Urban
"""
import unittest

from apronpy.var import PyVar


class TestPyVar(unittest.TestCase):

    def test_init(self):
        self.assertEqual(str(PyVar('x0')), 'x0')
        self.assertEqual(str(PyVar('X')), 'X')

    def test_cmp(self):
        self.assertTrue(PyVar('X') < PyVar('x0'))
        self.assertFalse(PyVar('X') == PyVar('x0'))
        self.assertTrue(PyVar('x0') == PyVar('x0'))
        self.assertFalse(PyVar('X') > PyVar('x0'))
        self.assertTrue(PyVar('y') > PyVar('x0'))


if __name__ == '__main__':
    unittest.main()
