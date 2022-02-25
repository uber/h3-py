# flake8: noqa

from . import basic_int
from . import basic_str
from . import memview_int


"""
Module to DRY-up code which is repeated across API modules.

Definitions of types
--------------------
H3Index:
    An unsigned 64-bit integer representing a valid H3 cell or
    unidirectional edge.
    Depending on the API, an H3Index may be represented as an
    unsigned integer type, or as a hexadecimal string.

H3 cell:
    A pentagon or hexagon that can be represented by an H3Index.

H3Cell:
    H3Index representation of an H3 cell.

H3Edge:
    H3Index representation of an H3 unidirectional edge.


Definitions of collections
--------------------------
Collection types vary between APIs. We'll use the following terms:

unordered collection:
    Inputs and outputs are interpreted as *unordered* collections.
    Examples: `set`, `numpy.ndarray`.

ordered collection:
    Inputs and outputs are interpreted as *ordered* collections.
    Examples: `list`, `numpy.ndarray`.

Notes
-----
Not sure if this function closure is the best solution.
There doesn't seem to be any obvious best-practice for
programmatically/dynamically creating modules.

Another approach: we could also just use `exec()`

todo: how do we lint these functions and docstrings? it seems to currently
be skipped due to it being inside the `_api_functions` function.
"""
