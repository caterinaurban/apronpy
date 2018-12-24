"""
APRON Boxes
===========

:Author: Caterina Urban
"""
from _ctypes import POINTER

from apronpy.abstract1 import PyAbstract1
from apronpy.cdll import libboxD, libboxMPQ, libboxMPFR
from apronpy.manager import Manager

libboxD.box_manager_alloc.restype = POINTER(Manager)
libboxMPQ.box_manager_alloc.restype = POINTER(Manager)
libboxMPFR.box_manager_alloc.restype = POINTER(Manager)


class PyBoxD(PyAbstract1):

    manager: POINTER(Manager) = libboxD.box_manager_alloc()


class PyBoxMPQ(PyAbstract1):

    manager: POINTER(Manager) = libboxMPQ.box_manager_alloc()


class PyBoxMPFR(PyAbstract1):

    manager: POINTER(Manager) = libboxMPFR.box_manager_alloc()
