from h3py.api._api_template import _api_functions
import numpy as np


def _id(x):
    return x


_funcs = _api_functions(
    _in_scalar = _id,
    _out_scalar = _id,
    _in_collection = _id,
    _out_collection = np.asarray,
)

# todo: not sure if this is the best way to do this...
# if too weird, we can always fall back to just cut-and-pasting the contents
# of the `_api_functions` body. However, that isn't very DRY.
# Something like a python #include macro would be nice here...
globals().update(_funcs)
