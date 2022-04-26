from .h3lib cimport bool, H3int

cpdef bool are_neighbors(H3int h1, H3int h2)
cpdef H3int edge(H3int origin, H3int destination) except 1
cpdef bool is_edge(H3int e)
cpdef H3int edge_origin(H3int e) except 1
cpdef H3int edge_destination(H3int e) except 1
cpdef (H3int, H3int) edge_cells(H3int e) except *
cpdef H3int[:] edges_from_cell(H3int origin)
cpdef double mean_edge_length(int resolution, unit=*) except -1
cpdef double edge_length(H3int e, unit=*) except -1
