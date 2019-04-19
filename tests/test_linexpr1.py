"""
APRON Linear Expressions (Level 1) - Unit Tests
===============================================

:Author: Caterina Urban
"""
import unittest
from copy import deepcopy

from apronpy.coeff import PyDoubleScalarCoeff, PyDoubleIntervalCoeff
from apronpy.environment import PyEnvironment
from apronpy.linexpr1 import PyLinexpr1
from apronpy.var import PyVar


class TestPyLinexpr1(unittest.TestCase):

    def test_init(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        self.assertEqual(str(PyLinexpr1(e)), '0.0')
        self.assertEqual(str(PyLinexpr1(e, 0)), '0.0·x0 + 0.0·y + 0.0·z + 0.0')

    def test_deepcopy(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        x0 = PyLinexpr1(e)
        x1 = deepcopy(x0)
        x2 = x0
        self.assertNotEqual(id(x0), id(x1))
        self.assertEqual(id(x0), id(x2))

    def test_is_integer(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        x0 = PyLinexpr1(e)
        x0.set_coeff(PyVar('x0'), PyDoubleScalarCoeff(3))
        self.assertTrue(x0.is_integer())
        x1 = PyLinexpr1(e)
        x1.set_coeff(PyVar('x0'), PyDoubleScalarCoeff(3))
        x1.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
        self.assertFalse(x1.is_integer())
        x2 = PyLinexpr1(e)
        x2.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
        self.assertFalse(x2.is_integer())

    def test_is_real(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        x0 = PyLinexpr1(e)
        x0.set_coeff(PyVar('x0'), PyDoubleScalarCoeff(3))
        self.assertFalse(x0.is_real())
        x1 = PyLinexpr1(e)
        x1.set_coeff(PyVar('x0'), PyDoubleScalarCoeff(3))
        x1.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
        self.assertFalse(x1.is_real())
        x2 = PyLinexpr1(e)
        x2.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
        self.assertTrue(x2.is_real())

    def test_is_linear(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        x0 = PyLinexpr1(e)
        x0.set_coeff(PyVar('x0'), PyDoubleScalarCoeff(3))
        x0.set_cst(PyDoubleScalarCoeff(-9))
        self.assertTrue(x0.is_linear())
        x1 = PyLinexpr1(e)
        x1.set_coeff(PyVar('x0'), PyDoubleIntervalCoeff(3, 3))
        x1.set_cst(PyDoubleIntervalCoeff(-9, 9))
        self.assertFalse(x1.is_linear())
        x2 = PyLinexpr1(e)
        x2.set_coeff(PyVar('x0'), PyDoubleScalarCoeff(3))
        x2.set_cst(PyDoubleIntervalCoeff(-9, 9))
        self.assertFalse(x2.is_linear())

    def test_is_quasilinear(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        x0 = PyLinexpr1(e)
        x0.set_coeff(PyVar('x0'), PyDoubleScalarCoeff(3))
        x0.set_cst(PyDoubleScalarCoeff(-9))
        self.assertTrue(x0.is_quasilinear())
        x1 = PyLinexpr1(e)
        x1.set_coeff(PyVar('x0'), PyDoubleIntervalCoeff(3, 3))
        x1.set_cst(PyDoubleIntervalCoeff(-9, 9))
        self.assertFalse(x1.is_quasilinear())
        x2 = PyLinexpr1(e)
        x2.set_coeff(PyVar('x0'), PyDoubleScalarCoeff(3))
        x2.set_cst(PyDoubleIntervalCoeff(-9, 9))
        self.assertTrue(x2.is_quasilinear())

    def test_get_cst(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        self.assertEqual(PyLinexpr1(e).get_cst(), PyDoubleScalarCoeff(0.0))
        self.assertNotEqual(PyLinexpr1(e).get_cst(), PyDoubleScalarCoeff(-3))

    def test_set_cst(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        x.set_cst(PyDoubleScalarCoeff(9))
        self.assertEqual(str(x), '9.0')

    def test_get_coeff(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        self.assertEqual(PyLinexpr1(e).get_coeff(PyVar('x0')), PyDoubleScalarCoeff(0.0))
        self.assertNotEqual(PyLinexpr1(e).get_coeff(PyVar('x0')), PyDoubleScalarCoeff(-3))

    def test_set_coeff(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        x.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
        self.assertEqual(str(x), '-9.0·z + 0.0')


if __name__ == '__main__':
    unittest.main()
