"""
APRON Octagons
==============

:Author: Caterina Urban
"""
from _ctypes import POINTER
from ctypes import CDLL

from apronpy.abstract1 import PyAbstract1
from apronpy.manager import PyManager, Manager
from apronpy.util import find_apron_library


liboctD = CDLL(find_apron_library('liboctD.so'))
liboctMPQ = CDLL(find_apron_library('liboctMPQ.so'))


class PyOctDManager(PyManager):

    def __init__(self):
        super().__init__(liboctD.oct_manager_alloc())


class PyOctMPQManager(PyManager):

    def __init__(self):
        super().__init__(liboctMPQ.oct_manager_alloc())


liboctD.oct_manager_alloc.restype = POINTER(Manager)
liboctMPQ.oct_manager_alloc.restype = POINTER(Manager)


class PyOct(PyAbstract1):       # parallelizable implementation
    pass
