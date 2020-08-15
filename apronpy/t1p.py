"""
APRON Taylor1+
==============

:Author: Caterina Urban
"""
from _ctypes import POINTER
from ctypes import CDLL

from apronpy.abstract1 import PyAbstract1
from apronpy.manager import PyManager, Manager


libt1pD = CDLL('libt1pD.so')
libt1pMPQ = CDLL('libt1pMPQ.so')
libt1pMPFR = CDLL('libt1pMPFR.so')


class PyT1pDManager(PyManager):

    def __init__(self):
        super().__init__(libt1pD.t1p_manager_alloc())


class PyT1pMPQManager(PyManager):

    def __init__(self):
        super().__init__(libt1pMPQ.t1p_manager_alloc())


class PyT1pMPFRManager(PyManager):

    def __init__(self):
        super().__init__(libt1pMPFR.t1p_manager_alloc())


libt1pD.t1p_manager_alloc.restype = POINTER(Manager)
libt1pMPQ.t1p_manager_alloc.restype = POINTER(Manager)
libt1pMPFR.t1p_manager_alloc.restype = POINTER(Manager)


class PyT1p(PyAbstract1):       # parallelizable implementation
    pass
