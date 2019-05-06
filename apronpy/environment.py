"""
APRON Environments
==================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER, byref
from ctypes import c_size_t, c_char_p
from typing import List, Type

from apronpy.cdll import libapron
from apronpy.dimension import Dim, AP_DIM_MAX, DimChange, DimPerm
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

    def __copy__(self):
        self.count += 1
        return self

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        int_vars = list()
        for i in range(self.intdim):
            int_vars.append(PyVar(self.var_of_dim[i].decode('utf-8')))
        real_vars = list()
        for i in range(self.realdim):
            real_vars.append(PyVar(self.var_of_dim[self.intdim+i].decode('utf-8')))
        result = PyEnvironment(int_vars, real_vars)
        memodict[id(self)] = result
        return result

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
        if not self.environment:
            raise ValueError('clashing variable names')

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        var_of_dim = self.environment.contents.var_of_dim
        int_vars = list()
        for i in range(self.environment.contents.intdim):
            int_vars.append(PyVar(var_of_dim[i].decode('utf-8')))
        real_vars = list()
        for i in range(self.environment.contents.realdim):
            real_vars.append(PyVar(var_of_dim[self.environment.contents.intdim+i].decode('utf-8')))
        result = PyEnvironment(int_vars, real_vars)
        memodict[id(self)] = result
        return result

    def __del__(self):
        if self.environment:
            if self.environment.contents.count <= 1:
                libapron.ap_environment_free2(self)
            else:
                self.environment.contents.count -= 1

    @property
    def _as_parameter_(self):
        return self.environment

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyEnvironment)
        return argument

    # noinspection PyTypeChecker
    def add(self, int_vars: List[PyVar] = None, real_vars: List[PyVar] = None):
        if int_vars:
            i_size = len(int_vars)
            typ: Type = c_char_p * i_size
            int_arr = typ(*(x._as_parameter_ for x in int_vars))
        else:
            i_size = 0
            int_arr = None
        if real_vars:
            r_size = len(real_vars)
            typ: Type = c_char_p * r_size
            real_arr = typ(*(x._as_parameter_ for x in real_vars))
        else:
            r_size = 0
            real_arr = None
        self.environment = libapron.ap_environment_add(self, int_arr, i_size, real_arr, r_size)
        if not self.environment:
            raise ValueError('clashing variable names')
        return self

    # noinspection PyTypeChecker
    def rename(self, old_vars: List[PyVar], new_vars: List[PyVar]):
        o_size = len(old_vars)
        n_size = len(new_vars)
        assert o_size == n_size
        old_typ: Type = c_char_p * o_size
        old_arr = old_typ(*(x._as_parameter_ for x in old_vars))
        new_typ: Type = c_char_p * o_size
        new_arr = new_typ(*(x._as_parameter_ for x in new_vars))
        p = DimPerm()
        self.environment = libapron.ap_environment_rename(self, old_arr, new_arr, o_size, p)
        if not self.environment:
            raise ValueError('invalid renaming')
        return self

    # noinspection PyTypeChecker
    def remove(self, del_vars: List[PyVar] = None):
        if del_vars:
            size = len(del_vars)
            typ: Type = c_char_p * size
            arr = typ(*(x._as_parameter_ for x in del_vars))
        else:
            size = 0
            arr = None
        self.environment = libapron.ap_environment_remove(self, arr, size)
        if not self.environment:
            raise ValueError('non-existing variable(s)')
        return self

    def __repr__(self):
        return str(self.environment.contents)

    def __len__(self):
        return self.environment.contents.intdim + self.environment.contents.realdim

    def __contains__(self, item: 'PyVar'):
        assert isinstance(item, PyVar)
        return libapron.ap_environment_dim_of_var(self, item) != AP_DIM_MAX

    def __lt__(self, other: 'PyEnvironment'):
        assert isinstance(other, PyEnvironment)
        return libapron.ap_environment_compare(self, other) == -1

    def __le__(self, other: 'PyEnvironment'):
        assert isinstance(other, PyEnvironment)
        return self.__lt__(other) or self.__eq__(other)

    def __eq__(self, other: 'PyEnvironment'):
        assert isinstance(other, PyEnvironment)
        return libapron.ap_environment_compare(self, other) == 0

    def __ne__(self, other: 'PyEnvironment'):
        assert isinstance(other, PyEnvironment)
        return not self.__eq__(other)

    def __ge__(self, other: 'PyEnvironment'):
        assert isinstance(other, PyEnvironment)
        return self.__gt__(other) or self.__eq__(other)

    def __gt__(self, other: 'PyEnvironment'):
        assert isinstance(other, PyEnvironment)
        return libapron.ap_environment_compare(self, other) == 1

    def __or__(self, other: 'PyEnvironment') -> 'PyEnvironment':
        assert isinstance(other, PyEnvironment)
        d1 = DimChange()
        d2 = DimChange()
        environment = PyEnvironment()
        environment.environment = libapron.ap_environment_lce(self, other, byref(d1), byref(d2))
        if not environment.environment:
            raise ValueError('incompatible environments')
        return environment

    def union(self, other: 'PyEnvironment') -> 'PyEnvironment':
        assert isinstance(other, PyEnvironment)
        return self.__or__(other)


pyvar_p = POINTER(c_char_p)
libapron.ap_environment_alloc_empty.restype = POINTER(Environment)
libapron.ap_environment_alloc.argtypes = [pyvar_p, c_size_t, pyvar_p, c_size_t]
libapron.ap_environment_alloc.restype = POINTER(Environment)
libapron.ap_environment_add.argtypes = [PyEnvironment, pyvar_p, c_size_t, pyvar_p, c_size_t]
libapron.ap_environment_add.restype = POINTER(Environment)
libapron.ap_environment_remove.argtypes = [PyEnvironment, pyvar_p, c_size_t]
libapron.ap_environment_remove.restype = POINTER(Environment)
libapron.ap_environment_compare.argtypes = [PyEnvironment, PyEnvironment]
libapron.ap_environment_dim_of_var.argtypes = [PyEnvironment, PyVar]
libapron.ap_environment_dim_of_var.restype = Dim
dimchange_p = POINTER(DimChange)
libapron.ap_environment_lce.argtypes = [PyEnvironment, PyEnvironment, dimchange_p, dimchange_p]
libapron.ap_environment_lce.restype = POINTER(Environment)
dimperm_p = POINTER(DimPerm)
libapron.ap_environment_rename.argtypes = [PyEnvironment, pyvar_p, pyvar_p, c_size_t, dimperm_p]
libapron.ap_environment_rename.restype = POINTER(Environment)
