"""Binding of public API names to module scope

Prior to binding the API to module scope explicitly, we dynamically modified the
`globals` object when `h3` was imported, which caused problems with static tooling not
being able to understand the H3 API.

This file exists to avoid dynamically modifying `globals` and support static tooling.
"""
from ._binding import _binding

cell_area = _binding.cell_area
hex_area = _binding.hex_area
edge_length = _binding.edge_length
exact_edge_length = _binding.exact_edge_length
cell_to_local_ij = _binding.cell_to_local_ij
local_ij_to_cell = _binding.local_ij_to_cell
latlng_to_cell = _binding.latlng_to_cell
cell_to_latlng = _binding.cell_to_latlng
cell_to_boundary = _binding.cell_to_boundary
get_pentagons = _binding.get_pentagons
get_res0_cells = _binding.get_res0_cells
grid_distance = _binding.grid_distance
grid_ring = _binding.grid_ring
grid_disk = _binding.grid_disk
grid_path_cells = _binding.grid_path_cells
get_base_cell_number = _binding.get_base_cell_number
get_icosahedron_faces = _binding.get_icosahedron_faces
get_resolution = _binding.get_resolution
are_neighbor_cells = _binding.are_neighbor_cells
is_pentagon = _binding.is_pentagon
is_res_class_III = _binding.is_res_class_III
is_valid_cell = _binding.is_valid_cell
cells_to_multi_polygon = _binding.cells_to_multi_polygon
cell_to_center_child = _binding.cell_to_center_child
cell_to_children = _binding.cell_to_children
cell_to_parent = _binding.cell_to_parent
int_to_string = _binding.int_to_string
string_to_int = _binding.string_to_int
is_valid_directed_edge = _binding.is_valid_directed_edge
get_num_cells = _binding.get_num_cells
great_circle_distance = _binding.great_circle_distance
polyfill = _binding.polyfill
polyfill_geojson = _binding.polyfill_geojson
polyfill_polygon = _binding.polyfill_polygon
compact_cells = _binding.compact_cells
uncompact_cells = _binding.uncompact_cells

get_directed_edge_origin = _binding.get_directed_edge_origin
get_directed_edge_destination = _binding.get_directed_edge_destination
directed_edge_to_cells = _binding.directed_edge_to_cells
cells_to_directed_edge = _binding.cells_to_directed_edge
directed_edge_to_boundary = _binding.directed_edge_to_boundary
origin_to_directed_edges = _binding.origin_to_directed_edges

versions = _binding.versions
