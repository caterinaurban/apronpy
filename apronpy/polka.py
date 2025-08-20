"""
APRON Polyhedra
===============

:Author: Caterina Urban
"""
from _ctypes import POINTER
from ctypes import CDLL

from apronpy.abstract1 import PyAbstract1
from apronpy.manager import PyManager, Manager
from apronpy.util import find_apron_library


libpolkaMPQ = CDLL(find_apron_library('libpolkaMPQ.so'))
libpolkaRll = CDLL(find_apron_library('libpolkaRll.so'))


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
