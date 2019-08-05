"""
APRON Taylor1+
==============

:Author: Caterina Urban
"""
from _ctypes import POINTER

from apronpy.abstract1 import PyAbstract1
from apronpy.cdll import libt1pD, libt1pMPQ, libt1pMPFR
from apronpy.manager import Manager, PyManager, PyT1pDManager, PyT1pMPQManager, PyT1pMPFRManager


class PyT1pD(PyAbstract1):

    manager: PyManager = PyT1pDManager()


class PyT1pMPQ(PyAbstract1):

    manager: PyManager = PyT1pMPQManager()


class PyT1pMPFR(PyAbstract1):

    manager: PyManager = PyT1pMPFRManager()
