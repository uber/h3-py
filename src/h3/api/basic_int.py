"""
This API handles H3 Indexes of type `int`, using
basic Python collections (`set`, `list`, `tuple`).
`h3` will interpret these Indexes as unsigned 64-bit integers.

Input collections:

- `Iterable[int]`

Output collections:

- `Set[int]` for unordered
- `List[int]` for ordered
"""

from typing import Set

from .. import _cy
from ._api_template import _API_FUNCTIONS
from ._util import _update_globals


def _id(x):
    return x


def _in_collection(hexes):
    it = list(hexes)

    return _cy.from_iter(it)


basic_int = _API_FUNCTIONS[int, Set[int]](
    _in_scalar=_id,
    _out_scalar=_id,
    _in_collection=_in_collection,
    _out_unordered=set,  # todo: should this be an (immutable) frozenset?
    _out_ordered=list,  # todo: should this be an (immutable) tuple?
)

_update_globals(basic_int, globals())
