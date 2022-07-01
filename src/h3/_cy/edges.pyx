cimport h3lib
from .h3lib cimport bool, H3int

from .util cimport (
    create_ptr,
    create_mv,
)

from .error_system cimport check_for_error

# todo: make bint
cpdef bool are_neighbors(H3int h1, H3int h2):
    cdef:
        int out

    err = h3lib.areNeighborCells(h1, h2, &out)

    # note: we are specifically not raising an error here, and just
    # returning false.
    # todo: is this choice consistent across the Python and C libs?
    if err:
        return False

    return out == 1


cpdef H3int edge(H3int origin, H3int destination) except *:
    cdef:
        int neighbor_out
        H3int out

    check_for_error(
        h3lib.cellsToDirectedEdge(origin, destination, &out)
    )

    return out


cpdef bool is_edge(H3int e):
    return h3lib.isValidDirectedEdge(e) == 1

cpdef H3int edge_origin(H3int e) except 1:
    cdef:
        H3int out

    check_for_error(
        h3lib.getDirectedEdgeOrigin(e, &out)
    )

    return out

cpdef H3int edge_destination(H3int e) except 1:
    cdef:
        H3int out

    check_for_error(
        h3lib.getDirectedEdgeDestination(e, &out)
    )

    return out

cpdef (H3int, H3int) edge_cells(H3int e) except *:
    return edge_origin(e), edge_destination(e)

cpdef H3int[:] edges_from_cell(H3int origin):
    """ Returns the 6 (or 5 for pentagons) directed edges
    for the given origin cell
    """

    ptr = create_ptr(6)

    check_for_error(
        h3lib.originToDirectedEdges(origin, ptr)
    )

    mv = create_mv(ptr, 6)

    return mv


cpdef double mean_edge_length(int resolution, unit='km') except -1:
    cdef:
        double length

    h3lib.getHexagonEdgeLengthAvgKm(resolution, &length)

    # todo: multiple units
    convert = {
        'km': 1.0,
        'm': 1000.0
    }

    try:
        length *= convert[unit]
    except:
        raise ValueError('Unknown unit: {}'.format(unit))

    return length


cpdef double edge_length(H3int e, unit='km') except -1:
    cdef:
        double length

    # todo: maybe kick this logic up to the python level
    # it might be a little cleaner, because we can do the "switch statement"
    # with a dict, but would require exposing more C functions

    if unit == 'rads':
        h3lib.exactEdgeLengthRads(e, &length)
    elif unit == 'km':
        h3lib.exactEdgeLengthKm(e, &length)
    elif unit == 'm':
        h3lib.exactEdgeLengthM(e, &length)
    else:
        raise ValueError('Unknown unit: {}'.format(unit))

    return length
