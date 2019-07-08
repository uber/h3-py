import h3py.hexmem as hexmem
from h3py.api._api_template import api_functions


# todo: add validation (just do it in `_in_scalar()`?)
# todo: how to write documentation once and have it carry over to each interface?


def _in_scalar(h):
    "Input formatter for this module."
    # todo: validation here?
    return hexmem.hex2int(h)

def _out_scalar(h):
    "Output formatter for this module."
    return hexmem.int2hex(h)

def _in_collection(hexes):
    return hexmem.from_strs(hexes)

def _out_collection(hm):
    "Output formatter for this module."
    return set(_out_scalar(h) for h in hm.memview())


funcs = api_functions(
    _in_scalar,
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
