"""
APRON Tree Constraints (Level 0)
================================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER

from apronpy.scalar import Scalar, c_uint, c_size_t
from apronpy.texpr0 import Texpr0


class Tcons0(Structure):
    """
    typedef struct ap_tcons0_t {
      ap_texpr0_t* texpr0;  /* expression */
      ap_constyp_t constyp; /* type of constraint */
      ap_scalar_t* scalar;  /* maybe NULL. For EQMOD constraint, indicates the modulo */
    } ap_tcons0_t;
    """

    _fields_ = [
        ('texpr0', POINTER(Texpr0)),
        ('constyp', c_uint),
        ('scalar', POINTER(Scalar))
    ]


class Tcons0Array(Structure):
    """
    typedef struct ap_tcons0_array_t {
      ap_tcons0_t* p;
      size_t size;
    } ap_tcons0_array_t;
    """

    _fields_ = [
        ('p', POINTER(Tcons0)),
        ('size', c_size_t)
    ]
