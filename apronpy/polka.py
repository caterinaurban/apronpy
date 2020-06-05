"""
APRON Polyhedra
===============

:Author: Caterina Urban
"""
from _ctypes import POINTER

from apronpy.abstract1 import PyAbstract1
from apronpy.cdll import libpolkaMPQ, libpolkaRll
from apronpy.manager import PyManager, Manager


class PyPolkaMPQlooseManager(PyManager):

    def __init__(self):
        super().__init__(libpolkaMPQ.pk_manager_alloc(False))


class PyPolkaMPQstrictManager(PyManager):

    def __init__(self):
        super().__init__(libpolkaMPQ.pk_manager_alloc(True))


class PyPolkaRlllooseManager(PyManager):

    def __init__(self):
        super().__init__(libpolkaRll.pk_manager_alloc(False))


class PyPolkaRllstrictManager(PyManager):

    def __init__(self):
        super().__init__(libpolkaRll.pk_manager_alloc(True))


libpolkaMPQ.pk_manager_alloc.restype = POINTER(Manager)
libpolkaRll.pk_manager_alloc.restype = POINTER(Manager)


class PyPolka(PyAbstract1):     # parallelizable implementation
    pass
