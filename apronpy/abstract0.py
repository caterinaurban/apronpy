"""
APRON Abstract Values (Level 0)
===============================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER
from ctypes import c_void_p

from apronpy.manager import Manager


class Abstract0(Structure):
    """
    struct ap_abstract0_t {
      void* value;       /* Abstract value of the underlying library */
      ap_manager_t* man; /* Used to identify the effective type of value */
    };
    """

    _fields_ = [
        ('value', c_void_p),
        ('man', POINTER(Manager))
    ]
