from .h3lib cimport H3int, H3str

cpdef H3int hex2int(H3str h)
cpdef H3str int2hex(H3int x)

cdef H3int* create_ptr(size_t n) except *
cdef H3int[:] create_mv(H3int* ptr, size_t n)


cdef check_addr(H3int h)
cdef check_edge(H3int e)
cdef check_res(int res)
