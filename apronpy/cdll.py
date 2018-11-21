"""
C DLLs
======

:Author: Caterina Urban
"""

from ctypes import util, CDLL

libc = CDLL(util.find_library('c'))
libapron = CDLL(util.find_library('libapron.so'))
libgmp = CDLL(util.find_library('gmp'))
libmpfr = CDLL(util.find_library('mpfr'))
