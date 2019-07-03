import h3py.h3core as h3core
from h3py.hexmem import hex2int, int2hex

# todo: add validation
# todo: how to write documentation once and have it carry over to each interface?


def is_valid(h):
    """Validates an `h3_address` given as a string

    :returns: boolean
    """
    # todo: below
    return h3core.is_valid(hex2int(h))


def geo_to_h3(lat, lng, resolution):
    return int2hex(h3core.geo_to_h3(lat, lng, resolution))


def h3_to_geo(h):
    """Reverse lookup an h3 address into a geo-coordinate"""

    return h3core.h3_to_geo(hex2int(h))

def resolution(h):
    """Returns the resolution of an `h3_address`

    :return: nibble (0-15)
    """
    return h3core.resolution(hex2int(h))

# todo: what's a good variable name? h vs h3_address vs h3str?
def parent(h3_address, resolution):
    h = hex2int(h3_address)
    h = h3core.parent(h, resolution)
    h = int2hex(h)

    return h

def distance(h1, h2):
    """ compute the hex-distance between two hexagons

    todo: figure out string typing.
    had to drop typing due to errors like
    `TypeError: Argument 'h2' has incorrect type (expected str, got numpy.str_)`
    """
    d = h3core.distance(
            hex2int(h1),
            hex2int(h2)
        )

    return d

def h3_to_geo_boundary(h, geo_json=False):
    return h3core.h3_to_geo_boundary(hex2int(h), geo_json)


def k_ring(h, ring_size):
    hm = h3core.k_ring(hex2int(h), ring_size)

    # todo: take these out of the HexMem class
    return hm.set_str()

def hex_ring(h, ring_size):
    hm = h3core.hex_ring(hex2int(h), ring_size)

    # todo: take these out of the HexMem class
    return hm.set_str()

def children(h, res):
    hm = h3core.children(hex2int(h), res)

    return hm.set_str()

# todo: nogil for expensive C operation?
def compact(hexes):
    # move this helper to this module?
    hu = h3core.from_strs(hexes)
    hc = h3core.compact(hu.memview())

    return hc.set_str()

def uncompact(hexes, res):
    hc = h3core.from_strs(hexes)
    hu = h3core.uncompact(hc.memview(), res)

    return hu.set_str()


def polyfill(geos, res):
    hm = h3core.polyfill(geos, res)

    return hm.set_str()


