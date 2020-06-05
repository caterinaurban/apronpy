"""
APRON Taylor1+
==============

:Author: Caterina Urban
"""
from _ctypes import POINTER

from apronpy.abstract1 import PyAbstract1
from apronpy.cdll import libt1pD, libt1pMPQ, libt1pMPFR
from apronpy.manager import PyManager, Manager


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
