"""
APRON Manager

:Author: Caterina Urban
"""
from _ctypes import Structure, POINTER
from ctypes import c_char_p, c_void_p, CFUNCTYPE, c_size_t, c_int, c_bool, c_uint
from enum import IntEnum


class FunId(IntEnum):
    """
    typedef enum ap_funid_t {
      AP_FUNID_UNKNOWN,
      AP_FUNID_COPY,
      AP_FUNID_FREE,
      AP_FUNID_ASIZE, /* For avoiding name conflict with AP_FUNID_SIZE */
      AP_FUNID_MINIMIZE,
      AP_FUNID_CANONICALIZE,
      AP_FUNID_HASH,
      AP_FUNID_APPROXIMATE,
      AP_FUNID_FPRINT,
      AP_FUNID_FPRINTDIFF,
      AP_FUNID_FDUMP,
      AP_FUNID_SERIALIZE_RAW,
      AP_FUNID_DESERIALIZE_RAW,
      AP_FUNID_BOTTOM,
      AP_FUNID_TOP,
      AP_FUNID_OF_BOX,
      AP_FUNID_DIMENSION,
      AP_FUNID_IS_BOTTOM,
      AP_FUNID_IS_TOP,
      AP_FUNID_IS_LEQ,
      AP_FUNID_IS_EQ,
      AP_FUNID_IS_DIMENSION_UNCONSTRAINED,
      AP_FUNID_SAT_INTERVAL,
      AP_FUNID_SAT_LINCONS,
      AP_FUNID_SAT_TCONS,
      AP_FUNID_BOUND_DIMENSION,
      AP_FUNID_BOUND_LINEXPR,
      AP_FUNID_BOUND_TEXPR,
      AP_FUNID_TO_BOX,
      AP_FUNID_TO_LINCONS_ARRAY,
      AP_FUNID_TO_TCONS_ARRAY,
      AP_FUNID_TO_GENERATOR_ARRAY,
      AP_FUNID_MEET,
      AP_FUNID_MEET_ARRAY,
      AP_FUNID_MEET_LINCONS_ARRAY,
      AP_FUNID_MEET_TCONS_ARRAY,
      AP_FUNID_JOIN,
      AP_FUNID_JOIN_ARRAY,
      AP_FUNID_ADD_RAY_ARRAY,
      AP_FUNID_ASSIGN_LINEXPR_ARRAY,
      AP_FUNID_SUBSTITUTE_LINEXPR_ARRAY,
      AP_FUNID_ASSIGN_TEXPR_ARRAY,
      AP_FUNID_SUBSTITUTE_TEXPR_ARRAY,
      AP_FUNID_ADD_DIMENSIONS,
      AP_FUNID_REMOVE_DIMENSIONS,
      AP_FUNID_PERMUTE_DIMENSIONS,
      AP_FUNID_FORGET_ARRAY,
      AP_FUNID_EXPAND,
      AP_FUNID_FOLD,
      AP_FUNID_WIDENING,
      AP_FUNID_CLOSURE,
      AP_FUNID_SIZE,
      AP_FUNID_CHANGE_ENVIRONMENT,
      AP_FUNID_RENAME_ARRAY,
      AP_FUNID_SIZE2
    } ap_funid_t;
    """
    AP_FUNID_UNKNOWN = 0
    AP_FUNID_COPY = 1
    AP_FUNID_FREE = 2
    AP_FUNID_ASIZE = 3
    AP_FUNID_MINIMIZE = 4
    AP_FUNID_CANONICALIZE = 5
    AP_FUNID_HASH = 6
    AP_FUNID_APPROXIMATE = 7
    AP_FUNID_FPRINT = 8
    AP_FUNID_FPRINTDIFF = 9
    AP_FUNID_FDUMP = 10
    AP_FUNID_SERIALIZE_RAW = 11
    AP_FUNID_DESERIALIZE_RAW = 12
    AP_FUNID_BOTTOM = 13
    AP_FUNID_TOP = 14
    AP_FUNID_OF_BOX = 15
    AP_FUNID_DIMENSION = 16
    AP_FUNID_IS_BOTTOM = 17
    AP_FUNID_IS_TOP = 18
    AP_FUNID_IS_LEQ = 19
    AP_FUNID_IS_EQ = 20
    AP_FUNID_IS_DIMENSION_UNCONSTRAINED = 21
    AP_FUNID_SAT_INTERVAL = 22
    AP_FUNID_SAT_LINCONS = 23
    AP_FUNID_SAT_TCONS = 24
    AP_FUNID_BOUND_DIMENSION = 25
    AP_FUNID_BOUND_LINEXPR = 26
    AP_FUNID_BOUND_TEXPR = 27
    AP_FUNID_TO_BOX = 28
    AP_FUNID_TO_LINCONS_ARRAY = 29
    AP_FUNID_TO_TCONS_ARRAY = 30
    AP_FUNID_TO_GENERATOR_ARRAY = 31
    AP_FUNID_MEET = 32
    AP_FUNID_MEET_ARRAY = 33
    AP_FUNID_MEET_LINCONS_ARRAY = 34
    AP_FUNID_MEET_TCONS_ARRAY = 35
    AP_FUNID_JOIN = 36
    AP_FUNID_JOIN_ARRAY = 37
    AP_FUNID_ADD_RAY_ARRAY = 38
    AP_FUNID_ASSIGN_LINEXPR_ARRAY = 39
    AP_FUNID_SUBSTITUTE_LINEXPR_ARRAY = 40
    AP_FUNID_ASSIGN_TEXPR_ARRAY = 41
    AP_FUNID_SUBSTITUTE_TEXPR_ARRAY = 42
    AP_FUNID_ADD_DIMENSIONS = 43
    AP_FUNID_REMOVE_DIMENSIONS = 44
    AP_FUNID_PERMUTE_DIMENSIONS = 45
    AP_FUNID_FORGET_ARRAY = 46
    AP_FUNID_EXPAND = 47
    AP_FUNID_FOLD = 48
    AP_FUNID_WIDENING = 49
    AP_FUNID_CLOSURE = 50
    AP_FUNID_SIZE = 51
    AP_FUNID_CHANGE_ENVIRONMENT = 52
    AP_FUNID_RENAME_ARRAY = 53
    AP_FUNID_SIZE2 = 54


