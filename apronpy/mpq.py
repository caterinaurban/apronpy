"""
GMP Multi-Precision Rationals
=============================

:Author: Caterina Urban
"""
from _ctypes import Structure, byref
from ctypes import c_int, c_char_p, c_long
from apronpy.mpz import MPZ
from apronpy.cdll import libgmp


class MPQ(Structure):
    """
    typedef struct
    {
      __mpz_struct _mp_num;
      __mpz_struct _mp_den;
    } __mpq_struct;
    """
    _fields_ = [
        ('_mp_num', MPZ),
        ('_mp_den', MPZ)
    ]

    def __repr__(self):
        return '{}/{}'.format(self._mp_num, self._mp_den)


MPQ_canonicalize = libgmp.__gmpq_canonicalize
# initialization functions
MPQ_init = libgmp.__gmpq_init
MPQ_clear = libgmp.__gmpq_clear
# assignment functions
MPQ_set_si = libgmp.__gmpq_set_si
# conversion functions
MPQ_get_str = libgmp.__gmpq_get_str
# comparison functions
MPQ_cmp = libgmp.__gmpq_cmp  # -1: op1 < op2, 0: op1 == op2, 1: op1 > op2
# arithmetic functions
MPQ_add = libgmp.__gmpq_add
MPQ_sub = libgmp.__gmpq_sub
MPQ_mul = libgmp.__gmpq_mul
MPQ_neg = libgmp.__gmpq_neg
MPQ_abs = libgmp.__gmpq_abs


class PyMPQ:

    def __init__(self, numerator: int = 0, denominator: int = 1):
        self.mpq = MPQ()
        MPQ_init(self)
        MPQ_set_si(self, numerator, denominator)
        MPQ_canonicalize(self)

    def __del__(self):
        MPQ_clear(self)

    @property
    def _as_parameter_(self):
        return byref(self.mpq)

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyMPQ)
        return argument

    """
    Conversion Functions
    """

    def __repr__(self):
        return MPQ_get_str(None, 10, self).decode("utf-8")

    """
    Comparison Functions
    """

    def __lt__(self, other: 'PyMPQ'):
        assert isinstance(other, PyMPQ)
        return MPQ_cmp(self, other) < 0

    def __le__(self, other: 'PyMPQ'):
        assert isinstance(other, PyMPQ)
        return self.__lt__(other) or self.__eq__(other)

    def __eq__(self, other: 'PyMPQ'):
        assert isinstance(other, PyMPQ)
        return MPQ_cmp(self, other) == 0

    def __ne__(self, other: 'PyMPQ'):
        assert isinstance(other, PyMPQ)
        return not self.__eq__(other)

    def __ge__(self, other: 'PyMPQ'):
        assert isinstance(other, PyMPQ)
        return self.__gt__(other) or self.__eq__(other)

    def __gt__(self, other: 'PyMPQ'):
        assert isinstance(other, PyMPQ)
        return MPQ_cmp(self, other) > 0

    """
    Arithmetic Functions
    """

    def __add__(self, other: 'PyMPQ'):
        assert isinstance(other, PyMPQ)
        MPQ_add(self, self, other)
        return self

    def __sub__(self, other: 'PyMPQ'):
        assert isinstance(other, PyMPQ)
        MPQ_sub(self, self, other)
        return self

    def __mul__(self, other: 'PyMPQ'):
        assert isinstance(other, PyMPQ)
        MPQ_mul(self, self, other)
        return self

    def __neg__(self):
        MPQ_neg(self, self)
        return self

    def __abs__(self):
        MPQ_abs(self, self)
        return self


MPQ_canonicalize.argtypes = [PyMPQ]
# initialization functions
MPQ_init.argtypes = [PyMPQ]
MPQ_clear.argtypes = [PyMPQ]
# assignment functions
MPQ_set_si.argtypes = [PyMPQ, c_long, c_long]
# conversion functions
MPQ_get_str.argtypes = [c_char_p, c_int, PyMPQ]
MPQ_get_str.restype = c_char_p
# comparison functions
MPQ_cmp.argtypes = [PyMPQ, PyMPQ]
# arithmetic functions
MPQ_add.argtypes = [PyMPQ, PyMPQ, PyMPQ]
MPQ_sub.argtypes = [PyMPQ, PyMPQ, PyMPQ]
MPQ_mul.argtypes = [PyMPQ, PyMPQ, PyMPQ]
MPQ_neg.argtypes = [PyMPQ, PyMPQ]
MPQ_abs.argtypes = [PyMPQ, PyMPQ]
