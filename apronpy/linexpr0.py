"""
APRON Linear Expressions (Level 0)
==================================

:Author: Caterina Urban
"""
from _ctypes import Structure, Union, POINTER
from ctypes import c_uint, c_size_t
from enum import IntEnum

from apronpy.coeff import Coeff
from apronpy.dimension import Dim


class LinexprDiscr(IntEnum):
    """
    typedef enum ap_linexpr_discr_t {
      AP_LINEXPR_DENSE,
      AP_LINEXPR_SPARSE
    } ap_linexpr_discr_t;
    """
    AP_LINEXPR_DENSE = 0
    AP_LINEXPR_SPARSE = 1


class LinTerm(Structure):
    """
    typedef struct ap_linterm_t {
      ap_dim_t dim;
      ap_coeff_t coeff;
    } ap_linterm_t;
    """

    _fields_ = [
        ('dim', Dim),
        ('coeff', Coeff)
    ]

    def __repr__(self):
        return '{}'.format(self.coeff)


class Linexpr0(Structure):
    """
    typedef struct ap_linexpr0_t {
      ap_coeff_t cst;             /* constant */
      ap_linexpr_discr_t discr;   /* discriminant for array */
      size_t size;             /* size of the array */
      union {
        ap_coeff_t* coeff;     /* array of coefficients */
        ap_linterm_t* linterm; /* array of linear terms */
      } p;
    } ap_linexpr0_t;
    """

    class P(Union):
        """
        union {
          ap_coeff_t* coeff;     /* array of coefficients */
          ap_linterm_t* linterm; /* array of linear terms */
        } p;
        """

        _fields_ = [
            ('coeff', POINTER(Coeff)),
            ('linterm', POINTER(LinTerm))
        ]

    _fields_ = [
        ('cst', Coeff),
        ('discr', c_uint),
        ('size', c_size_t),
        ('p', P)
    ]

    def __repr__(self):
        result = ''
        # result += '+'.join(self.var_of_dim[i].decode('utf-8') for i in range(self.size))
        # result += '|'
        # result += ','.join(
        #     self.var_of_dim[self.intdim + i].decode('utf-8') for i in range(self.realdim)
        # )
        # result += '}'
        return result