# -*- coding: utf-8 -*-

# Copyright (c) 2021-2022, J. D. Mitchell
#
# Distributed under the terms of the GPL license version 3.
#
# The full license is in the file LICENSE, distributed with this software.

# pylint: disable=no-name-in-module

"""
This package provides the user-facing python part of libsemigroups_pybind11
"""

from _libsemigroups_pybind11 import (
    NEGATIVE_INFINITY,
    POSITIVE_INFINITY,
    UNDEFINED,
    Forest,
    Gabow,
    Paths,
    Strings,
    ToWord,
    WordGraph,
    Words,
    algorithm,
    number_of_words,
    order,
    ReportGuard,
    parse_relations,
    random_word,
    to_word,
    to_string,
    congruence_kind,
    overlap,
)


from .transf import PPerm, Transf
from .presentation import Presentation, redundant_rule

# from .knuth_bendix import KnuthBendix


"""
from .froidure_pin import FroidurePin
from .konieczny import Konieczny
from .matrix import Matrix, MatrixKind, make_identity
from .tools import compare_version_numbers, libsemigroups_version
from .transf import PPerm, Transf
"""
