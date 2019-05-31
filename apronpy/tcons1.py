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
from apronpy.scalar import c_uint, PyScalar
from apronpy.tcons0 import Tcons0, Tcons0Array
from apronpy.texpr0 import TexprOp, TexprDiscr
from apronpy.texpr1 import PyTexpr1
from apronpy.var import PyVar


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

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        result = Tcons1()
        result.tcons0 = Tcons0()
        result.tcons0.texpr0 = libapron.ap_texpr0_copy(self.tcons0.texpr0)
        result.tcons0.constyp = self.tcons0.constyp
        if self.tcons0.scalar:
            result.tcons0.scalar = libapron.ap_scalar_alloc_set(self.tcons0.scalar)
        else:
            result.tcons0.scalar = None
        self.env.contents.count += 1
        result.env = self.env
        memodict[id(self)] = result
        return result

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

        array = list()
        for i in range(self.tcons0_array.size):
            constyp = ConsTyp(self.tcons0_array.p[i].constyp)
            scalar = self.tcons0_array.p[i].scalar
            result = do(self.tcons0_array.p[i].texpr0.contents, self.env.contents)
            result = result.replace('+ -', '- ')
            if scalar:
                array.append('{} {} {}'.format(result, repr(constyp), scalar.contents))
            else:
                array.append('{} {} 0'.format(result, repr(constyp)))
        return ' ∧ '.join(array)


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
        x = PyTexpr1.cst(environment, PyDoubleScalarCoeff(-1.0))
        return cls.make(x, ConsTyp.AP_CONS_SUPEQ)

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        result = PyTcons1(deepcopy(self.tcons1))
        memodict[id(self)] = result
        return result

    def __del__(self):
        libapron.ap_tcons1_clear(self)
        del self.tcons1

    @property
    def _as_parameter_(self):
        return byref(self.tcons1)

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyTcons1)
        return argument

    def __repr__(self):
        return '{}'.format(self.tcons1)

    def substitute(self, var: PyVar, dst: PyTexpr1):
        self.tcons1.env.contents.count += 1
        dim = libapron.ap_environment_dim_of_var(PyEnvironment(self.tcons1.env), var)
        texpr0 = self.tcons1.tcons0.texpr0
        libapron.ap_texpr0_substitute_with(texpr0, dim, dst.texpr1.contents.texpr0)
        return self


libapron.ap_tcons1_clear.argtypes = [PyTcons1]


class PyTcons1Array:

    def __init__(self, tcons1s: Union[TCons1Array, List[PyTcons1]] = None,
                 environment: PyEnvironment = None):
        if isinstance(tcons1s, TCons1Array):
            self.tcons1array = tcons1s
        elif tcons1s:
            size = len(tcons1s)
            self.tcons1array = libapron.ap_tcons1_array_make(tcons1s[0].tcons1.env, size)
            for i in range(size):
                libapron.ap_tcons1_array_set(self, i, deepcopy(tcons1s[i].tcons1))
        else:
            self.tcons1array = libapron.ap_tcons1_array_make(environment, 0)

    def __del__(self):
        libapron.ap_tcons1_array_clear(self)
        del self.tcons1array

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
