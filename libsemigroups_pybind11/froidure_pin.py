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

from .transf import Transf, PPerm, Perm

from _libsemigroups_pybind11 import (
    FroidurePinBase,
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
    product_by_reduction,
)

Element = TypeVar("Element")


class FroidurePin(CppObjWrapper):
    __doc__ = _FroidurePinPBR.__doc__

    # TODO put this in a function call, to avoid the underscores etc
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

    def __init__(self: Self, *args) -> None:
        if len(args) == 0:
            raise ValueError("expected at least 1 argument, found 0")
        if isinstance(args[0], list) and len(args) == 1:
            gens = args[0]
        else:
            gens = args
        cpp_obj_t = self._cpp_obj_type_from(
            samples=(to_cpp(gens[0]),),
        )
        self.Element = type(gens[0])
        self._cpp_obj = cpp_obj_t([to_cpp(x) for x in gens])
        self._degree = gens[0].degree()

    @returns_element
    def __getitem__(self: Self, i: int) -> Element:
        return self.cpp_call_mem_fn("__getitem__", i)

    def __iter__(self: Self) -> Iterator:
        if self.Element in (Transf, PPerm, Perm):
            return map(
                lambda x: to_py(self.Element, x, self.degree()),
                self.cpp_call_mem_fn("__iter__"),
            )
        return map(
            lambda x: to_py(self.Element, x),
            self.cpp_call_mem_fn("__iter__"),
        )

    def degree(self: Self) -> int:
        return self._degree

    @returns_element
    def generator(self: Self, i: int) -> Element:
        return self.cpp_call_mem_fn("generator", i)

    @may_return_undefined
    def current_position(self: Self, x: Element | List[int]) -> int:
        return self.cpp_call_mem_fn("current_position", x)

    def idempotents(self: Self) -> Iterator:
        return map(
            lambda x: to_py(self.Element, x, self.degree()),
            self.cpp_call_mem_fn("idempotents"),
        )

    @may_return_undefined
    def position(self: Self, x: Element | List[int]) -> int:
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


# Methods from FroidurePin itself
pass_thru_methods(
    FroidurePin,
    "add_generator",
    "add_generators",
    "closure",
    "contains",
    "copy_add_generators",
    "copy_closure",
    "copy",
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
    "sorted_position",
    "to_sorted_position",
)

# Methods from FroidurePinBase itself
pass_thru_methods(
    FroidurePin,
    "batch_size",
    "current_left_cayley_graph",
    "current_length",
    "current_max_word_length",
    "current_minimal_factorisation",
    "current_normal_forms",
    "current_number_of_rules",
    "current_right_cayley_graph",
    "current_rules",
    "current_size",
    "enumerate",
    "final_letter",
    "first_letter",
    "is_monoid",
    "left_cayley_graph",
    "length",
    "normal_forms",
    "number_of_elements_of_length",
    "number_of_rules",
    "prefix",
    "right_cayley_graph",
    "rules",
    "size",
    "suffix",
)

# Methods from Runner
pass_thru_methods(
    FroidurePin,
    "current_state",
    "dead",
    "finished",
    "kill",
    "run",
    "run_for",
    "run_until",
    "running",
    "running_for",
    "running_until",
    "started",
    "state",
    "stopped",
    "stopped_by_predicate",
    "timed_out",
)
