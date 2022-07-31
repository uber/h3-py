from libc cimport stdlib
from cython.view cimport array
from .h3lib cimport H3int


cdef size_t move_nonzeros(H3int* a, size_t n):
    """ Move nonzero elements to front of array `a` of length `n`.
    Return the number of nonzero elements.

    Loop invariant: Everything *before* `i` or *after* `j` is "done".
    Move `i` and `j` inwards until they equal, and exit.
    You can move `i` forward until there's a zero in front of it.
    You can move `j` backward until there's a nonzero to the left of it.
    Anything to the right of `j` is "junk" that can be reallocated.

    | a | b | 0 | c | d | ... |
            ^           ^
            i           j


    | a | b | d | c | d | ... |
            ^       ^
            i       j
    """
    cdef:
        size_t i = 0
        size_t j = n

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
        # so we can swap! (actually, move a[j-1] -> a[i])
        a[i] = a[j-1]
        j -= 1

    return i


cdef H3int[:] empty_memory_view():
    # todo: get rid of this?
    # there's gotta be a better way to do this...
    # create an empty cython.view.array?
    cdef:
        H3int a[1]

    return (<H3int[:]>a)[:0]


cdef H3int[:] simple_mv(size_t n):
    # cdef:
    #     array x

    if n == 0:
        return empty_memory_view()

    ptr = <H3int*> stdlib.calloc(n, sizeof(H3int))
    if not ptr:
        raise MemoryError()

    x = <H3int[:n]> ptr
    x.callback_free_data = stdlib.free

    return x


cdef class H3MemoryManager:
    def __cinit__(self, size_t n):
        self.n = n
        self.ptr = <H3int*> stdlib.calloc(self.n, sizeof(H3int))

        if (self.n > 0) and (not self.ptr):
            raise MemoryError()

    cdef H3int[:] create_mv(self):
        cdef:
            array x

        self.n = move_nonzeros(self.ptr, self.n)
        if self.n <= 0:
            stdlib.free(self.ptr)
            self.ptr = NULL
            self.n = 0
            return empty_memory_view()

        self.ptr = <H3int*> stdlib.realloc(self.ptr, self.n*sizeof(H3int))

        if self.ptr is NULL:
            raise MemoryError()

        x = <H3int[:self.n]> self.ptr
        x.callback_free_data = stdlib.free

        # responsibility for the memory moves from this object to the array/memoryview
        self.ptr = NULL
        self.n = 0

        return x

    def __dealloc__(self):
        # If the memory has been handed off to a memoryview, this pointer
        # should be NULL, and deallocing on NULL is fine.
        # If the pointer is *not* NULL, then this means the MemoryManager
        # has is still responsible for the memory (it hasn't given the memory away to another object).
        stdlib.free(self.ptr)
        self.ptr = NULL


"""
Can someone please swoop in and find a much cleaner way to do all of this Cython memory management baloney?
"""
cdef int[:] int_mv(size_t n):
    cdef:
        int* ptr
        array arr

    if n <= 0:
        raise MemoryError()
    ptr = <int*>stdlib.calloc(n, sizeof(int))
    if ptr is NULL:
        raise MemoryError()

    arr = <int[:n]> ptr
    arr.callback_free_data = stdlib.free

    return arr
