import h3


from .. import util as u


def test_cells_to_h3shape():
    h = '8928308280fffff'
    cells = h3.grid_disk(h, 1)

    mpoly = h3.cells_to_h3shape(cells, tight=False)
    poly = mpoly[0]

    poly2 = h3.LatLngPoly(poly.outer, *poly.holes)
    out = h3.h3shape_to_cells(poly2, 9)

    assert u.same_set(out, cells)


def test_cells_to_h3shape_tight():
    h = '8928308280fffff'
    cells = h3.grid_disk(h, 1)

    poly = h3.cells_to_h3shape(cells, tight=True)
    poly2 = h3.LatLngPoly(poly.outer, *poly.holes)
    out = h3.h3shape_to_cells(poly2, 9)

    assert u.same_set(out, cells)


def test_2_polys():
    h = '8928308280fffff'
    cells = h3.grid_ring(h, 2)
    cells = cells + [h]
    # cells should be a center hex, and the 2-ring around it
    # (with the 1-ring being absent)

    mpoly = h3.cells_to_h3shape(cells)

    out = [
        set(h3.h3shape_to_cells(poly, 9))
        for poly in mpoly
    ]

    assert u.same_set(
        set.union(*out),
        cells
    )
    assert set(map(len, out)) == {1, 12}
