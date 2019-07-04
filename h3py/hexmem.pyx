from libc cimport stdlib
from h3py.h3api cimport H3int, H3str

cpdef H3int hex2int(h):  # we get typing problems if we try to type input as `H3str h`
    return int(h, 16)


cpdef H3str int2hex(H3int x):
    return hex(x)[2:]


cdef class HexMem:
    """ A small class to manage memory for H3Index arrays
    Memory is allocated and deallocated at object creation and garbage collection
    """

    # The data members are already declared in hexmem.pxd, we do not re-declare here.
    # cdef:
    #     unsigned int n
    #     H3int* ptr

    def __cinit__(self, n):
        self.n = n
        self.ptr = <H3int*> stdlib.calloc(n, sizeof(H3int))

        if not self.ptr:
            raise MemoryError()

    def __dealloc__(self):
        if self.ptr:
            stdlib.free(self.ptr)

    def __len__(self):
        return self.n

    cdef void resize(self, int n):
        cdef:
            H3int* a = NULL

        self.n = n
        a = <H3int*> stdlib.realloc(self.ptr, n*sizeof(H3int))

        if a is NULL:
            stdlib.free(self.ptr)
            raise MemoryError()
        else:
            self.ptr = a

    cpdef void drop_zeros(self):
        """ Move nonzero elements to front of array.
        Does not preserve order of nonzero elements.

        Tail of array will still have nonzero elements,
        but we don't care, because we will realloc the array
        to free that memory.

        Modify self.ptr and self.n **in place**.
        """
        n = move_nonzeros(self.ptr, self.n)
        self.resize(n)

    def set_str(self):
        return set(int2hex(h) for h in self.memview())

    def set_int(self):
        return set(self.memview())

    cpdef H3int[:] memview(self):
        self.drop_zeros() # how to make sure we always run this when appropriate?
        # ideally, it would just run right after the pointer is **exposed**, not
        # when we are looking to get the data.

        if self.n > 0:
            return <H3int[:self.n]> self.ptr
        else:
            return empty_memory_view()


cdef int move_nonzeros(H3int* a, int n):
    """ Move nonzero elements to front of array `a` of length `n`.

    Return the number of nonzero elements.
    """
    cdef:
        int i = 0
        int j = n

    while i < j:
        if a[j-1] == 0:
            j -= 1
            continue

        if a[i] != 0:
            i += 1
            continue

        # if we're here, we know:
        # a[i] == 0
        # a[j-1] != 0
        # i < j
        # so we can swap!
        # todo: what about j vs j-1 ....?
        a[i] = a[j-1]
        j -= 1

    return i


cdef inline H3int[:] empty_memory_view():
    # there's gotta be a better way to do this...
    cdef:
        H3int a[1]

    return (<H3int[:]>a)[:0]


cpdef HexMem from_ints(hexes):
    hm = HexMem(len(hexes))

    for i, h in enumerate(hexes):
        hm.ptr[i] = h

    return hm

# maybe drop the cpdef???
cpdef HexMem from_strs(hexes):
    hm = HexMem(len(hexes))

    for i, h in enumerate(hexes):
        hm.ptr[i] = hex2int(h)

    return hm
