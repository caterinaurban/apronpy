"""
APRON Tree Constraints (Level 1) - Unit Tests
=============================================

:Author: Caterina Urban
"""
import unittest

from apronpy.coeff import PyDoubleScalarCoeff
from apronpy.environment import PyEnvironment
from apronpy.lincons0 import ConsTyp
from apronpy.lincons1 import PyLincons1
from apronpy.linexpr1 import PyLinexpr1
from apronpy.tcons1 import PyTcons1
from apronpy.var import PyVar


class TestPyTcons1(unittest.TestCase):

    def test_init(self):
        e = PyEnvironment([PyVar('x0'), PyVar('y')], [PyVar('z')])
        x = PyLinexpr1(e)
        x.set_coeff(PyVar('x0'), PyDoubleScalarCoeff(3))
        x.set_coeff(PyVar('z'), PyDoubleScalarCoeff(-9))
        x.set_cst(PyDoubleScalarCoeff(8))
        c = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        self.assertEqual(str(PyTcons1(c)), '8.0 + 3.0 · x0 - 9.0 · z >= 0')
        self.assertEqual(str(PyTcons1.unsat(e)), '-1.0 >= 0')
        z = PyLincons1(ConsTyp.AP_CONS_DISEQ, PyLinexpr1(e))
        self.assertEqual(str(PyTcons1(z)), '0.0 != 0')


if __name__ == '__main__':
    unittest.main()
