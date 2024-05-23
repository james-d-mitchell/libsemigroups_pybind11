
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

// C++ stl headers....
#include <string>  // for basic_string, string

// libsemigroups headers
#include <libsemigroups/action.hpp>
#include <libsemigroups/bmat8.hpp>
#include <libsemigroups/transf.hpp>
#include <libsemigroups/word-graph.hpp>

#include <fmt/core.h>  // for format, print

// pybind11....
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

// libsemigroups_pybind11....
#include "main.hpp"  // for init_TODO

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
      py::class_<Action_, Runner> thing(m, name.c_str());
      // The Action_ class doc is in action.rst

      thing.def("__repr__", &detail::to_string<Action_ const&>);
      thing.def(py::init<>(), R"pbdoc(
Default constructor. A constructor that creates an uninitialized
action representing a left or right action.

:complexity:
   Constant.
)pbdoc");
      thing.def(py::init<Action_ const&>(), R"pbdoc(
Default copy constructor.
)pbdoc");
      thing.def("init",
                &Action_::init,
                R"pbdoc(
Initialize an existing object. This function puts an action
object back into the same state as if it had been newly default
constructed.

:returns: ``self``.
:rtype: Action
)pbdoc");
      thing.def("reserve",
                &Action_::reserve,
                py::arg("val"),
                R"pbdoc(
Increase the capacity to a value that is greater or equal to ``val``.

:param val: new capacity of an action instance.
:type val: int

:raises ValueError:  if ``val`` is too large.

:complexity: At most linear in the :any:`size()` of the ``Action``.

:returns: ``self``.
:rtype: Action
)pbdoc");
      thing.def("add_seed",
                &Action_::add_seed,
                py::arg("seed"),
                R"pbdoc(
Add a seed to the action.

A *seed* is just a starting point for the action, it will belong to the action, as will every point that can be obtained from the seed by acting with the generators of the action.

:param seed: the seed to add.
:type seed: Point

:complexity: Constant.

:returns: ``self``
:rtype: Action
)pbdoc");
      thing.def("add_generator",
                &Action_::add_generator,
                py::arg("gen"),
                R"pbdoc(
Add a generator to the action.

An ``Action`` instance represents the action of the semigroup generated by the elements added via this member function.

:param gen: the generator to add.
:type gen: Element

:complexity: Constant.

:returns: ``self``.
:rtype: Action
)pbdoc");
      thing.def("number_of_generators",
                &Action_::number_of_generators,
                R"pbdoc(
Returns the number of generators.

:complexity:
   Constant.

:returns:
   The number of generators.

:rtype:
   int
)pbdoc");
      thing.def("generators",
                &Action_::generators,
                R"pbdoc(
Returns the list of generators.

:complexity:
   Constant.

:returns:
   The generators.

:rtype:
   list[Element]
)pbdoc");
      thing.def("position",
                &Action_::position,
                py::arg("pt"),
                R"pbdoc(
Returns the position of a point in the so far discovered points.

:param pt: the point whose position is sought.
:type pt: Point

:complexity: Constant.

:returns: The index of ``pt`` in ``self`` or :any:`UNDEFINED`.
:rtype: int
)pbdoc");
      thing.def("empty",
                &Action_::empty,
                R"pbdoc(
Checks if the Action contains any points.

:complexity:
   Constant.

:returns:
   ``True`` if the action contains no points (including seeds), and
   ``False`` if not.

:rtype:
   bool
)pbdoc");
      thing.def("__getitem__",
                &Action_::at,
                py::is_operator(),
                py::arg("pos"),
                R"pbdoc(
Returns the point in a given position.

:param pos:
   the index of an point.

:type pos:
  int

:raises IndexError:
   if ``pos >= current_size())``.

:complexity:
   Constant.

:returns:
   The *Point* in position ``pos`` of the currently enumerated points.

