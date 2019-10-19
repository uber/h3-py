cimport h3lib
from h3lib cimport H3int
from .util cimport check_addr


# need to define coord2geo here because of this Cython bug:
# https://github.com/cython/cython/issues/2745
cdef (double, double) mercator(double lat, double lng):
    """Helper to coerce lat/lng range"""
    lat = lat - 180 if lat > 90  else lat
    lng = lng - 360 if lng > 180 else lng

    return lat, lng


cdef (double, double) coord2geo(h3lib.GeoCoord c):
    return mercator(
        h3lib.radsToDegs(c.lat),
        h3lib.radsToDegs(c.lng)
    )

# todo: it's driving me crazy that these three functions are all essentially the same linked list walker...
# grumble: no way to do iterators in with cdef functions!
cdef walk_polys(const h3lib.LinkedGeoPolygon* L):
    out = []
    while L:
        out += [walk_loops(L.data)]
        L = L.next

    return out


cdef walk_loops(const h3lib.LinkedGeoLoop* L):
    out = []
    while L:
        out += [walk_coords(L.data)]
        L = L.next

    return out


cdef walk_coords(const h3lib.LinkedGeoCoord* L):
    out = []
    while L:
        out += [coord2geo(L.data)]
        L = L.next

    return out


# todo: loop_to_geojson
# todo: poly_to_geojson
# todo: multipoly_to_geojson
def h3_set_to_multi_polygon(const H3int[:] hexes):
    cdef:
        h3lib.LinkedGeoPolygon polygon

    # todo: should we have a helper that checks a collection of inputs?
    for h in hexes:
        check_addr(h) # todo: maybe should name this `check_index`?

    h3lib.h3SetToLinkedGeo(&hexes[0], len(hexes), &polygon)

    out = walk_polys(&polygon)

    # does this thing dealloc the passed in poly address?
    h3lib.destroyLinkedPolygon(&polygon)

    return out
