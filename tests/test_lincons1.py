"""
APRON Linear Constraints (Level 1) - Unit Tests
===============================================

:Author: Caterina Urban
"""
import unittest

from apronpy.scalar import PyMPQScalar

from apronpy.coeff import PyDoubleScalarCoeff, PyMPQScalarCoeff
from apronpy.environment import PyEnvironment
from apronpy.lincons0 import ConsTyp
from apronpy.lincons1 import PyLincons1, PyLincons1Array
from apronpy.linexpr1 import PyLinexpr1
from apronpy.var import PyVar


class TestPyLincons1(unittest.TestCase):

    def test_init(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        x1 = PyLinexpr1(e)
        x1.set_coeff(PyVar('x0'), PyDoubleScalarCoeff(3))
        x1.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
        x1.set_cst(PyDoubleScalarCoeff(8))
        c1 = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x1)
        self.assertEqual(str(c1), '3.0·x0 - 9.0·z + 8.0 >= 0')
        self.assertEqual(str(PyLincons1.unsat(e)), '-1.0 >= 0')
        self.assertEqual(str(PyLincons1(ConsTyp.AP_CONS_DISEQ, PyLinexpr1(e))), '0.0 != 0')
        x2 = PyLinexpr1(e)
        x2.set_coeff(PyVar('y'), PyMPQScalarCoeff(1))
        k = PyMPQScalar(2)
        c2 = PyLincons1(ConsTyp.AP_CONS_EQMOD, x2, k)
        self.assertEqual(str(c2), '1·y + 0.0 %= 2')

    def test_is_unsat(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        x.set_coeff(PyVar('x0'), PyDoubleScalarCoeff(3))
        x.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
        x.set_cst(PyDoubleScalarCoeff(8))
        c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        self.assertFalse(c.is_unsat())
        self.assertTrue(PyLincons1.unsat(e).is_unsat())
        self.assertTrue(PyLincons1(ConsTyp.AP_CONS_DISEQ, PyLinexpr1(e)).is_unsat())

    def test_get_typ(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        self.assertEqual(repr(c.get_typ()), '>=')
        self.assertNotEqual(repr(c.get_typ()), '<')

    def test_set_typ(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        c.set_typ(ConsTyp.AP_CONS_DISEQ)
        self.assertEqual(str(c), '0.0 != 0')

    def test_get_cst(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        self.assertEqual(c.get_cst(), PyDoubleScalarCoeff(0.0))
        self.assertNotEqual(c.get_cst(), PyDoubleScalarCoeff(-3))

    def test_set_cst(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        c.set_cst(PyDoubleScalarCoeff(9))
        self.assertEqual(str(c), '9.0 >= 0')

    def test_get_coeff(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        self.assertEqual(c.get_coeff(PyVar('x0')), PyDoubleScalarCoeff(0.0))
        self.assertNotEqual(c.get_coeff(PyVar('x0')), PyDoubleScalarCoeff(-3))

    def test_set_coeff(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        c.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
        self.assertEqual(str(c), '-9.0·z + 0.0 >= 0')


class TestPyLincons1Array(unittest.TestCase):

    def test_init(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        x1 = PyLinexpr1(e)
        x1.set_coeff(PyVar('x'), PyDoubleScalarCoeff(3))
        x1.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
        x1.set_cst(PyDoubleScalarCoeff(8))
        c1 = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x1)
        x2 = PyLinexpr1(e)
        x2.set_coeff(PyVar('x'), PyDoubleScalarCoeff(1))
        c2 = PyLincons1(ConsTyp.AP_CONS_SUP, x2)
        a = PyLincons1Array([c1, c2])
        self.assertEqual(str(a), '3.0·x - 9.0·z + 8.0 >= 0 ∧ 1.0·x + 0.0 > 0')

    def test_get(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        x1 = PyLinexpr1(e)
        x1.set_coeff(PyVar('x'), PyDoubleScalarCoeff(3))
        x1.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
        x1.set_cst(PyDoubleScalarCoeff(8))
        c1 = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x1)
        x2 = PyLinexpr1(e)
        x2.set_coeff(PyVar('x'), PyDoubleScalarCoeff(1))
        c2 = PyLincons1(ConsTyp.AP_CONS_SUP, x2)
        a = PyLincons1Array([c1, c2])
        c = a.get(1)
        self.assertNotEqual(str(c), str(c1))
        self.assertEqual(str(c), str(c2))

    def test_set(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        x1 = PyLinexpr1(e)
        x1.set_coeff(PyVar('x'), PyDoubleScalarCoeff(3))
        x1.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
        x1.set_cst(PyDoubleScalarCoeff(8))
        c1 = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x1)
        x2 = PyLinexpr1(e)
        x2.set_coeff(PyVar('x'), PyDoubleScalarCoeff(1))
        c2 = PyLincons1(ConsTyp.AP_CONS_SUP, x2)
        a = PyLincons1Array([c1, c2])
        x = PyLinexpr1(e)
        x.set_coeff(PyVar('y'), PyDoubleScalarCoeff(1))
        c = PyLincons1(ConsTyp.AP_CONS_SUP, x)
        a.set(0, c)
        self.assertEqual(str(a), '1.0·y + 0.0 > 0 ∧ 1.0·x + 0.0 > 0')


if __name__ == '__main__':
    unittest.main()
