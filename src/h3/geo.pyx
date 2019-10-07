cimport h3lib
from .util cimport (
    check_addr,
    check_edge,
    check_res,
    create_ptr,
    create_mv,
)
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


cpdef h3lib.H3int geo_to_h3(double lat, double lng, int res) except 1:
    cdef:
        h3lib.GeoCoord c

    check_res(res)

    c = geo2coord(lat, lng)

    return h3lib.geoToH3(&c, res)


cpdef (double, double) h3_to_geo(h3lib.H3int h) except *:
    """Map an H3 cell into its centroid geo-coordinate (lat/lng)"""
    cdef:
        h3lib.GeoCoord c

    check_addr(h)

    h3lib.h3ToGeo(h, &c)

    return coord2geo(c)


cdef h3lib.Geofence make_geofence(geos):
    cdef:
        h3lib.Geofence gf

    gf.numVerts = len(geos)

    # todo: figure out when/how to free this memory
    gf.verts = <h3lib.GeoCoord*> stdlib.calloc(gf.numVerts, sizeof(h3lib.GeoCoord))

    for i, (lat, lng) in enumerate(geos):
        gf.verts[i] = geo2coord(lat, lng)

    return gf


cdef free_geofence(h3lib.Geofence* gf):
    if gf.verts:
        stdlib.free(gf.verts)
    gf.verts = NULL


cdef class GeoPolygon:
    """ Basic version of GeoPolygon

    """
    cdef:
        h3lib.GeoPolygon gp

    def __cinit__(self, outer, holes=None):
        """

        Parameters
        ----------
        outer : list or tuple
            GeoFence
            A GeoFence is a sequence of >= 4 (lat, lng) pairs where the last
            element is the same as the first.
        holes : list or tuple
            A sequence of GeoFences

        """
        if holes is None:
            holes = []

        self.gp.geofence = make_geofence(outer)
        self.gp.numHoles = len(holes)
        self.gp.holes = NULL

        if len(holes) > 0:
            self.gp.holes =  <h3lib.Geofence*> stdlib.calloc(len(holes), sizeof(h3lib.Geofence))
            for i, hole in enumerate(holes):
                self.gp.holes[i] = make_geofence(hole)


    def __dealloc__(self):
        free_geofence(&self.gp.geofence)

        for i in range(self.gp.numHoles):
            free_geofence(&self.gp.holes[i])

        stdlib.free(self.gp.holes)


def _swap_coord_order(linear_ring):
    """ Swap order between lat/lng <=> lng/lat in sequence of coordinates.

    A LinearRing (as defined by GeoJson) is a sequence of >= 4 (lat, lng) or
    (lng, lat) pairs where the last pair is the same as the first.
    """
    out = [
        p[::-1]
        for p in linear_ring
    ]

    return out


def polyfill_polygon(outer, holes=None, int res=9, order='latlng'):
    """ Set of hexagons whose center is contained in a polygon.

    The polygon is defined as in the GeoJson standard, with an exterior
    LinearRing `outer` and a list of LinearRings `holes`, which define any
    holes in the polygon.

    Parameters
    ----------
    outer : list or tuple
        A LinearRing, a sequence of (lat/lng) or (lng/lat) pairs
    holes : list or tuple
        A collection of LinearRings, describing any holes in the polygon
    res : int
        The resolution of the output hexagons
    order : str
        'latlng' or 'lnglat'
        Describe the expected order of the coordinate pairs
    """

    #check_res(res)

    if order == 'latlng':
        pass
    elif order == 'lnglat':
        outer = _swap_coord_order(outer)
        if holes:
            holes = [_swap_coord_order(h) for h in holes]
    else:
        raise ValueError("`order` parameter must be either 'latlng' or 'lnglat'.")

    gp = GeoPolygon(outer, holes)

    n = h3lib.maxPolyfillSize(&gp.gp, res)
    ptr = create_ptr(n)

    h3lib.polyfill(&gp.gp, res, ptr)
    mv = create_mv(ptr, n)

    return mv


def polyfill_geojson(geojson, int res=9):
    """ Set of hexagons whose center is contained in a GeoJson Polygon object.

    The polygon is defined exactly as in the GeoJson standard, so
    `geojson` should be a dictionary like:
    {
        'type': 'Polygon',
        'coordinates': [...]
    }

    'coordinates' should be a list of LinearRings, where the first ring describes
    the exterior boundary of the Polygon, and any subsequent LinearRings
    describe holes in the polygon.

    Note that we don't provide an option for the order of the coordinates,
    as the GeoJson standard requires them to be in lng/lat order.

    Parameters
    ----------
    geojson : dict
    res : int
        The resolution of the output hexagons
    """

    # todo: this one could handle multipolygons...

    if geojson['type'] != 'Polygon':
        raise ValueError('Only Polygon GeoJSON supported')

    coords = geojson['coordinates']

    out = polyfill_polygon(coords[0], holes=coords[1:], res=res, order='lnglat')

    return out





def polyfill(geojson, int res, geo_json_conformant=False):
    """ Light wrapper around `polyfill_geojson` to provide backward compatibility.
    """

    gj = geojson.copy()
    if not geo_json_conformant:
        gj['coordinates'] = [_swap_coord_order(h) for h in gj['coordinates']]

    return polyfill_geojson(gj, res)


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