from h3.api._api_template import _api_functions
import numpy as np


def _id(x):
    return x


_funcs = _api_functions(
    _in_scalar = _id,
    _out_scalar = _id,
    _in_collection = _id,
    _out_unordered = np.asarray,
    _out_ordered = np.asarray,
)

globals().update(_funcs)
