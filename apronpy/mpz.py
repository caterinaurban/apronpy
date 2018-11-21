"""
GMP Multi-Precision Integers
============================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER, byref
from ctypes import c_int, c_ulonglong, c_double, c_char_p
from apronpy.cdll import libgmp


class _MPZ(Structure):
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
        return str(self._mp_d.contents.value)


# initialization functions
MPZ_init = libgmp.__gmpz_init
MPZ_clear = libgmp.__gmpz_clear
# assignment functions
MPZ_set_d = libgmp.__gmpz_set_d
MPZ_set_str = libgmp.__gmpz_set_str
# combined initialization and assignment functions
MPZ_init_set_d = libgmp.__gmpz_init_set_d
# conversion functions
MPZ_get_str = libgmp.__gmpz_get_str
# arithmetic functions
MPZ_add = libgmp.__gmpz_add
MPZ_sub = libgmp.__gmpz_sub
MPZ_mul = libgmp.__gmpz_mul
MPZ_neg = libgmp.__gmpz_neg
MPZ_abs = libgmp.__gmpz_abs
# comparison functions
MPZ_cmp = libgmp.__gmpz_cmp  # -1: op1 < op2, 0: op1 == op2, 1: op1 > op2


class PyMPZ:
    def __init__(self, value: float = 0.0):
        self.mpz = _MPZ()
        MPZ_init_set_d(self, value)

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
        return MPZ_get_str(None, 10, self).decode("utf-8")

    def __add__(self, other: 'PyMPZ'):
        assert isinstance(other, PyMPZ)
        result = PyMPZ()
        MPZ_add(result, self, other)
        return result

    def __sub__(self, other: 'PyMPZ'):
        assert isinstance(other, PyMPZ)
        result = PyMPZ()
        MPZ_sub(result, self, other)
        return result

    def __mul__(self, other: 'PyMPZ'):
        assert isinstance(other, PyMPZ)
        result = PyMPZ()
        MPZ_mul(result, self, other)
        return result

    def __neg__(self):
        result = PyMPZ()
        MPZ_neg(result, self)
        return result

    def __abs__(self):
        result = PyMPZ()
        MPZ_abs(result, self)
        return result

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


# initialization functions
MPZ_init.argtypes = [PyMPZ]
MPZ_clear.argtypes = [PyMPZ]
# assignment functions
MPZ_set_d.argtypes = [PyMPZ, c_double]
MPZ_set_str.argtypes = [PyMPZ, c_char_p, c_int]
# combined initialization and assignment functions
MPZ_init_set_d.argtypes = [PyMPZ, c_double]
# conversion functions
MPZ_get_str.argtypes = [c_char_p, c_int, PyMPZ]
MPZ_get_str.restype = c_char_p
# arithmetic functions
MPZ_add.argtypes = [PyMPZ, PyMPZ, PyMPZ]
MPZ_sub.argtypes = [PyMPZ, PyMPZ, PyMPZ]
MPZ_mul.argtypes = [PyMPZ, PyMPZ, PyMPZ]
MPZ_neg.argtypes = [PyMPZ, PyMPZ]
MPZ_abs.argtypes = [PyMPZ, PyMPZ]
# # comparison functions
MPZ_cmp.argtypes = [PyMPZ, PyMPZ]
