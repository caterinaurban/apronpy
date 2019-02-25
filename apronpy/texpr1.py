"""
APRON Tree Expressions (Level 1)
================================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER, byref
from ctypes import c_uint, c_size_t, c_char_p

from apronpy.linexpr1 import PyLinexpr1

from apronpy.cdll import libapron
from apronpy.coeff import Coeff, CoeffDiscr, PyDoubleIntervalCoeff, PyDoubleScalarCoeff, \
    PyMPQScalarCoeff, PyMPFRScalarCoeff, PyMPQIntervalCoeff, PyMPFRIntervalCoeff, PyCoeff
from apronpy.environment import Environment, PyEnvironment
from apronpy.linexpr0 import Linexpr0, LinexprDiscr
from apronpy.scalar import ScalarDiscr
from apronpy.texpr0 import Texpr0, TexprDiscr, TexprOp
from apronpy.var import PyVar


class Texpr1(Structure):
    """
    typedef struct ap_texpr1_t {
      ap_texpr0_t* texpr0;
      ap_environment_t* env;
    } ap_texpr1_t;
    """

    _fields_ = [
        ('texpr0', POINTER(Texpr0)),
        ('env', POINTER(Environment))
    ]

    def __repr__(self):

        def precendence(texpr0):
            op_precedence = {
                TexprOp.AP_TEXPR_ADD: 1,
                TexprOp.AP_TEXPR_SUB: 1,
                TexprOp.AP_TEXPR_MUL: 2,
                TexprOp.AP_TEXPR_DIV: 2,
                TexprOp.AP_TEXPR_MOD: 2,
                TexprOp.AP_TEXPR_POW: 3,
                TexprOp.AP_TEXPR_NEG: 4,
                TexprOp.AP_TEXPR_CAST: 5,
                TexprOp.AP_TEXPR_SQRT: 5
            }
            if texpr0.discr == TexprDiscr.AP_TEXPR_CST or texpr0.discr == TexprDiscr.AP_TEXPR_DIM:
                return op_precedence[TexprOp.AP_TEXPR_NEG]
            return op_precedence[texpr0.val.node.contents.op]
        def do(texpr0, env):
            if texpr0.discr == TexprDiscr.AP_TEXPR_CST:
                return '{}'.format(texpr0.val.cst)
            elif texpr0.discr == TexprDiscr.AP_TEXPR_DIM:
                return '{}'.format(env.var_of_dim[texpr0.val.dim.value].decode('utf-8'))
            else:   # texpr0.discr == TexprDiscr.AP_TEXPR_NODE
                prec = precendence(texpr0)
                precA = precendence(texpr0.val.node.contents.exprA.contents)
                if precA < prec:
                    exprA = '(' + do(texpr0.val.node.contents.exprA.contents, env) + ')'
                else:
                    exprA = do(texpr0.val.node.contents.exprA.contents, env)
                op = texpr0.val.node.contents.op
                if texpr0.val.node.contents.exprB:  # binary operation
                    precB = precendence(texpr0.val.node.contents.exprB.contents)
                    if precB <= prec:
                        exprB = '(' + do(texpr0.val.node.contents.exprB.contents, env) + ')'
                    else:
                        exprB = do(texpr0.val.node.contents.exprB.contents, env)
                    return '{} {} {}'.format(exprA, repr(TexprOp(op)), exprB)
                else:
                    return '{} {}'.format(repr(TexprOp(op)), exprA)
        return do(self.texpr0.contents, self.env.contents).replace('+ -', '- ')


class PyTexpr1:

    def __init__(self, linexpr: PyLinexpr1):
        self.texpr1 = libapron.ap_texpr1_from_linexpr1(linexpr)

    def __del__(self):
        libapron.ap_texpr1_free(self)

    @property
    def _as_parameter_(self):
        return self.texpr1

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyTexpr1)
        return argument

    def __repr__(self):
        return '{}'.format(self.texpr1.contents)

    def substitute(self, var: PyVar, dst: 'PyTexpr1'):
        texpr = type(self)(PyLinexpr1(PyEnvironment()))
        texpr.texpr1 = libapron.ap_texpr1_substitute(self, var._as_parameter_, dst)
        return texpr


libapron.ap_texpr1_from_linexpr1.argtypes = [PyLinexpr1]
libapron.ap_texpr1_from_linexpr1.restype = POINTER(Texpr1)
libapron.ap_texpr1_free.argtypes = [PyTexpr1]
libapron.ap_texpr1_substitute.argtypes = [PyTexpr1, c_char_p, PyTexpr1]
libapron.ap_texpr1_substitute.restype = POINTER(Texpr1)
