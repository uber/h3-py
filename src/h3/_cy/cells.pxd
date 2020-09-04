from .h3lib cimport bool, int64_t, H3int
cpdef H3int[:] ring(H3int h, int k)
cpdef H3int[:] _ring_fallback(H3int h, int k)

