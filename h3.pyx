cimport _h3

cdef class GeoCoord:
    cdef _h3.GeoCoord _coord

    cdef to_h3(self, int resolution):
        return _h3.geoToH3(&self._coord, resolution)

cdef GeoCoord h3_to_geo(_h3.H3Index address):
    coord = GeoCoord()
    _h3.h3ToGeo(address, &coord._coord)
    return coord

cdef class GeoBoundary:
    cdef _h3.GeoBoundary _boundary

cdef GeoBoundary h3_to_geo_boundary(_h3.H3Index address):
    boundary = GeoBoundary()
    _h3.h3ToGeoBoundary(address, &boundary._boundary)
    return boundary
