"""
APRON Linear Constraints (Level 1)
==================================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER, byref

from apronpy.cdll import libapron
from apronpy.coeff import PyDoubleScalarCoeff
from apronpy.environment import Environment, PyEnvironment
from apronpy.lincons0 import Lincons0, ConsTyp
from apronpy.linexpr0 import LinexprDiscr
from apronpy.linexpr1 import PyLinexpr1
from apronpy.scalar import PyScalar, c_uint


class Lincons1(Structure):
    """
    typedef struct ap_lincons1_t {
      ap_lincons0_t lincons0;
      ap_environment_t* env;
    } ap_lincons1_t;
    """

    _fields_ = [
        ('lincons0', Lincons0),
        ('env', POINTER(Environment))
    ]

    def __repr__(self):
        linexpr0 = self.lincons0.linexpr0.contents
        constyp = ConsTyp(self.lincons0.constyp)
        scalar = self.lincons0.scalar
        env = self.env.contents
        result = ''
        if linexpr0.discr == LinexprDiscr.AP_LINEXPR_DENSE:
            result += ' + '.join(
                '{}·{}'.format(linexpr0.p.coeff[i], env.var_of_dim[i].decode('utf-8'))
                for i in range(linexpr0.size)
            )
            result += ' + {}'.format(linexpr0.cst) if result else '{}'.format(linexpr0.cst)
        else:   # self.discr == LinexprDiscr.AP_LINEXPR_SPARSE:
            terms = list()
            for i in range(linexpr0.size):
                coeff = linexpr0.p.linterm[i].coeff
                dim = linexpr0.p.linterm[i].dim.value
                if dim < linexpr0.size:
                    terms.append('{}·{}'.format(coeff, env.var_of_dim[dim].decode('utf-8')))
            result += ' + '.join(terms)
            result += ' + {}'.format(linexpr0.cst) if result else '{}'.format(linexpr0.cst)
        if scalar:
            return '{} {} {}'.format(result.replace('+ -', '- '), repr(constyp), scalar.contents)
        else:
            return '{} {} 0'.format(result.replace('+ -', '- '), repr(constyp))


class PyLincons1:

    def __init__(self, typ: ConsTyp, linexpr: PyLinexpr1, scalar: PyScalar = None):
        self.lincons1 = Lincons1()
        linexpr_copy = libapron.ap_linexpr1_copy(linexpr)
        self.lincons1.lincons0.linexpr0 = linexpr_copy.linexpr0
        self.lincons1.lincons0.constyp = c_uint(typ)
        if scalar:
            scalar_copy = libapron.ap_scalar_alloc()
            libapron.ap_scalar_set(scalar_copy, scalar)
            self.lincons1.lincons0.scalar = scalar_copy
        self.lincons1.env = linexpr_copy.env

    @classmethod
    def unsat(cls, environment: PyEnvironment):
        x = PyLinexpr1(environment)
        x.set_cst(PyDoubleScalarCoeff(-1.0))
        lincons = cls(ConsTyp.AP_CONS_SUPEQ, x)
        return lincons

    def __del__(self):
        libapron.ap_lincons1_clear(self)

    @property
    def _as_parameter_(self):
        return byref(self.lincons1)

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyLincons1)
        return argument

    def __repr__(self):
        return '{}'.format(self.lincons1)


libapron.ap_lincons1_make_unsat.argtypes = [PyEnvironment]
libapron.ap_lincons1_make_unsat.restype = Lincons1
libapron.ap_lincons1_clear.argtypes = [PyLincons1]
