from cpython.mem cimport PyMem_Malloc, PyMem_Free

from cpython cimport bool
from libc.math cimport pi

cimport _h3core as h3c

# why are we doing all this rad and mercator math? can the c library not do this automatically?
# two versions of functions? int/hex(str) versions?


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
    h3c.kRing(hex2int(h3_address), ring_size, hm.hexptr)

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

    flag = h3c.hexRing(hex2int(h3_address), ring_size, hm.hexptr)

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
        h3c.H3Index* hexptr

    def __cinit__(self, array_len):
        self.array_len = array_len
        self.hexptr = <h3c.H3Index*> PyMem_Malloc(array_len * sizeof(h3c.H3Index))
        # question: do we need to zero out memory before operations?

        if not self.hexptr:
            raise MemoryError()

    def __dealloc__(self):
        PyMem_Free(self.hexptr)

    def hexset(self):
        """ Return set of hex strings
        """
        out = set(
                int2hex(self.hexptr[i])
                for i in range(self.array_len)
                if self.hexptr[i] != 0
            )
        return out


def h3_is_valid(str h3_address):
    """Validates an `h3_address`

    :returns: boolean
    """
    try:
        return h3c.h3IsValid(hex2int(h3_address)) is 1
    except Exception:
        return False


def h3_get_resolution(str h3_address):
    """Returns the resolution of an `h3_address`

    :return: nibble (0-15)
    """
    return int(h3_address[1], 16)


def h3_to_parent(str h3_address, int res):
    h = hex2int(h3_address)
    h = h3c.h3ToParent(h, res)
    h = int2hex(h)

    return h


def h3_to_children(str h3_address, int res):
    h = hex2int(h3_address)
    max_children = h3c.maxH3ToChildrenSize(h, res)

    hm = HexMem(max_children)

    h3c.h3ToChildren(h, res, hm.hexptr)

    return hm.hexset()


def h3distance(str h1, str h2):
    d = h3c.h3Distance(
            hex2int(h1),
            hex2int(h2)
        )

    return d


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
