from .h3lib cimport H3int

cdef class H3MemoryManager:
    cdef:
        size_t n
        H3int* ptr

    cdef H3int[:] create_mv(self)


"""
todo: read: https://cython.readthedocs.io/en/latest/src/tutorial/pxd_files.html
"""
