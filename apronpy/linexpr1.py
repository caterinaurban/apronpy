"""
APRON Linear Expressions (Level 1)
==================================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER, byref
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


class PyLinexpr1:

    def __init__(self, environment: PyEnvironment, discr=LinexprDiscr.AP_LINEXPR_SPARSE):
        self.linexpr1 = libapron.ap_linexpr1_make(environment, discr, len(environment))

    def __del__(self):
        libapron.ap_linexpr1_clear(self)

    @property
    def _as_parameter_(self):
        return byref(self.linexpr1)

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyLinexpr1)
        return argument

    """Tests"""

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

    def get_coeff(self, var: PyVar):
        coeff = libapron.ap_linexpr1_coeffref(self, var._as_parameter_)
        if coeff.contents.discr == CoeffDiscr.AP_COEFF_INTERVAL:
            if coeff.contents.val.interval.contents.inf.contents.discr == ScalarDiscr.AP_SCALAR_MPQ:
                result = PyMPQIntervalCoeff()
            elif coeff.contents.val.interval.contents.inf.contents.discr == ScalarDiscr.AP_SCALAR_MPFR:
                result = PyMPFRIntervalCoeff(0, 0)
            else:  # coeff.contents.val.interval.contents.inf.contents.discr == ScalarDiscr.AP_SCALAR_DOUBLE
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
        libapron.ap_coeff_set(libapron.ap_linexpr1_coeffref(self, var._as_parameter_), coeff)


libapron.ap_linexpr1_make.argtypes = [PyEnvironment, c_uint, c_size_t]
libapron.ap_linexpr1_make.restype = Linexpr1
libapron.ap_linexpr1_clear.argtypes = [PyLinexpr1]
libapron.ap_linexpr0_is_integer.argtypes = [POINTER(Linexpr0), c_size_t]
libapron.ap_linexpr0_is_real.argtypes = [POINTER(Linexpr0), c_size_t]
libapron.ap_linexpr0_is_linear.argtypes = [POINTER(Linexpr0)]
libapron.ap_linexpr0_is_quasilinear.argtypes = [POINTER(Linexpr0)]
libapron.ap_linexpr1_coeffref.argtypes = [PyLinexpr1, c_char_p]
libapron.ap_linexpr1_coeffref.restype = POINTER(Coeff)
libapron.ap_linexpr1_get_coeff.argtypes = [POINTER(Coeff), PyLinexpr1, c_char_p]
