from libc cimport stdlib
from libc.math cimport pi
from cpython cimport bool

cimport h3py.h3api as h3c
from h3py.h3api cimport H3int, H3str

from h3py.hexmem cimport HexMem



cdef double degs_to_rads(double deg):
    """Helper degrees to radians"""
    """
    todo: use C API functions instead:

    double degsToRads(double degrees);
    double radsToDegs(double radians);

    """

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


cdef h3c.GeoCoord geo2coord(double lat, double lng):
    cdef:
        h3c.GeoCoord c

    c.lat = degs_to_rads(mercator_lat(lat))
    c.lng = degs_to_rads(mercator_lng(lng))

    return c


cdef (double, double) coord2geo(h3c.GeoCoord c):
    return (
        mercator_lat(rads_to_degs(c.lat)),
        mercator_lng(rads_to_degs(c.lng))
    )


cpdef H3int geo_to_h3(double lat, double lng, int res):
    cdef:
        h3c.GeoCoord c

    c = geo2coord(lat, lng)

    return h3c.geoToH3(&c, res)


cpdef (double, double) h3_to_geo(H3int h):
    """Reverse lookup an h3 address into a geo-coordinate"""
    cdef:
        h3c.GeoCoord c

    h3c.h3ToGeo(h, &c)

    return coord2geo(c)

cdef h3c.Geofence make_geofence(geos):
    cdef:
        h3c.Geofence gf

    gf.numVerts = len(geos)

    # todo: figure out when/how to free this memory
    gf.verts = <h3c.GeoCoord*> stdlib.calloc(gf.numVerts, sizeof(h3c.GeoCoord))

    for i, (lat, lng) in enumerate(geos):
        gf.verts[i] = geo2coord(lat, lng)

    return gf


cdef class GeoPolygon:
    """ Basic version of GeoPolygon

    Doesn't work with holes.
    """
    cdef:
        h3c.GeoPolygon gp

    def __cinit__(self, geos):
        self.gp.numHoles = 0
        self.gp.holes = NULL
        self.gp.geofence = make_geofence(geos)

    def __dealloc__(self):
        if self.gp.geofence.verts:
            stdlib.free(self.gp.geofence.verts)
        self.gp.geofence.verts = NULL


# todo: nogil for expensive C operation?
def polyfill(geos, int res):
    """ A quick implementation of polyfill
    I think it *should* properly free allocated memory.
    Doesn't work with GeoPolygons with holes.

    `geos` should be a list of (lat, lng) tuples.

    """
    gp = GeoPolygon(geos)

    n = h3c.maxPolyfillSize(&gp.gp, res)
    hm = HexMem(n)

    h3c.polyfill(&gp.gp, res, hm.ptr)

    return hm


def h3_to_geo_boundary(H3int h, bool geo_json=False):
    """Compose an array of geo-coordinates that outlines a hexagonal cell"""
    cdef:
        h3c.GeoBoundary gb

    h3c.h3ToGeoBoundary(h, &gb)

    verts = tuple(
        coord2geo(gb.verts[i])
        for i in range(gb.num_verts)
    )

    if geo_json:
        #lat/lng -> lng/lat and last point same as first
        verts = tuple(tuple(reversed(v)) for v in verts)
        verts += (verts[0],)

    return verts

