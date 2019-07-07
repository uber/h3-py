from h3py.h3core import (
    is_valid,
    geo_to_h3,
    h3_to_geo,
    resolution,
    parent,
    distance,
    h3_to_geo_boundary,
    num_hexagons,
    hex_area,
    edge_length,
    is_pentagon,
    base_cell,
    are_neighbors,
    uni_edge,
    is_uni_edge,
    uni_edge_origin,
    uni_edge_destination,
    uni_edge_hexes,
    uni_edge_boundary
)

import h3py.h3core as h3core
import h3py.hexmem as hexmem

# todo: add validation


def _in_scalar(h):
    "Output formatter for this module."
    # todo: but add validation
    # todo: but what about the functions imported above. how to add validation?
    # todo: acutally use this function
    return h

def _out_scalar(h):
    "Output formatter for this module."
    return h

def _out_collection(hm):
    "Output formatter for this module."
    return set(hm.memview())

def k_ring(h, ring_size):
    hm = h3core.k_ring(h, ring_size)

    return _out_collection(hm)


# todo: simpler wrappers for these functions?
def hex_ring(h, ring_size):
    hm = h3core.hex_ring(h, ring_size)

    return _out_collection(hm)


def children(h, res):
    hm = h3core.children(h, res)

    #todo: move these conversion functions to this module
    return _out_collection(hm)


def compact(hexes):
    hu = hexmem.from_ints(hexes)
    hc = h3core.compact(hu.memview())

    return _out_collection(hc)

def uncompact(hexes, res):
    hc = hexmem.from_ints(hexes) ## todo: is this the right logic for packing/unpacking?
    hu = h3core.uncompact(hc.memview(), res)

    return _out_collection(hu)

def polyfill(geos, res):
    hm = h3core.polyfill(geos, res)

    return _out_collection(hm)

def uni_edges_from_hex(origin):
    hm = h3core.uni_edges_from_hex(origin)

    return _out_collection(hm)
