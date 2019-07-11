import h3py.hexmem as hexmem
from h3py.api._api_template import api_functions


# todo: add validation (just do it in `_in_scalar()`?)
# todo: how to write documentation once and have it carry over to each interface?


def _in_addr(h):
    "Input formatter for this module."
    if not h3core.is_valid(h):
        raise ValueError('Invalid H3 address: {}'.format(h))

    return h

def _in_edge(e):
    if not h3core.is_uni_edge(e):
        raise ValueError('Invalid H3 edge: {}'.format(e))

    return e

def _out_scalar(h):
    "Output formatter for this module."
    return h

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

globals().update(funcs)

