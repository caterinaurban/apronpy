"""
MPFR Multiprecision Floating-Point Numbers
==========================================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER
from ctypes import c_long, c_int, c_ulonglong


class _MPFR(Structure):
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

