"""
APRON Environments
==================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER
from ctypes import c_size_t, c_char_p
from typing import List, Type

from apronpy.cdll import libapron
from apronpy.var import PyVar


class Environment(Structure):
    """
    typedef struct ap_environment_t {
      ap_var_t* var_of_dim;
      /*
        Array of size intdim+realdim, indexed by dimensions.
        - It should not contain identical strings..
        - Slice [0..intdim-1] is lexicographically sorted,
          and denotes integer variables.
        - Slice [intdim..intdim+realdim-1] is lexicographically sorted,
          and denotes real variables.
        - The memory allocated for the variables are attached to the structure
          (they are freed when the structure is no longer in use)
      */
      size_t intdim; /* Number of integer variables */
      size_t realdim;/* Number of real variables */
      size_t count; /* For reference counting */
    } ap_environment_t;
    """

    _fields_ = [
        ('var_of_dim', POINTER(c_char_p)),
        ('intdim', c_size_t),
        ('realdim', c_size_t),
        ('count', c_size_t)
    ]

    def __repr__(self):
        result = '{'
        result += ','.join(self.var_of_dim[i].decode('utf-8') for i in range(self.intdim))
        result += '|'
        result += ','.join(
            self.var_of_dim[self.intdim+i].decode('utf-8') for i in range(self.realdim)
        )
        result += '}'
        return result


class PyEnvironment:

    # noinspection PyTypeChecker
    def __init__(self, int_vars: List[PyVar] = None, real_vars: List[PyVar] = None):
        if int_vars:
            int_size = len(int_vars)
            typ: Type = c_char_p * int_size
            int_arr = typ(*(x._as_parameter_ for x in int_vars))
        else:
            int_size = 0
            int_arr = None
        if real_vars:
            real_size = len(real_vars)
            typ: Type = c_char_p * real_size
            real_arr = typ(*(x._as_parameter_ for x in real_vars))
        else:
            real_size = 0
            real_arr = None
        self.environment = libapron.ap_environment_alloc(int_arr, int_size, real_arr, real_size)

    def __del__(self):
        libapron.ap_environment_free2(self)

    @property
    def _as_parameter_(self):
        return self.environment

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyEnvironment)
        return argument

    def __repr__(self):
        return str(self.environment.contents)


libapron.ap_environment_alloc_empty.restype = POINTER(Environment)
libapron.ap_environment_alloc.argtypes = [POINTER(c_char_p), c_size_t, POINTER(c_char_p), c_size_t]
libapron.ap_environment_alloc.restype = POINTER(Environment)
