"""
APRON Scalar Numbers
====================

:Author: Caterina Urban
"""
from abc import ABCMeta
from copy import deepcopy
from ctypes import *
from enum import IntEnum

from apronpy.mpfr import MPFR, PyMPFR, Rnd
from apronpy.mpq import PyMPQ, MPQ
from apronpy.cdll import libapron


class ScalarDiscr(IntEnum):
    """
    typedef enum ap_scalar_discr_t {
      AP_SCALAR_DOUBLE, /* double-precision floating-point number */
      AP_SCALAR_MPQ,    /* GMP arbitrary precision rational */
      AP_SCALAR_MPFR,   /* MPFR floating-point number */
    } ap_scalar_discr_t;
    """
    AP_SCALAR_DOUBLE = 0
    AP_SCALAR_MPQ = 1
    AP_SCALAR_MPFR = 2


class Scalar(Structure):
    """
    typedef struct ap_scalar_t {
      ap_scalar_discr_t discr;
      union {
        double dbl;
        mpq_ptr mpq; /* +infty coded by 1/0, -infty coded by -1/0 */
        mpfr_ptr mpfr;
      } val;
    } ap_scalar_t;
    """

    class Val(Union):
        """
        union {
          double dbl;
          mpq_ptr mpq; /* +infty coded by 1/0, -infty coded by -1/0 */
          mpfr_ptr mpfr;
        } val;
        """

        _fields_ = [
            ('dbl', c_double),
            ('mpq_ptr', POINTER(MPQ)),
            ('mpfr_ptr', POINTER(MPFR))
        ]

    _fields_ = [
        ('discr', c_uint),
        ('val', Val)
    ]

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        result = libapron.ap_scalar_alloc_set(byref(self)).contents
        memodict[id(self)] = result
        return result

    def __repr__(self):
        if self.discr == ScalarDiscr.AP_SCALAR_MPQ:
            return '{}'.format(self.val.mpq_ptr.contents)
        elif self.discr == ScalarDiscr.AP_SCALAR_MPFR:
            return '{}'.format(self.val.mpfr_ptr.contents)
        else:  # self.discr == Discr.AP_SCALAR_DOUBLE
            return '{}'.format(self.val.dbl)


class PyScalar(metaclass=ABCMeta):

    def __init__(self, value, discr: ScalarDiscr = ScalarDiscr.AP_SCALAR_DOUBLE):
        if isinstance(value, Scalar):
            self.scalar = byref(value)
        elif discr == ScalarDiscr.AP_SCALAR_MPQ:
            self.scalar = libapron.ap_scalar_alloc_set_mpq(value)
        elif discr == ScalarDiscr.AP_SCALAR_MPFR:
            self.scalar = libapron.ap_scalar_alloc_set_mpfr(value)
        else:
            assert discr == ScalarDiscr.AP_SCALAR_DOUBLE
            self.scalar = libapron.ap_scalar_alloc_set_double(value)

    @classmethod
    def init_infty(cls, sign: int):
        scalar = cls(0)
        libapron.ap_scalar_set_infty(scalar, sign)
        return scalar

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        result = type(self)(deepcopy(self.scalar.contents))
        memodict[id(self)] = result
        return result

    def __del__(self):
        libapron.ap_scalar_free(self)

    @property
    def _as_parameter_(self):
        return self.scalar

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyScalar)
        return argument

    def __repr__(self):
        return '{}'.format(self.scalar.contents)

    def infty(self):
        """-1: -infty, 0: finite; 1: +infty"""
        return libapron.ap_scalar_infty(self)

    def __lt__(self, other: 'PyScalar'):
        assert isinstance(other, PyScalar)
        return libapron.ap_scalar_cmp(self, other) < 0

    def __le__(self, other: 'PyScalar'):
        assert isinstance(other, PyScalar)
        return self.__lt__(other) or self.__eq__(other)

    def __eq__(self, other: 'PyScalar'):
        assert isinstance(other, PyScalar)
        return libapron.ap_scalar_cmp(self, other) == 0

    def __ne__(self, other: 'PyScalar'):
        assert isinstance(other, PyScalar)
        return not self.__eq__(other)

    def __ge__(self, other: 'PyScalar'):
        assert isinstance(other, PyScalar)
        return self.__gt__(other) or self.__eq__(other)

    def __gt__(self, other: 'PyScalar'):
        assert isinstance(other, PyScalar)
        return libapron.ap_scalar_cmp(self, other) > 0

    def sign(self):
        """-1: negative, 0: null, +1: positive"""
        return libapron.ap_scalar_sgn(self)

    def __neg__(self) -> 'PyScalar':
        scalar = type(self)(0)
        libapron.ap_scalar_neg(scalar, self)
        return scalar


libapron.ap_scalar_alloc.restype = POINTER(Scalar)
libapron.ap_scalar_set.argtypes = [POINTER(Scalar), PyScalar]
libapron.ap_scalar_alloc_set.argtypes = [POINTER(Scalar)]
libapron.ap_scalar_alloc_set.restype = POINTER(Scalar)
libapron.ap_scalar_alloc_set_double.argtypes = [c_double]
libapron.ap_scalar_alloc_set_double.restype = POINTER(Scalar)
libapron.ap_scalar_alloc_set_mpq.argtypes = [PyMPQ]
libapron.ap_scalar_alloc_set_mpq.restype = POINTER(Scalar)
libapron.ap_scalar_alloc_set_mpfr.argtypes = [PyMPFR]
libapron.ap_scalar_alloc_set_mpfr.restype = POINTER(Scalar)
libapron.ap_scalar_set_infty.argtypes = [PyScalar, c_int]
libapron.ap_scalar_free.argtypes = [PyScalar]
libapron.ap_scalar_infty.argtypes = [PyScalar]
libapron.ap_scalar_cmp.argtypes = [PyScalar, PyScalar]
libapron.ap_scalar_sgn.argtypes = [PyScalar]
libapron.ap_scalar_neg.argtypes = [PyScalar, PyScalar]


class PyDoubleScalar(PyScalar):

    def __init__(self, value=0.0):
        if isinstance(value, Scalar):
            super().__init__(discr=ScalarDiscr.AP_SCALAR_DOUBLE, value=value)
        elif isinstance(value, c_double):
            super().__init__(discr=ScalarDiscr.AP_SCALAR_DOUBLE, value=value)
        else:
            assert isinstance(value, (int, float))
            super().__init__(discr=ScalarDiscr.AP_SCALAR_DOUBLE, value=c_double(value))


class PyMPQScalar(PyScalar):

    def __init__(self, value_or_numerator=0, denumerator=1):
        if isinstance(value_or_numerator, (Scalar, PyMPQ)):
            super().__init__(discr=ScalarDiscr.AP_SCALAR_MPQ, value=value_or_numerator)
        elif isinstance(value_or_numerator, float):
            mpq = PyMPQ(value_or_numerator)
            super().__init__(discr=ScalarDiscr.AP_SCALAR_MPQ, value=mpq)
        else:
            assert isinstance(value_or_numerator, int) and isinstance(denumerator, int)
            mpq = PyMPQ(value_or_numerator, denumerator)
            super().__init__(discr=ScalarDiscr.AP_SCALAR_MPQ, value=mpq)


class PyMPFRScalar(PyScalar):

    def __init__(self, value, rounding: Rnd = Rnd.MPFR_RNDN):
        if isinstance(value, (Scalar, PyMPFR)):
            super().__init__(discr=ScalarDiscr.AP_SCALAR_MPFR, value=value)
        else:
            super().__init__(discr=ScalarDiscr.AP_SCALAR_MPFR, value=PyMPFR(value, rounding))
