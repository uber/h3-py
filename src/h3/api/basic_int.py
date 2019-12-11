from ._api_template import _api_functions
from .. import _cy

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


def _id(x):
    return x


def _in_collection(hexes):
    it = list(hexes)

    return _cy.from_iter(it)


_api_functions(
    _in_scalar = _id,
    _out_scalar = _id,
    _in_collection = _in_collection,
    _out_unordered = set,
    _out_ordered = list,
    _globals = globals(),
)
