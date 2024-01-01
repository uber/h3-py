def _in_scalar(x):
    return x


def _out_scalar(x):
    return x


def _in_collection(x):
    import numpy as np
    # array is copied only if dtype does not match
    # `list`s should work, but not `set`s of integers
    return np.asarray(x, dtype='uint64')


def _out_unordered(x):
    import numpy as np
    return np.asarray(x)


_out_ordered = _out_unordered
