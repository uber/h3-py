from h3py.api._api_template import _api_functions
from h3py.util import hex2int, int2hex, from_iter

# todo: how to write documentation once and have it carry over to each interface?


def _in_collection(hexes):
    it = [hex2int(h) for h in hexes]

    return from_iter(it)

def _out_collection(mv):
    return set(int2hex(h) for h in mv)


_funcs = _api_functions(
    _in_scalar = hex2int,
    _out_scalar = int2hex,
    _in_collection = _in_collection,
    _out_collection = _out_collection,
)

# todo: not sure if this is the best way to do this...
# if too weird, we can always fall back to just cut-and-pasting the contents
# of the `_api_functions` body. However, that isn't very DRY.
# Something like a python #include macro would be nice here...
globals().update(_funcs)

# todo: would just using `exec()` be simpler?

# todo: or should we create multiple copies of the base module,
# and monkey patch the input/output functions?
