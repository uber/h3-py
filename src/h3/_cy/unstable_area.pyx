cimport h3lib
from h3lib cimport H3int, GeoCoord, GeoBoundary
from .util cimport deg2coord

from cython cimport boundscheck, wraparound
from libc.math cimport sqrt, sin, cos, tan, asin, atan

# cdef double haversine_cells
# cdef double haversine_vertices


cdef double haversine_points(GeoCoord a, GeoCoord b) nogil:
    """
    Haversine distance between two points.

    Input/output: both in radians
    """
    a.lng -= b.lng

    x = cos(a.lng) * cos(a.lat) - cos(b.lat)
    y = sin(a.lng) * cos(a.lat)
    z = sin(a.lat) - sin(b.lat)

    return 2*asin( 0.5*sqrt(x*x + y*y + z*z) )


cdef double area_triangle(GeoCoord a, GeoCoord b, GeoCoord c) nogil:
    """ Surface area of a spherical triangle given by three lat/lng points

    input: radians
    ouput: unit sphere area
    """
    A = haversine_points(b, c)
    B = haversine_points(c, a)
    C = haversine_points(a, b)

    S = (A + B + C)/2

    T = sqrt(
          tan((S  )/2)
        * tan((S-A)/2)
        * tan((S-B)/2)
        * tan((S-C)/2)
    )

    E = 4*atan(T)

    return E


cdef double cell_area_radians(H3int h) nogil:
    cdef:
        GeoCoord c
        GeoBoundary gb
        int i, j
        double A

    h3lib.h3ToGeo(h, &c)
    h3lib.h3ToGeoBoundary(h, &gb)

    A = 0.0
    for i in range(gb.num_verts):
        j = i + 1
        if j == gb.num_verts:
            j = 0

        A += area_triangle(gb.verts[i], gb.verts[j], c)

    return A

cpdef double cell_area_km2(H3int h):
    # how about a `unit_per_km` factor, defaults to 1?
    # we really don't need two functions...
    # except, maybe, for radian functions
    cdef double earth_radius_km = 6371.007180918475

    return cell_area_radians(h)*earth_radius_km*earth_radius_km
