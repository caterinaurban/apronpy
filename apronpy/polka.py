"""
APRON Polyhedra
===============

:Author: Caterina Urban
"""
from _ctypes import POINTER
from abc import ABCMeta

from apronpy.abstract1 import PyAbstract1
from apronpy.cdll import libpolkaMPQ, libpolkaRll
from apronpy.manager import Manager

libpolkaMPQ.pk_manager_alloc.restype = POINTER(Manager)
libpolkaRll.pk_manager_alloc.restype = POINTER(Manager)


class PyPolkaMPQ(PyAbstract1, metaclass=ABCMeta):
    pass


class PyPolkaMPQloose(PyPolkaMPQ):

    manager: POINTER(Manager) = libpolkaMPQ.pk_manager_alloc(False)


class PyPolkaMPQstrict(PyPolkaMPQ):

    manager: POINTER(Manager) = libpolkaMPQ.pk_manager_alloc(True)


class PyPolkaRll(PyAbstract1, metaclass=ABCMeta):
    pass


class PyPolkaRllloose(PyPolkaRll):

    manager: POINTER(Manager) = libpolkaRll.pk_manager_alloc(False)


class PyPolkaRllstrict(PyPolkaRll):

    manager: POINTER(Manager) = libpolkaRll.pk_manager_alloc(True)
