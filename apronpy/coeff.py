"""
APRON Coefficients
==================

:Author: Caterina Urban
"""
from _ctypes import Union, Structure, POINTER
from abc import ABCMeta
from ctypes import c_uint
from enum import IntEnum

from apronpy.cdll import libapron
from apronpy.interval import Interval, PyInterval, PyDoubleInterval, PyMPQInterval, PyMPFRInterval
from apronpy.mpfr import Rnd
from apronpy.scalar import Scalar, PyScalar, PyDoubleScalar, PyMPQScalar, PyMPFRScalar


class CoeffDiscr(IntEnum):
    """
    typedef enum ap_coeff_discr_t {
      AP_COEFF_SCALAR,
      AP_COEFF_INTERVAL
    } ap_coeff_discr_t;
    """
    AP_COEFF_SCALAR = 0
    AP_COEFF_INTERVAL = 1


class Coeff(Structure):
    """
    typedef struct ap_coeff_t {
      ap_coeff_discr_t discr; /* discriminant for coefficient */
      union {
        ap_scalar_t* scalar;       /* cst (normal linear expression) */
        ap_interval_t* interval;   /* interval (quasi-linear expression) */
      } val;
    } ap_coeff_t;
    """
    class Val(Union):
        """
        union {
          ap_scalar_t* scalar;       /* cst (normal linear expression) */
          ap_interval_t* interval;   /* interval (quasi-linear expression) */
        } val;
        """

        _fields_ = [
            ('scalar', POINTER(Scalar)),
            ('interval', POINTER(Interval))
        ]

    _fields_ = [
        ('discr', c_uint),
        ('val', Val)
    ]

    def __repr__(self):
        if self.discr == CoeffDiscr.AP_COEFF_INTERVAL:
            return '{}'.format(self.val.interval.contents)
        else:  # self.discr == CoefficientDiscr.AP_COEFF_SCALAR
            return '{}'.format(self.val.scalar.contents)


class PyCoeff(metaclass=ABCMeta):

    def __init__(self, value, discr: CoeffDiscr = CoeffDiscr.AP_COEFF_SCALAR):
        self.coeff = libapron.ap_coeff_alloc(discr)
        if discr == CoeffDiscr.AP_COEFF_INTERVAL:
            libapron.ap_coeff_set_interval(self, value)
        else:  # discr == CoeffDiscr.AP_COEFF_SCALAR
            libapron.ap_coeff_set_scalar(self, value)

    def __del__(self):
        libapron.ap_coeff_free(self)

    @property
    def _as_parameter_(self):
        return self.coeff

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyCoeff)
        return argument

    def __repr__(self):
        return str(self.coeff.contents)

    def __lt__(self, other: 'PyCoeff'):
        assert isinstance(other, PyCoeff)
        return libapron.ap_coeff_cmp(self, other) == -1

    def __le__(self, other: 'PyCoeff'):
        assert isinstance(other, PyCoeff)
        return self.__lt__(other) or self.__eq__(other)

    def __eq__(self, other: 'PyCoeff'):
        assert isinstance(other, PyCoeff)
        return libapron.ap_coeff_cmp(self, other) == 0

    def __ne__(self, other: 'PyCoeff'):
        assert isinstance(other, PyCoeff)
        return not self.__eq__(other)

    def __ge__(self, other: 'PyCoeff'):
        assert isinstance(other, PyCoeff)
        return self.__gt__(other) or self.__eq__(other)

    def __gt__(self, other: 'PyCoeff'):
        assert isinstance(other, PyCoeff)
        return libapron.ap_coeff_cmp(self, other) == 1

    def __neg__(self) -> 'PyCoeff':
        if self.coeff.contents.discr == CoeffDiscr.AP_COEFF_INTERVAL:
            coeff = type(self)(0, 0)
        else:  # self.coeff.contents.discr == CoefficientDiscr.AP_COEFF_SCALAR
            coeff = type(self)(0)
        libapron.ap_coeff_neg(coeff, self)
        return coeff


libapron.ap_coeff_alloc.argtypes = [c_uint]
libapron.ap_coeff_alloc.restype = POINTER(Coeff)
libapron.ap_coeff_set.argtypes = [POINTER(Coeff), POINTER(Coeff)]
libapron.ap_coeff_set_scalar.argtypes = [PyCoeff, PyScalar]
libapron.ap_coeff_set_interval.argtypes = [PyCoeff, PyInterval]
libapron.ap_coeff_cmp.argtypes = [PyCoeff, PyCoeff]
libapron.ap_coeff_neg.argtypes = [PyCoeff, PyCoeff]


class PyScalarCoeff(PyCoeff, metaclass=ABCMeta):

    def __init__(self, scalar: PyScalar):
        super().__init__(discr=CoeffDiscr.AP_COEFF_SCALAR, value=scalar)


class PyDoubleScalarCoeff(PyScalarCoeff):

    def __init__(self, value=0.0):
        if isinstance(value, PyDoubleScalar):
            super().__init__(value)
        else:
            super().__init__(PyDoubleScalar(value))


class PyMPQScalarCoeff(PyScalarCoeff):

    def __init__(self, numerator=0, denumerator=1):
        if isinstance(numerator, PyMPQScalar):
            super().__init__(numerator)
        else:
            super().__init__(PyMPQScalar(numerator, denumerator))


class PyMPFRScalarCoeff(PyScalarCoeff):

    def __init__(self, value, rounding: Rnd = Rnd.MPFR_RNDN):
        if isinstance(value, PyMPFRScalar):
            super().__init__(value)
        else:
            super().__init__(PyMPFRScalar(value, rounding))


class PyIntervalCoeff(PyCoeff, metaclass=ABCMeta):

    def __init__(self, interval: PyInterval):
        super().__init__(discr=CoeffDiscr.AP_COEFF_INTERVAL, value=interval)


class PyDoubleIntervalCoeff(PyIntervalCoeff):

    def __init__(self, inf=0.0, sup=0.0):
        if isinstance(inf, PyDoubleInterval):
            super().__init__(inf)
        else:
            super().__init__(PyDoubleInterval(inf, sup))


class PyMPQIntervalCoeff(PyIntervalCoeff):

    def __init__(self, inf_num=0, sup_num=0, inf_den=1, sup_den=1):
        if isinstance(inf_num, PyMPQInterval):
            super().__init__(inf_num)
        else:
            super().__init__(PyMPQInterval(inf_num, sup_num, inf_den, sup_den))


class PyMPFRIntervalCoeff(PyIntervalCoeff):

    def __init__(self, inf, sup, rounding: Rnd = Rnd.MPFR_RNDN):
        if isinstance(inf, PyMPFRInterval):
            super().__init__(inf)
        else:
            super().__init__(PyMPFRInterval(inf, sup, rounding))
