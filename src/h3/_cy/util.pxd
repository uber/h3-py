from .h3lib cimport H3int, H3str, LatLng, H3Error

cdef LatLng deg2coord(double lat, double lng) nogil
cdef (double, double) coord2deg(LatLng c) nogil

cpdef H3int hex2int(H3str h) except? 0
cpdef H3str int2hex(H3int x)

cdef H3int* create_ptr(size_t n) except? NULL
cdef H3int[:] create_mv(H3int* ptr, size_t n)


cdef check_cell(H3int h)
cdef check_edge(H3int e)
cdef check_res(int res)
cdef check_distance(int k)
cdef check_for_error(H3Error err)

cdef H3int[:] empty_memory_view() # want to drop this if possible
