"""
APRON Tree Expressions (Level 1)
================================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER, byref
from copy import deepcopy
from ctypes import c_char_p, c_uint, c_int
from typing import Union

from apronpy.cdll import libapron
from apronpy.coeff import PyCoeff, PyMPFRScalarCoeff
from apronpy.environment import Environment, PyEnvironment
from apronpy.linexpr1 import PyLinexpr1
from apronpy.texpr0 import Texpr0, TexprDiscr, TexprOp, TexprRtype, TexprRdir
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
            else:  # texpr0.discr == TexprDiscr.AP_TEXPR_NODE
                prec = precendence(texpr0)
                prec_a = precendence(texpr0.val.node.contents.exprA.contents)
                if prec_a < prec:
                    expr_a = '(' + do(texpr0.val.node.contents.exprA.contents, env) + ')'
                else:
                    expr_a = do(texpr0.val.node.contents.exprA.contents, env)
                op = texpr0.val.node.contents.op
                if texpr0.val.node.contents.exprB:  # binary operation
                    prec_b = precendence(texpr0.val.node.contents.exprB.contents)
                    if prec_b <= prec:
                        expr_b = '(' + do(texpr0.val.node.contents.exprB.contents, env) + ')'
                    else:
                        expr_b = do(texpr0.val.node.contents.exprB.contents, env)
                    return '{} {} {}'.format(expr_a, repr(TexprOp(op)), expr_b)
                else:
                    return '{} {}'.format(repr(TexprOp(op)), expr_a)

        return do(self.texpr0.contents, self.env.contents).replace('+ -', '- ')


class PyTexpr1:

    def __init__(self, expr: Union[Texpr1, PyLinexpr1]):
        if isinstance(expr, PyLinexpr1):
            self.texpr1: POINTER(Texpr1) = libapron.ap_texpr1_from_linexpr1(expr)
        else:
            assert isinstance(expr, POINTER(Texpr1))
            self.texpr1: POINTER(Texpr1) = expr

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        result = type(self)(libapron.ap_texpr1_copy(self))
        memodict[id(self)] = result
        return result

    def __del__(self):
        libapron.ap_texpr1_free(self)

    @classmethod
    def cst(cls, environment: PyEnvironment, cst: PyCoeff):
        return cls(libapron.ap_texpr1_cst(environment, cst))

    @classmethod
    def var(cls, environment: PyEnvironment, var: PyVar):
        return cls(libapron.ap_texpr1_var(environment, var))

    @classmethod
    def unop(cls, op: TexprOp, expr, typ: TexprRtype, dir: TexprRdir):
        return cls(libapron.ap_texpr1_unop(op, libapron.ap_texpr1_copy(expr), typ, dir))

    @classmethod
    def binop(cls, op: TexprOp, expr_a, expr_b, typ: TexprRtype, dir: TexprRdir):
        left = libapron.ap_texpr1_copy(expr_a)
        right = libapron.ap_texpr1_copy(expr_b)
        return cls(libapron.ap_texpr1_binop(op, left, right, typ, dir))

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


libapron.ap_texpr1_cst.argtypes = [PyEnvironment, PyCoeff]
libapron.ap_texpr1_cst.restype = POINTER(Texpr1)
libapron.ap_texpr1_var.argtypes = [PyEnvironment, c_char_p]
libapron.ap_texpr1_var.restype = POINTER(Texpr1)
libapron.ap_texpr1_unop.argtypes = [c_int, POINTER(Texpr1), c_int, c_int]
libapron.ap_texpr1_unop.restype = POINTER(Texpr1)
libapron.ap_texpr1_binop.argtypes = [c_int, POINTER(Texpr1), POINTER(Texpr1), c_int, c_int]
libapron.ap_texpr1_binop.restype = POINTER(Texpr1)
libapron.ap_texpr1_copy.argtypes = [PyTexpr1]
libapron.ap_texpr1_copy.restype = POINTER(Texpr1)
libapron.ap_texpr1_free.argtypes = [PyTexpr1]
libapron.ap_texpr1_from_linexpr1.argtypes = [PyLinexpr1]
libapron.ap_texpr1_from_linexpr1.restype = POINTER(Texpr1)
libapron.ap_texpr1_substitute.argtypes = [PyTexpr1, c_char_p, PyTexpr1]
libapron.ap_texpr1_substitute.restype = POINTER(Texpr1)
