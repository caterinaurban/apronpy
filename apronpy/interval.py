"""
APRON Intervals on Scalars
==========================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER
from ctypes import c_double, c_int
from warnings import warn

from apronpy.cdll import libapron
from apronpy.mpfr import PyMPFR
from apronpy.mpq import PyMPQ
from apronpy.scalar import Scalar, PyScalar


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


class PyInterval:

    def __init__(self, inf=0.0, sup=0.0):
        self.interval = libapron.ap_interval_alloc()
        if isinstance(inf, int) and isinstance(sup, int):
            libapron.ap_interval_set_int(self, c_int(inf), c_int(sup))
        elif isinstance(inf, c_int) and isinstance(sup, c_int):
            libapron.ap_interval_set_int(self, inf, sup)
        elif isinstance(inf, float) and isinstance(sup, float):
            libapron.ap_interval_set_double(self, c_double(inf), c_double(sup))
        elif isinstance(inf, c_double) and isinstance(sup, c_double):
            libapron.ap_interval_set_double(self, inf, sup)
        elif isinstance(inf, PyMPQ) and isinstance(sup, PyMPQ):
            libapron.ap_interval_set_mpq(self, inf, sup)
        elif isinstance(inf, PyMPFR) and isinstance(sup, PyMPFR):
            libapron.ap_interval_set_mpfr(self, inf, sup)
        elif isinstance(inf, PyScalar) and isinstance(sup, PyScalar):
            libapron.ap_interval_set_scalar(self, inf, sup)
        else:
            warning = "interval bounds have unexpected types "
            warning += "so their value has been discarded.\n"
            warning += "Expected types are: "
            warning += "int, c_int, float, c_double, PyMPQ, PyMPFR, or PyScalar."
            warn(warning)

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
