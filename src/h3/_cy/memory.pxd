from .h3lib cimport H3int

cdef class H3MemoryManager:
    cdef:
        size_t n
        H3int* ptr

    cdef H3int[:] create_mv(self)


cdef int[:] int_mv(size_t n)
cdef H3int[:] empty_memory_view()

"""
todo: read: https://cython.readthedocs.io/en/latest/src/tutorial/pxd_files.html

todo: should i be allocating with python memory functions?
https://cython.readthedocs.io/en/latest/src/tutorial/memory_allocation.html
"""
