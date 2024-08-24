from .h3lib cimport bool, H3int

cpdef H3int latlng_to_cell(double lat, double lng, int res) except 1
cpdef (double, double) cell_to_latlng(H3int h) except *
cpdef double great_circle_distance(
    double lat1, double lng1,
    double lat2, double lng2, unit=*) except -1
cpdef H3int cell_to_vertex(H3int h, int vertex_num) except 1
cpdef H3int[:] cell_to_vertexes(H3int h)
cpdef (double, double) vertex_to_latlng(H3int v) except *
cpdef bool is_valid_vertex(H3int v)
