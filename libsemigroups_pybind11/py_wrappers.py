# -*- coding: utf-8 -*-

# Copyright (c) 2024 J. D. Mitchell
#
# Distributed under the terms of the GPL license version 3.
#
# The full license is in the file LICENSE, distributed with this software.

# pylint: disable=no-member, protected-access

"""
This package provides some functions and a class CppObjWrapper to help wrap
multiple C++ types into a single python type. See:

    * action.py
    * adapters.py
    * transf.py

for examples.
"""

import abc
from functools import partial, partialmethod
from typing import Any, Union

from typing_extensions import Self

from _libsemigroups_pybind11 import UNDEFINED as _UNDEFINED


def to_cpp(x: Any) -> Any:
    """
    This function returns x._cpp_obj if x is a CppObjWrapper, and x o/w.
    """
    if isinstance(x, CppObjWrapper):
        return x._cpp_obj
    return x


def to_py(Element: Any, x: Any, *args) -> Any:  # pylint: disable=invalid-name
    """
    This function returns Element(x) if x is not None and type(x) != Element, and x o/w.
    """
    if x is not None and not isinstance(x, Element):
        return Element(x, *args)
    return x


class CppObjWrapper:
    # pylint: disable=missing-class-docstring
    # pylint: disable=protected-access, no-member, too-few-public-methods

    def __getattr__(self: Self, meth_name: str):
        # if hasattr(self, "_init_cpp_obj"):
        #     self._init_cpp_obj()

        def cxx_fn_wrapper(*args) -> Any:
            if len(args) == 1 and isinstance(args[0], list):
                args = args[0]
                return getattr(self._cpp_obj, meth_name)([to_cpp(x) for x in args])
            return getattr(self._cpp_obj, meth_name)(*(to_cpp(x) for x in args))

        return cxx_fn_wrapper

    @property
    def _lookup(self: Self) -> dict:
        return self.__class__.__lookup

    def __repr__(self: Self) -> str:
        if self._cpp_obj is not None:
            return self._cpp_obj.__repr__()
        return ""

    def _cpp_obj_type_from(self: Self, samples=(), types=()) -> Any:
        py_types = tuple([type(x) for x in samples] + list(types))
        lookup = self._lookup
        if py_types not in lookup:
            raise ValueError(
                f"unexpected keyword argument combination {py_types}, "
                f"expected one of {tuple(lookup.keys())}"
            )
        if not isinstance(lookup[py_types], dict):
            return lookup[py_types]
        lookup = lookup[py_types]
        cpp_types = tuple([type(to_cpp(x)) for x in samples] + list(types))
        if cpp_types not in lookup:
            raise ValueError(
                f"unexpected keyword argument combination {cpp_types}, "
                f"expected one of {lookup.keys()}"
            )
        return lookup[cpp_types]

    def __init__(self: Self, expected_kwargs, **kwargs):
        # pylint: disable=invalid-name
        if len(kwargs) != len(expected_kwargs):
            raise TypeError(
                f"expected {len(expected_kwargs)} keyword arguments,"
                f" found {len(kwargs)}"
            )
        for kwarg in expected_kwargs:
            if kwarg not in kwargs:
                raise ValueError(
                    f'required keyword argument "{kwarg}" not found, '
                    f"found {kwargs} instead"
                )
        # the next line ensures we get the values in the same order as in
        # lookup
        values = tuple(kwargs[x] for x in expected_kwargs)
        lookup = self._lookup
        if values in lookup:
            for key, val in kwargs.items():
                setattr(self, key, val)
            self._cpp_obj = None
            # return

        # TODO really comment this out?
        # raise ValueError(
        #     f"unexpected keyword argument combination {kwargs.values()}, "
        #     f"expected one of {lookup.keys()}"
        # )


# Decorators


def may_return_undefined(func):
    """
    This function is a decorator for functions/methods that might return
    UNDEFINED (as an integer, since there's no other option in C++), and which
    should return the UNDEFINED object.
    """

    def wrapper(*args):
        result = func(*args)
        if result in (4294967295, 18446744073709551615):
            return _UNDEFINED
        return result

    return wrapper
