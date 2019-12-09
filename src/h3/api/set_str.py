from ._api_template import _api_functions
from .. import _internal_api as _a


# `set` isn't the best name here, as we might return a list if the output is ordered
# perhaps we just want to distinguish between standard python collections,
# numpy arrays, and memoryviews?

# todo: how to write documentation once and have it carry over to each interface?


def _in_collection(hexes):
    it = [_a.hex2int(h) for h in hexes]

    return _a.from_iter(it)


def _out_unordered(mv):
    return set(_a.int2hex(h) for h in mv)


def _out_ordered(mv):
    return list(_a.int2hex(h) for h in mv)


_api_functions(
    _in_scalar = _a.hex2int,
    _out_scalar = _a.int2hex,
    _in_collection = _in_collection,
    _out_unordered = _out_unordered,
    _out_ordered = _out_ordered,
    _globals = globals(),
)
