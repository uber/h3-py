from libc cimport stdint
from cpython cimport bool
from libc.stdint cimport int64_t

ctypedef stdint.uint64_t H3int
ctypedef basestring H3str

cdef extern from "h3api.h":
    cdef int H3_VERSION_MAJOR
    cdef int H3_VERSION_MINOR
    cdef int H3_VERSION_PATCH

    ctypedef stdint.uint64_t H3Index
