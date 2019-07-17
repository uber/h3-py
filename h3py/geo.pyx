from libc cimport stdlib

cimport h3py.h3api as h3c
from h3py.h3api cimport H3int, H3str

from h3py.util cimport create_ptr, create_mv

cimport h3py.util as u



cdef (double, double) mercator(double lat, double lng):
    """Helper coerce lat/lng range"""
    lat = lat - 180 if lat > 90  else lat
    lng = lng - 360 if lng > 180 else lng

    return lat, lng


cdef h3c.GeoCoord geo2coord(double lat, double lng):
    cdef:
        h3c.GeoCoord c

    lat, lng = mercator(lat, lng)
    c.lat = h3c.degsToRads(lat)
    c.lng = h3c.degsToRads(lng)

    return c


cdef (double, double) coord2geo(h3c.GeoCoord c):
    return mercator(
        h3c.radsToDegs(c.lat),
        h3c.radsToDegs(c.lng)
    )


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



cpdef H3int geo_to_h3(double lat, double lng, int res) except 1:
    cdef:
        h3c.GeoCoord c

    u._v_res(res)

    c = geo2coord(lat, lng)

    return h3c.geoToH3(&c, res)


cpdef (double, double) h3_to_geo(H3int h) except *:
    """Reverse lookup an h3 address into a geo-coordinate"""
    cdef:
        h3c.GeoCoord c

    u._v_addr(h)

    h3c.h3ToGeo(h, &c)

    return coord2geo(c)


# todo: nogil for expensive C operation?
def polyfill(geos, int res):
    """ A quick implementation of polyfill
    I think it *should* properly free allocated memory.
    Doesn't work with GeoPolygons with holes.

    `geos` should be a list of (lat, lng) tuples.

    """
    #u._v_res(res)

    gp = GeoPolygon(geos)

    n = h3c.maxPolyfillSize(&gp.gp, res)
    ptr = create_ptr(n)

    h3c.polyfill(&gp.gp, res, ptr)
    mv = create_mv(ptr, n)

    return mv


def h3_to_geo_boundary(H3int h, geo_json=False):
    """Compose an array of geo-coordinates that outlines a hexagonal cell"""
    cdef:
        h3c.GeoBoundary gb

    u._v_addr(h)

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

def uni_edge_boundary(H3int edge):
    """ Returns the GeoBoundary containing the coordinates of the edge
    """
    cdef:
        h3c.GeoBoundary gb

    u._v_edge(edge)

    h3c.getH3UnidirectionalEdgeBoundary(edge, &gb)

    # todo: move this verts transform into the GeoBoundary object
    verts = tuple(
        coord2geo(gb.verts[i])
        for i in range(gb.num_verts)
    )

    return verts
