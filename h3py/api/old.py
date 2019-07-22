from .set_str import (
    hex2int
        as string_to_h3,
    int2hex
        as h3_to_string,
    is_cell
        as h3_is_valid,
    resolution
        as h3_get_resolution,
    geo_to_h3,
    h3_to_geo,
    cell_boundary
        as h3_to_geo_boundary,
    disk
        as k_ring,
    # k_ring_distances
    polyfill,
    #h3_set_to_multi_polygon
    ring
        as hex_ring,
    compact,
    uncompact,
    parent
        as h3_to_parent,
    children
        as h3_to_children,
    # hex_range
    # hex_range_distances
    # hex_ranges
    mean_hex_area,
    mean_edge_length,
    num_hexagons,
    get_base_cell
        as h3_get_base_cell,
    # h3_is_res_class_iii
    # h3_is_res_class_III
    is_pentagon
        as h3_is_pentagon,
    are_neighbors
        as h3_indexes_are_neighbors,
    edge
        as get_h3_unidirectional_edge,
    is_edge
        as h3_unidirectional_edge_is_valid,
    edge_origin
        as get_origin_h3_index_from_unidirectional_edge,
    edge_destination
        as get_destination_h3_index_from_unidirectional_edge,
    edge_hexes
        as get_h3_indexes_from_unidirectional_edge,
    edges_from_hex
        as get_h3_unidirectional_edges_from_hexagon,
    edge_boundary
        as get_h3_unidirectional_edge_boundary,
    distance
        as h3_distance,
    # h3_line_size
    line
        as h3_line,
)