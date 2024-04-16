# API Quick Reference

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

## Polygon interface

The ``H3Poly`` and ``H3MultiPoly`` objects and their related functions allow users to represent (multi)polygons of lat/lng points and convert back and forth between H3 cells.

The objects and functions also compatible with the popular [``__geo_interface__`` protocol](https://gist.github.com/sgillies/2217756), which is used by Python geospatial libraries like [GeoPandas](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.__geo_interface__.html) and many plotting libraries.

See the [polygon tutorial](./polygon_tutorial.ipynb) for a walkthrough.

### Polygon objects

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   H3Shape
   H3Poly
   H3MultiPoly
```

### Conversion functions

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   h3shape_to_geo
   geo_to_h3shape
   h3shape_to_cells
   cells_to_h3shape
   geo_to_cells
   cells_to_geo
```