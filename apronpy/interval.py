"""
APRON Intervals on Scalars
==========================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER
from abc import ABCMeta
from ctypes import c_double, c_int

from apronpy.cdll import libapron
from apronpy.mpfr import PyMPFR, Rnd
from apronpy.mpq import PyMPQ
from apronpy.scalar import Scalar, PyScalar, PyDoubleScalar, PyMPQScalar, PyMPFRScalar


class Interval(Structure):
    """
    typedef struct ap_interval_t {
      ap_scalar_t* inf;
      ap_scalar_t* sup;
    } ap_interval_t;
    """
    _fields_ = [
        ('inf', POINTER(Scalar)),
        ('sup', POINTER(Scalar))
    ]

    def __repr__(self):
        return '[{},{}]'.format(self.inf.contents, self.sup.contents)


class PyInterval(metaclass=ABCMeta):

    def __init__(self, inf, sup):
        self.interval = libapron.ap_interval_alloc()
        if isinstance(inf, c_double) and isinstance(sup, c_double):
            libapron.ap_interval_set_double(self, inf, sup)
        elif isinstance(inf, PyMPQ) and isinstance(sup, PyMPQ):
            libapron.ap_interval_set_mpq(self, inf, sup)
        elif isinstance(inf, PyMPFR) and isinstance(sup, PyMPFR):
            libapron.ap_interval_set_mpfr(self, inf, sup)
        elif isinstance(inf, PyScalar) and isinstance(sup, PyScalar):
            libapron.ap_interval_set_scalar(self, inf, sup)

    @classmethod
    def init_top(cls):
        interval = cls(0, 0)
        libapron.ap_interval_set_top(interval)
        return interval

    @classmethod
    def init_bottom(cls):
        interval = cls(0, 0)
        libapron.ap_interval_set_bottom(interval)
        return interval

    def __del__(self):
        libapron.ap_interval_free(self)

    @property
    def _as_parameter_(self):
        return self.interval

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyInterval)
        return argument

    def __repr__(self):
        return str(self.interval.contents)


libapron.ap_interval_alloc.restype = POINTER(Interval)
libapron.ap_interval_set_int.argtypes = [PyInterval, c_int, c_int]
libapron.ap_interval_set_double.argtypes = [PyInterval, c_double, c_double]
libapron.ap_interval_set_mpq.argtypes = [PyInterval, PyMPQ, PyMPQ]
libapron.ap_interval_set_mpfr.argtypes = [PyInterval, PyMPFR, PyMPFR]
libapron.ap_interval_set_scalar.argtypes = [PyInterval, PyScalar, PyScalar]


class PyDoubleInterval(PyInterval):

    def __init__(self, inf=0.0, sup=0.0):
        if isinstance(inf, PyDoubleScalar) and isinstance(sup, PyDoubleScalar):
            super().__init__(inf, sup)
        elif isinstance(inf, c_double) and isinstance(sup, c_double):
            super().__init__(inf, sup)
        else:
            super().__init__(c_double(inf), c_double(sup))


class PyMPQInterval(PyInterval):

    def __init__(self, inf_num=0, sup_num=0, inf_den=1, sup_den=1):
        if isinstance(inf_num, PyMPQScalar) and isinstance(sup_num, PyMPQScalar):
            super().__init__(inf_num, sup_num)
        elif isinstance(inf_num, PyMPQ) and isinstance(sup_num, PyMPQ):
            super().__init__(inf_num, sup_num)
        else:
            super().__init__(PyMPQ(inf_num, inf_den), PyMPQ(sup_num, sup_den))


class PyMPFRInterval(PyInterval):

    def __init__(self, inf, sup, rounding: Rnd = Rnd.MPFR_RNDN):
        if isinstance(inf, PyMPFRScalar) and isinstance(sup, PyMPFRScalar):
            super().__init__(inf, sup)
        elif isinstance(inf, PyMPFR) and isinstance(sup, PyMPFR):
            super().__init__(inf, sup)
        else:
            super().__init__(PyMPFR(inf, rounding), PyMPFR(sup, rounding))
