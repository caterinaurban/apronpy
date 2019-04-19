"""
APRON Linear Constraints (Level 1)
==================================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER, byref
from copy import deepcopy
from ctypes import c_char_p, c_size_t
from typing import List

from apronpy.cdll import libapron
from apronpy.coeff import PyDoubleScalarCoeff, CoeffDiscr, PyMPQIntervalCoeff, \
    PyMPFRIntervalCoeff, \
    PyDoubleIntervalCoeff, PyMPQScalarCoeff, PyMPFRScalarCoeff, PyCoeff, Coeff
from apronpy.environment import Environment, PyEnvironment
from apronpy.lincons0 import Lincons0, ConsTyp, Lincons0Array
from apronpy.linexpr0 import LinexprDiscr
from apronpy.linexpr1 import PyLinexpr1
from apronpy.scalar import PyScalar, c_uint, ScalarDiscr
from apronpy.var import PyVar


class Lincons1(Structure):
    """
    typedef struct ap_lincons1_t {
      ap_lincons0_t lincons0;
      ap_environment_t* env;
    } ap_lincons1_t;
    """

    _fields_ = [
        ('lincons0', Lincons0),
        ('env', POINTER(Environment))
    ]

    def __repr__(self):
        linexpr0 = self.lincons0.linexpr0.contents
        constyp = ConsTyp(self.lincons0.constyp)
        scalar = self.lincons0.scalar
        env = self.env.contents
        result = ''
        if linexpr0.discr == LinexprDiscr.AP_LINEXPR_DENSE:
            result += ' + '.join(
                '{}·{}'.format(linexpr0.p.coeff[i], env.var_of_dim[i].decode('utf-8'))
                for i in range(linexpr0.size)
            )
            result += ' + {}'.format(linexpr0.cst) if result else '{}'.format(linexpr0.cst)
        else:   # self.discr == LinexprDiscr.AP_LINEXPR_SPARSE:
            terms = list()
            for i in range(linexpr0.size):
                coeff = linexpr0.p.linterm[i].coeff
                dim = linexpr0.p.linterm[i].dim.value
                if dim < linexpr0.size:
                    terms.append('{}·{}'.format(coeff, env.var_of_dim[dim].decode('utf-8')))
            result += ' + '.join(terms)
            result += ' + {}'.format(linexpr0.cst) if result else '{}'.format(linexpr0.cst)
        if scalar:
            return '{} {} {}'.format(result.replace('+ -', '- '), repr(constyp), scalar.contents)
        else:
            return '{} {} 0'.format(result.replace('+ -', '- '), repr(constyp))


class Lincons1Array(Structure):
    """
    typedef struct ap_lincons1_array_t {
      ap_lincons0_array_t lincons0_array;
      ap_environment_t* env;
    } ap_lincons1_array_t;
    """

    _fields_ = [
        ('lincons0_array', Lincons0Array),
        ('env', POINTER(Environment))
    ]

    def __repr__(self):
        env = self.env.contents
        array = list()
        for i in range(self.lincons0_array.size):

            linexpr0 = self.lincons0_array.p[i].linexpr0.contents
            constyp = ConsTyp(self.lincons0_array.p[i].constyp)
            scalar = self.lincons0_array.p[i].scalar

            result = ''
            if linexpr0.discr == LinexprDiscr.AP_LINEXPR_DENSE:
                result += ' + '.join(
                    '{}·{}'.format(linexpr0.p.coeff[j], env.var_of_dim[j].decode('utf-8'))
                    for j in range(linexpr0.size) if str(linexpr0.p.coeff[j]) != '0'
                )
                result += ' + {}'.format(linexpr0.cst) if result else '{}'.format(linexpr0.cst)
            else:  # self.discr == LinexprDiscr.AP_LINEXPR_SPARSE:
                terms = list()
                for j in range(linexpr0.size):
                    coeff = linexpr0.p.linterm[j].coeff
                    dim = linexpr0.p.linterm[j].dim.value
                    if dim < linexpr0.size:
                        terms.append('{}·{}'.format(coeff, env.var_of_dim[dim].decode('utf-8')))
                result += ' + '.join(terms)
                result += ' + {}'.format(linexpr0.cst) if result else '{}'.format(linexpr0.cst)
            if scalar:
                result = result.replace('+ -', '- ')
                array.append('{} {} {}'.format(result, repr(constyp), scalar.contents))
            else:
                array.append('{} {} 0'.format(result.replace('+ -', '- '), repr(constyp)))

        return '[' + ' , '.join(array) + ']'


class PyLincons1:

    def __init__(self, typ: ConsTyp, linexpr: PyLinexpr1, scalar: PyScalar = None):
        self.lincons1 = Lincons1()
        linexpr_copy = deepcopy(linexpr.linexpr1)
        self.lincons1.lincons0.linexpr0 = linexpr_copy.linexpr0
        self.lincons1.lincons0.constyp = c_uint(typ)
        if scalar:
            self.lincons1.lincons0.scalar = deepcopy(scalar)
        self.lincons1.env = linexpr_copy.env

    @classmethod
    def unsat(cls, environment: PyEnvironment):
        x = PyLinexpr1(environment)
        x.set_cst(PyDoubleScalarCoeff(-1.0))
        lincons = cls(ConsTyp.AP_CONS_SUPEQ, x)
        return lincons

    def __del__(self):
        libapron.ap_lincons1_clear(self)

    @property
    def _as_parameter_(self):
        return byref(self.lincons1)

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyLincons1)
        return argument

    def __repr__(self):
        return '{}'.format(self.lincons1)

    def is_unsat(self):
        return bool(libapron.ap_lincons0_is_unsat(self.lincons1.lincons0))

    def get_typ(self):
        return ConsTyp(self.lincons1.lincons0.constyp)

    def set_typ(self, typ: ConsTyp):
        self.lincons1.lincons0.constyp = c_uint(typ)

    def get_cst(self):
        cst = self.lincons1.lincons0.linexpr0.contents.cst
        if cst.discr == CoeffDiscr.AP_COEFF_INTERVAL:
            if cst.val.interval.contents.inf.contents.discr == ScalarDiscr.AP_SCALAR_MPQ:
                result = PyMPQIntervalCoeff()
            elif cst.val.interval.contents.inf.contents.discr == ScalarDiscr.AP_SCALAR_MPFR:
                result = PyMPFRIntervalCoeff(0, 0)
            else:  # cst.val.interval.contents.inf.contents.discr == ScalarDiscr.AP_SCALAR_DOUBLE
                result = PyDoubleIntervalCoeff()
        else:  # CoeffDiscr.AP_COEFF_SCALAR
            if cst.val.scalar.contents.discr == ScalarDiscr.AP_SCALAR_MPQ:
                result = PyMPQScalarCoeff()
            elif cst.val.scalar.contents.discr == ScalarDiscr.AP_SCALAR_MPFR:
                result = PyMPFRScalarCoeff(0)
            else:  # cst.val.scalar.contents.discr == ScalarDiscr.AP_SCALAR_DOUBLE
                result = PyDoubleScalarCoeff()
        libapron.ap_coeff_set(result.coeff, self.lincons1.lincons0.linexpr0.contents.cst)
        return result

    def set_cst(self, cst: PyCoeff):
        libapron.ap_coeff_set(byref(self.lincons1.lincons0.linexpr0.contents.cst), cst.coeff)

    def get_coeff(self, var: PyVar):
        coeff = libapron.ap_lincons1_coeffref(self, var._as_parameter_)
        if coeff.contents.discr == CoeffDiscr.AP_COEFF_INTERVAL:
            discr = coeff.contents.val.interval.contents.inf.contents.discr
            if discr == ScalarDiscr.AP_SCALAR_MPQ:
                result = PyMPQIntervalCoeff()
            elif discr == ScalarDiscr.AP_SCALAR_MPFR:
                result = PyMPFRIntervalCoeff(0, 0)
            else:  # discr == ScalarDiscr.AP_SCALAR_DOUBLE
                result = PyDoubleIntervalCoeff()
        else:  # CoeffDiscr.AP_COEFF_SCALAR
            if coeff.contents.val.scalar.contents.discr == ScalarDiscr.AP_SCALAR_MPQ:
                result = PyMPQScalarCoeff()
            elif coeff.contents.val.scalar.contents.discr == ScalarDiscr.AP_SCALAR_MPFR:
                result = PyMPFRScalarCoeff(0)
            else:  # coeff.contents.val.scalar.contents.discr == ScalarDiscr.AP_SCALAR_DOUBLE
                result = PyDoubleScalarCoeff()
        libapron.ap_lincons1_get_coeff(result.coeff, self, var._as_parameter_)
        return result

    def set_coeff(self, var: PyVar, coeff: PyCoeff):
        libapron.ap_coeff_set(libapron.ap_lincons1_coeffref(self, var._as_parameter_), coeff.coeff)


libapron.ap_lincons1_clear.argtypes = [PyLincons1]
libapron.ap_lincons1_coeffref.argtypes = [PyLincons1, c_char_p]
libapron.ap_lincons1_coeffref.restype = POINTER(Coeff)
libapron.ap_lincons1_get_coeff.argtypes = [POINTER(Coeff), PyLincons1, c_char_p]


class PyLincons1Array:

    def __init__(self, lincons1s: List[PyLincons1] = None, environment: PyEnvironment = None):
        if lincons1s:
            size = len(lincons1s)
            lincons1s[0].lincons1.env.contents.count += 1
            self.lincons1array = libapron.ap_lincons1_array_make(lincons1s[0].lincons1.env, size)
            for i in range(size):
                lincons1i_copy = Lincons1()
                lincons1i_copy.lincons0 = Lincons0()
                linexpr0_copy = libapron.ap_linexpr0_copy(lincons1s[i].lincons1.lincons0.linexpr0)
                lincons1i_copy.lincons0.linexpr0 = linexpr0_copy
                lincons1i_copy.lincons0.constyp = c_uint(lincons1s[i].lincons1.lincons0.constyp)
                scalar = lincons1s[i].lincons1.lincons0.scalar
                if scalar:
                    lincons1i_copy.lincons0.scalar = libapron.ap_scalar_alloc_set(scalar)
                else:
                    lincons1i_copy.lincons0.scalar = None
                lincons1s[i].lincons1.env.contents.count += 1
                lincons1i_copy.env = lincons1s[i].lincons1.env
                libapron.ap_lincons1_array_set(self, i, byref(lincons1i_copy))
        else:
            self.lincons1array = libapron.ap_lincons1_array_make(environment, 0)

    def __del__(self):
        libapron.ap_lincons1_array_clear(self)

    @property
    def _as_parameter_(self):
        return byref(self.lincons1array)

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyLincons1Array)
        return argument

    def __repr__(self):
        return '{}'.format(self.lincons1array)


libapron.ap_lincons1_array_make.argtypes = [POINTER(Environment), c_size_t]
libapron.ap_lincons1_array_make.restype = Lincons1Array
libapron.ap_lincons1_array_clear.argtypes = [PyLincons1Array]
libapron.ap_lincons1_array_set.argtypes = [PyLincons1Array, c_size_t, POINTER(Lincons1)]