:rtype:
   *Point*
)pbdoc");
      thing.def("size",
                &Action_::size,
                R"pbdoc(
Returns the size of the fully enumerated action.

:complexity:
   The time complexity is :math:`O(mn)` where :math:`m` is the total
   number of points in the orbit and :math:`n` is the number of
   generators.

:returns:
   The size of the action, a value of type ``int``.

:rtype:
   int
)pbdoc");
      thing.def("current_size",
                &Action_::current_size,
                R"pbdoc(
Returns the number of points found so far.

:complexity:
   Constant.

:returns:
   The current size.

:rtype:
   int
)pbdoc");
      thing.def(
          "iterator",
          [](Action_ const& self) {
            return py::make_iterator(self.cbegin(), self.cend());
          },
          R"pbdoc(
Returns an iterator containing the so far enumerated points in the orbit (if any).
No enumeration is triggered by calling this function.

:complexity:
   Constant.

:returns:
   An ``Iterator``.

:rtype:
   Iterator
)pbdoc");
      thing.def(
          "cache_scc_multipliers",
          [](Action_ const& self) { return self.cache_scc_multipliers(); },
          R"pbdoc(
Returns whether or not we are caching scc multipliers. If the returned
value of this function is ``True`` , then the values returned by
:any:`multiplier_from_scc_root()` and :any:`multiplier_to_scc_root()`
are cached, and not recomputed every time one of these functions is
called.

:complexity:
   Constant.

:returns:
   ``True`` if caching is enabled, and ``False`` if not.

:rtype:
   bool
)pbdoc");
      thing.def(
          "cache_scc_multipliers",
          [](Action_& self, bool val) {
            return self.cache_scc_multipliers(val);
          },
          py::arg("val"),
          R"pbdoc(
Set whether or not to cache scc multipliers.

If the parameter **val** is ``True`` , then the values returned by :any:`multiplier_from_scc_root()` and :any:`multiplier_to_scc_root()` are cached, and not recomputed every time one of these functions is called.

:param val: the value.
:type val: bool

:complexity: Constant.

:returns: ``self``.

:rtype: Action
)pbdoc");
      thing.def("multiplier_from_scc_root",
                &Action_::multiplier_from_scc_root,
                py::arg("pos"),
                R"pbdoc(
Returns a multiplier from a scc root to a given index.

Returns an element ``x`` of the semigroup generated by the generators in the action such that if ``r`` is the root of the strongly connected component containing ``at(pos)``, then calling ``Func(res, r, x)`` the point ``res`` equals ``at(pos)``.

:param pos: a position in the action.
:type pos: int

:complexity: At most :math:`O(mn)` where :math:`m` is the complexity of multiplying elements of type *Element* and :math:`n` is the size of the fully enumerated orbit.

:raises LibsemigroupsError:  if there are no generators yet added or the index ``pos`` is out of range.

:returns: The multiplier.
:rtype: *Element*
)pbdoc");
      thing.def("multiplier_to_scc_root",
                &Action_::multiplier_to_scc_root,
                py::arg("pos"),
                R"pbdoc(
Returns a multiplier from a given index to a scc root.

Returns an element ``x`` of the semigroup generated by the generators in the action such that after ``Func(res, at(pos), x)`` the point ``res`` is the root of the strongly connected component containing ``at(pos)``.

:param pos: a position in the action.
:type pos: int

:complexity: At most :math:`O(mn)` where :math:`m` is the complexity of multiplying elements of type *Element* and :math:`n` is the size of the fully enumerated orbit.

:raises LibsemigroupsError:  if there are no generators yet added or the index ``pos`` is out of range.

:returns: The multiplier.
:rtype: *Element*
)pbdoc");
      thing.def(
          "root_of_scc",
          [](Action_& self, const_reference_point_type x) {
            return self.root_of_scc(x);
          },
          py::arg("x"),
          R"pbdoc(
Returns the root point of a strongly connected component containing an *Point*.

:param x: the point whose root we want to find.
:type x: Point

:complexity: At most :math:`O(mn)` where :math:`m` is the complexity of multiplying elements of type *Element* and :math:`n` is the size of the fully enumerated orbit.

:raises LibsemigroupsError:  if the point ``x`` does not belong to the action.

:returns: The root point.
:rtype: *Point*
)pbdoc");
      thing.def(
          "root_of_scc",
          [](Action_& self, index_type pos) { return self.root_of_scc(pos); },
          py::arg("pos"),
          R"pbdoc(
Returns the root point of a strongly connected component.

:param pos: the index of the point in the action whose root we want to find.
:type pos: int

:complexity: At most :math:`O(mn)` where :math:`m` is the complexity of multiplying elements of type *Element* and :math:`n` is the size of the fully enumerated orbit.

:raises LibsemigroupsError:  if the index ``pos`` is out of range.

:returns: The root point.
:rtype: *Point*
)pbdoc");
      thing.def("word_graph",
                &Action_::word_graph,
                R"pbdoc(
Returns the word graph of the completely enumerated action.

:complexity:
   At most :math:`O(mn)` where :math:`m` is the complexity of
   multiplying elements of type *Element* and :math:`n` is the
   size of the fully enumerated orbit.

:returns:
   The word graph of the action.
:rtype:
   WordGraph
)pbdoc");
      thing.def("scc",
                &Action_::scc,
                R"pbdoc(
Returns a Gabow object for strongly connected components.

:complexity:
   At most :math:`O(mn)` where :math:`m` is the complexity of
   multiplying elements of type *Element* and :math:`n` is the
   size of the fully enumerated orbit.

:returns:
   A :any:`Gabow` object.
:rtype:
   Gabow
)pbdoc");
    }  // bind_action
  }    // namespace
  void init_action(py::module& m) {
    py::enum_<side>(m, "side", R"pbdoc(
This value indicates that the action in an :any:`Action` instance should
be a left action.
)pbdoc")
        .value("left", side::left, R"pbdoc(
This value indicates that the action in an :any:`Action` instance should
be a left action.
)pbdoc")
        .value("right", side::right, R"pbdoc(
This value indicates that the action in an :any:`Action` instance should
be a right action.
)pbdoc");

    // One call to bind is required per list of types
    bind_action<BMat8,
                BMat8,
                ImageRightAction<BMat8, BMat8>,
                ActionTraits<BMat8, BMat8>,
                side::right>(m, "RowActionBMat8");
    bind_action<BMat8,
                BMat8,
                ImageLeftAction<BMat8, BMat8>,
                ActionTraits<BMat8, BMat8>,
                side::left>(m, "ColActionBMat8");

    bind_action<PPerm<16>,
                PPerm<16>,
                ImageRightAction<PPerm<16>, PPerm<16>>,
                ActionTraits<PPerm<16>, PPerm<16>>,
                side::right>(m, "RightActionPPerm16PPerm16");
    bind_action<PPerm<16>,
                PPerm<16>,
                ImageLeftAction<PPerm<16>, PPerm<16>>,
                ActionTraits<PPerm<16>, PPerm<16>>,
                side::left>(m, "LeftActionPPerm16PPerm16");
  }

}  // namespace libsemigroups
