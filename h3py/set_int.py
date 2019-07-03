from h3py.h3core import (
    is_valid,
    geo_to_h3,
    h3_to_geo,
    resolution,
    parent,
    distance,
    h3_to_geo_boundary,
)

import h3py.h3core as h3core

# todo: add validation

def k_ring(h, ring_size):
    hm = h3core.k_ring(h, ring_size)

    return hm.set_int()


# todo: simpler wrappers for these functions?
def hex_ring(h, ring_size):
    hm = h3core.hex_ring(h, ring_size)

    return hm.set_int()


def children(h, res):
    hm = h3core.children(h, res)

    #todo: move these conversion functions to this module
    return hm.set_int()


def compact(hexes):
    hu = h3core.from_ints(hexes)
    hc = h3core.compact(hu.memview())

    return hc.set_int()

def uncompact(hexes, res):
    hc = h3core.from_ints(hexes) ## todo: is this the right logic for packing/unpacking?
    hu = h3core.uncompact(hc.memview(), res)

    return hu.set_int()

def polyfill(geos, res):
    hm = h3core.polyfill(geos, res)

    return hm.set_int()
