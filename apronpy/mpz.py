"""
GMP Multi-Precision Integers
============================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER, byref
from ctypes import c_int, c_ulonglong, c_double, c_char_p
from typing import Union

from apronpy.cdll import libgmp

# initialization and assignment functions
MPZ_clear = libgmp.__gmpz_clear
MPZ_init_set = libgmp.__gmpz_init_set
MPZ_init_set_d = libgmp.__gmpz_init_set_d
# conversion functions
MPZ_get_str = libgmp.__gmpz_get_str
# comparison functions
MPZ_cmp = libgmp.__gmpz_cmp  # -1: op1 < op2, 0: op1 == op2, 1: op1 > op2
# arithmetic functions
MPZ_add = libgmp.__gmpz_add
MPZ_sub = libgmp.__gmpz_sub
MPZ_mul = libgmp.__gmpz_mul
MPZ_neg = libgmp.__gmpz_neg
MPZ_abs = libgmp.__gmpz_abs


class MPZ(Structure):
    """
    typedef struct
    {
      int _mp_alloc;
      int _mp_size;
      mp_limb_t *_mp_d;
    } __mpz_struct;
    """
    _fields_ = [
        ('_mp_alloc', c_int),
        ('_mp_size', c_int),
        ('_mp_d', POINTER(c_ulonglong))
    ]

    def __repr__(self):
        return MPZ_get_str(None, 10, self).decode('utf-8')


class PyMPZ:

    def __init__(self, value: Union[MPZ, int, float] = 0):
        self.mpz = MPZ()
        if isinstance(value, MPZ):
            MPZ_init_set(self, value)
        else:
            assert isinstance(value, (int, float))
            MPZ_init_set_d(self, c_double(value))

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        result = PyMPZ(self.mpz)
        memodict[id(self)] = result
        return result

    def __del__(self):
        MPZ_clear(self)

    @property
    def _as_parameter_(self):
        return byref(self.mpz)

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyMPZ)
        return argument

    def __repr__(self):
        return MPZ_get_str(None, 10, self.mpz).decode('utf-8')

    def __lt__(self, other: 'PyMPZ'):
        assert isinstance(other, PyMPZ)
        return MPZ_cmp(self, other) < 0

    def __le__(self, other: 'PyMPZ'):
        assert isinstance(other, PyMPZ)
        return self.__lt__(other) or self.__eq__(other)

    def __eq__(self, other: 'PyMPZ'):
        assert isinstance(other, PyMPZ)
        return MPZ_cmp(self, other) == 0

    def __ne__(self, other: 'PyMPZ'):
        assert isinstance(other, PyMPZ)
        return not self.__eq__(other)

    def __ge__(self, other: 'PyMPZ'):
        assert isinstance(other, PyMPZ)
        return self.__gt__(other) or self.__eq__(other)

    def __gt__(self, other: 'PyMPZ'):
        assert isinstance(other, PyMPZ)
        return MPZ_cmp(self, other) > 0

    def __add__(self, other: 'PyMPZ') -> 'PyMPZ':
        assert isinstance(other, PyMPZ)
        mpz = type(self)(0)
        MPZ_add(mpz, self, other)
        return mpz

    def __sub__(self, other: 'PyMPZ') -> 'PyMPZ':
        assert isinstance(other, PyMPZ)
        mpz = type(self)(0)
        MPZ_sub(mpz, self, other)
        return mpz

    def __mul__(self, other: 'PyMPZ') -> 'PyMPZ':
        assert isinstance(other, PyMPZ)
        mpz = type(self)(0)
        MPZ_mul(mpz, self, other)
        return mpz

    def __neg__(self) -> 'PyMPZ':
        mpz = type(self)(0)
        MPZ_neg(mpz, self)
        return mpz

    def __abs__(self) -> 'PyMPZ':
        mpz = type(self)(0)
        MPZ_abs(mpz, self)
        return mpz


# initialization and assignment functions
MPZ_clear.argtypes = [PyMPZ]
MPZ_init_set.argtypes = [PyMPZ, POINTER(MPZ)]
MPZ_init_set_d.argtypes = [PyMPZ, c_double]
# conversion functions
MPZ_get_str.argtypes = [c_char_p, c_int, POINTER(MPZ)]
MPZ_get_str.restype = c_char_p
# comparison functions
MPZ_cmp.argtypes = [PyMPZ, PyMPZ]
# arithmetic functions
MPZ_add.argtypes = [PyMPZ, PyMPZ, PyMPZ]
MPZ_sub.argtypes = [PyMPZ, PyMPZ, PyMPZ]
MPZ_mul.argtypes = [PyMPZ, PyMPZ, PyMPZ]
MPZ_neg.argtypes = [PyMPZ, PyMPZ]
MPZ_abs.argtypes = [PyMPZ, PyMPZ]
