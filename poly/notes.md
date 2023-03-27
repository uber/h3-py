# notes

- https://github.com/uber/h3-py/issues/284
- https://gist.github.com/sgillies/2217756
- "GeoJSON-like"
    + https://geopandas.org/en/stable/docs/reference/api/geopandas.GeoDataFrame.__geo_interface__.html


```
h3.polygon_to_cells(cells)
h3.cells_to_polygons(cells)
h3.polygons_to_cells(polys, res)
```


```
h3.cells_to_shape(cells) -> H3Poly or H3MultiPoly
h3.shape_to_cells(H3Poly or H3MulitPoly) -> cells
```

```
shape.__geo_interface__
shape.to_cells(res)
```

```
H3Shape(<something with geo_interface>)
H3Shape(dict)
H3Shape(geojson string)
```
