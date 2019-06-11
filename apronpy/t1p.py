"""
APRON Taylor1+
==============

:Author: Caterina Urban
"""
from _ctypes import POINTER

from apronpy.abstract1 import PyAbstract1
from apronpy.cdll import libt1pD, libt1pMPQ, libt1pMPFR
from apronpy.manager import Manager

libt1pD.t1p_manager_alloc.restype = POINTER(Manager)
libt1pMPQ.t1p_manager_alloc.restype = POINTER(Manager)
libt1pMPFR.t1p_manager_alloc.restype = POINTER(Manager)


class PyT1pD(PyAbstract1):

    manager: POINTER(Manager) = libt1pD.t1p_manager_alloc()


class PyT1pMPQ(PyAbstract1):

    manager: POINTER(Manager) = libt1pMPQ.t1p_manager_alloc()


class PyT1pMPFR(PyAbstract1):

    manager: POINTER(Manager) = libt1pMPFR.t1p_manager_alloc()
