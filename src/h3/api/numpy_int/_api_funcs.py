import numpy as np


def _in_scalar(x):
    return x


def _out_scalar(x):
    return x


def _in_collection(x):
    # array is copied only if dtype does not match
    # `list`s should work, but not `set`s of integers
    return np.asarray(x, dtype='uint64')


_out_unordered = np.asarray
_out_ordered = np.asarray
