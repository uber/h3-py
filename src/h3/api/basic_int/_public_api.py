"""Binding of public API names to module scope

Prior to binding the API to module scope explicitly, we dynamically modified the
`globals` object when `h3` was imported, which caused problems with static tooling not
being able to understand the H3 API.

This file exists to avoid dynamically modifying `globals` and support static tooling.
"""
from ._binding import _binding

cell_area = _binding.cell_area
edge_length = _binding.edge_length
exact_edge_length = _binding.exact_edge_length
experimental_h3_to_local_ij = _binding.experimental_h3_to_local_ij
experimental_local_ij_to_h3 = _binding.experimental_local_ij_to_h3
latlng_to_cell = _binding.latlng_to_cell
cell_to_latlng = _binding.cell_to_latlng
cell_to_boundary = _binding.cell_to_boundary
get_pentagons = _binding.get_pentagons
get_res0_cells = _binding.get_res0_cells
grid_distance = _binding.grid_distance
get_base_cell_number = _binding.get_base_cell_number
get_faces = _binding.get_faces
get_resolution = _binding.get_resolution
h3_indexes_are_neighbors = _binding.h3_indexes_are_neighbors
is_pentagon = _binding.is_pentagon
is_res_class_III = _binding.is_res_class_III
is_valid_cell = _binding.is_valid_cell
h3_line = _binding.h3_line
h3_set_to_multi_polygon = _binding.h3_set_to_multi_polygon
cell_to_center_child = _binding.cell_to_center_child
cell_to_children = _binding.cell_to_children
cell_to_parent = _binding.cell_to_parent
int_to_string = _binding.int_to_string
string_to_int = _binding.string_to_int
is_valid_directed_edge = _binding.is_valid_directed_edge
hex_area = _binding.hex_area
hex_range_distances = _binding.hex_range_distances
hex_ranges = _binding.hex_ranges
hex_ring = _binding.hex_ring
k_ring = _binding.k_ring
num_hexagons = _binding.num_hexagons
point_dist = _binding.point_dist
polyfill = _binding.polyfill
polyfill_geojson = _binding.polyfill_geojson
polyfill_polygon = _binding.polyfill_polygon
compact_cells = _binding.compact_cells
uncompact_cells = _binding.uncompact_cells
get_destination_h3_index_from_unidirectional_edge = (
    _binding.get_destination_h3_index_from_unidirectional_edge
)
get_h3_indexes_from_unidirectional_edge = (
    _binding.get_h3_indexes_from_unidirectional_edge
)
get_h3_unidirectional_edge = _binding.get_h3_unidirectional_edge
get_h3_unidirectional_edge_boundary = _binding.get_h3_unidirectional_edge_boundary
get_h3_unidirectional_edges_from_hexagon = (
    _binding.get_h3_unidirectional_edges_from_hexagon
)
get_origin_h3_index_from_unidirectional_edge = (
    _binding.get_origin_h3_index_from_unidirectional_edge
)
versions = _binding.versions
