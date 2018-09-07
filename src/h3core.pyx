#cimport libc.stdlib
#from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free

from cpython cimport bool
from libc.math cimport pi

from _h3core cimport H3Index
cimport _h3core


# when do i want to use cpdef?


# todo: c versions?
cdef H3Index hex2int(str h):
    return int(h, 16)

def int2hex(H3Index x):
    return hex(x)[2:]


cdef double degs_to_rads(double deg):
    """Helper degrees to radians"""
    return deg * pi / 180.0


cdef double rads_to_degs(double rad):
    """Helper radians to degrees"""
    return rad * 180.0 / pi


cdef double mercator_lat(double lat):
    """Helper coerce lat range"""
    return lat - 180 if lat > 90 else lat


cdef double mercator_lng(double lng):
    """Helper coerce lng range"""
    return lng - 360 if lng > 180 else lng

# todo: i see what  he was trying to do. maybe a class manages this weird transformation better


cdef _h3core.GeoCoord geo2coord(double lat, double lng):
    cdef:
        _h3core.GeoCoord c

    c.lat = degs_to_rads(mercator_lat(lat))
    c.lng = degs_to_rads(mercator_lng(lng))

    return c


cdef (double, double) coord2geo(_h3core.GeoCoord c):
    return (
        mercator_lat(rads_to_degs(c.lat)),
        mercator_lng(rads_to_degs(c.lng))
    )


def geo_to_h3(double lat, double lng, int res):
    # these cdef's are actually optional. they can be inferred
    cdef:
        _h3core.GeoCoord c
        H3Index h

    c = geo2coord(lat, lng)
    h = _h3core.geoToH3(&c, res)

    return int2hex(h)


def h3_to_geo(str h3_address):
    """Reverse lookup an h3 address into a geo-coordinate"""
    cdef:
        _h3core.GeoCoord c

    _h3core.h3ToGeo(hex2int(h3_address), &c)

    return coord2geo(c)


def h3_to_geo_boundary(str h3_address, bool geo_json=False):
    """Compose an array of geo-coordinates that outlines a hexagonal cell"""
    cdef:
        _h3core.GeoBoundary gb

    _h3core.h3ToGeoBoundary(hex2int(h3_address), &gb)

    out = tuple(
        coord2geo(gb.verts[i])
        for i in range(gb.num_verts)
    )

    if geo_json:
        out = tuple(tuple(reversed(x)) for x in out)
        out += (out[0],)

    return out



# cdef class Geofence:
#     cdef _h3core.Geofence _fence
#     cdef bint _owned

#     def __cinit__(self):
#         self._fence.verts = NULL
#         self._fence.numVerts = 0
#         self._owned = False

#     def __dealloc__(self):
#         if self._owned:
#             libc.stdlib.free(self._fence.verts)

#     @property
#     def num_verts(self):
#         return self._fence.numVerts

#     @property
#     def verts(self):
#         return [self._fence.verts[i] for i in range(self._fence.numVerts)]


# cdef class GeoJsonLite:
#     cdef _h3core.GeoPolygon _polygon

#     def __cinit__(self):
#         self._polygon.geofence = _h3core.Geofence()
#         self._polygon.numHoles = 0
#         self._polygon.holes = NULL

# #    def __deinit__(self):
# #        libc.stdlib.free(self._polygon.holes)
# #        libc.stdlib.free(self._polygon.geofence.verts)

#     @property
#     def geofence(self):
#         fence = Geofence()
#         fence._fence = self._polygon.geofence
#         return fence

#     @property
#     def num_holes(self):
#         return self._polygon.numHoles

#     @property
#     def holes(self):
#         return [self._polygen.holes[i] for i in range(self._polygon.numHoles)]
