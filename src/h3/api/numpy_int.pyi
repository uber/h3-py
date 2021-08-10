import numpy as np
from numpy.typing import NDArray

from . import _api

H3Cell = np.uint64
H3Edge = np.uint64
UnorderedH3Cell = NDArray[H3Cell]

# Should be no changes in each API file below this line

versions = _api.versions
string_to_h3 = _api.string_to_h3
h3_to_string = _api.h3_to_string
num_hexagons = _api.num_hexagons
hex_area = _api.hex_area
edge_length = _api.edge_length
h3_is_valid = _api.h3_is_valid[H3Cell]
h3_unidirectional_edge_is_valid = _api.h3_unidirectional_edge_is_valid[H3Edge]
geo_to_h3 = _api.geo_to_h3[H3Cell]
h3_to_geo = _api.h3_to_geo[H3Cell]
h3_get_resolution = _api.h3_get_resolution[H3Cell]
h3_to_parent = _api.h3_to_parent[H3Cell]
h3_distance = _api.h3_distance[H3Cell]
h3_to_geo_boundary = _api.h3_to_geo_boundary[H3Cell]

k_ring = _api.k_ring[H3Cell, UnorderedH3Cell]
hex_range = _api.hex_range[H3Cell, UnorderedH3Cell]
hex_ring = _api.hex_ring[H3Cell, UnorderedH3Cell]
hex_range_distances = _api.hex_range_distances[H3Cell]

hex_ranges = _api.hex_ranges[H3Cell]
k_ring_distances = _api.k_ring_distances[H3Cell]
h3_to_children = _api.h3_to_children[H3Cell, UnorderedH3Cell]
compact = _api.compact[H3Cell, UnorderedH3Cell]
uncompact = _api.uncompact[H3Cell, UnorderedH3Cell]

h3_set_to_multi_polygon = _api.h3_set_to_multi_polygon[H3Cell]
h3_is_pentagon = _api.h3_is_pentagon[H3Cell]
h3_get_base_cell = _api.h3_get_base_cell[H3Cell]
h3_indexes_are_neighbors = _api.h3_indexes_are_neighbors[H3Cell]
get_h3_unidirectional_edge = _api.get_h3_unidirectional_edge[H3Cell, H3Edge]

get_origin_h3_index_from_unidirectional_edge = (
    _api.get_origin_h3_index_from_unidirectional_edge[H3Edge, H3Cell]
)
get_destination_h3_index_from_unidirectional_edge = (
    _api.get_destination_h3_index_from_unidirectional_edge[H3Edge, H3Cell]
)
get_h3_indexes_from_unidirectional_edge = _api.get_h3_indexes_from_unidirectional_edge[
    H3Edge, H3Cell
]
get_h3_unidirectional_edges_from_hexagon = (
    _api.get_h3_unidirectional_edges_from_hexagon[H3Cell, H3Edge]
)
get_h3_unidirectional_edge_boundary = _api.get_h3_unidirectional_edge_boundary[H3Edge]

h3_line = _api.h3_line[H3Cell]
h3_is_res_class_III = _api.h3_is_res_class_III[H3Cell]
h3_is_res_class_iii = _api.h3_is_res_class_iii[H3Cell]

get_pentagon_indexes = _api.get_pentagon_indexes[H3Cell]
get_res0_indexes = _api.get_res0_indexes[H3Cell]
h3_to_center_child = _api.h3_to_center_child[H3Cell]
h3_get_faces = _api.h3_get_faces[H3Cell]
experimental_h3_to_local_ij = _api.experimental_h3_to_local_ij[H3Cell]
experimental_local_ij_to_h3 = _api.experimental_local_ij_to_h3[H3Cell]
cell_area = _api.cell_area[H3Cell]
exact_edge_length = _api.exact_edge_length[H3Edge]
point_dist = _api.point_dist
