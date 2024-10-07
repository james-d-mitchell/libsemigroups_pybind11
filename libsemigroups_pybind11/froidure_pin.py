# -*- coding: utf-8 -*-

# Copyright (c) 2021-2024 J. D. Mitchell
#
# Distributed under the terms of the GPL license version 3.
#
# The full license is in the file LICENSE, distributed with this software.

# pylint: disable=no-name-in-module, invalid-name

"""
This package provides the user-facing python part of libsemigroups_pybind11 for
FroidurePin.
"""

from typing import Self, List, TypeVar, Iterator

from .py_wrappers import (
    to_cpp,
    to_py,
    CppObjWrapper,
    may_return_undefined,
    pass_thru_methods,
)


from _libsemigroups_pybind11 import (
    UNDEFINED,
    StaticTransf16 as _StaticTransf16,
    Transf1 as _Transf1,
    Transf2 as _Transf2,
    Transf4 as _Transf4,
    StaticPPerm16 as _StaticPPerm16,
    PPerm1 as _PPerm1,
    PPerm2 as _PPerm2,
    PPerm4 as _PPerm4,
    StaticPerm16 as _StaticPerm16,
    Perm1 as _Perm1,
    Perm2 as _Perm2,
    Perm4 as _Perm4,
    BMat as _BMat,
    IntMat as _IntMat,
    MaxPlusMat as _MaxPlusMat,
    MinPlusMat as _MinPlusMat,
    ProjMaxPlusMat as _ProjMaxPlusMat,
    MaxPlusTruncMat as _MaxPlusTruncMat,
    MinPlusTruncMat as _MinPlusTruncMat,
    NTPMat as _NTPMat,
    Bipartition as _Bipartition,
    PBR as _PBR,
    BMat8 as _BMat8,
    FroidurePinTransf16 as _FroidurePinTransf16,
    FroidurePinTransf1 as _FroidurePinTransf1,
    FroidurePinTransf2 as _FroidurePinTransf2,
    FroidurePinTransf4 as _FroidurePinTransf4,
    FroidurePinPPerm16 as _FroidurePinPPerm16,
    FroidurePinPPerm1 as _FroidurePinPPerm1,
    FroidurePinPPerm2 as _FroidurePinPPerm2,
    FroidurePinPPerm4 as _FroidurePinPPerm4,
    FroidurePinPerm16 as _FroidurePinPerm16,
    FroidurePinPerm1 as _FroidurePinPerm1,
    FroidurePinPerm2 as _FroidurePinPerm2,
    FroidurePinPerm4 as _FroidurePinPerm4,
    FroidurePinBipartition as _FroidurePinBipartition,
    FroidurePinPBR as _FroidurePinPBR,
    FroidurePinBMat8 as _FroidurePinBMat8,
    FroidurePinBMat as _FroidurePinBMat,
    FroidurePinIntMat as _FroidurePinIntMat,
    FroidurePinMaxPlusMat as _FroidurePinMaxPlusMat,
    FroidurePinMinPlusMat as _FroidurePinMinPlusMat,
    FroidurePinProjMaxPlusMat as _FroidurePinProjMaxPlusMat,
    FroidurePinMaxPlusTruncMat as _FroidurePinMaxPlusTruncMat,
    FroidurePinMinPlusTruncMat as _FroidurePinMinPlusTruncMat,
    FroidurePinNTPMat as _FroidurePinNTPMat,
)

Element = TypeVar("Element")

_ElementToFroidurePin = {
    _StaticTransf16: _FroidurePinTransf16,
    _Transf1: _FroidurePinTransf1,
    _Transf2: _FroidurePinTransf2,
    _Transf4: _FroidurePinTransf4,
    _StaticPPerm16: _FroidurePinPPerm16,
    _PPerm1: _FroidurePinPPerm1,
    _PPerm2: _FroidurePinPPerm2,
    _PPerm4: _FroidurePinPPerm4,
    _StaticPerm16: _FroidurePinPerm16,
    _Perm1: _FroidurePinPerm1,
    _Perm2: _FroidurePinPerm2,
    _Perm4: _FroidurePinPerm4,
    _Bipartition: _FroidurePinBipartition,
    _PBR: _FroidurePinPBR,
    _BMat8: _FroidurePinBMat8,
    _BMat: _FroidurePinBMat,
    _IntMat: _FroidurePinIntMat,
    _MaxPlusMat: _FroidurePinMaxPlusMat,
    _MinPlusMat: _FroidurePinMinPlusMat,
    _ProjMaxPlusMat: _FroidurePinProjMaxPlusMat,
    _MaxPlusTruncMat: _FroidurePinMaxPlusTruncMat,
    _MinPlusTruncMat: _FroidurePinMinPlusTruncMat,
    _NTPMat: _FroidurePinNTPMat,
}

