"""
APRON Boxes
===========

:Author: Caterina Urban
"""
from _ctypes import POINTER
from ctypes import CDLL

from apronpy.abstract1 import PyAbstract1
from apronpy.manager import PyManager, Manager
from apronpy.util import find_apron_library


libboxD = CDLL(find_apron_library('libboxD.so'))
libboxMPQ = CDLL(find_apron_library('libboxMPQ.so'))
libboxMPFR = CDLL(find_apron_library('libboxMPFR.so'))


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
