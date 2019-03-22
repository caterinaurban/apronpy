"""
C DLLs
======

:Author: Caterina Urban
"""
from ctypes import util, CDLL, c_void_p

libc = CDLL(util.find_library('c'))
cstdout = c_void_p.in_dll(libc, '__stdoutp')

libboxD = CDLL(util.find_library('libboxD.so'))
libboxMPQ = CDLL(util.find_library('libboxMPQ.so'))
libboxMPFR = CDLL(util.find_library('libboxMPFR.so'))

liboctD = CDLL(util.find_library('liboctD.so'))
liboctMPQ = CDLL(util.find_library('liboctMPQ.so'))

libpolkaMPQ = CDLL(util.find_library('libpolkaMPQ.so'))
libpolkaRll = CDLL(util.find_library('libpolkaRll.so'))

libt1D = CDLL(util.find_library('libt1D.so'))
libt1MPQ = CDLL(util.find_library('libt1MPQ.so'))
libt1MPFR = CDLL(util.find_library('libt1MPFR.so'))

libapron = CDLL(util.find_library('libapron.so'))

libgmp = CDLL(util.find_library('gmp'))
libmpfr = CDLL(util.find_library('mpfr'))
