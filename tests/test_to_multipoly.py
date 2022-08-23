import h3


def test_cells_to_polygons():
    h = '8928308280fffff'
    cells = h3.grid_disk(h, 1)

    polys = h3.cells_to_polygons(cells)
    poly = polys[0]

    poly2 = h3.Polygon(poly.outer, *poly.holes)
    out = h3.polygon_to_cells(poly2, 9)

    assert out == cells


def test_2_polys():
    h = '8928308280fffff'
    cells = h3.grid_ring(h, 2)
    cells = cells | {h}
    # cells should be a center hex, and the 2-ring around it
    # (with the 1-ring being absent)

    polys = h3.cells_to_polygons(cells)

    out = [
        h3.polygon_to_cells(poly, 9)
        for poly in polys
    ]

    assert set.union(*out) == cells
    assert set(map(len, out)) == {1, 12}
