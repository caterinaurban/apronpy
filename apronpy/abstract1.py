"""
APRON Abstract Values (Level 1)
===============================

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER, byref
from abc import ABCMeta
from ctypes import c_size_t, c_char_p, c_bool
from typing import List, Type, Union

from apronpy.lincons1 import Lincons1Array, PyLincons1Array
from apronpy.linexpr1 import PyLinexpr1

from apronpy.abstract0 import Abstract0
from apronpy.cdll import libapron
from apronpy.environment import Environment, PyEnvironment
from apronpy.interval import Interval, PyInterval
from apronpy.manager import Manager
from apronpy.tcons1 import PyTcons1Array
from apronpy.texpr1 import PyTexpr1
from apronpy.var import PyVar


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

    manager: POINTER(Manager)

    # noinspection PyTypeChecker
    def __init__(self, abstract1_or_environment: Union[Abstract1, PyEnvironment],
                 bottom: bool = False, array: Union[PyLincons1Array, PyTcons1Array] = None,
                 variables: List[PyVar] = None, intervals: List[PyInterval] = None):
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

    @classmethod
    def bottom(cls, environment: PyEnvironment):
        return cls(environment, bottom=True)

    @classmethod
    def from_constraints(cls, environment: PyEnvironment, array):
        return cls(environment, array=array)

    @classmethod
    def top(cls, environment: PyEnvironment):
        return cls(environment)

    def __deepcopy__(self, memodict=None):
        if memodict is None:
            memodict = {}
        abstract1 = libapron.ap_abstract1_copy(self.manager, self)
        result = type(self)(abstract1)
        memodict[id(self)] = result
        return result

    def __del__(self):
        libapron.ap_abstract1_clear(self.manager, self)

    @property
    def _as_parameter_(self):
        return byref(self.abstract1)

    @staticmethod
    def from_param(argument):
        assert isinstance(argument, PyAbstract1)
        return argument

    def __repr__(self):
        return '{}'.format(libapron.ap_abstract1_to_lincons_array(self.manager, self))

    @property
    def environment(self) -> 'PyEnvironment':
        environment = PyEnvironment()
        environment.environment = libapron.ap_abstract1_environment(self.manager, self)
        return environment

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

    def meet(self, other: Union['PyAbstract1', PyLincons1Array, PyTcons1Array]):
        abstract1 = type(self)(self.environment)
        if isinstance(other, PyLincons1Array):
            result = libapron.ap_abstract1_meet_lincons_array(self.manager, False, self, other)
            abstract1.abstract1 = result
        elif isinstance(other, PyTcons1Array):
            result = libapron.ap_abstract1_meet_tcons_array(self.manager, False, self, other)
            abstract1.abstract1 = result
        else:
            assert isinstance(other, PyAbstract1)
            abstract1.abstract1 = libapron.ap_abstract1_meet(self.manager, False, self, other)
        return abstract1

    def join(self, other: 'PyAbstract1'):
        assert isinstance(other, PyAbstract1)
        abstract1 = type(self)(self.environment)
        abstract1.abstract1 = libapron.ap_abstract1_join(self.manager, False, self, other)
        return abstract1

    def widening(self, other: 'PyAbstract1'):
        assert isinstance(other, PyAbstract1)
        abstract1 = type(self)(self.environment)
        abstract1.abstract1 = libapron.ap_abstract1_widening(self.manager, self, other)
        return abstract1

    def assign(self, var: PyVar, expr: Union[PyLinexpr1, PyTexpr1]):
        abstract1 = type(self)(self.environment)
        man = self.manager
        if isinstance(expr, PyLinexpr1):
            result = libapron.ap_abstract1_assign_linexpr(man, False, self, var, expr, None)
            abstract1.abstract1 = result 
        else:
            assert isinstance(expr, PyTexpr1)
            result = libapron.ap_abstract1_assign_texpr(man, False, self, var, expr, None)
            abstract1.abstract1 = result
        return abstract1

    def substitute(self, var: PyVar, expr: Union[PyLinexpr1, PyTexpr1]):
        abstract1 = type(self)(self.environment)
        man = self.manager
        if isinstance(expr, PyLinexpr1):
            result = libapron.ap_abstract1_substitute_linexpr(man, False, self, var, expr, None)
            abstract1.abstract1 = result
        else:
            assert isinstance(expr, PyTexpr1)
            result = libapron.ap_abstract1_substitute_texpr(man, False, self, var, expr, None)
            abstract1.abstract1 = result
        return abstract1


man_p = POINTER(Manager)
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
libapron.ap_abstract1_is_top.argtypes = [man_p, pya1]
libapron.ap_abstract1_is_leq.argtypes = [man_p, pya1, pya1]
libapron.ap_abstract1_is_eq.argtypes = [man_p, pya1, pya1]
libapron.ap_abstract1_to_lincons_array.argtypes = [man_p, pya1]
libapron.ap_abstract1_to_lincons_array.restype = Lincons1Array
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
pyl1 = PyLinexpr1
pya1_p = POINTER(Abstract1)
libapron.ap_abstract1_of_lincons_array.argtypes = [man_p, PyEnvironment, PyLincons1Array]
libapron.ap_abstract1_of_lincons_array.restype = Abstract1
libapron.ap_abstract1_of_tcons_array.argtypes = [man_p, PyEnvironment, PyTcons1Array]
libapron.ap_abstract1_of_tcons_array.restype = Abstract1
libapron.ap_abstract1_assign_linexpr.argtypes = [man_p, c_bool, pya1, PyVar, pyl1, pya1_p]
libapron.ap_abstract1_assign_linexpr.restype = Abstract1
libapron.ap_abstract1_substitute_linexpr.argtypes = [man_p, c_bool, pya1, PyVar, pyl1, pya1_p]
libapron.ap_abstract1_substitute_linexpr.restype = Abstract1
libapron.ap_abstract1_assign_texpr.argtypes = [man_p, c_bool, pya1, PyVar, PyTexpr1, pya1_p]
libapron.ap_abstract1_assign_texpr.restype = Abstract1
libapron.ap_abstract1_substitute_texpr.argtypes = [man_p, c_bool, pya1, PyVar, PyTexpr1, pya1_p]
libapron.ap_abstract1_substitute_texpr.restype = Abstract1
