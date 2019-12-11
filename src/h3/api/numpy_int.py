from ._api_template import _api_functions
import numpy as np

"""
This API handles H3 Indexes of type `int` (specifically, `uint64`),
using `numpy.array` objects for collections.
H3 will interpret these Indexes as unsigned 64-bit integers.

This API is **optional**, and will only work if the
user has `numpy` installed.

Input collections:

- `memoryview[uint64]`

Output collections:

- `np.ndarray[np.uint64]` for unordered
- `np.ndarray[np.uint64]` for ordered
"""


def _id(x):
    return x


_api_functions(
    _in_scalar = _id,
    _out_scalar = _id,
    _in_collection = _id,
    _out_unordered = np.asarray,
    _out_ordered = np.asarray,
    _globals = globals(),
)
