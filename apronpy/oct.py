"""
APRON Octagons
==============

:Author: Caterina Urban
"""
from _ctypes import POINTER

from apronpy.abstract1 import PyAbstract1
from apronpy.cdll import liboctD, liboctMPQ
from apronpy.manager import Manager, PyManager, PyOctDManager, PyOctMPQManager


class PyOctD(PyAbstract1):

    manager: PyManager = PyOctDManager()


class PyOctMPQ(PyAbstract1):

    manager: PyManager = PyOctMPQManager()
