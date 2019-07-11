import numpy as np

import h3py.hexmem as hexmem
from h3py.api._api_template import api_functions


def _in_addr(h):
    return h

def _in_edge(e):
    return e

def _in_scalar(h):
    "Input formatter for this module."
    return h

def _out_scalar(h):
    "Output formatter for this module."
    return h

def _in_collection(mv):
    """ Expect input collections to be a numpy array (or at least a memoryview)
    """
    return mv

def _out_collection(mv):
    """ np.asarray should re-use the memory from the memoryview object mv
    """
    return np.asarray(mv)


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


