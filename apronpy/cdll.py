"""
C DLLs
======

:Author: Caterina Urban
"""
from ctypes import util, CDLL

from apronpy.util import find_apron_library

libc = CDLL(util.find_library('c'))

libapron = CDLL(find_apron_library('libapron.so'))

libgmp = CDLL(util.find_library('gmp'))
libmpfr = CDLL(util.find_library('mpfr'))
