"""
APRON Linear Expressions (Level 1)
==================================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER, byref
from copy import deepcopy
from ctypes import c_uint, c_size_t, c_char_p

from apronpy.cdll import libapron
from apronpy.coeff import Coeff, CoeffDiscr, PyDoubleIntervalCoeff, PyDoubleScalarCoeff, \
    PyMPQScalarCoeff, PyMPFRScalarCoeff, PyMPQIntervalCoeff, PyMPFRIntervalCoeff, PyCoeff
from apronpy.environment import Environment, PyEnvironment
from apronpy.linexpr0 import Linexpr0, LinexprDiscr
from apronpy.scalar import ScalarDiscr
from apronpy.var import PyVar


class Linexpr1(Structure):
    """
    typedef struct ap_linexpr1_t {
      ap_linexpr0_t* linexpr0;
      ap_environment_t* env;
    } ap_linexpr1_t;
    """

    _fields_ = [
        ('linexpr0', POINTER(Linexpr0)),
        ('env', POINTER(Environment))
    ]

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        result = libapron.ap_linexpr1_copy(byref(self))
        memodict[id(self)] = result
        return result

    def __repr__(self):
        linexpr0 = self.linexpr0.contents
        env = self.env.contents
        result = ''
        if linexpr0.discr == LinexprDiscr.AP_LINEXPR_DENSE:
            result += ' + '.join(
                '{}·{}'.format(linexpr0.p.coeff[i], env.var_of_dim[i].decode('utf-8'))
                for i in range(linexpr0.size)
            )
            result += ' + {}'.format(linexpr0.cst) if result else '{}'.format(linexpr0.cst)
        else:
            assert linexpr0.discr == LinexprDiscr.AP_LINEXPR_SPARSE
            terms = list()
            for i in range(linexpr0.size):
                coeff = linexpr0.p.linterm[i].coeff
                dim = linexpr0.p.linterm[i].dim.value
                if dim < linexpr0.size:
                    terms.append('{}·{}'.format(coeff, env.var_of_dim[dim].decode('utf-8')))
            result += ' + '.join(terms)
            result += ' + {}'.format(linexpr0.cst) if result else '{}'.format(linexpr0.cst)
        return result.replace('+ -', '- ')


class PyLinexpr1:

    def __init__(self, linexpr1_or_environment, discr=LinexprDiscr.AP_LINEXPR_SPARSE):
        if isinstance(linexpr1_or_environment, Linexpr1):
            self.linexpr1 = linexpr1_or_environment
        else:
            assert isinstance(linexpr1_or_environment, PyEnvironment)
            size = len(linexpr1_or_environment)
            self.linexpr1 = libapron.ap_linexpr1_make(linexpr1_or_environment, discr, size)

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        result = PyLinexpr1(deepcopy(self.linexpr1))
        memodict[id(self)] = result
        return result

    def __del__(self):
        libapron.ap_linexpr1_clear(self)

    @property
    def _as_parameter_(self):
        return byref(self.linexpr1)

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyLinexpr1)
        return argument

    def __repr__(self):
        return '{}'.format(self.linexpr1)

    def is_integer(self):
        linexpr0 = self.linexpr1.linexpr0
        intdim = self.linexpr1.env.contents.intdim
        return bool(libapron.ap_linexpr0_is_integer(linexpr0, intdim))

    def is_real(self):
        linexpr0 = self.linexpr1.linexpr0
        intdim = self.linexpr1.env.contents.intdim
        return bool(libapron.ap_linexpr0_is_real(linexpr0, intdim))

    def is_linear(self):
        linexpr0 = self.linexpr1.linexpr0
        return bool(libapron.ap_linexpr0_is_linear(linexpr0))

    def is_quasilinear(self):
        linexpr0 = self.linexpr1.linexpr0
        return bool(libapron.ap_linexpr0_is_quasilinear(linexpr0))

    def get_cst(self):
        cst = deepcopy(self.linexpr1.linexpr0.contents.cst)
        if cst.discr == CoeffDiscr.AP_COEFF_INTERVAL:
            if cst.val.interval.contents.inf.contents.discr == ScalarDiscr.AP_SCALAR_MPQ:
                result = PyMPQIntervalCoeff(cst)
            elif cst.val.interval.contents.inf.contents.discr == ScalarDiscr.AP_SCALAR_MPFR:
                result = PyMPFRIntervalCoeff(cst)
            else:
                assert cst.val.interval.contents.inf.contents.discr == ScalarDiscr.AP_SCALAR_DOUBLE
                result = PyDoubleIntervalCoeff(cst)
        else:
            assert cst.discr == CoeffDiscr.AP_COEFF_SCALAR
            if cst.val.scalar.contents.discr == ScalarDiscr.AP_SCALAR_MPQ:
                result = PyMPQScalarCoeff(cst)
            elif cst.val.scalar.contents.discr == ScalarDiscr.AP_SCALAR_MPFR:
                result = PyMPFRScalarCoeff(cst)
            else:
                assert cst.val.scalar.contents.discr == ScalarDiscr.AP_SCALAR_DOUBLE
                result = PyDoubleScalarCoeff(cst)
        return result

    def set_cst(self, cst: PyCoeff):
        libapron.ap_coeff_set(byref(self.linexpr1.linexpr0.contents.cst), cst.coeff)

    def get_coeff(self, var: PyVar):
        coeff = libapron.ap_linexpr1_coeffref(self, var._as_parameter_)
        if coeff.contents.discr == CoeffDiscr.AP_COEFF_INTERVAL:
            discr = coeff.contents.val.interval.contents.inf.contents.discr
            if discr == ScalarDiscr.AP_SCALAR_MPQ:
                result = PyMPQIntervalCoeff()
            elif discr == ScalarDiscr.AP_SCALAR_MPFR:
                result = PyMPFRIntervalCoeff(0, 0)
            else:  # discr == ScalarDiscr.AP_SCALAR_DOUBLE
                result = PyDoubleIntervalCoeff()
        else:  # CoeffDiscr.AP_COEFF_SCALAR
            if coeff.contents.val.scalar.contents.discr == ScalarDiscr.AP_SCALAR_MPQ:
                result = PyMPQScalarCoeff()
            elif coeff.contents.val.scalar.contents.discr == ScalarDiscr.AP_SCALAR_MPFR:
                result = PyMPFRScalarCoeff(0)
            else:  # coeff.contents.val.scalar.contents.discr == ScalarDiscr.AP_SCALAR_DOUBLE
                result = PyDoubleScalarCoeff()
        libapron.ap_linexpr1_get_coeff(result.coeff, self, var._as_parameter_)
        return result

    def set_coeff(self, var: PyVar, coeff: PyCoeff):
        libapron.ap_coeff_set(libapron.ap_linexpr1_coeffref(self, var._as_parameter_), coeff.coeff)


libapron.ap_linexpr1_make.argtypes = [PyEnvironment, c_uint, c_size_t]
libapron.ap_linexpr1_make.restype = Linexpr1
libapron.ap_linexpr1_copy.argtypes = [POINTER(Linexpr1)]
libapron.ap_linexpr1_copy.restype = Linexpr1
libapron.ap_linexpr1_clear.argtypes = [PyLinexpr1]
libapron.ap_linexpr1_coeffref.argtypes = [PyLinexpr1, c_char_p]
libapron.ap_linexpr1_coeffref.restype = POINTER(Coeff)
libapron.ap_linexpr1_get_coeff.argtypes = [POINTER(Coeff), PyLinexpr1, c_char_p]
