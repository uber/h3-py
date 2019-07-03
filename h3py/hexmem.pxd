from h3py.h3api cimport H3int, H3str

cpdef H3int hex2int(h)
cpdef H3str int2hex(H3int x)

cdef class HexMem:
    """ A small class to manage memory for H3Index arrays
    Memory is allocated and deallocated at object creation and garbage collection
    """
    cdef:
        unsigned int n
        H3int* ptr

    cdef void resize(self, int n)
    cpdef void drop_zeros(self)
    cpdef H3int[:] memview(self)
