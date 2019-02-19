"""
APRON Linear Constraints (Level 1) - Unit Tests
===============================================

:Author: Caterina Urban
"""
import unittest

from apronpy.coeff import PyDoubleScalarCoeff
from apronpy.environment import PyEnvironment
from apronpy.lincons0 import ConsTyp
from apronpy.lincons1 import PyLincons1
from apronpy.linexpr1 import PyLinexpr1
from apronpy.var import PyVar


class TestPyLincons1(unittest.TestCase):

    def test_init(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        x.set_coeff(PyVar('x'), PyDoubleScalarCoeff(3))
        x.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
        x.set_cst(PyDoubleScalarCoeff(8))
        c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        self.assertEqual(str(c), '3.0·x - 9.0·z + 8.0 >= 0')
        self.assertEqual(str(PyLincons1.unsat(e)), '-1.0 >= 0')
        self.assertEqual(str(PyLincons1(ConsTyp.AP_CONS_DISEQ, PyLinexpr1(e))), '0.0 != 0')

    def test_is_unsat(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        x.set_coeff(PyVar('x'), PyDoubleScalarCoeff(3))
        x.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
        x.set_cst(PyDoubleScalarCoeff(8))
        c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        self.assertFalse(c.is_unsat())
        self.assertTrue(PyLincons1.unsat(e).is_unsat())
        self.assertTrue(PyLincons1(ConsTyp.AP_CONS_DISEQ, PyLinexpr1(e)).is_unsat())

    def test_get_typ(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        self.assertEqual(repr(c.get_typ()), '>=')
        self.assertNotEqual(repr(c.get_typ()), '<')

    def test_set_typ(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        c.set_typ(ConsTyp.AP_CONS_DISEQ)
        self.assertEqual(str(c), '0.0 != 0')

    def test_get_cst(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        self.assertEqual(c.get_cst(), PyDoubleScalarCoeff(0.0))
        self.assertNotEqual(c.get_cst(), PyDoubleScalarCoeff(-3))

    def test_set_cst(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        c.set_cst(PyDoubleScalarCoeff(9))
        self.assertEqual(str(c), '9.0 >= 0')

    def test_get_coeff(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        self.assertEqual(c.get_coeff(PyVar('x')), PyDoubleScalarCoeff(0.0))
        self.assertNotEqual(c.get_coeff(PyVar('x')), PyDoubleScalarCoeff(-3))

    def test_set_coeff(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        c.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
        self.assertEqual(str(c), '-9.0·z + 0.0 >= 0')


if __name__ == '__main__':
    unittest.main()
