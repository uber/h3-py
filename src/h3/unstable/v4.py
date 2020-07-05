# flake8: noqa

# todo: what are the pythonic names?

# what if we put this in an object? what would it look like?
# a temporary API wrapper

# what if we organized by module

from ..api.basic_str import (
    compact as
        compact,

    edge_length as
        hex_edge_length_avg,

    geo_to_h3 as
        point_to_cell,

    get_destination_h3_index_from_unidirectional_edge as
        edge_destination,

    get_h3_indexes_from_unidirectional_edge as
        directed_edge_cells,

    get_h3_unidirectional_edge as
        cells_to_directed_edge,

    get_h3_unidirectional_edge_boundary as
        directed_edge_boundary, # what's a boundary?

    get_h3_unidirectional_edges_from_hexagon as
        origin_to_directed_edges,

    get_origin_h3_index_from_unidirectional_edge as
        edge_origin,

    get_pentagon_indexes as
        pentagons,

    get_res0_indexes as
        res0_cells,

    h3_distance as
        grid_distance,

    h3_get_base_cell as
        base_cell_number,

    h3_get_faces as
        faces,

    h3_get_resolution as
        resolution,

    h3_indexes_are_neighbors as
        are_neighbor_cells,

    h3_is_pentagon as
        is_pentagon,

    h3_is_res_class_III as
        is_res_class_III,
    # h3_is_res_class_iii as _, # executive decision!

    h3_is_valid as
        is_valid_cell,

    h3_line as
        grid_path_cells,

    h3_set_to_multi_polygon as
        cells_to_multipolygon,

    h3_to_center_child as
        center_child,

    h3_to_children as
        children,

    h3_to_geo as
        cell_to_point,

    h3_to_geo_boundary as
        cell_to_boundary,

    h3_to_parent as
        parent,

    h3_to_string as
        int_to_str,

    h3_unidirectional_edge_is_valid as
        is_valid_directed_edge,

    hex_area as
        hex_area_avg,

    # hex_range as _,
    # hex_range_distances as _, # not sure we want this one; easy for user to implement
    # hex_ranges as _,

    hex_ring as
        grid_ring,
    hex_ring as
        ring, # used often enough that i think it deserves an alias

    k_ring as
        grid_disk,
    k_ring as
        disk, # used often enough that i think it deserves an alias

    k_ring_distances as
        grid_disk_distances,

    num_hexagons as
        num_cells,

    polyfill as
        polygon_to_cells,

    polyfill_geojson as
        geojson_to_cells, # still need to figure out the final polyfill interface

    #polyfill_polygon as _,

    string_to_h3 as
        str_to_int,

    uncompact as
        uncompact,

    versions as
        versions,
)
