
//
// libsemigroups_pybind11
// Copyright (C) 2024 James D. Mitchell
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//

// C std headers....
// action complete or delete

// C++ stl headers....
// action complete or delete

// libsemigroups headers
#include <libsemigroups/action.hpp>
#include <libsemigroups/bmat8.hpp>
// action complete or delete

// pybind11....
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
// action complete or delete

// libsemigroups_pybind11....
#include "main.hpp"  // for init_action

namespace py = pybind11;

namespace libsemigroups {

  namespace {
    template <typename Element,
              typename Point,
              typename Func,
              typename Traits,
              side LeftOrRight>
    void bind_action(py::module& m, std::string const& name) {
      using Action_ = Action<Element, Point, Func, Traits, LeftOrRight>;
      using const_reference_point_type =
          typename Action_::const_reference_point_type;
      using index_type = typename Action_::index_type;

      py::class_<Action_, Runner>(m, name.c_str())
          .def(py::init<>())
          .def(py::init<Action_ const&>(), R"pbdoc(TODO)pbdoc")
          .def("__getitem__", &Action_::at, py::is_operator())
          .def("__repr__", &detail::to_string<Action_ const&>)
          .def("init",
               &Action_::init,
               R"pbdoc(
Initialize an existing :any:`RowActionBMat8` object.

This function puts a :any:`RowActionBMat8` object back into the same state as if
it had been newly default constructed.

:returns: ``self``.
:rtype: RowActionBMat8
)pbdoc")
          .def("reserve",
               &Action_::reserve,
               py::arg("val"),
               R"pbdoc(
Increase the capacity to a value that is greater or equal to val.

:param val: new capacity of an action instance.
:type val: int

:raises ValueError:
    if ``val`` is too large.

:raises MemoryError:
    if the action grows too large.

:complexity:
    At most linear in the :any:`size()`  of the :any:`RowActionBMat8` .

:returns: ``self``.
:rtype: RowActionBMat8
)pbdoc")
          .def("add_seed",
               &Action_::add_seed,
               py::arg("seed"),
               R"pbdoc(
Add a seed to the action.

A *seed* is just a starting point for the action, it will belong to the action,
as will every point that can be obtained from the seed by acting with the
generators of the action.

:param seed: the seed to add.
:type seed: a point

:complexity:
    At most linear in the :any:`size()`  of the action.

:returns: ``self``
:rtype: RowActionBMat8
)pbdoc")
          .def("add_generator",
               &Action_::add_generator,
               py::arg("gen"),
               R"pbdoc(
Add a generator to the action.

An :any:`RowActionBMat8`  instance represents the action of the semigroup generated by
the elements added via this member function.

:param gen: the generator to add.
:type gen: an element

:complexity:
   At most linear in the :any:`size()`  of the action.

:returns: ``self``
:rtype: RowActionBMat8
)pbdoc")
          .def("position",
               &Action_::position,
               py::arg("pt"),
               R"pbdoc(
Returns the position of a point in the so far discovered points.

:param pt: the point whose position is sought.
:type pt: a point

:complexity:
  Constant.

:returns:
  The index of ``pt`` in ``self`` or :any:`UNDEFINED`.
:rtype: int
)pbdoc")
          .def("empty",
               &Action_::empty,
               R"pbdoc(
Checks if the RowActionBMat8 contains any points.

:complexity: Constant.

:returns:
 ``True`` if the action contains no points (including seeds), and ``False`` if not.
:rtype: bool
)pbdoc")
          .def("at",
               &Action_::at,
               py::arg("pos"),
               R"pbdoc(
Returns a const reference to the point in a given position.

:param pos: the index of an element.
:type pos: int

:raises IndexError: if ``not (pos < current_size())``.

:complexity:
  Constant.

:returns:
  The point in position ``pos`` of the currently enumerated points.
:rtype: A point.
)pbdoc")
          .def("size",
               &Action_::size,
               R"pbdoc(
Returns the size of the fully enumerated action.

:complexity:
  The time complexity is :math:`O(mn)` where :math:`m` is the total number of
  points in the orbit and :math:`n` is the number of generators.

:returns:
  The size of the action.
:rtype: int
)pbdoc")
          .def("current_size",
               &Action_::current_size,
               R"pbdoc(
Returns the number of points found so far.

:complexity:
  Constant.

:returns:
   A value of type ``int``.
:rtype: int
)pbdoc")
          .def(
              "iterator",
              [](Action_ const& self) {
                return py::make_iterator(self.begin(), self.end());
              },
              R"pbdoc(
Returns an iterator to the current points in the action.

:complexity:
  Constant.

:returns:
  A range object.
)pbdoc")
          .def(
              "cache_scc_multipliers",
              [](Action_ const& self) { return self.cache_scc_multipliers(); },
              R"pbdoc(
Returns whether or not we are caching scc multipliers.

If the returned value of this function is ``True`` , then the values returned by
:any:`multiplier_from_scc_root()`  and :any:`multiplier_to_scc_root()`  are
cached, and not recomputed every time one of these functions is called.

:complexity: Constant.

:returns: A value of type ``bool``.
:rtype: bool
)pbdoc")
          .def(
              "cache_scc_multipliers",
              [](Action_& self, bool val) {
                return self.cache_scc_multipliers(val);
              },
              py::arg("val"),
              R"pbdoc(
Set whether or not to cache scc multipliers.

If the parameter ``val`` is ``True`` , then the values returned by
:any:`multiplier_from_scc_root()`  and :any:`multiplier_to_scc_root()`  are
cached, and not recomputed every time one of these functions is called.

:param val: the value.
:type val: bool

:complexity: Constant.

:returns: ``self``.
:rtype: RowActionBMat8
)pbdoc")
          .def("multiplier_from_scc_root",
               &Action_::multiplier_from_scc_root,
               py::arg("pos"),
               R"pbdoc(
Returns a multiplier from a scc root to a given index.

Returns an element ``x`` of the semigroup generated by the generators in the
action such that if ``r`` is the root of the strongly connected component
containing ``at(pos)`` , then after ``Func()(res, r, x)`` the point ``res``
equals ``at(pos)``.

:param pos: a position in the action.
:type pos: int

:complexity:
  At most :math:`O(mn)` where :math:`m` is the complexity of multiplying elements
  and :math:`n` is the size of the fully enumerated orbit.

:raises LibsemigroupsError:
  if there are no generators yet added or the index ``pos`` is out of range.

:returns:
  An element.
)pbdoc")
          .def("multiplier_to_scc_root",
               &Action_::multiplier_to_scc_root,
               py::arg("pos"),
               R"pbdoc(
Returns a multiplier from a given index to a scc root.

Returns an element ``x`` of the semigroup generated by the generators in the
action such that after ``Func()(res, at(pos), x)`` the point ``res`` is the root
of the strongly connected component containing ``at(pos)``.

:param pos: a position in the action.
:type pos: int
:complexity:
  At most :math:`O(mn)` where :math:`m` is the complexity of multiplying elements
  and :math:`n` is the size of the fully enumerated orbit.

:raises LibsemigroupsError:
  if there are no generators yet added or the
  index ``pos`` is out of range.

:returns:
  An element.
)pbdoc")
          .def(
              "root_of_scc",
              [](Action_& self, const_reference_point_type x) {
                return self.root_of_scc(x);
              },
              py::arg("x"),
              R"pbdoc(
Returns a const reference to the root point of a strongly connected component.

:param x: the point whose root we want to find.
:type x: const_reference_point_type

:complexity:
  At most :math:`O(mn)` where :math:`m` is the complexity of multiplying elements
  and :math:`n` is the size of the fully enumerated orbit.

:raises LibsemigroupsError:
    if the point ``x`` does not belong to the action.

:returns: A point in the action.
:rtype: point
)pbdoc")
          .def(
              "root_of_scc",
              [](Action_& self, index_type pos) {
                return self.root_of_scc(pos);
              },
              py::arg("pos"),
              R"pbdoc(
Returns the root point of a strongly connected component.

:param pos: the index of the point in the action whose root we want to find.
:type pos: int

:complexity:
  At most :math:`O(mn)` where :math:`m` is the complexity of multiplying
  elements and :math:`n` is the size of the fully
  enumerated orbit.

:raises LibsemigroupsError:
  if the index ``pos`` is out of range.

:returns:
    The root of the strongly connected component containing the element in
    position ``pos`` of the action.
:rtype: A point.
)pbdoc")
          .def("word_graph",
               &Action_::word_graph,
               R"pbdoc(
Returns the word graph of the completely enumerated action.

:complexity:
  At most :math:`O(mn)` where :math:`m` is the complexity of multiplying elements
  and :math:`n` is the size of the fully enumerated orbit.

:returns:
  A :any:`WordGraph` .
:rtype: WordGraph
)pbdoc")
          .def("scc",
               &Action_::scc,
               R"pbdoc(
Returns a reference to a Gabow object for strongly connected components.

:complexity:
   At most :math:`O(mn)` where :math:`m` is the complexity of
   multiplying elements and :math:`n` is the
   size of the fully enumerated orbit.

:returns: A Gabow object.
:rtype: Gabow)pbdoc");
    }  // bind_action
  }    // namespace
  void init_action(py::module& m) {
    // One call to bind is required per list of types
    bind_action<BMat8,
                BMat8,
                ImageRightAction<BMat8, BMat8>,
                ActionTraits<BMat8, BMat8>,
                side::right>(m, "RowActionBMat8");
  }

}  // namespace libsemigroups
