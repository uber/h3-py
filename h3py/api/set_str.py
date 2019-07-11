import h3py.hexmem as hexmem
from h3py.api._api_template import api_functions

import h3py.h3core as h3core


# todo: add validation (just do it in `_in_scalar()`?)
# todo: how to write documentation once and have it carry over to each interface?


def _in_addr(h):
    "Input formatter for this module."
    h2 = hexmem.hex2int(h) # todo: what if it fails on the conversion?
    if not h3core.is_valid(h2):
        raise ValueError('Invalid H3 address: {}'.format(h))

    return h2

def _in_edge(e):
    e2 = hexmem.hex2int(e)
    if not h3core.is_uni_edge(e2):
        raise ValueError('Invalid H3 edge: {}'.format(e))

    return e2

def _out_scalar(h):
    "Output formatter for this module."
    return hexmem.int2hex(h)

def _in_collection(hexes):
    it = [_in_addr(h) for h in hexes]

    return hexmem.from_iter(it)

def _out_collection(mv):
    "Output formatter for this module."
    return set(_out_scalar(h) for h in mv)


funcs = api_functions(
    _in_addr,
    _in_edge,
    _out_scalar,
    _in_collection,
    _out_collection,
)

# todo: not sure if this is the best way to do this...
# if too weird, we can always fall back to just cut-and-pasting the contents
# of the `api_functions` body. However, that isn't very DRY.
# Something like a python #include macro would be nice here...
globals().update(funcs)

# todo: would just using `exec()` be simpler?

# todo: or should we create multiple copies of the base module,
# and monkey patch the input/output functions?
