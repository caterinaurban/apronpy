"""
APRON Tree Constraints (Level 1)
================================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER, byref
from copy import deepcopy
from ctypes import c_size_t
from typing import List, Union

from apronpy.cdll import libapron
from apronpy.coeff import PyDoubleScalarCoeff
from apronpy.environment import Environment, PyEnvironment
from apronpy.lincons0 import ConsTyp
from apronpy.lincons1 import PyLincons1
from apronpy.linexpr1 import PyLinexpr1
from apronpy.scalar import c_uint, PyScalar
from apronpy.tcons0 import Tcons0, Tcons0Array
from apronpy.texpr0 import TexprOp, TexprDiscr
from apronpy.texpr1 import PyTexpr1
from apronpy.texpr0 import Texpr0


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


class TCons1Array(Structure):
    """
    typedef struct ap_tcons1_array_t {
      ap_tcons0_array_t tcons0_array;
      ap_environment_t* env;
    } ap_tcons1_array_t;
    """

    _fields_ = [
        ('tcons0_array', Tcons0Array),
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

        env = self.env.contents
        array = list()
        for i in range(self.tcons0_array.size):
            constyp = ConsTyp(self.tcons0_array.p[i].constyp)
            scalar = self.tcons0_array.p[i].scalar
            result = do(self.tcons0_array.p[i].texpr0.contents, env).replace('+ -', '- ')
            if scalar:
                array.append('{} {} {}'.format(result, repr(constyp), scalar.contents))
            else:
                array.append('{} {} 0'.format(result, repr(constyp)))
        return '[' + ' , '.join(array) + ']'


class PyTcons1:

    def __init__(self, cons: Union[PyLincons1, Tcons1]):
        if isinstance(cons, PyLincons1):
            self.tcons1 = Tcons1()
            texpr = libapron.ap_texpr0_from_linexpr0(cons.lincons1.lincons0.linexpr0)
            self.tcons1.tcons0.texpr0 = texpr
            self.tcons1.tcons0.constyp = c_uint(cons.lincons1.lincons0.constyp)
            scalar = cons.lincons1.lincons0.scalar
            if scalar:
                self.tcons1.tcons0.scalar = libapron.ap_scalar_alloc_set(scalar)
            cons.lincons1.env.contents.count += 1
            self.tcons1.env = cons.lincons1.env
        else:
            self.tcons1 = cons

    @classmethod
    def make(cls, texpr: PyTexpr1, typ: ConsTyp, cst: PyScalar = None):
        tcons1 = Tcons1()
        tcons1.tcons0 = Tcons0()
        tcons1.tcons0.texpr0 = libapron.ap_texpr0_copy(texpr.texpr1.contents.texpr0)
        tcons1.tcons0.constyp = c_uint(typ)
        if cst:
            tcons1.tcons0.scalar = libapron.ap_scalar_alloc_set(cst)
        else:
            tcons1.tcons0.scalar = None
        texpr.texpr1.contents.env.contents.count += 1
        tcons1.env = texpr.texpr1.contents.env
        return cls(tcons1)

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


class PyTcons1Array:

    def __init__(self, tcons1s: List[Tcons1] = None, environment: PyEnvironment = None):
        if tcons1s:
            size = len(tcons1s)
            tcons1s[0].env.contents.count += 1
            self.tcons1array = libapron.ap_tcons1_array_make(tcons1s[0].env, size)
            for i in range(size):
                tcons1i_copy = Tcons1()
                tcons1i_copy.tcons0 = Tcons0()
                texpr0_copy = libapron.ap_texpr0_copy(tcons1s[i].tcons0.texpr0)
                tcons1i_copy.tcons0.texpr0 = texpr0_copy
                tcons1i_copy.tcons0.constyp = c_uint(tcons1s[i].tcons0.constyp)
                scalar = tcons1s[i].tcons0.scalar
                if scalar:
                    tcons1i_copy.tcons0.scalar = libapron.ap_scalar_alloc_set(scalar)
                else:
                    tcons1i_copy.tcons0.scalar = None
                tcons1s[i].env.contents.count += 1
                tcons1i_copy.env = tcons1s[i].env
                libapron.ap_tcons1_array_set(self, i, byref(tcons1i_copy))
        else:
            self.tcons1array = libapron.ap_tcons1_array_make(environment, 0)

    def __del__(self):
        libapron.ap_tcons1_array_clear(self)

    @property
    def _as_parameter_(self):
        return byref(self.tcons1array)

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyTcons1Array)
        return argument

    def __repr__(self):
        return '{}'.format(self.tcons1array)


libapron.ap_tcons1_array_make.argtypes = [POINTER(Environment), c_size_t]
libapron.ap_tcons1_array_make.restype = TCons1Array
libapron.ap_tcons1_array_clear.argtypes = [PyTcons1Array]
libapron.ap_tcons1_array_set.argtypes = [PyTcons1Array, c_size_t, POINTER(Tcons1)]
