#!python
import numpy as np
cimport numpy as np

# https://github.com/cython/cython/wiki/tutorials-numpy#c-api-initialization
np.import_array()

cimport h3lib
from h3lib cimport H3int, H3Index
from .util cimport deg2coord
from .cells import ring

from cython cimport boundscheck, wraparound
from libc.math cimport sqrt, sin, cos, asin

cdef double haversineDistance(double th1, double ph1, double th2, double ph2) nogil:
    cdef:
        double dx, dy, dz
        double R = 6371.0088

    ph1 -= ph2

    dz = sin(th1) - sin(th2)
    dx = cos(ph1) * cos(th1) - cos(th2)
    dy = sin(ph1) * cos(th1)

    return asin(sqrt(dx*dx + dy*dy + dz*dz) / 2)*2*R


@boundscheck(False)
@wraparound(False)
cpdef void haversine_vect(
    const H3int[:] a,
    const H3int[:] b,
         double[:] out
) nogil:

    cdef h3lib.GeoCoord p1, p2

    with nogil:
        # todo: add these back in when cython 3.0 comes out
        #assert len(a) == len(b)
        #assert len(a) <= len(out)

        for i in range(len(a)):
            h3lib.h3ToGeo(a[i], &p1)
            h3lib.h3ToGeo(b[i], &p2)
            out[i] = haversineDistance(
                p1.lat, p1.lng,
                p2.lat, p2.lng
            )

@boundscheck(False)
@wraparound(False)
cpdef void geo_to_h3_vect(
    const double[:] lat,
    const double[:] lng,
    int res,
    H3int[:] out
) nogil:

    cdef h3lib.GeoCoord c

    with nogil:
        for i in range(len(lat)):
            c = deg2coord(lat[i], lng[i])
            out[i] = h3lib.geoToH3(&c, res)

@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[H3Index, ndim=1] h3_to_parent(
    np.ndarray[H3Index, ndim=1] h,
    int res
):
    # generate a new output array of the correct shape
    cdef np.ndarray[H3Index, ndim=1] out = np.empty(len(h), np.uint64)

    # Py_ssize_t is the proper C type for Python array indices.
    cdef Py_ssize_t i

    for i in range(len(h)):
        out[i] = h3lib.h3ToParent(h[i], res)

    return out

@boundscheck(False)
@wraparound(False)
cpdef np.ndarray[H3Index, ndim=2] hex_ring(
    np.ndarray[H3Index, ndim=1] h,
    int k
):
    # new dimension size
    cdef int newdim = k * 6

    cdef np.ndarray[H3Index, ndim=2] out = np.empty((len(h), newdim), np.uint64)
    cdef H3Index [:, :] out_view = out
    cdef H3Index [:] h_view = h

    # Py_ssize_t is the proper C type for Python array indices.
    cdef Py_ssize_t i, j
    cdef H3int[:] ring_vals

    for i in range(len(h)):
        ring_vals = ring(h[i], k)
        for j in range(newdim):
            out[i, j] = ring_vals[j]

    return out
