"""
APRON Tree Expressions (Level 0)
================================

:Author: Caterina Urban
"""
from _ctypes import Structure, Union, POINTER
from ctypes import c_uint
from enum import IntEnum

from apronpy.cdll import libapron
from apronpy.coeff import Coeff
from apronpy.dimension import Dim
from apronpy.linexpr0 import Linexpr0
from apronpy.mpfr import Rnd


class TexprOp(IntEnum):
    """
    typedef enum ap_texpr_op_t {
      /* Binary operators */
      AP_TEXPR_ADD, AP_TEXPR_SUB, AP_TEXPR_MUL, AP_TEXPR_DIV,
      AP_TEXPR_MOD,  /* either integer or real, no rounding */
      AP_TEXPR_POW,
      /* Unary operators */
      AP_TEXPR_NEG   /* no rounding */,
      AP_TEXPR_CAST, AP_TEXPR_SQRT,
    } ap_texpr_op_t;
    """
    AP_TEXPR_ADD = 0
    AP_TEXPR_SUB = 1
    AP_TEXPR_MUL = 2
    AP_TEXPR_DIV = 3
    AP_TEXPR_MOD = 4
    AP_TEXPR_POW = 5
    AP_TEXPR_NEG = 6
    AP_TEXPR_CAST = 7
    AP_TEXPR_SQRT = 8

    def __repr__(self):
        if self.value == 0:
            return '+'
        elif self.value == 1:
            return '-'
        elif self.value == 2:
            return '·'
        elif self.value == 3:
            return '/'
        elif self.value == 4:
            return '%'
        elif self.value == 5:
            return '^'
        elif self.value == 6:
            return '-'
        elif self.value == 7:
            return 'cast'
        elif self.value == 8:
            return 'sqrt'
        return ValueError('no matching constraint type')


class TexprRtype(IntEnum):
    """
    typedef enum ap_texpr_rtype_t {
      AP_RTYPE_REAL,     // real (no rounding)
      AP_RTYPE_INT,      // integer
      AP_RTYPE_SINGLE,   // IEEE 754 32-bit single precision, e.g.: C's float
      AP_RTYPE_DOUBLE,   // IEEE 754 64-bit double precision, e.g.: C's double
      AP_RTYPE_EXTENDED, // non-standard 80-bit double extended, e.g.: Intel's long double
      AP_RTYPE_QUAD,     // non-standard 128-bit quadruple precision, e.g.: Motorola's long double
      AP_RTYPE_SIZE      // Not to be used !
    } ap_texpr_rtype_t;
    """
    AP_RTYPE_REAL = 0
    AP_RTYPE_INT = 1
    AP_RTYPE_SINGLE = 2
    AP_RTYPE_DOUBLE = 3
    AP_RTYPE_EXTENDED = 4
    AP_RTYPE_QUAD = 5
    AP_RTYPE_SIZE = 6


class TexprRdir(IntEnum):
    """
    typedef enum ap_texpr_rdir_t {
      AP_RDIR_NEAREST = GMP_RNDN, /* Nearest */
      AP_RDIR_ZERO    = GMP_RNDZ, /* Zero (truncation for integers) */
      AP_RDIR_UP      = GMP_RNDU, /* + Infinity */
      AP_RDIR_DOWN    = GMP_RNDD, /* - Infinity */
      AP_RDIR_RND,    /* All possible mode, non deterministically */
      AP_RDIR_SIZE    /* Not to be used ! */
    } ap_texpr_rdir_t;
    """
    AP_RDIR_NEAREST = Rnd.MPFR_RNDN
    AP_RDIR_ZERO = Rnd.MPFR_RNDZ
    AP_RDIR_UP = Rnd.MPFR_RNDU
    AP_RDIR_DOWN = Rnd.MPFR_RNDD
    AP_RDIR_RND = 4
    AP_RDIR_SIZE = 5


class Texpr0Node(Structure):
    """
    typedef struct ap_texpr0_node_t {
      ap_texpr_op_t    op;
      ap_texpr_rtype_t type;
      ap_texpr_rdir_t  dir;
      struct ap_texpr0_t* exprA; /* First operand */
      struct ap_texpr0_t* exprB; /* Second operand (for binary operations) or NULL */
    } ap_texpr0_node_t;
    """
    pass


class TexprDiscr(IntEnum):
    """
    typedef enum ap_texpr_discr_t {
      AP_TEXPR_CST, AP_TEXPR_DIM, AP_TEXPR_NODE
    } ap_texpr_discr_t;
    """
    AP_TEXPR_CST = 0
    AP_TEXPR_DIM = 1
    AP_TEXPR_NODE = 2


class Texpr0(Structure):
    """
    typedef struct ap_texpr0_t {
      ap_texpr_discr_t discr;
      union {
        ap_coeff_t cst;
        ap_dim_t dim;
        ap_texpr0_node_t* node;
      } val;
    } ap_texpr0_t;
    """

    class Val(Union):
        """
        union {
          ap_coeff_t cst;
          ap_dim_t dim;
          ap_texpr0_node_t* node;
        } val;
        """

        _fields_ = [
            ('cst', Coeff),
            ('dim', Dim),
            ('node', POINTER(Texpr0Node))
        ]

    _fields_ = [
        ('discr', c_uint),
        ('val', Val)
    ]


Texpr0Node._fields_ = [
        ('op', c_uint),
        ('type', c_uint),
        ('dir', c_uint),
        ('exprA', POINTER(Texpr0)),
        ('exprB', POINTER(Texpr0))
    ]


libapron.ap_texpr0_copy.argtypes = [POINTER(Texpr0)]
libapron.ap_texpr0_copy.restype = POINTER(Texpr0)
libapron.ap_texpr0_from_linexpr0.argtypes = [POINTER(Linexpr0)]
libapron.ap_texpr0_from_linexpr0.restype = POINTER(Texpr0)
