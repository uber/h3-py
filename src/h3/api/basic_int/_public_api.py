"""Binding of public API names to module scope

Prior to binding the API to module scope explicitly, we dynamically modified the
`globals` object when `h3` was imported, which caused problems with static tooling not
being able to understand the H3 API.

This file exists to avoid dynamically modifying `globals` and support static tooling.
"""
from ._binding import _binding as _b


is_valid_cell = _b.is_valid_cell
is_pentagon = _b.is_pentagon
is_valid_directed_edge = _b.is_valid_directed_edge
is_res_class_III = _b.is_res_class_III

int_to_str = _b.int_to_str
str_to_int = _b.str_to_int

cell_area = _b.cell_area
edge_length = _b.edge_length
great_circle_distance = _b.great_circle_distance
average_hexagon_area = _b.average_hexagon_area
average_hexagon_edge_length = _b.average_hexagon_edge_length

latlng_to_cell = _b.latlng_to_cell
cell_to_latlng = _b.cell_to_latlng
cell_to_boundary = _b.cell_to_boundary
cell_to_local_ij = _b.cell_to_local_ij
local_ij_to_cell = _b.local_ij_to_cell

grid_ring = _b.grid_ring
grid_disk = _b.grid_disk
grid_distance = _b.grid_distance
grid_path_cells = _b.grid_path_cells

get_num_cells = _b.get_num_cells
get_pentagons = _b.get_pentagons
get_res0_cells = _b.get_res0_cells
get_resolution = _b.get_resolution
get_base_cell_number = _b.get_base_cell_number
get_icosahedron_faces = _b.get_icosahedron_faces

cell_to_parent = _b.cell_to_parent
cell_to_children = _b.cell_to_children
cell_to_center_child = _b.cell_to_center_child
compact_cells = _b.compact_cells
uncompact_cells = _b.uncompact_cells

polygon_to_cells = _b.polygon_to_cells
cells_to_polygons = _b.cells_to_polygons

are_neighbor_cells = _b.are_neighbor_cells
cells_to_directed_edge = _b.cells_to_directed_edge
directed_edge_to_cells = _b.directed_edge_to_cells
origin_to_directed_edges = _b.origin_to_directed_edges
get_directed_edge_origin = _b.get_directed_edge_origin
get_directed_edge_destination = _b.get_directed_edge_destination
directed_edge_to_boundary = _b.directed_edge_to_boundary

versions = _b.versions
