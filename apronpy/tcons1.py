"""
APRON Tree Constraints (Level 1)
================================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER, byref
from ctypes import c_char_p

from apronpy.cdll import libapron
from apronpy.coeff import PyDoubleScalarCoeff, Coeff
from apronpy.environment import Environment, PyEnvironment
from apronpy.lincons0 import ConsTyp
from apronpy.lincons1 import PyLincons1
from apronpy.linexpr1 import PyLinexpr1
from apronpy.scalar import c_uint
from apronpy.tcons0 import Tcons0
from apronpy.texpr0 import TexprOp, TexprDiscr


class Tcons1(Structure):
    """
    typedef struct ap_tcons1_t {
      ap_tcons0_t tcons0;
      ap_environment_t* env;
    } ap_tcons1_t;
    """

    _fields_ = [
        ('tcons0', Tcons0),
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

        constyp = ConsTyp(self.tcons0.constyp)
        scalar = self.tcons0.scalar
        result = do(self.tcons0.texpr0.contents, self.env.contents).replace('+ -', '- ')
        if scalar:
            return '{} {} {}'.format(result, repr(constyp), scalar.contents)
        else:
            return '{} {} 0'.format(result, repr(constyp))


class PyTcons1:

    def __init__(self, lincons: PyLincons1):
        self.tcons1 = Tcons1()
        texpr = libapron.ap_texpr0_from_linexpr0(lincons.lincons1.lincons0.linexpr0)
        self.tcons1.tcons0.texpr0 = texpr
        self.tcons1.tcons0.constyp = c_uint(lincons.lincons1.lincons0.constyp)
        scalar = lincons.lincons1.lincons0.scalar
        if scalar:
            self.tcons1.tcons0.scalar = libapron.ap_scalar_alloc_set(scalar)
        lincons.lincons1.env.contents.count += 1
        self.tcons1.env = lincons.lincons1.env

    @classmethod
    def unsat(cls, environment: PyEnvironment):
        x = PyLinexpr1(environment)
        x.set_cst(PyDoubleScalarCoeff(-1.0))
        lincons = PyLincons1(ConsTyp.AP_CONS_SUPEQ, x)
        return cls(lincons)

    def __del__(self):
        libapron.ap_tcons1_clear(self)

    @property
    def _as_parameter_(self):
        return byref(self.tcons1)

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyTcons1)
        return argument

    def __repr__(self):
        return '{}'.format(self.tcons1)


libapron.ap_tcons1_clear.argtypes = [PyTcons1]
libapron.ap_lincons1_coeffref.argtypes = [PyLincons1, c_char_p]
libapron.ap_lincons1_coeffref.restype = POINTER(Coeff)
libapron.ap_lincons1_get_coeff.argtypes = [POINTER(Coeff), PyLincons1, c_char_p]
