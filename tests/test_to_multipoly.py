import h3


def test_cells_to_multi_polygon():
    h = '8928308280fffff'
    hexes = h3.grid_disk(h, 1)

    mpoly = h3.cells_to_multi_polygon(hexes)

    out = h3.polygon_to_cells(mpoly[0][0], 9, holes=None)

    assert out == hexes


def test_2_polys():
    h = '8928308280fffff'
    hexes = h3.grid_ring(h, 2)
    hexes = hexes | {h}
    # hexes should be a center hex, and the 2-ring around it
    # (with the 1-ring being absent)

    out = [
        h3.polygon_to_cells(poly[0], 9, holes=poly[1:])
        for poly in h3.cells_to_multi_polygon(hexes, geo_json=False)
    ]

    assert set.union(*out) == hexes


def test_2_polys_json():
    h = '8928308280fffff'
    hexes = h3.grid_ring(h, 2)
    hexes = hexes | {h}
    # hexes should be a center hex, and the 2-ring around it
    # (with the 1-ring being absent)

    # not deterministic which poly is first..
    poly1, poly2 = h3.cells_to_multi_polygon(hexes, geo_json=True)

    assert {len(poly1), len(poly2)} == {1, 2}

    for poly in poly1, poly2:
        for loop in poly:
            assert loop[0] == loop[-1]


def test_2_polys_not_json():
    h = '8928308280fffff'
    hexes = h3.grid_ring(h, 2)
    hexes = hexes | {h}
    # hexes should be a center hex, and the 2-ring around it
    # (with the 1-ring being absent)

    # not deterministic which poly is first..
    poly1, poly2 = h3.cells_to_multi_polygon(hexes, geo_json=False)

    assert {len(poly1), len(poly2)} == {1, 2}

    for poly in poly1, poly2:
        for loop in poly:
            assert loop[0] != loop[-1]
