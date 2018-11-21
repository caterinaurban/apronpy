"""
GMP Multi-Precision Rationals
=============================

:Author: Caterina Urban
"""
from _ctypes import Structure, byref
from ctypes import c_int, c_double, c_char_p
from apronpy.mpz import _MPZ
from apronpy.cdll import libgmp


class _MPQ(Structure):
    """
    typedef struct
    {
      __mpz_struct _mp_num;
      __mpz_struct _mp_den;
    } __mpq_struct;
    """
    _fields_ = [
        ('_mp_num', _MPZ),
        ('_mp_den', _MPZ)
    ]

    def __repr__(self):
        return '{}/{}'.format(self._mp_num, self._mp_den)


# initialization functions
MPQ_init = libgmp.__gmpq_init
MPQ_clear = libgmp.__gmpq_clear
# assignment functions
MPQ_set_d = libgmp.__gmpq_set_d
MPQ_set_str = libgmp.__gmpq_set_str
# conversion functions
MPQ_get_str = libgmp.__gmpq_get_str
# arithmetic functions
MPQ_add = libgmp.__gmpq_add
MPQ_sub = libgmp.__gmpq_sub
MPQ_mul = libgmp.__gmpq_mul
MPQ_neg = libgmp.__gmpq_neg
MPQ_abs = libgmp.__gmpq_abs
# comparison functions
MPQ_cmp = libgmp.__gmpq_cmp  # -1: op1 < op2, 0: op1 == op2, 1: op1 > op2


class PyMPQ:
    def __init__(self, value: float = 0.0):
        self.mpq = _MPQ()
        MPQ_init(self)
        MPQ_set_d(self, value)

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
        return MPQ_get_str(None, 10, self).decode("utf-8")

    def __add__(self, other: 'PyMPQ'):
        assert isinstance(other, PyMPQ)
        result = PyMPQ()
        MPQ_add(result, self, other)
        return result

    def __sub__(self, other: 'PyMPQ'):
        assert isinstance(other, PyMPQ)
        result = PyMPQ()
        MPQ_sub(result, self, other)
        return result

    def __mul__(self, other: 'PyMPQ'):
        assert isinstance(other, PyMPQ)
        result = PyMPQ()
        MPQ_mul(result, self, other)
        return result

    def __neg__(self):
        result = PyMPQ()
        MPQ_neg(result, self)
        return result

    def __abs__(self):
        result = PyMPQ()
        MPQ_abs(result, self)
        return result

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


# initialization functions
MPQ_init.argtypes = [PyMPQ]
MPQ_clear.argtypes = [PyMPQ]
# assignment functions
MPQ_set_d.argtypes = [PyMPQ, c_double]
MPQ_set_str.argtypes = [PyMPQ, c_char_p, c_int]
# conversion functions
MPQ_get_str.argtypes = [c_char_p, c_int, PyMPQ]
MPQ_get_str.restype = c_char_p
# arithmetic functions
MPQ_add.argtypes = [PyMPQ, PyMPQ, PyMPQ]
MPQ_sub.argtypes = [PyMPQ, PyMPQ, PyMPQ]
MPQ_mul.argtypes = [PyMPQ, PyMPQ, PyMPQ]
MPQ_neg.argtypes = [PyMPQ, PyMPQ]
MPQ_abs.argtypes = [PyMPQ, PyMPQ]
# # comparison functions
MPQ_cmp.argtypes = [PyMPQ, PyMPQ]

# q = PyMPQ(0.5)
# print(q)
