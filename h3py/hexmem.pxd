from h3py.h3api cimport H3int, H3str

cpdef H3int hex2int(h)
cpdef H3str int2hex(H3int x)

cpdef HexMem from_ints(hexes)
cpdef HexMem from_ints(hexes)

cdef class HexMem:
    """ A small class to manage memory for H3Index arrays
    Memory is allocated and deallocated at object creation and garbage collection
    """
    cdef:
        size_t n
        H3int* ptr

    cdef void resize(self, size_t n)
    cpdef void drop_zeros(self)
    cpdef H3int[:] memview(self)
