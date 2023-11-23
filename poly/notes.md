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

note: `h3.shape_to_cells()` could take in lots of formats. or do we put that in the H3shape constructor? maybe functional is better?

```
shape.__geo_interface__
shape.to_cells(res)
```

```
H3Shape(<something with geo_interface>)
H3Shape(dict)
H3Shape(geojson string)
```

## 2023-03-26

- todo: set up H3Shape constructor (and subclasses) to take in `__geo_interface__` inputs


## 2023-11-07

- all the `__init__.py` for the APIs should be sync'd
    + three dots is too many dots for an import statement
 
# 2023-11-23 Reprs for poly and multipoly

"""
Q: what do codes of the form `[n/(x,y,z)]` mean?
A: a polygon with an outer ring of n unique vertices, and 3 holes with x,y,and z unique vertices, respectively.
"""

```
h3.H3Poly(
    [(37.68, -122.54), (37.68, -122.34), (37.82, -122.34), (37.82, -122.54)],
    [(37.76, -122.51), (37.76, -122.44), (37.81, -122.51)],
    [(37.71, -122.43), (37.71, -122.37), (37.73, -122.37), (37.75, -122.41),
     (37.73, -122.43)],
)

<H3Poly: [4/(3, 5)]>
<H3Poly: 4/(3, 5)> (best)
<H3Poly 4/(3, 5)>

h3.H3Poly([(37.68, -122.54), (37.68, -122.34), (37.82, -122.34), (37.82, -122.54)],)
<H3Poly: [4]>
<H3Poly: 4>
```

```
<H3MultiPoly: 632/(6, 6, 6, 6, 6), 290/(6,), 120, 12, 10, 10>
<H3MultiPoly: 632/(6,6,6,6,6), 290/(6), 120, 12, 10, 10>   (best?)
<H3MultiPoly: <632/(6, 6, 6, 6, 6)>, <290/(6,)>, <120>, <12>, <10>, <10>>
<H3MultiPoly: [632/(6, 6, 6, 6, 6)], [290/(6,)], [120], [12], [10], [10]>
```

