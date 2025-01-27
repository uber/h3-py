# API Quick Reference

```{tip}
Function names changed significantly with `h3-py` `v4.0` to align with the C library: https://h3geo.org/docs/library/migration-3.x/functions
```

We list the functions that are shared between the
[provided APIs](api_comparison).
The APIs differ only in their input/output types
(e.g., `int` vs. `str` or `list` vs `numpy.array`).

These functions correspond to those explained in the
[H3 C library documentation](https://h3geo.org/docs/api/indexing),
and should be generally aligned with the
[other language bindings](https://h3geo.org/docs/community/bindings).

## Identification

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   is_valid_cell
   is_pentagon
   is_res_class_III
   is_valid_directed_edge
   is_valid_vertex
```

## Index representation

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   int_to_str
   str_to_int
```


## Cell properties

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   get_res0_cells
   get_pentagons
   get_num_cells
   get_resolution
   get_base_cell_number
```

## Geographic coordinates

Functions relating H3 objects to geographic (lat/lng) coordinates.

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   latlng_to_cell
   cell_to_latlng
   cell_area
   edge_length
   cell_to_boundary
   directed_edge_to_boundary
   great_circle_distance
   average_hexagon_area
   average_hexagon_edge_length
```

## Hierarchical relationships

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   cell_to_parent
   cell_to_children
   cell_to_center_child
   cell_to_children_size
   cell_to_child_pos
   child_pos_to_cell
   compact_cells
   uncompact_cells
```

## Cell grid relationships

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   grid_ring
   grid_disk
   grid_distance
   are_neighbor_cells
   grid_path_cells
```

## Edges

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   cells_to_directed_edge
   directed_edge_to_cells
   get_directed_edge_origin
   get_directed_edge_destination
   origin_to_directed_edges
```

## Vertexes

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   cell_to_vertex
   cell_to_vertexes
   vertex_to_latlng
```

## Polygon interface

The ``LatLngPoly`` and ``LatLngMultiPoly`` objects and their related functions allow users to represent (multi)polygons of lat/lng points and convert back and forth between H3 cells.

The objects and functions also compatible with the popular [``__geo_interface__`` protocol](https://gist.github.com/sgillies/2217756), which is used by Python geospatial libraries like [GeoPandas](https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.__geo_interface__.html) and many plotting libraries.

See the [polygon tutorial](./polygon_tutorial.ipynb) for a walkthrough.

```{tip}
As with other `h3-py` functions, the polygon interface expects coordinate pairs in **lat/lng** order.
Note that this is reversed from [``__geo_interface__``](https://gist.github.com/sgillies/2217756) objects, which are given in **lng/lat** order.
```

### Polygon objects

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   H3Shape
   LatLngPoly
   LatLngMultiPoly
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

#### Additional functions

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   polygon_to_cells
   polygon_to_cells_experimental
   h3shape_to_cells_experimental
```


## Specialized functions

### `h3-py` library

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   versions
```

### IJ-indexing

```{eval-rst}
.. currentmodule:: h3

.. autosummary::
   get_icosahedron_faces
   cell_to_local_ij
   local_ij_to_cell
```
