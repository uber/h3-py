from libc cimport stdlib
from cython.view cimport array
from .h3lib cimport H3int, H3str, isValidCell, isValidDirectedEdge

cimport h3lib

from .error_system import (
    H3ResDomainError,
    H3DomainError,
    H3DirEdgeInvalidError,
    H3CellInvalidError,
)

from .memory cimport (
    H3MemoryManager,
    empty_memory_view,
    simple_mv,
)


cdef h3lib.LatLng deg2coord(double lat, double lng) nogil:
    cdef:
        h3lib.LatLng c

    c.lat = h3lib.degsToRads(lat)
    c.lng = h3lib.degsToRads(lng)

    return c


cdef (double, double) coord2deg(h3lib.LatLng c) nogil:
    return (
        h3lib.radsToDegs(c.lat),
        h3lib.radsToDegs(c.lng)
    )


cpdef basestring c_version():
    v = (
        h3lib.H3_VERSION_MAJOR,
        h3lib.H3_VERSION_MINOR,
        h3lib.H3_VERSION_PATCH,
    )

    return '{}.{}.{}'.format(*v)


cpdef H3int hex2int(H3str h) except? 0:
    return int(h, 16)


cpdef H3str int2hex(H3int x):
    """ Convert H3 integer to hex string representation

    Need to be careful in Python 2 because `hex(x)` may return a string
    with a trailing `L` character (denoting a "large" integer).
    The formatting approach below avoids this.

    Also need to be careful about unicode/str differences.
    """
    return '{:x}'.format(x)


cdef check_cell(H3int h):
    """ Check if valid H3 "cell" (hexagon or pentagon).

    Does not check if a valid H3 edge, for example.

    Since this function is used by multiple interfaces (int or str),
    we want the error message to be informative to the user
    in either case.

    We use the builtin `hex` function instead of `int2hex` to
    prepend `0x` to indicate that this **integer** representation
    is incorrect, but in a format that is easily compared to
    `str` inputs.
    """
    if isValidCell(h) == 0:
        raise H3CellInvalidError('Integer is not a valid H3 cell: {}'.format(hex(h)))

cdef check_edge(H3int e):
    if isValidDirectedEdge(e) == 0:
        raise H3DirEdgeInvalidError('Integer is not a valid H3 edge: {}'.format(hex(e)))

cdef check_res(int res):
    if (res < 0) or (res > 15):
        raise H3ResDomainError(res)

cdef check_distance(int k):
    if k < 0:
        raise H3DomainError(
            'Grid distances must be nonnegative. Received: {}'.format(k)
        )


cdef H3int* create_ptr(size_t n) except? NULL:
    cdef H3int* ptr = <H3int*> stdlib.calloc(n, sizeof(H3int))
    if (n > 0) and (not ptr):
        raise MemoryError()

    return ptr

cdef H3int[:] foo(size_t n):
    cdef:
        array x

    if n == 0:
        return empty_memory_view()

    x = <H3int[:n]> create_ptr(n)
    x.callback_free_data = stdlib.free

    return x


cpdef H3int[:] from_iter(hexes):
    """ hexes needs to be an iterable that knows its size...
    or should we have it match the np.fromiter function, which infers if not available?
    """
    cdef:
        # array x # this needs to be commented out to avoid an error
        size_t n
    n = len(hexes)

    x = simple_mv(n)

    for i,h in enumerate(hexes):
        x[i] = h

    return x
