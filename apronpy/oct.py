"""
APRON Octagons
==============

:Author: Caterina Urban
"""
from _ctypes import POINTER
from ctypes import CDLL

from apronpy.abstract1 import PyAbstract1
from apronpy.manager import PyManager, Manager


liboctD = CDLL('liboctD.so')
liboctMPQ = CDLL('liboctMPQ.so')


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
