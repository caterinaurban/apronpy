"""
APRON Polyhedra
===============

:Author: Caterina Urban
"""
from _ctypes import POINTER
from abc import ABCMeta

from apronpy.abstract1 import PyAbstract1
from apronpy.cdll import libpolkaMPQ, libpolkaRll
from apronpy.manager import Manager, PyPolkaMPQlooseManager, PyManager, PyPolkaMPQstrictManager, PyPolkaRlllooseManager, \
    PyPolkaRllstrictManager

libpolkaMPQ.pk_manager_alloc.restype = POINTER(Manager)
libpolkaRll.pk_manager_alloc.restype = POINTER(Manager)


class PyPolkaMPQ(PyAbstract1, metaclass=ABCMeta):
    pass


class PyPolkaMPQloose(PyPolkaMPQ):

    manager: PyManager = PyPolkaMPQlooseManager()


class PyPolkaMPQstrict(PyPolkaMPQ):

    manager: PyManager = PyPolkaMPQstrictManager()


class PyPolkaRll(PyAbstract1, metaclass=ABCMeta):
    pass


class PyPolkaRllloose(PyPolkaRll):

    manager: PyManager = PyPolkaRlllooseManager()


class PyPolkaRllstrict(PyPolkaRll):

    manager: PyManager = PyPolkaRllstrictManager()
