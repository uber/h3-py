from h3py.h3api cimport H3int, H3str

cpdef H3int hex2int(h)
cpdef H3str int2hex(H3int x)

cdef H3int* create_ptr(size_t n)
cdef H3int[:] create_mv(H3int* ptr, size_t n)
