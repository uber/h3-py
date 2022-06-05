from libc cimport stdlib
from libc.stdint cimport uint64_t

cimport h3lib
from h3lib cimport bool, H3int, H3Error

from .util cimport (
    check_cell,
    check_edge,
    check_res,
    create_ptr,
    create_mv,
    deg2coord,
    coord2deg,
)
from .util import H3ValueError

from .memory cimport H3MemoryManager


cpdef H3int geo_to_h3(double lat, double lng, int res) except 1:
    cdef:
        h3lib.LatLng c
        H3int out
        h3lib.H3Error err

    check_res(res)
    c = deg2coord(lat, lng)

    # todo: just ignoring the error for now, check in the future
    err = h3lib.latLngToCell(&c, res, &out)

    if err:
        raise H3ValueError()

    return out


cpdef (double, double) h3_to_geo(H3int h) except *:
    """Map an H3 cell into its centroid geo-coordinate (lat/lng)"""
    cdef:
        h3lib.LatLng c
        h3lib.H3Error err

    check_cell(h)

    err = h3lib.cellToLatLng(h, &c)
    if err:
        raise H3ValueError()

    return coord2deg(c)


cdef h3lib.GeoLoop make_geoloop(geos, bool lnglat_order=False) except *:
    """

    The returned `GeoLoop` must be freed with a call to `free_geoloop`.

    Parameters
    ----------
    geos : list or tuple
        GeoLoop: A sequence of >= 3 (lat, lng) pairs where the last
        element may or may not be same as the first (to form a closed loop).
        The order of the pairs may be either clockwise or counterclockwise.
    lnglat_order : bool
        If True, assume coordinate pairs like (lng, lat)
        If False, assume coordinate pairs like (lat, lng)
    """
    cdef:
        h3lib.GeoLoop gl

    gl.numVerts = len(geos)

    # todo: need for memory management
    gl.verts = <h3lib.LatLng*> stdlib.calloc(gl.numVerts, sizeof(h3lib.LatLng))

    if lnglat_order:
        latlng = (g[::-1] for g in geos)
    else:
        latlng = geos

    for i, (lat, lng) in enumerate(latlng):
        gl.verts[i] = deg2coord(lat, lng)

    return gl


cdef free_geoloop(h3lib.GeoLoop* gl):
    stdlib.free(gl.verts)
    gl.verts = NULL


cdef class GeoPolygon:
    cdef:
        h3lib.GeoPolygon gp

    def __cinit__(self, outer, holes=None, bool lnglat_order=False):
        """

        Parameters
        ----------
        outer : list or tuple
            GeoLoop
            A GeoLoop is a sequence of >= 3 (lat, lng) pairs where the last
            element may or may not be same as the first (to form a closed loop).
            The order of the pairs may be either clockwise or counterclockwise.
        holes : list or tuple
            A sequence of GeoLoops
        lnglat_order : bool
        If True, assume coordinate pairs like (lng, lat)
        If False, assume coordinate pairs like (lat, lng)

        """
        if holes is None:
            holes = []

        self.gp.geoloop = make_geoloop(outer, lnglat_order)
        self.gp.numHoles = len(holes)
        self.gp.holes = NULL

        if len(holes) > 0:
            self.gp.holes =  <h3lib.GeoLoop*> stdlib.calloc(len(holes), sizeof(h3lib.GeoLoop))
            for i, hole in enumerate(holes):
                self.gp.holes[i] = make_geoloop(hole, lnglat_order)


    def __dealloc__(self):
        free_geoloop(&self.gp.geoloop)

        for i in range(self.gp.numHoles):
            free_geoloop(&self.gp.holes[i])

        stdlib.free(self.gp.holes)


def polyfill_polygon(outer, int res, holes=None, bool lnglat_order=False):
    """ Set of hexagons whose center is contained in a polygon.

    The polygon is defined as in the GeoJson standard, with an exterior
    LinearRing `outer` and a list of LinearRings `holes`, which define any
    holes in the polygon.

    Each LinearRing may be in clockwise or counter-clockwise order
    (right-hand rule or not), and may or may not be a closed loop (where the last
    element is equal to the first).
    The GeoJSON spec requires the right-hand rule, and a closed loop, but
    this function will work with any input format.

    Parameters
    ----------
    outer : list or tuple
        A LinearRing, a sequence of (lat/lng) or (lng/lat) pairs
    res : int
        The resolution of the output hexagons
    holes : list or tuple
        A collection of LinearRings, describing any holes in the polygon
    lnglat_order : bool
        If True, assume coordinate pairs like (lng, lat)
        If False, assume coordinate pairs like (lat, lng)
    """
    cdef:
        uint64_t n

    check_res(res)
    gp = GeoPolygon(outer, holes=holes, lnglat_order=lnglat_order)

    h3lib.maxPolygonToCellsSize(&gp.gp, res, 0, &n)
    ptr = create_ptr(n)

    h3lib.polygonToCells(&gp.gp, res, 0, ptr)
    mv = create_mv(ptr, n)

    return mv


def polyfill_geojson(geojson, int res):
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

    out = polyfill_polygon(coords[0], res, holes=coords[1:], lnglat_order=True)

    return out


def polyfill(dict geojson, int res, bool geo_json_conformant=False):
    """ Light wrapper around `polyfill_geojson` to provide backward compatibility.
    """

    try:
        gj_type = geojson['type']
    except KeyError:
        raise KeyError("`geojson` dict must have key 'type'.") from None

    if gj_type != 'Polygon':
        raise ValueError('Only Polygon GeoJSON supported')

    if geo_json_conformant:
        out = polyfill_geojson(geojson, res)
    else:
        coords = geojson['coordinates']
        out = polyfill_polygon(coords[0], res, holes=coords[1:], lnglat_order=False)

    return out


def cell_boundary(H3int h, bool geo_json=False):
    """Compose an array of geo-coordinates that outlines a hexagonal cell"""
    cdef:
        h3lib.CellBoundary gb

    check_cell(h)

    h3lib.cellToBoundary(h, &gb)

    verts = tuple(
        coord2deg(gb.verts[i])
        for i in range(gb.num_verts)
    )

    if geo_json:
        #lat/lng -> lng/lat and last point same as first
        verts += (verts[0],)
        verts = tuple(v[::-1] for v in verts)

    return verts


def edge_boundary(H3int edge, bool geo_json=False):
    """ Returns the CellBoundary containing the coordinates of the edge
    """
    cdef:
        h3lib.CellBoundary gb

    check_edge(edge)

    h3lib.directedEdgeToBoundary(edge, &gb)

    # todo: move this verts transform into the CellBoundary object
    verts = tuple(
        coord2deg(gb.verts[i])
        for i in range(gb.num_verts)
    )

    if geo_json:
        #lat/lng -> lng/lat and last point same as first
        verts += (verts[0],)
        verts = tuple(v[::-1] for v in verts)

    return verts


cpdef double point_dist(
    double lat1, double lng1,
    double lat2, double lng2, unit='km') except -1:

    a = deg2coord(lat1, lng1)
    b = deg2coord(lat2, lng2)

    if unit == 'rads':
        d = h3lib.distanceRads(&a, &b)
    elif unit == 'km':
        d = h3lib.distanceKm(&a, &b)
    elif unit == 'm':
        d = h3lib.distanceM(&a, &b)
    else:
        raise H3ValueError('Unknown unit: {}'.format(unit))

    return d
