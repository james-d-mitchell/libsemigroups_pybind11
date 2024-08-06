# -*- coding: utf-8 -*-

# Copyright (c) 2024, Joseph Edwards
#
# Distributed under the terms of the GPL license version 3.
#
# The full license is in the file LICENSE, distributed with this software.
# pylint:disable=no-name-in-module, unused-import
"""
This module contains various helper functions for the class :any:`AhoCorasick`.
These functions could be functions of :any:`AhoCorasick` but they only use
public member functions of :any:`AhoCorasick`, and so they are declared
as free functions instead.
"""
from _libsemigroups_pybind11 import (
    add_word,
    rm_word,
    traverse_word,
    aho_corasick_dot as dot,
)
