"""
This API handles H3 Indexes of type `str`, using
basic Python collections (`set`, `list`, `tuple`).
`h3` will interpret these Indexes as hexadecimal
representations of unsigned 64-bit integers.

Input collections:

- `Iterable[str]`

Output collections:

- `Set[str]` for unordered
- `List[str]` for ordered
"""

from .. import _cy
from ._api_template import _API_FUNCTIONS


def _in_collection(hexes):
    it = [_cy.hex2int(h) for h in hexes]

    return _cy.from_iter(it)


def _out_unordered(mv):
    # todo: should this be an (immutable) frozenset?
    return set(_cy.int2hex(h) for h in mv)


def _out_ordered(mv):
    # todo: should this be an (immutable) tuple?
    return list(_cy.int2hex(h) for h in mv)


basic_str = _API_FUNCTIONS(
    _in_scalar = _cy.hex2int,
    _out_scalar = _cy.int2hex,
    _in_collection = _in_collection,
    _out_unordered = _out_unordered,
    _out_ordered = _out_ordered,
)

###############################
# Automatically generated API
# Do not edit below these lines
###############################

cell_area = basic_str.cell_area
compact = basic_str.compact
edge_length = basic_str.edge_length
exact_edge_length = basic_str.exact_edge_length
experimental_h3_to_local_ij = basic_str.experimental_h3_to_local_ij
experimental_local_ij_to_h3 = basic_str.experimental_local_ij_to_h3
geo_to_h3 = basic_str.geo_to_h3
get_destination_h3_index_from_unidirectional_edge = basic_str.get_destination_h3_index_from_unidirectional_edge
get_h3_indexes_from_unidirectional_edge = basic_str.get_h3_indexes_from_unidirectional_edge
get_h3_unidirectional_edge = basic_str.get_h3_unidirectional_edge
get_h3_unidirectional_edge_boundary = basic_str.get_h3_unidirectional_edge_boundary
get_h3_unidirectional_edges_from_hexagon = basic_str.get_h3_unidirectional_edges_from_hexagon
get_origin_h3_index_from_unidirectional_edge = basic_str.get_origin_h3_index_from_unidirectional_edge
get_pentagon_indexes = basic_str.get_pentagon_indexes
get_res0_indexes = basic_str.get_res0_indexes
h3_distance = basic_str.h3_distance
h3_get_base_cell = basic_str.h3_get_base_cell
h3_get_faces = basic_str.h3_get_faces
h3_get_resolution = basic_str.h3_get_resolution
h3_indexes_are_neighbors = basic_str.h3_indexes_are_neighbors
h3_is_pentagon = basic_str.h3_is_pentagon
h3_is_res_class_III = basic_str.h3_is_res_class_III
h3_is_res_class_iii = basic_str.h3_is_res_class_iii
h3_is_valid = basic_str.h3_is_valid
h3_line = basic_str.h3_line
h3_set_to_multi_polygon = basic_str.h3_set_to_multi_polygon
h3_to_center_child = basic_str.h3_to_center_child
h3_to_children = basic_str.h3_to_children
h3_to_geo = basic_str.h3_to_geo
h3_to_geo_boundary = basic_str.h3_to_geo_boundary
h3_to_parent = basic_str.h3_to_parent
h3_to_string = basic_str.h3_to_string
h3_unidirectional_edge_is_valid = basic_str.h3_unidirectional_edge_is_valid
hex_area = basic_str.hex_area
hex_range = basic_str.hex_range
hex_range_distances = basic_str.hex_range_distances
hex_ranges = basic_str.hex_ranges
hex_ring = basic_str.hex_ring
k_ring = basic_str.k_ring
k_ring_distances = basic_str.k_ring_distances
num_hexagons = basic_str.num_hexagons
point_dist = basic_str.point_dist
polyfill = basic_str.polyfill
polyfill_geojson = basic_str.polyfill_geojson
polyfill_polygon = basic_str.polyfill_polygon
string_to_h3 = basic_str.string_to_h3
uncompact = basic_str.uncompact
versions = basic_str.versions
