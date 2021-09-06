# API reference

This page lists the functions that are common to each of the
[provided APIs](api_comparison).
The APIs differ only in their input/output types
(e.g., `int` vs. `str` or `set` vs `numpy.array`).

These functions align with those explained in the
[core H3 documentation](https://h3geo.org/docs/api/indexing).

## Summaries

There is no strict hierarchy for H3 functions,
but we'll try to group functions in a reasonably logical manner.

### Identification

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   h3_is_valid
   h3_is_pentagon
   h3_is_res_class_III
   h3_is_res_class_iii
   h3_unidirectional_edge_is_valid
   versions
```

### Cells

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   geo_to_h3
   h3_to_geo
   h3_to_string
   string_to_h3
   get_res0_indexes
   get_pentagon_indexes
   num_hexagons
   h3_get_resolution
   compact
   uncompact
```

### Geographic coordinates

Functions relating H3 objects to geographic (lat/lng) coordinates.

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   point_dist
   hex_area
   cell_area
   edge_length
   exact_edge_length
   h3_to_geo_boundary
   get_h3_unidirectional_edge_boundary
   polyfill
   polyfill_geojson
   polyfill_polygon
   h3_set_to_multi_polygon
```

### Hierarchical relationships

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   h3_to_parent
   h3_to_children
   h3_to_center_child
```

### Cell grid relationships

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   hex_range
   hex_range_distances
   hex_ranges
   hex_ring
   k_ring
   k_ring_distances
   h3_distance
   h3_indexes_are_neighbors
   h3_line
```

### Edges

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   get_h3_unidirectional_edge
   get_destination_h3_index_from_unidirectional_edge
   get_h3_indexes_from_unidirectional_edge
   get_h3_unidirectional_edges_from_hexagon
   get_origin_h3_index_from_unidirectional_edge
```

### IJ-indexing

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   h3_get_base_cell
   h3_get_faces
   experimental_h3_to_local_ij
   experimental_local_ij_to_h3
```


## Definitions

```{eval-rst}
.. automodule:: h3
    :members:
    :imported-members:
```
