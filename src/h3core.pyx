from cpython.mem cimport PyMem_Malloc, PyMem_Free
from libc.string cimport memset

from cpython cimport bool
from libc.math cimport pi

cimport h3api

# why are we doing all this rad and mercator math? can the c library not do this automatically?
# two versions of functions? int/hex(str) versions?
# add neighbors/edges? https://uber.github.io/h3/#/documentation/api-reference/unidirectional-edges


# todo: c versions?
cdef h3api.H3Index hex2int(str h):
    return int(h, 16)

def int2hex(h3api.H3Index x):
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


cdef h3api.GeoCoord geo2coord(double lat, double lng):
    cdef:
        h3api.GeoCoord c

    c.lat = degs_to_rads(mercator_lat(lat))
    c.lng = degs_to_rads(mercator_lng(lng))

    return c


cdef (double, double) coord2geo(h3api.GeoCoord c):
    return (
        mercator_lat(rads_to_degs(c.lat)),
        mercator_lng(rads_to_degs(c.lng))
    )


cpdef str geo_to_h3(double lat, double lng, int res):
    # these cdef's are actually optional. they can be inferred
    cdef:
        h3api.GeoCoord c
        h3api.H3Index h

    c = geo2coord(lat, lng)
    h = h3api.geoToH3(&c, res)

    return int2hex(h)


cpdef (double, double) h3_to_geo(str h3_address):
    """Reverse lookup an h3 address into a geo-coordinate"""
    cdef:
        h3api.GeoCoord c

    h3api.h3ToGeo(hex2int(h3_address), &c)

    return coord2geo(c)


def is_valid(str h3_address):
    """Validates an `h3_address`

    :returns: boolean
    """
    try:
        return h3api.h3IsValid(hex2int(h3_address)) is 1
    except Exception:
        return False


def resolution(str h3_address):
    """Returns the resolution of an `h3_address`

    :return: nibble (0-15)
    """
    return int(h3_address[1], 16)


def parent(str h3_address, int res):
    h = hex2int(h3_address)
    h = h3api.h3ToParent(h, res)
    h = int2hex(h)

    return h


def distance(str h1, str h2):
    """ compute the hex-distance between two hexagons
    """
    d = h3api.h3Distance(
            hex2int(h1),
            hex2int(h2)
        )

    return d


cdef class HexMem:
    """ A small class to manage memory for H3Index arrays
    Memory is allocated and deallocated at object creation and garbage collection

    """
    cdef:
        # TODO: what if `n` is passed in (accidentally) as negative -- what
        # does the `unsigned` coercion do?
        unsigned int n
        h3api.H3Index* ptr

    def __cinit__(self, n):
        # TODO: saftey check for n>0?
        self.n = n
        self.ptr = <h3api.H3Index*> PyMem_Malloc(n * sizeof(h3api.H3Index))

        if not self.ptr:
            raise MemoryError()

        # h3c expects zero'd out memory in many cases
        memset(self.ptr, 0, len(self) * sizeof(h3api.H3Index))

    def __dealloc__(self):
        if self.ptr:
            PyMem_Free(self.ptr)
        self.ptr = NULL

    def hexset(self):
        """ Return set of hex strings
        """
        out = set(
            int2hex(self.ptr[i])
            for i in range(len(self))
            if self.ptr[i] != 0
        )
        return out

    def __len__(self):
        return self.n


    @staticmethod
    cdef HexMem from_hexes(set hexes):
        hm = HexMem(
            len(hexes)
        )

        for i, h in enumerate(hexes):
            hm.ptr[i] = hex2int(h)

        return hm


def h3_to_geo_boundary(str h3_address, bool geo_json=False):
    """Compose an array of geo-coordinates that outlines a hexagonal cell"""
    cdef:
        h3api.GeoBoundary gb

    h3api.h3ToGeoBoundary(hex2int(h3_address), &gb)

    verts = tuple(
        coord2geo(gb.verts[i])
        for i in range(gb.num_verts)
    )

    if geo_json:
        #lat/lng -> lng/lat and last point same as first
        verts = tuple(tuple(reversed(v)) for v in verts)
        verts += (verts[0],)

    return verts


def k_ring(str h3_address, int ring_size):
    hm = HexMem(
        h3api.maxKringSize(ring_size)
    )

    h3api.kRing(hex2int(h3_address), ring_size, hm.ptr)

    out = hm.hexset()

    return out


def hex_ring(str h3_address, int ring_size):
    """
    Get a hexagon ring for a given hexagon.
    Returns individual rings, unlike `k_ring`.

    If a pentagon is reachable, falls back to a
    MUCH slower form based on `k_ring`.
    """

    hm = HexMem(
        6 * ring_size if ring_size > 0 else 1
    )

    flag = h3api.hexRing(hex2int(h3_address), ring_size, hm.ptr)

    if flag == 0:
        out = hm.hexset()
    else:
        # C-style, so this is a failure case
        # might have hit a pentagon?
        out = k_ring(h3_address, ring_size  ) - \
              k_ring(h3_address, ring_size-1)

    return out


def children(str h3_address, int res):
    h = hex2int(h3_address)

    hm = HexMem(
        h3api.maxH3ToChildrenSize(h, res)
    )

    h3api.h3ToChildren(h, res, hm.ptr)

    return hm.hexset()


cdef h3api.Geofence make_geofence(geos):
    cdef:
        h3api.Geofence gf

    gf.numVerts = len(geos)

    # todo: figure out when/how to free this memory
    gf.verts = <h3api.GeoCoord*> PyMem_Malloc(gf.numVerts * sizeof(h3api.GeoCoord))

    for i, (lat, lng) in enumerate(geos):
        gf.verts[i] = geo2coord(lat, lng)

    return gf


cdef class GeoPolygon:
    """ Basic version of GeoPolygon

    Doesn't work with holes.
    """
    cdef:
        h3api.GeoPolygon gp

    def __cinit__(self, geos):
        self.gp.numHoles = 0
        self.gp.holes = NULL
        self.gp.geofence = make_geofence(geos)

    def __dealloc__(self):
        PyMem_Free(self.gp.geofence.verts)


# todo: nogil for expensive C operation?
def polyfill(geos, int res):
    """ A quick implementation of polyfill
    I think it *should* properly free allocated memory.
    Doesn't work with GeoPolygons with holes.

    `geos` should be a list of (lat, lng) tuples.

    """
    gp = GeoPolygon(geos)
    hm = HexMem(
        h3api.maxPolyfillSize(&gp.gp, res)
    )

    h3api.polyfill(&gp.gp, res, hm.ptr)

    return hm.hexset()

# todo: nogil for expensive C operation?
def compact(hexes):
    hu = HexMem.from_hexes(hexes)
    hc = HexMem(len(hu))

    flag = h3api.compact(hu.ptr, hc.ptr, len(hu))

    if flag != 0:
        raise ValueError('Could not compact set of hexagons!')

    return hc.hexset()

# todo: nogil for expensive C operation?
def uncompact(hexes, int res):
    hc = HexMem.from_hexes(hexes)

    hu = HexMem(
        h3api.maxUncompactSize(hc.ptr, len(hc), res)
    )

    flag = h3api.uncompact(
        hc.ptr, len(hc),
        hu.ptr, len(hu),
        res
    )

    if flag != 0:
        raise ValueError('Could not uncompact set of hexagons!')

    return hu.hexset()


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
