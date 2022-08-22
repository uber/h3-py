import h3


def test_repr():
    a = '8928308280fffff'
    b = h3.grid_ring(a, 5).pop()

    cells1 = h3.grid_ring(b, 2) | {a}
    cells2 = cells1 | {b}

    poly1 = h3.cells_to_polygons(cells1)
    poly2 = h3.cells_to_polygons(cells2)

    # unfortunately output order is nondeterministic
    poly1 = sorted(map(str, poly1))
    poly2 = sorted(map(str, poly2))

    assert poly1 == [
        '<h3.Polygon |outer|=30, |holes|=(18,)>',
        '<h3.Polygon |outer|=6, |holes|=()>',
    ]

    assert poly2 == [
        '<h3.Polygon |outer|=30, |holes|=(18,)>',
        '<h3.Polygon |outer|=6, |holes|=()>',
        '<h3.Polygon |outer|=6, |holes|=()>',
    ]
