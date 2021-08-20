# APIs

```{warning}
This page is a work in progress and incomplete.
```

## Summaries

### Functions

#### Identification

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

#### Cells

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   compact
   get_pentagon_indexes
   get_res0_indexes
   h3_distance
   h3_get_base_cell
   h3_get_faces
   h3_get_resolution
   h3_line
   h3_to_center_child
   h3_to_children
   h3_to_parent
   h3_to_string
   num_hexagons
   string_to_h3
   uncompact
```

#### Lat/Lng Conversion

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   geo_to_h3
   h3_to_geo
   h3_to_geo_boundary
   point_dist
   cell_area
   hex_area
   edge_length
   exact_edge_length
   polyfill
   polyfill_geojson
   polyfill_polygon
   h3_set_to_multi_polygon
```

#### Grid Ring and Disk

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   hex_range
   hex_range_distances
   hex_ranges
   hex_ring
   k_ring
   k_ring_distances
```

#### Edges

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   get_destination_h3_index_from_unidirectional_edge
   get_h3_indexes_from_unidirectional_edge
   get_h3_unidirectional_edge
   get_h3_unidirectional_edge_boundary
   get_h3_unidirectional_edges_from_hexagon
   get_origin_h3_index_from_unidirectional_edge
   h3_indexes_are_neighbors
```

#### Experimental

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   experimental_h3_to_local_ij
   experimental_local_ij_to_h3
```

### Errors

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   H3CellError
   H3DistanceError
   H3EdgeError
   H3ResolutionError
   H3ValueError
```



## Definitions

```{eval-rst}
.. automodule:: h3
    :members:
    :imported-members:
```
