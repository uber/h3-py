import h3
import pytest


def test_repr():
    a = '8928308280fffff'
    b = h3.grid_ring(a, 5).pop()

    cells1 = h3.grid_ring(b, 2) | {a}
    cells2 = cells1 | {b}

    mpoly1 = h3.cells_to_h3shape(cells1)
    mpoly2 = h3.cells_to_h3shape(cells2)

    # unfortunately output order is nondeterministic
    mpoly1 = sorted(map(str, mpoly1))
    mpoly2 = sorted(map(str, mpoly2))

    assert mpoly1 == [
        '<H3Poly: [30/(18,)]>',
        '<H3Poly: [6]>',
    ]

    assert mpoly2 == [
        '<H3Poly: [30/(18,)]>',
        '<H3Poly: [6]>',
        '<H3Poly: [6]>',
    ]


def test_h3poly_len():
    cells = {'8928308280fffff'}

    poly = h3.cells_to_h3shape(cells, tight=True)

    with pytest.raises(NotImplementedError):
        len(poly)


def test_bad_subclass():
    class H3Shoop(h3.H3Shape):
        def __geo_interface__():
            pass

    with pytest.raises(ValueError):
        h3.h3shape_to_cells(H3Shoop(), res=9)
