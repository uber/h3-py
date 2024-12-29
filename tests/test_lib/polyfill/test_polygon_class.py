import h3
import pytest


def test_repr():
    a = '8928308280fffff'
    b = h3.grid_ring(a, 5).pop()

    cells1 = h3.grid_ring(b, 2) + [a]
    cells2 = cells1 + [b]

    mpoly1 = h3.cells_to_h3shape(cells1)
    mpoly2 = h3.cells_to_h3shape(cells2)

    # unfortunately output order is nondeterministic
    mpoly1 = sorted(map(str, mpoly1))
    mpoly2 = sorted(map(str, mpoly2))

    assert mpoly1 == [
        '<LatLngPoly: [30/(18,)]>',
        '<LatLngPoly: [6]>',
    ]

    assert mpoly2 == [
        '<LatLngPoly: [30/(18,)]>',
        '<LatLngPoly: [6]>',
        '<LatLngPoly: [6]>',
    ]


def test_LatLngPoly_len():
    cells = {'8928308280fffff'}

    poly = h3.cells_to_h3shape(cells, tight=True)

    with pytest.raises(NotImplementedError):
        len(poly)


def test_bad_subclass():
    class H3Shoop(h3.H3Shape):
        def __geo_interface__(self):
            return 'foo'

    shoop = H3Shoop()
    shoop.__geo_interface__()
    with pytest.raises(ValueError):
        h3.h3shape_to_cells(shoop, res=9)
