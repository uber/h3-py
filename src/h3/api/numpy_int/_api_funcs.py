import numpy as np


def _id(x):
    return x


def _in_collection(x):
    # array is copied only if dtype does not match
    # `list`s should work, but not `set`s of integers
    return np.asarray(x, dtype='uint64')


_in_scalar = _id
_out_scalar = _id
_in_collection = _in_collection
_out_unordered = np.asarray
_out_ordered = np.asarray
