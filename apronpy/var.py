"""
APRON (String) Variables
========================

:Author: Caterina Urban
"""
from _ctypes import Structure
from ctypes import CFUNCTYPE, c_int, c_char_p, c_void_p

from apronpy.cdll import libapron


class VarOperations(Structure):
    """
    typedef struct ap_var_operations_t {
      int (*compare)(ap_var_t v1, ap_var_t v2); /* Total ordering function */
      int (*hash)(ap_var_t v);                  /* Hash function */
      ap_var_t (*copy)(ap_var_t var);           /* Duplication function */
      void (*free)(ap_var_t var);               /* Deallocation function */
      char* (*to_string)(ap_var_t var);         /* Conversion to a dynamically allocated string */
    } ap_var_operations_t;
    """

    _fields_ = [
        ('compare', CFUNCTYPE(c_int, c_void_p, c_void_p)),
        ('hash', CFUNCTYPE(c_int, c_void_p)),
        ('copy', CFUNCTYPE(c_void_p, c_void_p)),
        ('free', CFUNCTYPE(None, c_void_p)),
        ('to_string', CFUNCTYPE(c_char_p, c_char_p))
    ]


class PyVar:

    def __init__(self, name: str):
        self.var = name

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        result = PyVar('')
        operations = VarOperations.in_dll(libapron, 'ap_var_operations_default')
        operations.compare(result, self)
        memodict[id(self)] = result
        return result

    @property
    def _as_parameter_(self):
        return self.var.encode('utf-8')

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyVar)
        return argument.var.encode('utf-8')

    def __repr__(self):
        return self.var

    def __lt__(self, other: 'PyVar'):
        assert isinstance(other, PyVar)
        operations = VarOperations.in_dll(libapron, 'ap_var_operations_default')
        return operations.compare(self, other) < 0

    def __le__(self, other: 'PyVar'):
        assert isinstance(other, PyVar)
        return self.__lt__(other) or self.__eq__(other)

    def __eq__(self, other):
        assert isinstance(other, PyVar)
        operations = VarOperations.in_dll(libapron, 'ap_var_operations_default')
        return operations.compare(self, other) == 0

    def __ne__(self, other):
        assert isinstance(other, PyVar)
        return not self.__eq__(other)

    def __ge__(self, other):
        assert isinstance(other, PyVar)
        return self.__gt__(other) or self.__eq__(other)

    def __gt__(self, other):
        assert isinstance(other, PyVar)
        operations = VarOperations.in_dll(libapron, 'ap_var_operations_default')
        return operations.compare(self, other) > 0