class Exc(IntEnum):
    """
    typedef enum ap_exc_t {
      AP_EXC_NONE,             /* no exception detected */
      AP_EXC_TIMEOUT,          /* timeout detected */
      AP_EXC_OUT_OF_SPACE,     /* out of space detected */
      AP_EXC_OVERFLOW,         /* magnitude overflow detected */
      AP_EXC_INVALID_ARGUMENT, /* invalid arguments */
      AP_EXC_NOT_IMPLEMENTED,  /* not implemented */
      AP_EXC_SIZE
    } ap_exc_t;
    """
    AP_EXC_NONE = 0
    AP_EXC_TIMEOUT = 1
    AP_EXC_OUT_OF_SPACE = 2
    AP_EXC_OVERFLOW = 3
    AP_EXC_INVALID_ARGUMENT = 4
    AP_EXC_NOT_IMPLEMENTED = 5
    AP_EXC_SIZE = 6


class ExcLog(Structure):
    """
    typedef struct ap_exclog_t {
      ap_exc_t exn;
      ap_funid_t funid;
      char* msg;                   /* dynamically allocated */
      struct ap_exclog_t* tail;
    } ap_exclog_t;
    """
    pass


ExcLog._fields_ = [
        ('exn', c_uint),
        ('funid', c_uint),
        ('msg', c_char_p),
        ('tail', POINTER(ExcLog))
    ]


class Result(Structure):
    """
    typedef struct ap_result_t {
      ap_exclog_t* exclog; /* history of exceptions */
      ap_exc_t exn;        /* exception for the last called function */
      bool flag_exact;  /* result is mathematically exact or don't know */
      bool flag_best;   /* result is best correct approximation or don't know */
    } ap_result_t;
    """

    _fields_ = [
        ('exclog', POINTER(ExcLog)),
        ('exn', c_uint),
        ('flag_exact', c_bool),
        ('flag_best', c_bool)
    ]


class FunOpt(Structure):
    """
    typedef struct ap_funopt_t {
      int algorithm;
      /* Algorithm selection:
         - 0 is default algorithm;
         - MAX_INT is most accurate available;
         - MIN_INT is most efficient available;
         - otherwise, no accuracy or speed meaning
      */
      size_t timeout; /* unit !? */
      /* Above the given computation time, the function may abort with the
         exception flag flag_time_out on.
      */
      size_t max_object_size; /* in abstract object size unit. */
      /* If during the computation, the size of some object reach this limit, the
         function may abort with the exception flag flag_out_of_space on.
      */
      bool flag_exact_wanted;
      /* return information about exactitude if possible
      */
      bool flag_best_wanted;
      /* return information about best correct approximation if possible
      */
    } ap_funopt_t;
    """

    _fields_ = [
        ('algorithm', c_int),
        ('timeout', c_size_t),
        ('max_object_size', c_size_t),
        ('flag_exact_wanted', c_bool),
        ('flag_best_wanted', c_bool)
    ]


# noinspection PyTypeChecker
class Option(Structure):
    """
    typedef struct ap_option_t {
      ap_funopt_t funopt[AP_FUNID_SIZE];
      bool abort_if_exception[AP_EXC_SIZE];
      ap_scalar_discr_t scalar_discr; /* Preferred type for scalars */
    } ap_option_t;
    """

    _fields_ = [
        ('funopt', FunOpt * FunId.AP_FUNID_SIZE),
        ('abort_if_exception', c_bool * Exc.AP_EXC_SIZE),
        ('scalar_discr', c_uint)
    ]


# noinspection PyTypeChecker
class Manager(Structure):
    """
    typedef struct ap_manager_t {
      const char* library;           /* name of the effective library */
      const char* version;           /* version of the effective library */
      void* internal;                /* library dependent,
                                        should be different for each thread
                                        (working space) */
      void* funptr[AP_FUNID_SIZE];   /* Array of function pointers,
                                        initialized by the effective library */
      ap_option_t option;            /* Options (in) */
      ap_result_t result;            /* Exceptions and other indications (out) */
      void (*internal_free)(void*);  /* deallocation function for internal */
      size_t count;                  /* reference counter */
    } ap_manager_t;
    """

    _fields_ = [
        ('library', c_char_p),
        ('version', c_char_p),
        ('internal', c_void_p),
        ('funpts', c_void_p * FunId.AP_FUNID_SIZE),
        ('option', Option),
        ('result', Result),
        ('internal_free', CFUNCTYPE(None, c_void_p)),
        ('count', c_size_t)
    ]
