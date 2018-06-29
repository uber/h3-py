cimport libc.stdlib
from cpython.mem cimport PyMem_Malloc, PyMem_Realloc, PyMem_Free
cimport _h3core


cdef class GeoCoord:
    cdef _h3core.GeoCoord _coord

    @property
    def lat(self):
        return self._coord.lat

    @property
    def lng(self):
        return self._coord.lon

    cpdef _h3core.H3Index to_h3(self, int resolution):
        return _h3core.geoToH3(&self._coord, resolution)


cdef GeoCoord h3_to_geo(_h3core.H3Index address):
    coord = GeoCoord()
    _h3core.h3ToGeo(address, &coord._coord)
    return coord


cdef class GeoBoundary:
    cdef _h3core.GeoBoundary _boundary

    def __cinit__(self):
        self._boundary.numVerts = 0

    @property
    def num_verts(self):
        return self._boundary.numVerts

    @property
    def verts(self):
        return [self._boundary.verts[i] for i in range(self._boundary.numVerts)]


cdef GeoBoundary h3_to_geo_boundary(_h3core.H3Index address):
    boundary = GeoBoundary()
    _h3core.h3ToGeoBoundary(address, &boundary._boundary)
    return boundary


cdef class Geofence:
    cdef _h3core.Geofence _fence
    cdef bint _owned

    def __cinit__(self):
        self._fence.verts = NULL
        self._fence.numVerts = 0
        self._owned = False

    def __dealloc__(self):
        if self._owned:
            libc.stdlib.free(self._fence.verts)

    @property
    def num_verts(self):
        return self._fence.numVerts

    @property
    def verts(self):
        return [self._fence.verts[i] for i in range(self._fence.numVerts)]


cdef class GeoJsonLite:
    cdef _h3core.GeoPolygon _polygon

    def __cinit__(self):
        self._polygon.geofence = _h3core.Geofence()
        self._polygon.numHoles = 0
        self._polygon.holes = NULL

#    def __deinit__(self):
#        libc.stdlib.free(self._polygon.holes)
#        libc.stdlib.free(self._polygon.geofence.verts)

    @property
    def geofence(self):
        fence = Geofence()
        fence._fence = self._polygon.geofence
        return fence

    @property
    def num_holes(self):
        return self._polygon.numHoles

    @property
    def holes(self):
        return [self._polygen.holes[i] for i in range(self._polygon.numHoles)]
