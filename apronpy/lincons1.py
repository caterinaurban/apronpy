"""
APRON Linear Constraints (Level 1)
==================================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER

from apronpy.environment import Environment
from apronpy.lincons0 import Lincons0


class Lincons1(Structure):
    """
    typedef struct ap_lincons1_t {
      ap_lincons0_t lincons0;
      ap_environment_t* env;
    } ap_lincons1_t;
    """

    _fields_ = [
        ('lincons0', Lincons0),
        ('env', POINTER(Environment))
    ]


class PyLincons1:

    ...