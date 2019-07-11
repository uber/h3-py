from h3py.hexmem import hex2int, int2hex, from_iter
from h3py.api._api_template import api_functions

import h3py.h3core as h3core


# todo: add validation (just do it in `_in_scalar()`?)
# todo: how to write documentation once and have it carry over to each interface?

def _in_collection(hexes):
    it = [hex2int(h) for h in hexes]

    return from_iter(it)

def _out_collection(mv):
    return set(int2hex(h) for h in mv)


funcs = api_functions(
    _in_scalar = hex2int,
    _out_scalar = int2hex,
    _in_collection = _in_collection,
    _out_collection = _out_collection,
    _validate=True,
)

# todo: not sure if this is the best way to do this...
# if too weird, we can always fall back to just cut-and-pasting the contents
# of the `api_functions` body. However, that isn't very DRY.
# Something like a python #include macro would be nice here...
globals().update(funcs)

# todo: would just using `exec()` be simpler?

# todo: or should we create multiple copies of the base module,
# and monkey patch the input/output functions?
