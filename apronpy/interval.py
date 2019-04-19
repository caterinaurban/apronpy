"""
APRON Intervals on Scalars
==========================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER, byref
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

    def __init__(self, value_or_inf, sup=None):
        self.interval = libapron.ap_interval_alloc()
        if isinstance(value_or_inf, Interval):
            libapron.ap_interval_set(self, byref(value_or_inf))
        elif isinstance(value_or_inf, c_double) and isinstance(sup, c_double):
            libapron.ap_interval_set_double(self, value_or_inf, sup)
        elif isinstance(value_or_inf, PyMPQ) and isinstance(sup, PyMPQ):
            libapron.ap_interval_set_mpq(self, value_or_inf, sup)
        elif isinstance(value_or_inf, PyMPFR) and isinstance(sup, PyMPFR):
            libapron.ap_interval_set_mpfr(self, value_or_inf, sup)
        else:
            assert isinstance(value_or_inf, PyScalar) and isinstance(sup, PyScalar)
            libapron.ap_interval_set_scalar(self, value_or_inf, sup)

    @classmethod
    def top(cls):
        interval = cls(0, 0)
        libapron.ap_interval_set_top(interval)
        return interval

    @classmethod
    def bottom(cls):
        interval = cls(0, 0)
        libapron.ap_interval_set_bottom(interval)
        return interval

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        result = type(self)(self.interval.contents)
        memodict[id(self)] = result
        return result

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

    def is_bottom(self):
        return bool(libapron.ap_interval_is_bottom(self))
    
    def __lt__(self, other: 'PyInterval'):
        assert isinstance(other, PyInterval)
        return libapron.ap_interval_cmp(self, other) == -1

    def __le__(self, other: 'PyInterval'):
        assert isinstance(other, PyInterval)
        return self.__lt__(other) or self.__eq__(other)

    def __eq__(self, other):
        assert isinstance(other, PyInterval)
        return libapron.ap_interval_cmp(self, other) == 0

    def __ne__(self, other):
        assert isinstance(other, PyInterval)
        return not self.__eq__(other)

    def __ge__(self, other):
        assert isinstance(other, PyInterval)
        return self.__gt__(other) or self.__eq__(other)

    def __gt__(self, other):
        assert isinstance(other, PyInterval)
        return libapron.ap_interval_cmp(self, other) == 1

    def is_top(self):
        return bool(libapron.ap_interval_is_top(self))

    def __neg__(self) -> 'PyInterval':
        interval = type(self)(0, 0)
        libapron.ap_interval_neg(interval, self)
        return interval


libapron.ap_interval_alloc.restype = POINTER(Interval)
libapron.ap_interval_set.argtypes = [PyInterval, POINTER(Interval)]
libapron.ap_interval_set_int.argtypes = [PyInterval, c_int, c_int]
libapron.ap_interval_set_double.argtypes = [PyInterval, c_double, c_double]
libapron.ap_interval_set_mpq.argtypes = [PyInterval, PyMPQ, PyMPQ]
libapron.ap_interval_set_mpfr.argtypes = [PyInterval, PyMPFR, PyMPFR]
libapron.ap_interval_set_scalar.argtypes = [PyInterval, PyScalar, PyScalar]
libapron.ap_interval_is_bottom.argtypes = [PyInterval]
libapron.ap_interval_is_top.argtypes = [PyInterval]
libapron.ap_interval_cmp.argtypes = [PyInterval, PyInterval]
libapron.ap_interval_neg.argtypes = [PyInterval, PyInterval]


class PyDoubleInterval(PyInterval):

    def __init__(self, value_or_inf=0.0, sup=0.0):
        if isinstance(value_or_inf, Interval):
            super().__init__(value_or_inf)
        elif isinstance(value_or_inf, PyDoubleScalar) and isinstance(sup, PyDoubleScalar):
            super().__init__(value_or_inf, sup)
        elif isinstance(value_or_inf, c_double) and isinstance(sup, c_double):
            super().__init__(value_or_inf, sup)
        else:
            super().__init__(c_double(value_or_inf), c_double(sup))


class PyMPQInterval(PyInterval):

    def __init__(self, value_or_inf_num=0, sup_num=0, inf_den=1, sup_den=1):
        if isinstance(value_or_inf_num, Interval):
            super().__init__(value_or_inf_num)
        elif isinstance(value_or_inf_num, PyMPQScalar) and isinstance(sup_num, PyMPQScalar):
            super().__init__(value_or_inf_num, sup_num)
        elif isinstance(value_or_inf_num, PyMPQ) and isinstance(sup_num, PyMPQ):
            super().__init__(value_or_inf_num, sup_num)
        else:
            super().__init__(PyMPQ(value_or_inf_num, inf_den), PyMPQ(sup_num, sup_den))


class PyMPFRInterval(PyInterval):

    def __init__(self, value_or_inf, sup=None, rounding: Rnd = Rnd.MPFR_RNDN):
        if isinstance(value_or_inf, Interval):
            super().__init__(value_or_inf)
        elif isinstance(value_or_inf, PyMPFRScalar) and isinstance(sup, PyMPFRScalar):
            super().__init__(value_or_inf, sup)
        elif isinstance(value_or_inf, PyMPFR) and isinstance(sup, PyMPFR):
            super().__init__(value_or_inf, sup)
        else:
            super().__init__(PyMPFR(value_or_inf, rounding), PyMPFR(sup, rounding))
