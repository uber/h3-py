import h3py.h3core as h3core
import h3py.hexmem as hexmem

# todo: add validation (just do it in `_in_scalar()`?)
# todo: how to write documentation once and have it carry over to each interface?


def _in_scalar(h):
    "Output formatter for this module."
    return hexmem.hex2int(h)

def _out_scalar(h):
    "Output formatter for this module."
    return hexmem.int2hex(h)

def _out_collection(hm):
    "Output formatter for this module."
    # todo: this could just use the _out_scalar function...
    return set(_out_scalar(h) for h in hm.memview())


def is_valid(h):
    """Validates an `h3_address` given as a string

    :returns: boolean
    """
    # todo: below
    return h3core.is_valid(_in_scalar(h))


def geo_to_h3(lat, lng, resolution):
    return _out_scalar(h3core.geo_to_h3(lat, lng, resolution))


def h3_to_geo(h):
    """Reverse lookup an h3 address into a geo-coordinate"""

    return h3core.h3_to_geo(_in_scalar(h))

def resolution(h):
    """Returns the resolution of an `h3_address`

    :return: nibble (0-15)
    """
    return h3core.resolution(_in_scalar(h))

# todo: what's a good variable name? h vs h3_address vs h3str?
def parent(h3_address, resolution):
    h = _in_scalar(h3_address)
    h = h3core.parent(h, resolution)
    h = _out_scalar(h)

    return h

def distance(h1, h2):
    """ compute the hex-distance between two hexagons

    todo: figure out string typing.
    had to drop typing due to errors like
    `TypeError: Argument 'h2' has incorrect type (expected str, got numpy.str_)`
    """
    d = h3core.distance(
            _in_scalar(h1),
            _in_scalar(h2)
        )

    return d

def h3_to_geo_boundary(h, geo_json=False):
    return h3core.h3_to_geo_boundary(_in_scalar(h), geo_json)


def k_ring(h, ring_size):
    hm = h3core.k_ring(_in_scalar(h), ring_size)

    # todo: take these out of the HexMem class
    return _out_collection(hm)

def hex_ring(h, ring_size):
    hm = h3core.hex_ring(_in_scalar(h), ring_size)

    # todo: take these out of the HexMem class
    return _out_collection(hm)

def children(h, res):
    hm = h3core.children(_in_scalar(h), res)

    return _out_collection(hm)

# todo: nogil for expensive C operation?
def compact(hexes):
    # move this helper to this module?
    hu = hexmem.from_strs(hexes)
    hc = h3core.compact(hu.memview())

    return _out_collection(hc)

def uncompact(hexes, res):
    hc = hexmem.from_strs(hexes)
    hu = h3core.uncompact(hc.memview(), res)

    return _out_collection(hu)


def polyfill(geos, res):
    hm = h3core.polyfill(geos, res)

    return _out_collection(hm)


