"""
This API handles H3 Indexes of type `int`, using
basic Python collections (`set`, `list`, `tuple`).
`h3` will interpret these Indexes as unsigned 64-bit integers.

Input collections:

- `Iterable[int]`

Output collections:

- `Set[int]` for unordered
- `List[int]` for ordered
"""

from typing import Set

from .. import _cy
from ._api_template import _API_FUNCTIONS


def _id(x):
    return x


def _in_collection(hexes):
    it = list(hexes)

    return _cy.from_iter(it)


basic_int = _API_FUNCTIONS[int, Set[int]](
    _in_scalar=_id,
    _out_scalar=_id,
    _in_collection=_in_collection,
    _out_unordered=set,  # todo: should this be an (immutable) frozenset?
    _out_ordered=list,  # todo: should this be an (immutable) tuple?
)

###############################
# Automatically generated API
# Do not edit below these lines
###############################

versions = basic_int.versions
string_to_h3 = basic_int.string_to_h3
h3_to_string = basic_int.h3_to_string
num_hexagons = basic_int.num_hexagons
hex_area = basic_int.hex_area
edge_length = basic_int.edge_length
h3_is_valid = basic_int.h3_is_valid
h3_unidirectional_edge_is_valid = basic_int.h3_unidirectional_edge_is_valid
geo_to_h3 = basic_int.geo_to_h3
h3_to_geo = basic_int.h3_to_geo
h3_get_resolution = basic_int.h3_get_resolution
h3_to_parent = basic_int.h3_to_parent
h3_distance = basic_int.h3_distance
h3_to_geo_boundary = basic_int.h3_to_geo_boundary
k_ring = basic_int.k_ring
hex_range = basic_int.hex_range
hex_ring = basic_int.hex_ring
hex_range_distances = basic_int.hex_range_distances
hex_ranges = basic_int.hex_ranges
k_ring_distances = basic_int.k_ring_distances
h3_to_children = basic_int.h3_to_children
compact = basic_int.compact
uncompact = basic_int.uncompact
h3_set_to_multi_polygon = basic_int.h3_set_to_multi_polygon
polyfill_polygon = basic_int.polyfill_polygon
polyfill_geojson = basic_int.polyfill_geojson
polyfill = basic_int.polyfill
h3_is_pentagon = basic_int.h3_is_pentagon
h3_get_base_cell = basic_int.h3_get_base_cell
h3_indexes_are_neighbors = basic_int.h3_indexes_are_neighbors
get_h3_unidirectional_edge = basic_int.get_h3_unidirectional_edge
get_origin_h3_index_from_unidirectional_edge = basic_int.get_origin_h3_index_from_unidirectional_edge
get_destination_h3_index_from_unidirectional_edge = basic_int.get_destination_h3_index_from_unidirectional_edge
get_h3_indexes_from_unidirectional_edge = basic_int.get_h3_indexes_from_unidirectional_edge
get_h3_unidirectional_edges_from_hexagon = basic_int.get_h3_unidirectional_edges_from_hexagon
get_h3_unidirectional_edge_boundary = basic_int.get_h3_unidirectional_edge_boundary
h3_line = basic_int.h3_line
h3_is_res_class_III = basic_int.h3_is_res_class_III
h3_is_res_class_iii = basic_int.h3_is_res_class_iii
get_pentagon_indexes = basic_int.get_pentagon_indexes
get_res0_indexes = basic_int.get_res0_indexes
h3_to_center_child = basic_int.h3_to_center_child
h3_get_faces = basic_int.h3_get_faces
experimental_h3_to_local_ij = basic_int.experimental_h3_to_local_ij
experimental_local_ij_to_h3 = basic_int.experimental_local_ij_to_h3
cell_area = basic_int.cell_area
exact_edge_length = basic_int.exact_edge_length
point_dist = basic_int.point_dist
