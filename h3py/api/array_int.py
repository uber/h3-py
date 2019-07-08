# can start as a .py file, but when we make it no-copy, it'll probably have to be Cython
import numpy as np

import h3py.hexmem as hexmem
from h3py.api._api_template import api_functions

def _in_scalar(h):
    "Input formatter for this module."
    return h

def _out_scalar(h):
    "Output formatter for this module."
    return h

def _in_collection(hexes):
    # todo: this one is trickier...
    pass

def _out_collection(hm):
    """ Since this isn't compiled, we just make a copy instead of
    re-using the C memory. (for now)
    """
    return np.array(hm.memview())


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


