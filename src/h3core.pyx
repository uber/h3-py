from cpython.mem cimport PyMem_Malloc, PyMem_Free

from cpython cimport bool
from libc.math cimport pi

cimport _h3core as h3c

# why are we doing all this rad and mercator math? can the c library not do this automatically?
# two versions of functions? int/hex(str) versions?
# add neighbors/edges? https://uber.github.io/h3/#/documentation/api-reference/unidirectional-edges


# todo: c versions?
cdef h3c.H3Index hex2int(str h):
    return int(h, 16)

def int2hex(h3c.H3Index x):
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


cpdef str geo_to_h3(double lat, double lng, int res):
    # these cdef's are actually optional. they can be inferred
    cdef:
        h3c.GeoCoord c
        h3c.H3Index h

    c = geo2coord(lat, lng)
    h = h3c.geoToH3(&c, res)

    return int2hex(h)


cpdef (double, double) h3_to_geo(str h3_address):
    """Reverse lookup an h3 address into a geo-coordinate"""
    cdef:
        h3c.GeoCoord c

    h3c.h3ToGeo(hex2int(h3_address), &c)

    return coord2geo(c)


def h3_to_geo_boundary(str h3_address, bool geo_json=False):
    """Compose an array of geo-coordinates that outlines a hexagonal cell"""
    cdef:
        h3c.GeoBoundary gb

    h3c.h3ToGeoBoundary(hex2int(h3_address), &gb)

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
    hm = HexMem(h3c.maxKringSize(ring_size))

    # todo: does this guarantee all non-hex elements will be zeroed out?
    # do we need to pre-set our memory to zero?
    h3c.kRing(hex2int(h3_address), ring_size, hm.ptr)

    out = hm.hexset()

    return out


def hex_ring(str h3_address, int ring_size):
    """
    Get a hexagon ring for a given hexagon.
    Returns individual rings, unlike `k_ring`.

    If a pentagon is reachable, falls back to a
    MUCH slower form based on `k_ring`.
    """

    array_len = 6 * ring_size if ring_size > 0 else 1

    hm = HexMem(array_len)

    flag = h3c.hexRing(hex2int(h3_address), ring_size, hm.ptr)

    if flag == 0:
        out = hm.hexset()
    else:
        # C-style, so this is a failure case
        # might have hit a pentagon?
        out = k_ring(h3_address, ring_size  ) - \
              k_ring(h3_address, ring_size-1)

    return out


cdef class HexMem:
    """ A small class to manage memory for H3Index arrays
    Memory is allocated and deallocated at object creation and garbage collection

    """
    cdef:
        unsigned int array_len
        h3c.H3Index* ptr

    def __cinit__(self, array_len):
        self.array_len = array_len
        self.ptr = <h3c.H3Index*> PyMem_Malloc(array_len * sizeof(h3c.H3Index))
        # question: do we need to zero out memory before operations?

        if not self.ptr:
            raise MemoryError()

        # yeah, it looks like we really do have to zero out the memory. otherwise, `compact` messes up
        # what's the fast way to do this with C?
        for i in range(self.array_len):
            self.ptr[i] = 0

    def __dealloc__(self):
        PyMem_Free(self.ptr)

    def hexset(self):
        """ Return set of hex strings
        """
        out = set(
                int2hex(self.ptr[i])
                for i in range(self.array_len)
                if self.ptr[i] != 0
            )
        return out

    def __len__(self):
        return self.array_len


# todo: can i make this a class method? static method?
cdef HexMem hm_from_hexes(hexes):
    # todo: convert to integers first?
    hexes = set(hexes)
    n = len(hexes)
    hm = HexMem(n)

    for i, h in enumerate(hexes):
        hm.ptr[i] = hex2int(h)

    return hm


def is_valid(str h3_address):
    """Validates an `h3_address`

    :returns: boolean
    """
    try:
        return h3c.h3IsValid(hex2int(h3_address)) is 1
    except Exception:
        return False


def resolution(str h3_address):
    """Returns the resolution of an `h3_address`

    :return: nibble (0-15)
    """
    return int(h3_address[1], 16)


def parent(str h3_address, int res):
    h = hex2int(h3_address)
    h = h3c.h3ToParent(h, res)
    h = int2hex(h)

    return h


def children(str h3_address, int res):
    h = hex2int(h3_address)
    max_children = h3c.maxH3ToChildrenSize(h, res)

    hm = HexMem(max_children)

    h3c.h3ToChildren(h, res, hm.ptr)

    return hm.hexset()


def distance(str h1, str h2):
    """ compute the hex-distance between two hexagons
    """
    d = h3c.h3Distance(
            hex2int(h1),
            hex2int(h2)
        )

    return d


cdef h3c.Geofence make_geofence(geos):
    cdef:
        h3c.Geofence gf

    gf.numVerts = len(geos)

    # todo: figure out when/how to free this memory
    gf.verts = <h3c.GeoCoord*> PyMem_Malloc(gf.numVerts * sizeof(h3c.GeoCoord))

    for i, (lat, lng) in enumerate(geos):
        gf.verts[i] = geo2coord(lat, lng)

    return gf


cdef h3c.GeoPolygon make_geopolygon(geos):
    cdef:
        h3c.GeoPolygon gp

    gp.numHoles = 0
    gp.holes = NULL
    gp.geofence = make_geofence(geos)

    return gp


cdef int maxpolysize(geos, int res):
    # todo: make a python-accessible version, for easier testing?
    gp = make_geopolygon(geos)

    num = h3c.maxPolyfillSize(&gp, res)

    return num

# todo: nogil expensive C operation?
def polyfill(geos, int res):
    """ A quick, sloppy implementation of polyfill
    Works, but is inefficient with memory and doesn't free allocated memory.
    Doesn't work with GeoPolygons with holes.

    `geos` should be a list of (lat, lng) tuples.

    """
    array_len = maxpolysize(geos, res)

    hm = HexMem(array_len)

    # forming this poly multiple times... ok for now..
    gp = make_geopolygon(geos)
    # zero-out memory before?
    h3c.polyfill(&gp, res, hm.ptr)

    return hm.hexset()

# todo: nogil expensive C operation?
def compact(hexes):
    hm0 = hm_from_hexes(hexes)
    hm1 = HexMem(len(hm0))

    flag = h3c.compact(hm0.ptr, hm1.ptr, len(hm0))

    if flag != 0:
        raise ValueError('Could not compact set of hexagons!')

    return hm1.hexset()

# todo: nogil expensive C operation?
def uncompact(hexes, int res):
    hm0 = hm_from_hexes(hexes)

    max_hexes = h3c.maxUncompactSize(hm0.ptr, len(hm0), res)
    hm1 = HexMem(max_hexes)

    flag = h3c.uncompact(hm0.ptr, len(hm0), hm1.ptr, len(hm1), res)

    if flag != 0:
        raise ValueError('Could not uncompact set of hexagons!')

    return hm1.hexset()


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
