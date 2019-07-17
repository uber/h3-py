from libc cimport stdlib
from cython.view cimport array

from h3py.h3api cimport H3int, H3str
cimport h3py.h3api as h3c

# todo: should we use C API functions instead? (stringToH3 and h3ToString)
cpdef H3int hex2int(H3str h):
    return int(h, 16)

cpdef H3str int2hex(H3int x):
    return hex(x)[2:]


class H3ValueError(ValueError):
    pass

class InvalidH3Address(H3ValueError):
    pass

class InvalidH3Edge(H3ValueError):
    pass

class InvalidH3Resolution(H3ValueError):
    pass


# rename to: valid_cell, valid_addr? check_cell? raise_cell?
# prefix with util...?
cdef _v_addr(H3int h):
    if h3c.h3IsValid(h) == 0:
        raise InvalidH3Address(h)

cdef _v_edge(H3int e):
    if h3c.h3UnidirectionalEdgeIsValid(e) == 0:
        raise InvalidH3Edge(e)

cdef _v_res(int res):
    if res < 0 or res > 15:
        raise InvalidH3Resolution(res)


## todo: can i turn these two into a context manager?
cdef H3int* create_ptr(size_t n):
    cdef H3int* ptr = <H3int*> stdlib.calloc(n, sizeof(H3int))
    if not ptr:
        raise MemoryError()

    return ptr


# todo: helper function that returns (ptr, n_new) does the resize and error checking
cdef H3int[:] create_mv(H3int* ptr, size_t n):
    cdef:
        array x

    n = move_nonzeros(ptr, n)
    ptr = <H3int*> stdlib.realloc(ptr, n*sizeof(H3int))

    if ptr is NULL:
        raise MemoryError()

    if n > 0:
        x = <H3int[:n]> ptr
        x.callback_free_data = stdlib.free

        return x
    else:
        return empty_memory_view()


cpdef H3int[:] from_iter(hexes):
    """ hexes needs to be an iterable that knows its size...
    or should we have it match the np.fromiter function, which infers if not available?
    """
    cdef:
        array x
        size_t n
    n = len(hexes)
    x = <H3int[:n]> stdlib.calloc(n, sizeof(H3int))
    x.callback_free_data = stdlib.free

    for i,h in enumerate(hexes):
        x[i] = h

    return x


cdef size_t move_nonzeros(H3int* a, size_t n):
    """ Move nonzero elements to front of array `a` of length `n`.

    Return the number of nonzero elements.
    """
    cdef:
        size_t i = 0
        size_t j = n

    while i < j:
        if a[j-1] == 0:
            j -= 1
            continue

        if a[i] != 0:
            i += 1
            continue

        # if we're here, we know:
        # a[i] == 0
        # a[j-1] != 0
        # i < j
        # so we can swap!
        # todo: what about j vs j-1 ....?
        a[i] = a[j-1]
        j -= 1

    return i


cdef inline H3int[:] empty_memory_view():
    # there's gotta be a better way to do this...
    # create an empty cython.view.array?
    cdef:
        H3int a[1]

    return (<H3int[:]>a)[:0]



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

    def __cinit__(self, geos):
        self.gp.numHoles = 0
        self.gp.holes = NULL
        self.gp.geofence = make_geofence(geos)

    def __dealloc__(self):
        if self.gp.geofence.verts:
            stdlib.free(self.gp.geofence.verts)
        self.gp.geofence.verts = NULL
