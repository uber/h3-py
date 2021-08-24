# API reference

```{warning}
This page is a work in progress and incomplete.
```

This page lists the functions that are common to each of the standard APIs,
and differ only by their input/output types (e.g., `int` vs. `str` or `set` vs `numpy.array`).

## Summaries

Below, we try to group functions in a reasonably logical manner, but any such grouping
will be imperfect.

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
