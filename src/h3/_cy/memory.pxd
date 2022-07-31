from .h3lib cimport H3int

cdef class H3MemoryManager:
    cdef:
        size_t n
        H3int* ptr

    cdef H3int[:] to_mv(self)


cdef int[:] int_mv(size_t n)
cpdef H3int[:] iter_to_mv(hexes)


"""
todo: read: https://cython.readthedocs.io/en/latest/src/tutorial/pxd_files.html

## things i'm not happy about with this current situation

- there's gotta be a cleaner way to create a empty_memory_view()
- abolish any appearance of &thing[0]. (i.e., identical interfaces)
- can i make the interface for all these memory views identical?
- also, what's going on with the segfault stuff when we `.to_mv()` before checking an error? why isn't it robust to that?
"""
