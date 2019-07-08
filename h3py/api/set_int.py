import h3py.hexmem as hexmem
from h3py.api._api_template import api_functions


# todo: add validation (just do it in `_in_scalar()`?)
# todo: how to write documentation once and have it carry over to each interface?


def _in_scalar(h):
    "Input formatter for this module."
    # todo: validation here?
    return h

def _out_scalar(h):
    "Output formatter for this module."
    return h

def _in_collection(hexes):
    return hexmem.from_ints(hexes)

def _out_collection(hm):
    "Output formatter for this module."
    return set(_out_scalar(h) for h in hm.memview())


funcs = api_functions(
    _in_scalar,
    _out_scalar,
    _in_collection,
    _out_collection,
)

globals().update(funcs)

