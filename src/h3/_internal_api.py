# flake8: noqa

"""
This module should serve as the interface between the C/Cython code and
the Python code, i.e., an internal API. That is, this module should import all the Cython functions we
intend to expose to be used in pure Python code, and each of the h3 APIs should
*only* reference functions listed here.
"""

from .cells import (
    is_cell,
    is_pentagon,
    get_base_cell,
    resolution,
    parent,
    distance,
    disk,
    ring,
    children,
    compact,
    uncompact,
    num_hexagons,
    mean_hex_area,
    mean_edge_length,
    line,
    is_res_class_iii,
)

from .edges import (
    are_neighbors,
    edge,
    is_edge,
    edge_origin,
    edge_destination,
    edge_cells,
    edges_from_cell,
)

from .geo import (
    geo_to_h3,
    h3_to_geo,
    polyfill_polygon,
    polyfill_geojson,
    polyfill,
    cell_boundary,
    edge_boundary,
)

from .to_multipoly import (
    h3_set_to_multi_polygon
)

from .util import (
    versions,
    hex2int,
    int2hex,
    from_iter,
)
