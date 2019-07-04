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
import h3py.hexmem as hexmem

# todo: add validation

def format_out(hm):
    "Output formatter for this module."
    return set(hm.memview())

def k_ring(h, ring_size):
    hm = h3core.k_ring(h, ring_size)

    return format_out(hm)


# todo: simpler wrappers for these functions?
def hex_ring(h, ring_size):
    hm = h3core.hex_ring(h, ring_size)

    return format_out(hm)


def children(h, res):
    hm = h3core.children(h, res)

    #todo: move these conversion functions to this module
    return format_out(hm)


def compact(hexes):
    hu = hexmem.from_ints(hexes)
    hc = h3core.compact(hu.memview())

    return format_out(hc)

def uncompact(hexes, res):
    hc = hexmem.from_ints(hexes) ## todo: is this the right logic for packing/unpacking?
    hu = h3core.uncompact(hc.memview(), res)

    return format_out(hu)

def polyfill(geos, res):
    hm = h3core.polyfill(geos, res)

    return format_out(hm)
