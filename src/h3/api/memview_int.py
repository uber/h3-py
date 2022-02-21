"""
This API handles H3 Indexes of type `int` (specifically, `uint64`),
using Python `memoryview` objects for collections.
`h3` will interpret these Indexes as unsigned 64-bit integers.

Input collections:

- `memoryview[uint64]`, i.e., anything that supports the buffer protocol
    - `dtype` must be `uint64`. for example, `long` will raise an error
    - `list` or `set` inputs will not be accepted

Output collections:

- `memoryview[uint64]` for unordered
- `memoryview[uint64]` for ordered
"""

from ._api_template import _API_FUNCTIONS


def _id(x):
    return x


memview_int = _API_FUNCTIONS[memoryview, memoryview](
    _in_scalar = _id,
    _out_scalar = _id,
    _in_collection = _id,
    _out_unordered = _id,
    _out_ordered = _id,
)

###############################
# Automatically generated API
# Do not edit below these lines
###############################

versions = memview_int.versions
string_to_h3 = memview_int.string_to_h3
h3_to_string = memview_int.h3_to_string
num_hexagons = memview_int.num_hexagons
hex_area = memview_int.hex_area
edge_length = memview_int.edge_length
h3_is_valid = memview_int.h3_is_valid
h3_unidirectional_edge_is_valid = memview_int.h3_unidirectional_edge_is_valid
geo_to_h3 = memview_int.geo_to_h3
h3_to_geo = memview_int.h3_to_geo
h3_get_resolution = memview_int.h3_get_resolution
h3_to_parent = memview_int.h3_to_parent
h3_distance = memview_int.h3_distance
h3_to_geo_boundary = memview_int.h3_to_geo_boundary
k_ring = memview_int.k_ring
hex_range = memview_int.hex_range
hex_ring = memview_int.hex_ring
hex_range_distances = memview_int.hex_range_distances
hex_ranges = memview_int.hex_ranges
k_ring_distances = memview_int.k_ring_distances
h3_to_children = memview_int.h3_to_children
compact = memview_int.compact
uncompact = memview_int.uncompact
h3_set_to_multi_polygon = memview_int.h3_set_to_multi_polygon
polyfill_polygon = memview_int.polyfill_polygon
polyfill_geojson = memview_int.polyfill_geojson
polyfill = memview_int.polyfill
h3_is_pentagon = memview_int.h3_is_pentagon
h3_get_base_cell = memview_int.h3_get_base_cell
h3_indexes_are_neighbors = memview_int.h3_indexes_are_neighbors
get_h3_unidirectional_edge = memview_int.get_h3_unidirectional_edge
get_origin_h3_index_from_unidirectional_edge = memview_int.get_origin_h3_index_from_unidirectional_edge
get_destination_h3_index_from_unidirectional_edge = memview_int.get_destination_h3_index_from_unidirectional_edge
get_h3_indexes_from_unidirectional_edge = memview_int.get_h3_indexes_from_unidirectional_edge
get_h3_unidirectional_edges_from_hexagon = memview_int.get_h3_unidirectional_edges_from_hexagon
get_h3_unidirectional_edge_boundary = memview_int.get_h3_unidirectional_edge_boundary
h3_line = memview_int.h3_line
h3_is_res_class_III = memview_int.h3_is_res_class_III
h3_is_res_class_iii = memview_int.h3_is_res_class_iii
get_pentagon_indexes = memview_int.get_pentagon_indexes
get_res0_indexes = memview_int.get_res0_indexes
h3_to_center_child = memview_int.h3_to_center_child
h3_get_faces = memview_int.h3_get_faces
experimental_h3_to_local_ij = memview_int.experimental_h3_to_local_ij
experimental_local_ij_to_h3 = memview_int.experimental_local_ij_to_h3
cell_area = memview_int.cell_area
exact_edge_length = memview_int.exact_edge_length
point_dist = memview_int.point_dist
