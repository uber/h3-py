from .set_str import (
    string_to_h3,
    h3_to_string,
    h3_is_valid,
    h3_get_resolution,
    geo_to_h3,
    h3_to_geo,
    h3_to_geo_boundary,
    k_ring,
    # k_ring_distances
    polyfill,
    #h3_set_to_multi_polygon
    hex_ring,
    compact,
    uncompact,
    h3_to_parent,
    h3_to_children,
    # hex_range
    # hex_range_distances
    # hex_ranges
    mean_hex_area,
    mean_edge_length,
    num_hexagons,
    h3_get_base_cell,
    # h3_is_res_class_iii
    # h3_is_res_class_III
    h3_is_pentagon,
    h3_indexes_are_neighbors,
    get_h3_unidirectional_edge,
    h3_unidirectional_edge_is_valid,
    get_origin_h3_index_from_unidirectional_edge,
    get_destination_h3_index_from_unidirectional_edge,
    get_h3_indexes_from_unidirectional_edge,
    get_h3_unidirectional_edges_from_hexagon,
    get_h3_unidirectional_edge_boundary,
    h3_distance,
    h3_line,
)