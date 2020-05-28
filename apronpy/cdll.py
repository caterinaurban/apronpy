"""
C DLLs
======

:Author: Caterina Urban
"""
import platform
from ctypes import util, CDLL

libc = CDLL(util.find_library('c'))

platform = platform.uname()[0]
if platform == 'Darwin':
    libt1pD = CDLL(util.find_library('libt1pD.so'))
    libt1pMPQ = CDLL(util.find_library('libt1pMPQ.so'))
    libt1pMPFR = CDLL(util.find_library('libt1pMPFR.so'))

    libpolkaMPQ = CDLL(util.find_library('libpolkaMPQ.so'))
    libpolkaRll = CDLL(util.find_library('libpolkaRll.so'))

    liboctD = CDLL(util.find_library('liboctD.so'))
    liboctMPQ = CDLL(util.find_library('liboctMPQ.so'))

    libboxD = CDLL(util.find_library('libboxD.so'))
    libboxMPQ = CDLL(util.find_library('libboxMPQ.so'))
    libboxMPFR = CDLL(util.find_library('libboxMPFR.so'))
else: # platform == 'Linux'
    libt1pD = CDLL(util.find_library('t1pD'))
    libt1pMPQ = CDLL(util.find_library('t1pMPQ'))
    libt1pMPFR = CDLL(util.find_library('t1pMPFR'))

    libpolkaMPQ = CDLL(util.find_library('polkaMPQ'))
    libpolkaRll = CDLL(util.find_library('polkaRll'))

    liboctD = CDLL(util.find_library('octD'))
    liboctMPQ = CDLL(util.find_library('octMPQ'))

    libboxD = CDLL(util.find_library('boxD'))
    libboxMPQ = CDLL(util.find_library('boxMPQ'))
    libboxMPFR = CDLL(util.find_library('boxMPFR'))
libapron = CDLL(util.find_library('apron'))

libgmp = CDLL(util.find_library('gmp'))
libmpfr = CDLL(util.find_library('mpfr'))
