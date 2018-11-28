"""
APRON (String) Variables - Unit Tests
=====================================

:Author: Caterina Urban
"""
import unittest

from apronpy.var import PyVar


class TestPyVar(unittest.TestCase):

    def test_init(self):
        self.assertEqual(str(PyVar('x')), 'x')
        self.assertEqual(str(PyVar('X')), 'X')

    def test_cmp(self):
        self.assertTrue(PyVar('X') < PyVar('x'))
        self.assertFalse(PyVar('X') == PyVar('x'))
        self.assertTrue(PyVar('x') == PyVar('x'))
        self.assertFalse(PyVar('X') > PyVar('x'))
        self.assertTrue(PyVar('y') > PyVar('x'))


if __name__ == '__main__':
    unittest.main()
