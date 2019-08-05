"""
APRON Boxes
===========

:Author: Caterina Urban
"""
from _ctypes import POINTER

from apronpy.abstract1 import PyAbstract1
from apronpy.cdll import libboxD, libboxMPQ, libboxMPFR
from apronpy.manager import Manager, PyBoxDManager, PyManager, PyBoxMPQManager, PyBoxMPFRManager


class PyBoxD(PyAbstract1):

    manager: PyManager = PyBoxDManager()


class PyBoxMPQ(PyAbstract1):

    manager: PyManager = PyBoxMPQManager()


class PyBoxMPFR(PyAbstract1):

    manager: PyManager = PyBoxMPFRManager()
