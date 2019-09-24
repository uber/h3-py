cimport h3lib
from .h3utils cimport check_addr, check_edge, check_res, create_mv, create_ptr
from libc cimport stdlib


cdef (double, double) mercator(double lat, double lng):
    """Helper coerce lat/lng range"""
    lat = lat - 180 if lat > 90  else lat
    lng = lng - 360 if lng > 180 else lng

    return lat, lng


cdef h3lib.GeoCoord geo2coord(double lat, double lng):
    cdef:
        h3lib.GeoCoord c

    lat, lng = mercator(lat, lng)
    c.lat = h3lib.degsToRads(lat)
    c.lng = h3lib.degsToRads(lng)

    return c


cdef (double, double) coord2geo(h3lib.GeoCoord c):
    return mercator(
        h3lib.radsToDegs(c.lat),
        h3lib.radsToDegs(c.lng)
    )


cdef h3lib.Geofence make_geofence(geos):
    cdef:
        h3lib.Geofence gf

    gf.numVerts = len(geos)

    # todo: figure out when/how to free this memory
    gf.verts = <h3lib.GeoCoord*> stdlib.calloc(gf.numVerts, sizeof(h3lib.GeoCoord))

    for i, (lat, lng) in enumerate(geos):
        gf.verts[i] = geo2coord(lat, lng)

    return gf


cdef class GeoPolygon:
    """ Basic version of GeoPolygon
    Doesn't work with holes.
    """
    cdef:
        h3lib.GeoPolygon gp

    def __cinit__(self, geos):
        self.gp.numHoles = 0
        self.gp.holes = NULL
        self.gp.geofence = make_geofence(geos)

    def __dealloc__(self):
        if self.gp.geofence.verts:
            stdlib.free(self.gp.geofence.verts)
        self.gp.geofence.verts = NULL



cpdef h3lib.H3int geo_to_h3(double lat, double lng, int res) except 1:
    cdef:
        h3lib.GeoCoord c

    check_res(res)

    c = geo2coord(lat, lng)

    return h3lib.geoToH3(&c, res)


cpdef (double, double) h3_to_geo(h3lib.H3int h) except *:
    """Reverse lookup an h3 address into a geo-coordinate"""
    cdef:
        h3lib.GeoCoord c

    check_addr(h)

    h3lib.h3ToGeo(h, &c)

    return coord2geo(c)


# todo: nogil for expensive C operation?
def polyfill(geos, int res):
    """ A quick implementation of polyfill
    I think it *should* properly free allocated memory.
    Doesn't work with GeoPolygons with holes.
    `geos` should be a list of (lat, lng) tuples.
    """
    #check_res(res)

    gp = GeoPolygon(geos)

    n = h3lib.maxPolyfillSize(&gp.gp, res)
    ptr = create_ptr(n)

    h3lib.polyfill(&gp.gp, res, ptr)
    mv = create_mv(ptr, n)

    return mv


def cell_boundary(h3lib.H3int h, geo_json=False):
    """Compose an array of geo-coordinates that outlines a hexagonal cell"""
    cdef:
        h3lib.GeoBoundary gb

    check_addr(h)

    h3lib.h3ToGeoBoundary(h, &gb)

    verts = tuple(
        coord2geo(gb.verts[i])
        for i in range(gb.num_verts)
    )

    if geo_json:
        #lat/lng -> lng/lat and last point same as first
        verts = tuple(tuple(reversed(v)) for v in verts)
        verts += (verts[0],)

    return verts

def edge_boundary(h3lib.H3int edge):
    """ Returns the GeoBoundary containing the coordinates of the edge
    """
    cdef:
        h3lib.GeoBoundary gb

    check_edge(edge)

    h3lib.getH3UnidirectionalEdgeBoundary(edge, &gb)

    # todo: move this verts transform into the GeoBoundary object
    verts = tuple(
        coord2geo(gb.verts[i])
        for i in range(gb.num_verts)
    )

    return verts