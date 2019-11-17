from h3.api._api_template import _api_functions
from h3.util import hex2int, int2hex, from_iter


# `set` isn't the best name here, as we might return a list if the output is ordered
# perhaps we just want to distinguish between standard python collections,
# numpy arrays, and memoryviews?

# todo: how to write documentation once and have it carry over to each interface?


def _in_collection(hexes):
    it = [hex2int(h) for h in hexes]

    return from_iter(it)


def _out_unordered(mv):
    return set(int2hex(h) for h in mv)


def _out_ordered(mv):
    return list(int2hex(h) for h in mv)


_funcs = _api_functions(
    _in_scalar = hex2int,
    _out_scalar = int2hex,
    _in_collection = _in_collection,
    _out_unordered = _out_unordered,
    _out_ordered = _out_ordered,
)

# todo: not sure if this is the best way to do this...
# if too weird, we can always fall back to just cut-and-pasting the contents
# of the `_api_functions` body. However, that isn't very DRY.
# Something like a python #include macro would be nice here...
globals().update(_funcs)

# todo: would just using `exec()` be simpler?

# todo: or should we create multiple copies of the base module,
# and monkey patch the input/output functions?
