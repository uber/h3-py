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
   is_valid_cell
   is_pentagon
   is_res_class_III
   is_valid_directed_edge
   versions
```

### Cells

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   latlng_to_cell
   cell_to_latlng
   int_to_str
   str_to_int
   get_res0_cells
   get_pentagons
   get_num_cells
   get_resolution
   compact_cells
   uncompact_cells
```

### Geographic coordinates

Functions relating H3 objects to geographic (lat/lng) coordinates.

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   great_circle_distance
   average_hexagon_area
   cell_area
   edge_length
   average_hexagon_edge_length
   cell_to_boundary
   directed_edge_to_boundary
   polygon_to_cells
   cells_to_polygons
```

### Hierarchical relationships

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   cell_to_parent
   cell_to_children
   cell_to_center_child
```

### Cell grid relationships

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   grid_ring
   grid_disk
   grid_distance
   are_neighbor_cells
   grid_path_cells
```

### Edges

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   cells_to_directed_edge
   get_directed_edge_destination
   directed_edge_to_cells
   origin_to_directed_edges
   get_directed_edge_origin
```

### IJ-indexing

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   get_base_cell_number
   get_icosahedron_faces
   cell_to_local_ij
   local_ij_to_cell
```


## Definitions

```{eval-rst}
.. automodule:: h3
    :members:
    :imported-members:
```
