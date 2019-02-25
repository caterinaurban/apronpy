"""
APRON Tree Expressions (Level 1) - Unit Tests
=============================================

:Author: Caterina Urban
"""
import unittest

from apronpy.coeff import PyDoubleScalarCoeff, PyDoubleIntervalCoeff, PyMPQScalarCoeff
from apronpy.environment import PyEnvironment
from apronpy.linexpr1 import PyLinexpr1
from apronpy.texpr1 import PyTexpr1
from apronpy.var import PyVar


class TestPyTexpr1(unittest.TestCase):

    def test_init(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        x0 = PyLinexpr1(e, 0)
        self.assertEqual(str(PyTexpr1(x)), '0.0')
        self.assertEqual(str(PyTexpr1(x0)), '0.0 + 0.0 · x + 0.0 · y + 0.0 · z')
        x.set_coeff(PyVar('x'), PyDoubleScalarCoeff(-1))
        x.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
        x.set_cst(PyDoubleScalarCoeff(8))
        self.assertEqual(str(PyTexpr1(x)), '8.0 - 1.0 · x - 9.0 · z')

    def test_substitute(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        x0 = PyLinexpr1(e)
        x0.set_coeff(PyVar('x'), PyMPQScalarCoeff(1))
        x0.set_cst(PyMPQScalarCoeff(3))
        t0 = PyTexpr1(x0)
        self.assertEqual(str(t0), '3 + 1 · x')
        x1 = PyLinexpr1(e)
        x1.set_coeff(PyVar('x'), PyMPQScalarCoeff(1))
        x1.set_cst(PyMPQScalarCoeff(-1))
        t1 = PyTexpr1(x1)
        self.assertEqual(str(t1), '-1 + 1 · x')
        self.assertEqual(str(t0.substitute(PyVar('x'), t1)), '3 + 1 · (-1 + 1 · x)')
        x2 = PyLinexpr1(e)
        x2.set_coeff(PyVar('x'), PyMPQScalarCoeff(1))
        x2.set_cst(PyMPQScalarCoeff(2))
        t2 = PyTexpr1(x2)
        self.assertEqual(str(t2), '2 + 1 · x')


if __name__ == '__main__':
    unittest.main()