_FroidurePinTypes = {
    _FroidurePinTransf16: True,
    _FroidurePinTransf1: True,
    _FroidurePinTransf2: True,
    _FroidurePinTransf4: True,
    _FroidurePinPPerm16: True,
    _FroidurePinPPerm1: True,
    _FroidurePinPPerm2: True,
    _FroidurePinPPerm4: True,
    _FroidurePinPerm16: True,
    _FroidurePinPerm1: True,
    _FroidurePinPerm2: True,
    _FroidurePinPerm4: True,
    _FroidurePinBipartition: True,
    _FroidurePinPBR: True,
    _FroidurePinBMat8: True,
    _FroidurePinBMat: True,
    _FroidurePinIntMat: True,
    _FroidurePinMaxPlusMat: True,
    _FroidurePinMinPlusMat: True,
    _FroidurePinProjMaxPlusMat: True,
    _FroidurePinMaxPlusTruncMat: True,
    _FroidurePinMinPlusTruncMat: True,
    _FroidurePinNTPMat: True,
    # _FroidurePinKBE: True,
    # _FroidurePinTCE: True,
}


class FroidurePin(CppObjWrapper):
    __doc__ = _FroidurePinPBR.__doc__

    _CppObjWrapper__lookup = {
        (_StaticTransf16,): _FroidurePinTransf16,
        (_Transf1,): _FroidurePinTransf1,
        (_Transf2,): _FroidurePinTransf2,
        (_Transf4,): _FroidurePinTransf4,
        (_StaticPPerm16,): _FroidurePinPPerm16,
        (_PPerm1,): _FroidurePinPPerm1,
        (_PPerm2,): _FroidurePinPPerm2,
        (_PPerm4,): _FroidurePinPPerm4,
        (_StaticPerm16,): _FroidurePinPerm16,
        (_Perm1,): _FroidurePinPerm1,
        (_Perm2,): _FroidurePinPerm2,
        (_Perm4,): _FroidurePinPerm4,
        (_Bipartition,): _FroidurePinBipartition,
        (_PBR,): _FroidurePinPBR,
        (_BMat8,): _FroidurePinBMat8,
        (_BMat,): _FroidurePinBMat,
        (_IntMat,): _FroidurePinIntMat,
        (_MaxPlusMat,): _FroidurePinMaxPlusMat,
        (_MinPlusMat,): _FroidurePinMinPlusMat,
        (_ProjMaxPlusMat,): _FroidurePinProjMaxPlusMat,
        (_MaxPlusTruncMat,): _FroidurePinMaxPlusTruncMat,
        (_MinPlusTruncMat,): _FroidurePinMinPlusTruncMat,
        (_NTPMat,): _FroidurePinNTPMat,
    }

    @staticmethod
    def returns_element(method):
        def wrapper(self, *args):
            result = method(self, *args)
            return to_py(self.Element, result, self.degree())

        return wrapper

    def __init__(self: Self, gens: List[Element]) -> None:
        if len(gens) == 0:
            raise ValueError("expected at least 1 argument, found 0")
        cpp_obj_t = self._cpp_obj_type_from(
            samples=(to_cpp(gens[0]),),
        )
        self.Element = type(gens[0])
        self._cpp_obj = cpp_obj_t([to_cpp(x) for x in gens])
        self._degree = gens[0].degree()

    @returns_element
    def __getitem__(self: Self, i: int) -> Element:
        return self.cpp_call_mem_fn("__getitem__", i)

    def degree(self: Self) -> int:
        return self._degree

    @returns_element
    def generator(self: Self, i: int) -> Element:
        return self.cpp_call_mem_fn("generator", i)

    @may_return_undefined
    def current_position(self: Self, x: Element) -> int:
        return self.cpp_call_mem_fn("current_position", x)

    def idempotents(self: Self) -> Iterator:
        return map(
            lambda x: to_py(self.Element, x, self.degree()),
            self.cpp_call_mem_fn("idempotents"),
        )

    @may_return_undefined
    def position(self: Self, x: Element) -> int:
        return self.cpp_call_mem_fn("position", x)

    @returns_element
    def sorted_at(self: Self, i: int) -> Element:
        return self.cpp_call_mem_fn("sorted_at", i)

    def sorted_elements(self: Self) -> Iterator:
        return map(
            lambda x: to_py(self.Element, x, self.degree()),
            self.cpp_call_mem_fn("sorted_elements"),
        )

    @returns_element
    def to_element(self: Self, w: List[int]) -> Element:
        return self.cpp_call_mem_fn("to_element", w)


pass_thru_methods(
    FroidurePin,
    "add_generator",
    "add_generators",
    "closure",
    "contains",
    "copy_add_generators",
    "copy_closure",
    "equal_to",
    "factorisation",
    "fast_product",
    "init",
    "is_finite",
    "is_idempotent",
    "minimal_factorisation",
    "number_of_generators",
    "number_of_idempotents",
    "reserve",
    "size",
    "sorted_position",
    "to_sorted_position",
)

# def FroidurePin(*args):
#     """
#     Construct a FroidurePin instance of the type specified by its generators.
#     """
#     if len(args) == 0:
#         raise ValueError("expected at least 1 argument, found 0")
#     if type(args[0]) in _FroidurePinTypes:
#         return type(args[0])(args[0])
#     if isinstance(args[0], list):
#         args_ = args[0]
#     else:
#         args_ = args
#     if isinstance(args_[0], CppObjWrapper):
#         args_ = [to_cpp(x) for x in args]
#     type_ = type(args_[0])
#     return _ElementToFroidurePin[type_](args_)
