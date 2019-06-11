"""
APRON Octagons
==============

:Author: Caterina Urban
"""
from _ctypes import POINTER

from apronpy.abstract1 import PyAbstract1
from apronpy.cdll import liboctD, liboctMPQ
from apronpy.manager import Manager

liboctD.oct_manager_alloc.restype = POINTER(Manager)
liboctMPQ.oct_manager_alloc.restype = POINTER(Manager)


class PyOctD(PyAbstract1):

    manager: POINTER(Manager) = liboctD.oct_manager_alloc()


class PyOctMPQ(PyAbstract1):

    manager: POINTER(Manager) = liboctMPQ.oct_manager_alloc()
