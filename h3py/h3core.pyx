from libc cimport stdlib
from h3py.hexmem cimport HexMem, from_ints

from cpython cimport bool
from libc.math cimport pi

cimport h3py.h3api as h3c
from h3py.h3api cimport H3int, H3str


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


cpdef bool is_valid(H3int h):
    """Validates an `h3_address`

    :returns: boolean
    """
    try:
        return h3c.h3IsValid(h) is 1
    except Exception:
        return False

cpdef int resolution(H3int h):
    """Returns the resolution of an `h3_address`
    0--15
    """
    return h3c.h3GetResolution(h)


cpdef H3int parent(H3int h, int res):
    return h3c.h3ToParent(h, res)


cpdef int distance(H3int h1, H3int h2):
    """ compute the hex-distance between two hexagons
    """
    d = h3c.h3Distance(h1,h2)

    return d

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




cpdef HexMem k_ring(H3int h, int ring_size):
    n = h3c.maxKringSize(ring_size)
    hm = HexMem(n)

    h3c.kRing(h, ring_size, hm.ptr)

    return hm

cpdef HexMem hex_ring(H3int h, int ring_size):
    """
    Get a hexagon ring for a given hexagon.
    Returns individual rings, unlike `k_ring`.

    If a pentagon is reachable, falls back to a
    MUCH slower form based on `k_ring`.
    """
    n = 6*ring_size if ring_size > 0 else 1
    hm = HexMem(n)

    flag = h3c.hexRing(h, ring_size, hm.ptr)

    if flag != 0:
        s1 = k_ring(h, ring_size).set_int()
        s2 = k_ring(h, ring_size - 1).set_int()
        hm = from_ints(s1-s2)

    return hm



cpdef HexMem children(H3int h, int res):
    n = h3c.maxH3ToChildrenSize(h, res)
    hm = HexMem(n)

    h3c.h3ToChildren(h, res, hm.ptr)

    return hm



cpdef HexMem compact(const H3int[:] hu):
    hc = HexMem(len(hu))

    flag = h3c.compact(&hu[0], hc.ptr, len(hu))

    if flag != 0:
        raise ValueError('Could not compact set of hexagons!')

    return hc


cpdef HexMem uncompact(const H3int[:] hc, int res):
    N = h3c.maxUncompactSize(&hc[0], len(hc), res)
    hu = HexMem(N)

    flag = h3c.uncompact(
        &hc[0], len(hc),
        hu.ptr, len(hu),
        res
    )

    if flag != 0:
        raise ValueError('Could not uncompact set of hexagons!')

    # we need to keep the HexMem object around to keep the memory from getting freed
    return hu


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




