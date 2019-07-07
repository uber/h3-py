
from h3py.hexmem cimport HexMem, from_ints

from cpython cimport bool

cimport h3py.h3api as h3c
from h3py.h3api cimport H3int, H3str

from h3py.geo import polyfill, h3_to_geo_boundary, geo_to_h3, h3_to_geo


cpdef bool is_valid(H3int h):
    """Validates an `h3_address`

    :returns: boolean
    """
    try:
        return h3c.h3IsValid(h) is 1
    except Exception:
        return False

cpdef int resolution(H3int h):
    """Returns the resolution of an `h3_address`
    0--15
    """
    return h3c.h3GetResolution(h)


cpdef H3int parent(H3int h, int res):
    return h3c.h3ToParent(h, res)


cpdef int distance(H3int h1, H3int h2):
    """ compute the hex-distance between two hexagons
    """
    d = h3c.h3Distance(h1,h2)

    return d

cpdef HexMem k_ring(H3int h, int ring_size):
    n = h3c.maxKringSize(ring_size)
    hm = HexMem(n)

    h3c.kRing(h, ring_size, hm.ptr)

    return hm

cpdef HexMem hex_ring(H3int h, int ring_size):
    """
    Get a hexagon ring for a given hexagon.
    Returns individual rings, unlike `k_ring`.

    If a pentagon is reachable, falls back to a
    MUCH slower form based on `k_ring`.
    """
    n = 6*ring_size if ring_size > 0 else 1
    hm = HexMem(n)

    flag = h3c.hexRing(h, ring_size, hm.ptr)

    if flag != 0:
        s1 = k_ring(h, ring_size).set_int()
        s2 = k_ring(h, ring_size - 1).set_int()
        hm = from_ints(s1-s2)

    return hm



cpdef HexMem children(H3int h, int res):
    n = h3c.maxH3ToChildrenSize(h, res)
    hm = HexMem(n)

    h3c.h3ToChildren(h, res, hm.ptr)

    return hm



cpdef HexMem compact(const H3int[:] hu):
    hc = HexMem(len(hu))

    flag = h3c.compact(&hu[0], hc.ptr, len(hu))

    if flag != 0:
        raise ValueError('Could not compact set of hexagons!')

    return hc


cpdef HexMem uncompact(const H3int[:] hc, int res):
    N = h3c.maxUncompactSize(&hc[0], len(hc), res)
    hu = HexMem(N)

    flag = h3c.uncompact(
        &hc[0], len(hc),
        hu.ptr, len(hu),
        res
    )

    if flag != 0:
        raise ValueError('Could not uncompact set of hexagons!')

    # we need to keep the HexMem object around to keep the memory from getting freed
    return hu


cpdef H3int num_hexagons(int resolution):
    return h3c.numHexagons(resolution)

cpdef double hex_area(int resolution, unit='km'):
    area = h3c.hexAreaKm2(resolution)

    # todo: multiple units
    convert = {
        'km': 1.0,
    }
    area *= convert[unit]

    return area

cpdef double edge_length(int resolution, unit='km'):
    length = h3c.edgeLengthKm(resolution)

    # todo: multiple units
    convert = {
        'km': 1.0,
    }
    length *= convert[unit]

    return length

cpdef bool is_pentagon(H3int h):
    try:
        return h3c.h3IsPentagon(h) is 1
    except Exception:
        return False

cpdef int base_cell(H3int h):
    return h3c.h3GetBaseCell(h)

