cimport h3lib
from h3lib cimport bool, int64_t, H3int

from .h3utils cimport (
    check_addr,
    check_edge,
    check_res,
    create_mv,
    create_ptr
)

from h3.h3utils import H3ValueError
from h3.geo import (
    geo_to_h3,
    h3_to_geo,
    polyfill,
    cell_boundary,
    edge_boundary
)

cpdef basestring _c_version():
    v = (
        h3lib.H3_VERSION_MAJOR,
        h3lib.H3_VERSION_MINOR,
        h3lib.H3_VERSION_PATCH,
    )

    return '{}.{}.{}'.format(*v)

# todo: add notes about Cython exception handling


# bool is a python type, so we don't need the except clause
cpdef bool is_cell(H3int h):
    """Validates an H3 cell (hexagon or pentagon)

    Returns
    -------
    boolean
    """
    return h3lib.h3IsValid(h) == 1

cpdef bool is_pentagon(H3int h):
    return h3lib.h3IsPentagon(h) == 1

cpdef int get_base_cell(H3int h) except -1:
    check_addr(h)

    return h3lib.h3GetBaseCell(h)


cpdef int resolution(H3int h) except -1:
    """Returns the resolution of an H3 Index
    0--15
    """
    check_addr(h)

    return h3lib.h3GetResolution(h)


cpdef H3int parent(H3int h, res=None) except 1:
    check_addr(h)

    if res is None:
        res = resolution(h) - 1
    # todo: actually, do we want to raise an error if there are no children, or just return an empty set?
    check_res(res)

    return h3lib.h3ToParent(h, res)


cpdef int distance(H3int h1, H3int h2) except -1:
    """ compute the hex-distance between two hexagons
    """
    check_addr(h1)
    check_addr(h2)

    d = h3lib.h3Distance(h1,h2)

    return d

cpdef H3int[:] disk(H3int h, int k):
    """ Return cells at grid distance `<= k` from `h`.
    """
    check_addr(h)
    if k < 0:
        raise H3ValueError('Invalid ring size: {}'.format(k))

    n = h3lib.maxKringSize(k)

    ptr = create_ptr(n) # todo: return a "smart" pointer that knows its length?
    h3lib.kRing(h, k, ptr)
    mv = create_mv(ptr, n)

    return mv

cpdef H3int[:] ring(H3int h, int k):
    """ Return cells at grid distance `== k` from `h`.
    Collection is "hollow" for k >= 1.
    """
    check_addr(h)

    n = 6*k if k > 0 else 1
    ptr = create_ptr(n)

    flag = h3lib.hexRing(h, k, ptr)
    mv = create_mv(ptr, n)

    # todo: we can do this much more efficiently by using kRingDistances
    if flag != 0:
        raise H3ValueError("Couldn't run the fast version!")
        # # fall back to `kRingDistances` and filter for appropriate distance. don't need to use sets
        # n = maxKringSize(k)
        # ptr = create_ptr(n)

        # # hmmm. maybe use a cython array here instead
        # cdef int[:n] distances
        # distances[:] = 0


        # kRingDistances(h, k, ptr, &distances[0])

    return mv



cpdef H3int[:] children(H3int h, res=None):
    check_addr(h)

    if res is None:
        res = resolution(h) + 1
    # todo: actually, do we want to raise an error if there are no children, or just return an empty set?
    check_res(res)

    n = h3lib.maxH3ToChildrenSize(h, res)

    ptr = create_ptr(n)
    h3lib.h3ToChildren(h, res, ptr)
    mv = create_mv(ptr, n)

    return mv



cpdef H3int[:] compact(const H3int[:] hu):
    for h in hu:
        check_addr(h)

    ptr = create_ptr(len(hu))
    flag = h3lib.compact(&hu[0], ptr, len(hu))
    mv = create_mv(ptr, len(hu))

    if flag != 0:
        raise H3ValueError('Could not compact set of hexagons!')

    return mv

# todo: https://stackoverflow.com/questions/50684977/cython-exception-type-for-a-function-returning-a-typed-memoryview
# apparently, memoryviews are python objects, so we don't need to do the except clause
cpdef H3int[:] uncompact(const H3int[:] hc, int res):
    for h in hc:
        check_addr(h)

    N = h3lib.maxUncompactSize(&hc[0], len(hc), res)

    ptr = create_ptr(N)
    flag = h3lib.uncompact(
        &hc[0], len(hc),
           ptr, N,
        res
    )
    mv = create_mv(ptr, N)

    if flag != 0:
        raise H3ValueError('Could not uncompact set of hexagons!')

    return mv


cpdef int64_t num_hexagons(int resolution) except -1:
    check_res(resolution)

    return h3lib.numHexagons(resolution)


cpdef double mean_hex_area(int resolution, unit='km2') except -1:
    check_res(resolution)

    area = h3lib.hexAreaKm2(resolution)

    # todo: multiple units
    convert = {
        'km2': 1.0,
    }
    area *= convert[unit]

    return area

cpdef double mean_edge_length(int resolution, unit='km') except -1:
    check_res(resolution)

    length = h3lib.edgeLengthKm(resolution)

    # todo: multiple units
    convert = {
        'km': 1.0,
    }
    length *= convert[unit]

    return length




cpdef bool are_neighbors(H3int h1, H3int h2):
    check_addr(h1)
    check_addr(h2)

    return h3lib.h3IndexesAreNeighbors(h1, h2) == 1


cpdef H3int edge(H3int origin, H3int destination) except 1:
    check_addr(origin)
    check_addr(destination)

    if h3lib.h3IndexesAreNeighbors(origin, destination) != 1:
        raise H3ValueError('Cells are not neighbors: {} and {}'.format(origin, destination))

    return h3lib.getH3UnidirectionalEdge(origin, destination)


cpdef bool is_edge(H3int e):
    check_edge(e)

    return h3lib.h3UnidirectionalEdgeIsValid(e) == 1

cpdef H3int edge_origin(H3int e) except 1:
    check_edge(e)

    return h3lib.getOriginH3IndexFromUnidirectionalEdge(e)

cpdef H3int edge_destination(H3int e) except 1:
    check_edge(e)

    return h3lib.getDestinationH3IndexFromUnidirectionalEdge(e)

cpdef (H3int, H3int) edge_cells(H3int e) except *:
    check_edge(e)

    return edge_origin(e), edge_destination(e)

cpdef H3int[:] edges_from_cell(H3int origin):
    """ Returns the 6 (or 5 for pentagons) directed edges
    for the given origin cell
    """
    check_addr(origin)

    ptr = create_ptr(6)
    h3lib.getH3UnidirectionalEdgesFromHexagon(origin, ptr)
    mv = create_mv(ptr, 6)

    return mv

cpdef H3int[:] line(H3int start, H3int end):
    check_addr(start)
    check_addr(end)

    n = h3lib.h3LineSize(start, end)

    ptr = create_ptr(n)
    flag = h3lib.h3Line(start, end, ptr)
    mv = create_mv(ptr, n)

    if flag != 0:
        raise H3ValueError("Couldn't find line between cells {} and {}".format(start, end))

    return mv
