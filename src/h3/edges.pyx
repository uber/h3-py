cimport h3lib
from .h3lib cimport bool, H3int

from .util cimport (
    check_cell,
    check_edge,
    create_ptr,
    create_mv,
)

from .util import H3ValueError

cpdef bool are_neighbors(H3int h1, H3int h2):
    check_cell(h1)
    check_cell(h2)

    return h3lib.h3IndexesAreNeighbors(h1, h2) == 1


cpdef H3int edge(H3int origin, H3int destination) except 1:
    check_cell(origin)
    check_cell(destination)

    if h3lib.h3IndexesAreNeighbors(origin, destination) != 1:
        raise H3ValueError('Cells are not neighbors: {} and {}'.format(origin, destination))

    return h3lib.getH3UnidirectionalEdge(origin, destination)


cpdef bool is_edge(H3int e):
    return h3lib.h3UnidirectionalEdgeIsValid(e) == 1

cpdef H3int edge_origin(H3int e) except 1:
    # without the check, with an invalid input, the function will just return 0
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
    check_cell(origin)

    ptr = create_ptr(6)
    h3lib.getH3UnidirectionalEdgesFromHexagon(origin, ptr)
    mv = create_mv(ptr, 6)

    return mv
