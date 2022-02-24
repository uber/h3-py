"""
This API handles H3 Indexes of type `int` (specifically, `uint64`),
using `numpy.array` objects for collections.
`h3` will interpret these Indexes as unsigned 64-bit integers.

This API is **optional**, and will only work if the
user has `numpy` installed.

Input collections:

- `Iterable[int]`
    - works for `lists`, but not `sets`
    - will attempt to convert `int` to `uint64`
    - no memory copy is made if input dtype is `uint64`

Output collections:

- `np.ndarray[np.uint64]` for unordered
- `np.ndarray[np.uint64]` for ordered
"""

import numpy as np

from ._api_template import _API_FUNCTIONS


def _id(x):
    return x


def _to_uint64_scalar(x):
    return np.uint64(x)


def _in_collection(x):
    # array is copied only if dtype does not match
    # `list`s should work, but not `set`s of integers
    return np.asarray(x, dtype='uint64')


numpy_int = _API_FUNCTIONS(
    _in_scalar = _id,
    _out_scalar = _to_uint64_scalar,
    _in_collection = _in_collection,
    _out_unordered = np.asarray,
    _out_ordered = np.asarray,
)

###############################
# Automatically generated API
# Do not edit below these lines
###############################

cell_area = numpy_int.cell_area
compact = numpy_int.compact
edge_length = numpy_int.edge_length
exact_edge_length = numpy_int.exact_edge_length
experimental_h3_to_local_ij = numpy_int.experimental_h3_to_local_ij
experimental_local_ij_to_h3 = numpy_int.experimental_local_ij_to_h3
geo_to_h3 = numpy_int.geo_to_h3
get_destination_h3_index_from_unidirectional_edge = numpy_int.get_destination_h3_index_from_unidirectional_edge
get_h3_indexes_from_unidirectional_edge = numpy_int.get_h3_indexes_from_unidirectional_edge
get_h3_unidirectional_edge = numpy_int.get_h3_unidirectional_edge
get_h3_unidirectional_edge_boundary = numpy_int.get_h3_unidirectional_edge_boundary
get_h3_unidirectional_edges_from_hexagon = numpy_int.get_h3_unidirectional_edges_from_hexagon
get_origin_h3_index_from_unidirectional_edge = numpy_int.get_origin_h3_index_from_unidirectional_edge
get_pentagon_indexes = numpy_int.get_pentagon_indexes
get_res0_indexes = numpy_int.get_res0_indexes
h3_distance = numpy_int.h3_distance
h3_get_base_cell = numpy_int.h3_get_base_cell
h3_get_faces = numpy_int.h3_get_faces
h3_get_resolution = numpy_int.h3_get_resolution
h3_indexes_are_neighbors = numpy_int.h3_indexes_are_neighbors
h3_is_pentagon = numpy_int.h3_is_pentagon
h3_is_res_class_III = numpy_int.h3_is_res_class_III
h3_is_res_class_iii = numpy_int.h3_is_res_class_iii
h3_is_valid = numpy_int.h3_is_valid
h3_line = numpy_int.h3_line
h3_set_to_multi_polygon = numpy_int.h3_set_to_multi_polygon
h3_to_center_child = numpy_int.h3_to_center_child
h3_to_children = numpy_int.h3_to_children
h3_to_geo = numpy_int.h3_to_geo
h3_to_geo_boundary = numpy_int.h3_to_geo_boundary
h3_to_parent = numpy_int.h3_to_parent
h3_to_string = numpy_int.h3_to_string
h3_unidirectional_edge_is_valid = numpy_int.h3_unidirectional_edge_is_valid
hex_area = numpy_int.hex_area
hex_range = numpy_int.hex_range
hex_range_distances = numpy_int.hex_range_distances
hex_ranges = numpy_int.hex_ranges
hex_ring = numpy_int.hex_ring
k_ring = numpy_int.k_ring
k_ring_distances = numpy_int.k_ring_distances
num_hexagons = numpy_int.num_hexagons
point_dist = numpy_int.point_dist
polyfill = numpy_int.polyfill
polyfill_geojson = numpy_int.polyfill_geojson
polyfill_polygon = numpy_int.polyfill_polygon
string_to_h3 = numpy_int.string_to_h3
uncompact = numpy_int.uncompact
versions = numpy_int.versions
