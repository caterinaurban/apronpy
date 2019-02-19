"""
APRON Linear Constraints (Level 0)
==================================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER
from enum import IntEnum

from apronpy.cdll import libapron
from apronpy.linexpr0 import Linexpr0
from apronpy.scalar import Scalar, c_uint, c_size_t


class ConsTyp(IntEnum):
    """
    typedef enum ap_constyp_t {
      AP_CONS_EQ,    /* equality constraint */
      AP_CONS_SUPEQ, /* >= constraint */
      AP_CONS_SUP,   /* > constraint */
      AP_CONS_EQMOD, /* congruence equality constraint */
      AP_CONS_DISEQ  /* disequality constraint */
    } ap_constyp_t;
    """
    AP_CONS_EQ = 0
    AP_CONS_SUPEQ = 1
    AP_CONS_SUP = 2
    AP_CONS_EQMOD = 3
    AP_CONS_DISEQ = 4

    def __repr__(self):
        if self.value == 0:
            return '=='
        elif self.value == 1:
            return '>='
        elif self.value == 2:
            return '>'
        elif self.value == 3:
            return '%='
        elif self.value == 4:
            return '!='
        return ValueError('no matching constraint type')


class Lincons0(Structure):
    """
    typedef struct ap_lincons0_t {
      ap_linexpr0_t* linexpr0;  /* expression */
      ap_constyp_t constyp;     /* type of constraint */
      ap_scalar_t* scalar;      /* maybe NULL. For EQMOD constraint, indicates the modulo */
    } ap_lincons0_t;
    """

    _fields_ = [
        ('linexpr0', POINTER(Linexpr0)),
        ('constyp', c_uint),
        ('scalar', POINTER(Scalar))
    ]


class Lincons0Array(Structure):
    """
    typedef struct ap_lincons0_array_t {
      ap_lincons0_t* p;
      size_t size;
    } ap_lincons0_array_t;
    """

    _fields_ = [
        ('p', POINTER(Lincons0)),
        ('size', c_size_t)
    ]


libapron.ap_lincons0_is_unsat.argtypes = [POINTER(Lincons0)]
