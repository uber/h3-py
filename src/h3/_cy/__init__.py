# flake8: noqa

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
    cell_area,
    center_child,
    children,
    compact,
    disk,
    distance,
    experimental_h3_to_local_ij,
    experimental_local_ij_to_h3,
    get_base_cell,
    get_faces,
    get_pentagon_indexes,
    get_res0_indexes,
    is_cell,
    is_pentagon,
    is_res_class_iii,
    line,
    mean_hex_area,
    num_hexagons,
    parent,
    resolution,
    ring,
    uncompact,
)
from .edges import (
    are_neighbors,
    edge,
    edge_cells,
    edge_destination,
    edge_length,
    edge_origin,
    edges_from_cell,
    is_edge,
    mean_edge_length,
)
from .geo import (
    cell_boundary,
    edge_boundary,
    geo_to_h3,
    h3_to_geo,
    point_dist,
    polyfill,
    polyfill_geojson,
    polyfill_polygon,
)
from .to_multipoly import h3_set_to_multi_polygon
from .util import (
    H3CellError,
    H3DistanceError,
    H3EdgeError,
    H3ResolutionError,
    H3ValueError,
    c_version,
    from_iter,
    hex2int,
    int2hex,
)
