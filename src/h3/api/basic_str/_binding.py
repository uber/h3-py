"""
This API handles H3 Indexes of type `str`, using
basic Python collections (`set`, `list`, `tuple`).
`h3` will interpret these Indexes as hexadecimal
representations of unsigned 64-bit integers.

Input collections:

- `Iterable[str]`

Output collections:

- `Set[str]` for unordered
- `List[str]` for ordered
"""

from ... import _cy
from .._api_template import _API_FUNCTIONS


def _in_collection(cells):
    it = [_cy.str_to_int(h) for h in cells]

    return _cy.iter_to_mv(it)


def _out_unordered(mv):
    # todo: should this be an (immutable) frozenset?
    return set(_cy.int_to_str(h) for h in mv)


def _out_ordered(mv):
    # todo: should this be an (immutable) tuple?
    return list(_cy.int_to_str(h) for h in mv)


_binding = _API_FUNCTIONS(
    _in_scalar = _cy.str_to_int,
    _out_scalar = _cy.int_to_str,
    _in_collection = _in_collection,
    _out_unordered = _out_unordered,
    _out_ordered = _out_ordered,
)
