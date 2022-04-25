from .h3lib cimport bool, int64_t, H3int

cpdef bool is_cell(H3int h)
cpdef bool is_pentagon(H3int h)
cpdef int get_base_cell(H3int h) except -1
cpdef int resolution(H3int h) except -1
cpdef int distance(H3int h1, H3int h2) except -1
cpdef H3int[:] disk(H3int h, int k)
cpdef H3int[:] _ring_fallback(H3int h, int k)
cpdef H3int[:] ring(H3int h, int k)
cpdef H3int parent(H3int h, res=*) except 0
cpdef H3int[:] children(H3int h, res=*)
cpdef H3int center_child(H3int h, res=*) except 0
cpdef H3int[:] compact(const H3int[:] hu)
cpdef H3int[:] uncompact(const H3int[:] hc, int res)
cpdef int64_t num_hexagons(int resolution) except -1
cpdef double mean_hex_area(int resolution, unit=*) except -1
cpdef double cell_area(H3int h, unit=*) except -1
cpdef H3int[:] line(H3int start, H3int end)
cpdef bool is_res_class_iii(H3int h)
cpdef H3int[:] get_pentagon_indexes(int res)
cpdef H3int[:] get_res0_indexes()
cpdef get_faces(H3int h)
cpdef (int, int) experimental_h3_to_local_ij(H3int origin, H3int h) except *
cpdef H3int experimental_local_ij_to_h3(H3int origin, int i, int j) except 0
