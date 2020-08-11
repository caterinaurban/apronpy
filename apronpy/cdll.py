"""
C DLLs
======

:Author: Caterina Urban
"""
import platform
from ctypes import util, CDLL

libc = CDLL(util.find_library('c'))

libt1pD = CDLL('libt1pD.so')
libt1pMPQ = CDLL('libt1pMPQ.so')
libt1pMPFR = CDLL('libt1pMPFR.so')

libpolkaMPQ = CDLL('libpolkaMPQ.so')
libpolkaRll = CDLL('libpolkaRll.so')

liboctD = CDLL('liboctD.so')
liboctMPQ = CDLL('liboctMPQ.so')

libboxD = CDLL('libboxD.so')
libboxMPQ = CDLL('libboxMPQ.so')
libboxMPFR = CDLL('libboxMPFR.so')

libapron = CDLL('libapron.so')

libgmp = CDLL(util.find_library('gmp'))
libmpfr = CDLL(util.find_library('mpfr'))
