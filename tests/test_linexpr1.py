"""
APRON Linear Expressions (Level 1) - Unit Tests
===============================================

:Author: Caterina Urban
"""
import unittest

from apronpy.box import PyBoxD, PyBoxMPQ, PyBoxMPFR
from apronpy.coeff import PyDoubleScalarCoeff
from apronpy.environment import PyEnvironment
from apronpy.interval import PyDoubleInterval, PyMPQInterval, PyMPFRInterval
from apronpy.linexpr1 import PyLinexpr1
from apronpy.var import PyVar


class TestPyLinexpr1(unittest.TestCase):

    def test_init(self):
        pass

    def test_get_coeff(self):
        e = PyEnvironment([PyVar('x'), PyVar('y')], [PyVar('z')])
        self.assertEqual(PyLinexpr1(e).get_coeff(PyVar('x')), PyDoubleScalarCoeff(0.0))
        self.assertNotEqual(PyLinexpr1(e).get_coeff(PyVar('x')), PyDoubleScalarCoeff(-3))


if __name__ == '__main__':
    unittest.main()
