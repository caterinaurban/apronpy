"""
APRON Abstract Values (Level 1)
===============================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER, byref
from abc import ABCMeta
from ctypes import c_size_t, c_char_p, c_bool
from typing import List, Type, Union

from apronpy.abstract0 import Abstract0
from apronpy.cdll import libapron
from apronpy.environment import Environment, PyEnvironment
from apronpy.interval import Interval, PyInterval
from apronpy.lincons1 import Lincons1Array, PyLincons1Array
from apronpy.linexpr1 import PyLinexpr1, Linexpr1
from apronpy.manager import PyManager
from apronpy.tcons1 import PyTcons1Array, TCons1Array
from apronpy.texpr1 import PyTexpr1, Texpr1
from apronpy.var import PyVar

APRON_assign_linexpr_array = libapron.ap_abstract1_assign_linexpr_array
APRON_assign_texpr_array = libapron.ap_abstract1_assign_texpr_array
APRON_substitute_linexpr_array = libapron.ap_abstract1_substitute_linexpr_array
APRON_substitute_texpr_array = libapron.ap_abstract1_substitute_texpr_array


class Abstract1(Structure):
    """
    typedef struct ap_abstract1_t {
      ap_abstract0_t* abstract0;
      ap_environment_t* env;
    } ap_abstract1_t;
    """

    _fields_ = [
        ('abstract0', POINTER(Abstract0)),
        ('env', POINTER(Environment))
    ]


class PyAbstract1(metaclass=ABCMeta):

    # noinspection PyTypeChecker
    def __init__(self, manager: PyManager,
                 abstract1_or_environment: Union[Abstract1, PyEnvironment],
                 bottom: bool = False, array: Union[PyLincons1Array, PyTcons1Array] = None,
                 variables: List[PyVar] = None, intervals: List[PyInterval] = None):
        self.manager = manager
        if isinstance(abstract1_or_environment, Abstract1):
            self.abstract1 = abstract1_or_environment
        elif bottom:
            assert isinstance(abstract1_or_environment, PyEnvironment)
            self.abstract1 = libapron.ap_abstract1_bottom(self.manager, abstract1_or_environment)
        elif array and isinstance(array, PyLincons1Array):
            assert isinstance(abstract1_or_environment, PyEnvironment)
            man = self.manager
            a1 = libapron.ap_abstract1_of_lincons_array(man, abstract1_or_environment, array)
            self.abstract1 = a1
        elif array and isinstance(array, PyTcons1Array):
            assert isinstance(abstract1_or_environment, PyEnvironment)
            man = self.manager
            a1 = libapron.ap_abstract1_of_tcons_array(man, abstract1_or_environment, array)
            self.abstract1 = a1
        elif variables and intervals:
            assert isinstance(abstract1_or_environment, PyEnvironment)
            size = len(variables)
            v_typ: Type = c_char_p * size
            v_arr = v_typ(*(x._as_parameter_ for x in variables))
            i_typ: Type = POINTER(Interval) * size
            i_arr = i_typ(*(x._as_parameter_ for x in intervals))
            man = self.manager
            a1 = libapron.ap_abstract1_of_box(man, abstract1_or_environment, v_arr, i_arr, size)
            self.abstract1 = a1
        else:
            assert isinstance(abstract1_or_environment, PyEnvironment)
            self.abstract1 = libapron.ap_abstract1_top(self.manager, abstract1_or_environment)

    def closure(self):
        return type(self)(self.manager, libapron.ap_abstract1_closure(self.manager, False, self))

    @classmethod
    def bottom(cls, manager: PyManager, environment: PyEnvironment):
        return cls(manager, environment, bottom=True)

    @classmethod
    def from_constraints(cls, manager: PyManager, environment: PyEnvironment, array):
        return cls(manager, environment, array=array)

    @classmethod
    def top(cls, manager: PyManager, environment: PyEnvironment):
        return cls(manager, environment)

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        abstract1 = libapron.ap_abstract1_copy(self.manager, self)
        result = type(self)(self.manager, abstract1)
        memodict[id(self)] = result
        return result

    def __del__(self):
        libapron.ap_abstract1_clear(self.manager, self)
        del self.abstract1

    @property
    def _as_parameter_(self):
        return byref(self.abstract1)

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyAbstract1)
        return argument

    @property
    def to_lincons(self) -> PyLincons1Array:
        return PyLincons1Array(libapron.ap_abstract1_to_lincons_array(self.manager, self))

    @property
    def to_tcons(self) -> PyTcons1Array:
        return PyTcons1Array(libapron.ap_abstract1_to_tcons_array(self.manager, self))

    def __repr__(self):
        array = PyLincons1Array(libapron.ap_abstract1_to_lincons_array(self.manager, self))
        return '{}'.format(array)

    @property
    def environment(self) -> PyEnvironment:
        return PyEnvironment(libapron.ap_abstract1_environment(self.manager, self))

    @environment.setter
    def environment(self, environment: PyEnvironment):
        e_size = len(environment)
        a1 = libapron.ap_abstract1_change_environment(self.manager, False, self, environment, e_size, False)
        self.abstract1 = a1

    def is_bottom(self):
        return bool(libapron.ap_abstract1_is_bottom(self.manager, self))

    def is_top(self):
        return bool(libapron.ap_abstract1_is_top(self.manager, self))

    def __le__(self, other: 'PyAbstract1'):
        assert isinstance(other, PyAbstract1)
        return bool(libapron.ap_abstract1_is_leq(self.manager, self, other))

    def is_leq(self, other: 'PyAbstract1'):
        assert isinstance(other, PyAbstract1)
        return self.__le__(other)

    def __eq__(self, other: 'PyAbstract1'):
        assert isinstance(other, PyAbstract1)
        return bool(libapron.ap_abstract1_is_eq(self.manager, self, other))

    def is_eq(self, other: 'PyAbstract1'):
        assert isinstance(other, PyAbstract1)
        return self.__eq__(other)

    def bound_variable(self, var: PyVar):
        return PyInterval(libapron.ap_abstract1_bound_variable(self.manager, self, var))

    def bound_linexpr(self, linexpr: PyLinexpr1):
        return PyInterval(libapron.ap_abstract1_bound_linexpr(self.manager, self, linexpr))

    def bound_texpr(self, texpr: PyTexpr1):
        return PyInterval(libapron.ap_abstract1_bound_texpr(self.manager, self, texpr))

    def meet(self, other: Union['PyAbstract1', PyLincons1Array, PyTcons1Array]):
        if isinstance(other, PyLincons1Array):
            abstract1 = libapron.ap_abstract1_meet_lincons_array(self.manager, False, self, other)
            return type(self)(self.manager, abstract1)
        elif isinstance(other, PyTcons1Array):
            abstract1 = libapron.ap_abstract1_meet_tcons_array(self.manager, False, self, other)
            return type(self)(self.manager, abstract1)
        else:
            assert isinstance(other, PyAbstract1)
            abstract1 = libapron.ap_abstract1_meet(self.manager, False, self, other)
            return type(self)(self.manager, abstract1)

    def join(self, other: 'PyAbstract1'):
        assert isinstance(other, PyAbstract1)
        return type(self)(self.manager, libapron.ap_abstract1_join(self.manager, False, self, other))

    def widening(self, other: 'PyAbstract1'):
        assert isinstance(other, PyAbstract1)
        return type(self)(self.manager, libapron.ap_abstract1_widening(self.manager, self, other))

    # noinspection PyTypeChecker
    def assign(self, var_or_vars: PyVar, expr_or_exprs: Union[PyLinexpr1, PyTexpr1]):
        man = self.manager
        if isinstance(var_or_vars, PyVar):
            var = var_or_vars
            expr = expr_or_exprs
            if isinstance(expr, PyLinexpr1):
                abstract1 = libapron.ap_abstract1_assign_linexpr(man, False, self, var, expr, None)
                return type(self)(self.manager, abstract1)
            else:
                assert isinstance(expr, PyTexpr1)
                abstract1 = libapron.ap_abstract1_assign_texpr(man, False, self, var, expr, None)
                return type(self)(self.manager, abstract1)
        else:
            assert isinstance(var_or_vars, list)
            assert all(isinstance(var, PyVar) for var in var_or_vars)
            exprs = expr_or_exprs
            if all(isinstance(expr, PyLinexpr1) for expr in exprs):
                v_size = len(var_or_vars)
                e_size = len(exprs)
                assert v_size == e_size
                v_typ: Type = c_char_p * v_size
                v_arr = v_typ(*(x._as_parameter_ for x in var_or_vars))
                e_typ: Type = Linexpr1 * e_size
                e_arr = e_typ(*(e.linexpr1 for e in exprs))
                a1 = APRON_assign_linexpr_array(man, False, self, v_arr, e_arr, v_size, None)
                return type(self)(self.manager, a1)
            else:
                assert all(isinstance(expr, PyTexpr1) for expr in exprs)
                v_size = len(var_or_vars)
                e_size = len(exprs)
                assert v_size == e_size
                v_typ: Type = c_char_p * v_size
                v_arr = v_typ(*(x._as_parameter_ for x in var_or_vars))
                e_typ: Type = Texpr1 * e_size
                e_arr = e_typ(*(e.texpr1.contents for e in exprs))
                a1 = APRON_assign_texpr_array(man, False, self, v_arr, e_arr, v_size, None)
                return type(self)(self.manager, a1)

    # noinspection PyTypeChecker
    def substitute(self, var_or_vars: Union[PyVar, List[PyVar]],
                   expr_or_exprs: Union[PyLinexpr1, PyTexpr1, List[PyLinexpr1], List[PyTexpr1]]):
        man = self.manager
        if isinstance(var_or_vars, PyVar):
            var = var_or_vars
            expr = expr_or_exprs
            if isinstance(expr, PyLinexpr1):
                a1 = libapron.ap_abstract1_substitute_linexpr(man, False, self, var, expr, None)
                return type(self)(self.manager, a1)
            else:
                assert isinstance(expr, PyTexpr1)
                a1 = libapron.ap_abstract1_substitute_texpr(man, False, self, var, expr, None)
                return type(self)(self.manager, a1)
        else:
            assert isinstance(var_or_vars, list)
            assert all(isinstance(var, PyVar) for var in var_or_vars)
            exprs = expr_or_exprs
            if all(isinstance(expr, PyLinexpr1) for expr in exprs):
                v_size = len(var_or_vars)
                e_size = len(exprs)
                assert v_size == e_size
                v_typ: Type = c_char_p * v_size
                v_arr = v_typ(*(x._as_parameter_ for x in var_or_vars))
                e_typ: Type = Linexpr1 * e_size
                e_arr = e_typ(*(e.linexpr1 for e in exprs))
                a1 = APRON_substitute_linexpr_array(man, False, self, v_arr, e_arr, v_size, None)
                return type(self)(self.manager, a1)
            else:
                assert all(isinstance(expr, PyTexpr1) for expr in exprs)
                v_size = len(var_or_vars)
                e_size = len(exprs)
                assert v_size == e_size
                v_typ: Type = c_char_p * v_size
                v_arr = v_typ(*(x._as_parameter_ for x in var_or_vars))
                e_typ: Type = Texpr1 * e_size
                e_arr = e_typ(*(e.texpr1.contents for e in exprs))
                a1 = APRON_substitute_texpr_array(man, False, self, v_arr, e_arr, v_size, None)
                return type(self)(self.manager, a1)

    # noinspection PyTypeChecker
    def forget(self, variables: List[PyVar]):
        v_size = len(variables)
        v_typ: Type = c_char_p * v_size
        v_arr = v_typ(*(x._as_parameter_ for x in variables))
        a1 = libapron.ap_abstract1_forget_array(self.manager, False, self, v_arr, v_size, False)
        return type(self)(self.manager, a1)


man_p = PyManager
pya1 = PyAbstract1
libapron.ap_abstract1_copy.argtypes = [man_p, pya1]
libapron.ap_abstract1_copy.restype = Abstract1
libapron.ap_abstract1_clear.argtypes = [man_p, pya1]
libapron.ap_abstract1_bottom.argtypes = [man_p, PyEnvironment]
libapron.ap_abstract1_bottom.restype = Abstract1
pyvar_p = POINTER(c_char_p)
pyitv_p = POINTER(POINTER(Interval))
libapron.ap_abstract1_of_box.argtypes = [man_p, PyEnvironment, pyvar_p, pyitv_p, c_size_t]
libapron.ap_abstract1_of_box.restype = Abstract1
libapron.ap_abstract1_top.argtypes = [man_p, PyEnvironment]
libapron.ap_abstract1_top.restype = Abstract1
libapron.ap_abstract1_environment.argtypes = [man_p, pya1]
libapron.ap_abstract1_environment.restype = POINTER(Environment)
libapron.ap_abstract1_is_bottom.argtypes = [man_p, pya1]
libapron.ap_abstract1_is_bottom.restype = c_bool
libapron.ap_abstract1_is_top.argtypes = [man_p, pya1]
libapron.ap_abstract1_is_top.restype = c_bool
libapron.ap_abstract1_is_leq.argtypes = [man_p, pya1, pya1]
libapron.ap_abstract1_is_leq.restype = c_bool
libapron.ap_abstract1_is_eq.argtypes = [man_p, pya1, pya1]
libapron.ap_abstract1_is_eq.restype = c_bool
libapron.ap_abstract1_bound_linexpr.argtypes = [man_p, pya1, PyLinexpr1]
libapron.ap_abstract1_bound_linexpr.restype = POINTER(Interval)
libapron.ap_abstract1_bound_texpr.argtypes = [man_p, pya1, PyTexpr1]
libapron.ap_abstract1_bound_texpr.restype = POINTER(Interval)
libapron.ap_abstract1_bound_variable.argtypes = [man_p, pya1, PyVar]
libapron.ap_abstract1_bound_variable.restype = POINTER(Interval)
libapron.ap_abstract1_to_lincons_array.argtypes = [man_p, pya1]
libapron.ap_abstract1_to_lincons_array.restype = Lincons1Array
libapron.ap_abstract1_to_tcons_array.argtypes = [man_p, pya1]
libapron.ap_abstract1_to_tcons_array.restype = TCons1Array
libapron.ap_abstract1_meet.argtypes = [man_p, c_bool, pya1, pya1]
libapron.ap_abstract1_meet.restype = Abstract1
libapron.ap_abstract1_meet_lincons_array.argtypes = [man_p, c_bool, pya1, PyLincons1Array]
libapron.ap_abstract1_meet_lincons_array.restype = Abstract1
libapron.ap_abstract1_meet_tcons_array.argtypes = [man_p, c_bool, pya1, PyTcons1Array]
libapron.ap_abstract1_meet_tcons_array.restype = Abstract1
libapron.ap_abstract1_join.argtypes = [man_p, c_bool, pya1, pya1]
libapron.ap_abstract1_join.restype = Abstract1
libapron.ap_abstract1_widening.argtypes = [man_p, pya1, pya1]
libapron.ap_abstract1_widening.restype = Abstract1
libapron.ap_abstract1_closure.argtypes = [man_p, c_bool, pya1]
libapron.ap_abstract1_closure.restype = Abstract1
pyl1 = PyLinexpr1
pya1_p = POINTER(Abstract1)
libapron.ap_abstract1_of_lincons_array.argtypes = [man_p, PyEnvironment, PyLincons1Array]
libapron.ap_abstract1_of_lincons_array.restype = Abstract1
libapron.ap_abstract1_of_tcons_array.argtypes = [man_p, PyEnvironment, PyTcons1Array]
libapron.ap_abstract1_of_tcons_array.restype = Abstract1
pyl1_p = POINTER(Linexpr1)
APRON_assign_linexpr_array.argtypes = [man_p, c_bool, pya1, pyvar_p, pyl1_p, c_size_t, pya1_p]
APRON_assign_linexpr_array.restype = Abstract1
libapron.ap_abstract1_assign_linexpr.argtypes = [man_p, c_bool, pya1, PyVar, pyl1, pya1_p]
libapron.ap_abstract1_assign_linexpr.restype = Abstract1
APRON_substitute_linexpr_array.argtypes = [man_p, c_bool, pya1, pyvar_p, pyl1_p, c_size_t, pya1_p]
APRON_substitute_linexpr_array.restype = Abstract1
libapron.ap_abstract1_substitute_linexpr.argtypes = [man_p, c_bool, pya1, PyVar, pyl1, pya1_p]
libapron.ap_abstract1_substitute_linexpr.restype = Abstract1
pyt1_p = POINTER(Texpr1)
APRON_assign_texpr_array.argtypes = [man_p, c_bool, pya1, pyvar_p, pyt1_p, c_size_t, pya1_p]
APRON_assign_texpr_array.restype = Abstract1
libapron.ap_abstract1_assign_texpr.argtypes = [man_p, c_bool, pya1, PyVar, PyTexpr1, pya1_p]
libapron.ap_abstract1_assign_texpr.restype = Abstract1
APRON_substitute_texpr_array.argtypes = [man_p, c_bool, pya1, pyvar_p, pyt1_p, c_size_t, pya1_p]
APRON_substitute_texpr_array.restype = Abstract1
libapron.ap_abstract1_substitute_texpr.argtypes = [man_p, c_bool, pya1, PyVar, PyTexpr1, pya1_p]
libapron.ap_abstract1_substitute_texpr.restype = Abstract1
libapron.ap_abstract1_forget_array.argtypes = [man_p, c_bool, pya1, pyvar_p, c_size_t, c_bool]
libapron.ap_abstract1_forget_array.restype = Abstract1
pyenv = PyEnvironment
libapron.ap_abstract1_change_environment.argtypes = [man_p, c_bool, pya1, pyenv, c_size_t, c_bool]
libapron.ap_abstract1_change_environment.restype = Abstract1
