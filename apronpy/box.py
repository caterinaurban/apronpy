"""
APRON Boxes
===========

:Author: Caterina Urban
"""
from _ctypes import POINTER
from ctypes import CDLL

from apronpy.abstract1 import PyAbstract1
from apronpy.manager import PyManager, Manager


libboxD = CDLL('libboxD.so')
libboxMPQ = CDLL('libboxMPQ.so')
libboxMPFR = CDLL('libboxMPFR.so')


class PyBoxDManager(PyManager):

    def __init__(self):
        super().__init__(libboxD.box_manager_alloc())


class PyBoxMPQManager(PyManager):

    def __init__(self):
        super().__init__(libboxMPQ.box_manager_alloc())


class PyBoxMPFRManager(PyManager):

    def __init__(self):
        super().__init__(libboxMPFR.box_manager_alloc())


libboxD.box_manager_alloc.restype = POINTER(Manager)
libboxMPQ.box_manager_alloc.restype = POINTER(Manager)
libboxMPFR.box_manager_alloc.restype = POINTER(Manager)


class PyBox(PyAbstract1):       # parallelizable implementation
    pass
