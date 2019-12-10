from ._api_template import _api_functions
from .. import _cy


# `set` isn't the best name here, as we might return a list if the output is ordered
# perhaps we just want to distinguish between standard python collections,
# numpy arrays, and memoryviews?

# todo: how to write documentation once and have it carry over to each interface?


def _in_collection(hexes):
    it = [_cy.hex2int(h) for h in hexes]

    return _cy.from_iter(it)


def _out_unordered(mv):
    return set(_cy.int2hex(h) for h in mv)


def _out_ordered(mv):
    return list(_cy.int2hex(h) for h in mv)


_api_functions(
    _in_scalar = _cy.hex2int,
    _out_scalar = _cy.int2hex,
    _in_collection = _in_collection,
    _out_unordered = _out_unordered,
    _out_ordered = _out_ordered,
    _globals = globals(),
)
