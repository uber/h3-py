"""
This module should serve as the interface between the C/Cython code and
the Python code. That is, it is an internal API.
This module should import all the Cython functions we
intend to expose to be used in pure Python code, and each of the H3-py
APIs should *only* reference functions and symbols listed here.

These functions should handle input validation, guard against the
possibility of segfaults, raise appropriate errors, and handle memory
management. The API wrapping code around this should focus on the cosmetic
function interface and input conversion (string to int, for instance).
"""

from .cells import (
    average_hexagon_area,
    cell_area,
    cell_to_center_child,
    cell_to_child_pos,
    cell_to_children,
    cell_to_children_size,
    cell_to_local_ij,
    cell_to_parent,
    child_pos_to_cell,
    compact_cells,
    get_base_cell_number,
    get_icosahedron_faces,
    get_num_cells,
    get_pentagons,
    get_res0_cells,
    get_resolution,
    grid_disk,
    grid_distance,
    grid_path_cells,
    grid_ring,
    is_pentagon,
    is_res_class_iii,
    is_valid_cell,
    local_ij_to_cell,
    uncompact_cells,
)
from .edges import (
    are_neighbor_cells,
    average_hexagon_edge_length,
    cells_to_directed_edge,
    directed_edge_to_cells,
    edge_length,
    get_directed_edge_destination,
    get_directed_edge_origin,
    is_valid_directed_edge,
    origin_to_directed_edges,
)
from .error_system import (
    H3BaseException,
    H3CellInvalidError,
    H3DirEdgeInvalidError,
    H3DomainError,
    H3DuplicateInputError,
    H3FailedError,
    H3GridNavigationError,
    H3LatLngDomainError,
    H3MemoryAllocError,
    H3MemoryBoundsError,
    H3MemoryError,
    H3NotNeighborsError,
    H3OptionInvalidError,
    H3PentagonError,
    H3ResDomainError,
    H3ResMismatchError,
    H3UndirEdgeInvalidError,
    H3ValueError,
    H3VertexInvalidError,
    UnknownH3ErrorCode,
)
from .latlng import (
    cell_to_boundary,
    cell_to_latlng,
    directed_edge_to_boundary,
    great_circle_distance,
    latlng_to_cell,
    polygon_to_cells,
    polygons_to_cells,
)
from .memory import (
    iter_to_mv,
)
from .to_multipoly import cells_to_multi_polygon
from .util import (
    c_version,
    int_to_str,
    str_to_int,
)
from .vertex import (
    cell_to_vertex,
    cell_to_vertexes,
    is_valid_vertex,
    vertex_to_latlng,
)
