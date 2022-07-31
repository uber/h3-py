from cython.view cimport array
from .h3lib cimport H3int

"""
### Memory allocation options

We have a few options for the memory allocation functions.
There's a trade-off between using the Python allocators which let Python
track memory usage and offers some optimizations vs the system
allocators, which do not need to acquire the GIL.
"""

"""
System allocation functions. These do not acquire the GIL.
"""
from libc.stdlib cimport (
    # malloc as h3_malloc,  # not used
    calloc   as h3_calloc,
    realloc  as h3_realloc,
    free     as h3_free,
)


"""
PyMem_Raw* functions should just be wrappers around system allocators
also given in libc.stdlib. These functions do not acquire the GIL.

Note that these do not have a calloc function until py 3.5 and Cython 3.0,
so we would need to zero-out memory manually.

https://python.readthedocs.io/en/stable/c-api/memory.html#raw-memory-interface
"""
# from cpython.mem cimport (
#     PyMem_RawMalloc   as h3_malloc,
#     # PyMem_RawCalloc as h3_calloc,  # only in py3.5 (and cython 3.0?)
#     PyMem_RawRealloc  as h3_realloc,
#     PyMem_RawFree     as h3_free,
# )


"""
These functions use the Python allocator (instead of the system allocator),
which offers some optimizations for Python, and allows Python to track
memory usage. However, these functions must acquire the GIL.

Note that these do not have a calloc function until py 3.5 and Cython 3.0,
so we would need to zero-out memory manually.

https://cython.readthedocs.io/en/stable/src/tutorial/memory_allocation.html
https://python.readthedocs.io/en/stable/c-api/memory.html#memory-interface
"""
# from cpython.mem cimport (
#     PyMem_Malloc   as h3_malloc,
#     # PyMem_Calloc as h3_calloc,  # only in Python >=3.5 (and Cython >=3.0?)
#     PyMem_Realloc  as h3_realloc,
#     PyMem_Free     as h3_free,
# )


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


cdef (H3int*, size_t) _remove_zeros(H3int* ptr, size_t n):
    n = move_nonzeros(ptr, n)
    if n == 0:
        h3_free(ptr)
        ptr = NULL
        n = 0

    ptr = <H3int*> h3_realloc(ptr, n*sizeof(H3int))
    if not ptr:
        raise MemoryError()

    return ptr, n


cdef class H3MemoryManager:
    def __cinit__(self, size_t n):
        self.n = n
        self.ptr = <H3int*> h3_calloc(self.n, sizeof(H3int))

        if not self.ptr:
            raise MemoryError()

    cdef H3int[:] _create_mv(self):
        cdef:
            array mv

        if self.n == 0:
            return empty_memory_view()

        mv = <H3int[:self.n]> self.ptr
        mv.callback_free_data = h3_free

        # responsibility for the memory moves from this object to the array/memoryview
        self.ptr = NULL
        self.n = 0

        return mv

    cdef H3int[:] to_mv(self):
        self.ptr, self.n = _remove_zeros(self.ptr, self.n)
        return self._create_mv()

    def __dealloc__(self):
        # If the memory has been handed off to a memoryview, this pointer
        # should be NULL, and deallocing on NULL is fine.
        # If the pointer is *not* NULL, then this means the MemoryManager
        # has is still responsible for the memory (it hasn't given the memory away to another object).
        h3_free(self.ptr)


"""
Can someone please swoop in and find a much cleaner way to do all of this Cython memory management baloney?
"""
cdef int[:] int_mv(size_t n):
    cdef:
        int* ptr
        array arr

    if n <= 0:
        raise MemoryError()
    ptr = <int*> h3_calloc(n, sizeof(int))
    if ptr is NULL:
        raise MemoryError()

    arr = <int[:n]> ptr
    arr.callback_free_data = h3_free

    return arr


cdef H3int[:] simple_mv(size_t n):
    # cdef:
    #     array mv

    if n == 0:
        return empty_memory_view()

    ptr = <H3int*> h3_calloc(n, sizeof(H3int))
    if not ptr:
        raise MemoryError()

    mv = <H3int[:n]> ptr
    mv.callback_free_data = h3_free

    return mv


cpdef H3int[:] iter_to_mv(hexes):
    """ hexes needs to be an iterable that knows its size...
    or should we have it match the np.fromiter function, which infers if not available?
    """
    # cdef array x  # this needs to be commented out to avoid an error

    mv = simple_mv(len(hexes))

    for i,h in enumerate(hexes):
        mv[i] = h

    return mv
