"""
MPFR Multiprecision Floating-Point Numbers
==========================================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER, byref
from ctypes import c_long, c_int, c_ulonglong, c_double
from enum import IntEnum
from typing import Union

from apronpy.cdll import libmpfr


# initialization and assignment functions
MPFR_init = libmpfr.mpfr_init
MPFR_clear = libmpfr.mpfr_clear
MPFR_set = libmpfr.mpfr_set
MPFR_set_d = libmpfr.mpfr_set_d
# conversion functions
MPFR_get_d = libmpfr.mpfr_get_d
# comparison functions
MPFR_cmp = libmpfr.mpfr_cmp  # -1: op1 < op2, 0: op1 == op2, 1: op1 > op2
# arithmetic functions
MPFR_add = libmpfr.mpfr_add
MPFR_sub = libmpfr.mpfr_sub
MPFR_mul = libmpfr.mpfr_mul
MPFR_neg = libmpfr.mpfr_neg
MPFR_abs = libmpfr.mpfr_abs


class MPFR(Structure):
    """
    typedef struct {
      mpfr_prec_t  _mpfr_prec;
      mpfr_sign_t  _mpfr_sign;
      mpfr_exp_t   _mpfr_exp;
      mp_limb_t   *_mpfr_d;
    } __mpfr_struct;
    """
    _fields_ = [
        ('_mpfr_prec', c_long),
        ('_mpfr_sign', c_int),
        ('_mpfr_exp', c_long),
        ('_mpfr_d', POINTER(c_ulonglong))
    ]

    def __repr__(self):
        return '{}'.format(MPFR_get_d(self, 0))


class Rnd(IntEnum):
    """
    typedef enum {
      MPFR_RNDN=0,  /* round to nearest, with ties to even */
      MPFR_RNDZ,    /* round toward zero */
      MPFR_RNDU,    /* round toward +Inf */
      MPFR_RNDD,    /* round toward -Inf */
      MPFR_RNDA,    /* round away from zero */
      MPFR_RNDF,    /* faithful rounding */
      MPFR_RNDNA=-1 /* round to nearest, with ties away from zero (mpfr_round) */
    } mpfr_rnd_t;
    """
    MPFR_RNDN = 0
    MPFR_RNDZ = 1
    MPFR_RNDU = 2
    MPFR_RNDD = 3
    MPFR_RNDA = 4
    MPFR_RNDF = 5
    MPFR_RNDNA = -1


class PyMPFR:

    def __init__(self, value: Union[MPFR, int, float], rounding: Rnd = Rnd.MPFR_RNDN):
        self.mpfr = MPFR()
        MPFR_init(self)
        if isinstance(value, MPFR):
            MPFR_set(self, value, rounding)
        else:
            assert isinstance(value, (int, float))
            MPFR_set_d(self, value, rounding)
        self.rounding = rounding

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        result = PyMPFR(self.mpfr, self.rounding)
        memodict[id(self)] = result
        return result
        
    def __del__(self):
        MPFR_clear(self)

    @property
    def _as_parameter_(self):
        return byref(self.mpfr)

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyMPFR)
        return argument

    def __repr__(self):
        return '{}'.format(MPFR_get_d(self.mpfr, 0))

    def __lt__(self, other: 'PyMPFR'):
        assert isinstance(other, PyMPFR)
        return MPFR_cmp(self, other) < 0

    def __le__(self, other: 'PyMPFR'):
        assert isinstance(other, PyMPFR)
        return self.__lt__(other) or self.__eq__(other)

    def __eq__(self, other: 'PyMPFR'):
        assert isinstance(other, PyMPFR)
        return MPFR_cmp(self, other) == 0

    def __ne__(self, other: 'PyMPFR'):
        assert isinstance(other, PyMPFR)
        return not self.__eq__(other)

    def __ge__(self, other: 'PyMPFR'):
        assert isinstance(other, PyMPFR)
        return self.__gt__(other) or self.__eq__(other)

    def __gt__(self, other: 'PyMPFR'):
        assert isinstance(other, PyMPFR)
        return MPFR_cmp(self, other) > 0

    def __add__(self, other: 'PyMPFR') -> 'PyMPFR':
        assert isinstance(other, PyMPFR)
        mpfr = type(self)(0)
        MPFR_add(mpfr, self, other)
        return mpfr

    def __sub__(self, other: 'PyMPFR') -> 'PyMPFR':
        assert isinstance(other, PyMPFR)
        mpfr = type(self)(0)
        MPFR_sub(mpfr, self, other)
        return mpfr

    def __mul__(self, other: 'PyMPFR') -> 'PyMPFR':
        assert isinstance(other, PyMPFR)
        mpfr = type(self)(0)
        MPFR_mul(mpfr, self, other)
        return mpfr

    def __neg__(self) -> 'PyMPFR':
        mpfr = type(self)(0)
        MPFR_neg(mpfr, self)
        return mpfr

    def __abs__(self) -> 'PyMPFR':
        mpfr = type(self)(0)
        MPFR_abs(mpfr, self)
        return mpfr


# initialization and assignment functions
MPFR_init.argtypes = [PyMPFR]
MPFR_clear.argtypes = [PyMPFR]
MPFR_set.argtypes = [PyMPFR, POINTER(MPFR), c_int]
MPFR_set_d.argtypes = [PyMPFR, c_double, c_int]
# conversion functions
MPFR_get_d.argtypes = [POINTER(MPFR), c_int]
MPFR_get_d.restype = c_double
# comparison functions
MPFR_cmp.argtypes = [PyMPFR, PyMPFR]
# arithmetic functions
MPFR_add.argtypes = [PyMPFR, PyMPFR, PyMPFR]
MPFR_sub.argtypes = [PyMPFR, PyMPFR, PyMPFR]
MPFR_mul.argtypes = [PyMPFR, PyMPFR, PyMPFR]
MPFR_neg.argtypes = [PyMPFR, PyMPFR]
MPFR_abs.argtypes = [PyMPFR, PyMPFR]
