"""
GMP Multi-Precision Rationals
=============================

:Author: Caterina Urban
"""
from _ctypes import Structure, byref, POINTER
from ctypes import c_int, c_char_p, c_long, c_ulong, c_double
from typing import Union

from apronpy.cdll import libgmp
from apronpy.mpz import MPZ

MPQ_canonicalize = libgmp.__gmpq_canonicalize
# initialization functions
MPQ_init = libgmp.__gmpq_init
MPQ_clear = libgmp.__gmpq_clear
# assignment functions
MPQ_set = libgmp.__gmpq_set
MPQ_set_si = libgmp.__gmpq_set_si
MPQ_set_d = libgmp.__gmpq_set_d
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
        return MPQ_get_str(None, 10, self).decode("utf-8")


class PyMPQ:

    def __init__(self, value_or_numerator: Union[MPQ, float, int] = 0, denominator: int = 1):
        self.mpq = MPQ()
        MPQ_init(self)
        if isinstance(value_or_numerator, MPQ):
            MPQ_set(self, value_or_numerator)
        elif isinstance(value_or_numerator, float):
            MPQ_set_d(self, value_or_numerator)
        else:
            assert isinstance(value_or_numerator, int) and isinstance(denominator, int)
            MPQ_set_si(self, c_long(value_or_numerator), c_ulong(denominator))
            MPQ_canonicalize(self)

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        result = PyMPQ(self.mpq)
        memodict[id(self)] = result
        return result

    def __del__(self):
        MPQ_clear(self)

    @property
    def _as_parameter_(self):
        return byref(self.mpq)

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyMPQ)
        return argument

    def __repr__(self):
        return MPQ_get_str(None, 10, self.mpq).decode("utf-8")

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

    def __add__(self, other: 'PyMPQ') -> 'PyMPQ':
        assert isinstance(other, PyMPQ)
        mpq = type(self)(0, 1)
        MPQ_add(mpq, self, other)
        return mpq

    def __sub__(self, other: 'PyMPQ') -> 'PyMPQ':
        assert isinstance(other, PyMPQ)
        mpq = type(self)(0, 1)
        MPQ_sub(mpq, self, other)
        return mpq

    def __mul__(self, other: 'PyMPQ') -> 'PyMPQ':
        assert isinstance(other, PyMPQ)
        mpq = type(self)(0, 1)
        MPQ_mul(mpq, self, other)
        return mpq

    def __neg__(self) -> 'PyMPQ':
        mpq = type(self)(0, 1)
        MPQ_neg(mpq, self)
        return mpq

    def __abs__(self) -> 'PyMPQ':
        mpq = type(self)(0, 1)
        MPQ_abs(mpq, self)
        return mpq


MPQ_canonicalize.argtypes = [PyMPQ]
# initialization functions
MPQ_init.argtypes = [PyMPQ]
MPQ_clear.argtypes = [PyMPQ]
# assignment functions
MPQ_set.argtypes = [PyMPQ, POINTER(MPQ)]
MPQ_set_si.argtypes = [PyMPQ, c_long, c_ulong]
MPQ_set_d.argtypes = [PyMPQ, c_double]
# conversion functions
MPQ_get_str.argtypes = [c_char_p, c_int, POINTER(MPQ)]
MPQ_get_str.restype = c_char_p
# comparison functions
MPQ_cmp.argtypes = [PyMPQ, PyMPQ]
# arithmetic functions
MPQ_add.argtypes = [PyMPQ, PyMPQ, PyMPQ]
MPQ_sub.argtypes = [PyMPQ, PyMPQ, PyMPQ]
MPQ_mul.argtypes = [PyMPQ, PyMPQ, PyMPQ]
MPQ_neg.argtypes = [PyMPQ, PyMPQ]
MPQ_abs.argtypes = [PyMPQ, PyMPQ]
