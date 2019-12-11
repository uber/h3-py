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

from ._api_template import _api_functions
from .. import _cy


def _in_collection(hexes):
    it = [_cy.hex2int(h) for h in hexes]

    return _cy.from_iter(it)


def _out_unordered(mv):
    # todo: should this be an (immutable) frozenset?
    return set(_cy.int2hex(h) for h in mv)


def _out_ordered(mv):
    # todo: should this be an (immutable) tuple?
    return list(_cy.int2hex(h) for h in mv)


_api_functions(
    _in_scalar = _cy.hex2int,
    _out_scalar = _cy.int2hex,
    _in_collection = _in_collection,
    _out_unordered = _out_unordered,
    _out_ordered = _out_ordered,
    _globals = globals(),
)
