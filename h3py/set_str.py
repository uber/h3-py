import h3py.h3core as h3core
from h3py.hexmem import hex2int, int2hex

# todo: add validation


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
    h = h3core.parent(h, res)
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
