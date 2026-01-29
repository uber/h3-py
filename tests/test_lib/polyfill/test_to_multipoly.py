import pytest

import h3
from h3._cy.error_system import H3FailedError

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


def test_cells_to_h3shape_transmeridian_error():
    """
    Test for https://github.com/uber/h3-py/issues/476

    Cells along the equator and meridian trigger an error in the C library's
    normalizeMultiPolygon. Previously this caused a segfault because the error
    code wasn't checked. Now it should raise H3FailedError.
    """
    cells = [
        '81007ffffffffff', '81017ffffffffff', '81033ffffffffff',
        '81047ffffffffff', '81057ffffffffff', '81093ffffffffff',
        '81097ffffffffff', '8109bffffffffff', '810cbffffffffff',
        '810dbffffffffff', '81167ffffffffff', '81177ffffffffff',
        '81187ffffffffff', '81197ffffffffff', '81227ffffffffff',
        '8132bffffffffff', '8133bffffffffff', '81383ffffffffff',
        '8138bffffffffff', '81397ffffffffff', '8147bffffffffff',
        '8158bffffffffff', '81593ffffffffff', '8159bffffffffff',
        '815abffffffffff', '815bbffffffffff', '815f3ffffffffff',
        '81617ffffffffff', '81657ffffffffff', '8166fffffffffff',
        '8168bffffffffff', '8168fffffffffff', '816abffffffffff',
        '816afffffffffff', '816c7ffffffffff', '816cfffffffffff',
        '816f3ffffffffff', '816f7ffffffffff', '816fbffffffffff',
        '81707ffffffffff', '8170bffffffffff', '8170fffffffffff',
        '8171bffffffffff', '8172bffffffffff', '8172fffffffffff',
        '8173bffffffffff', '81743ffffffffff', '8174bffffffffff',
        '81753ffffffffff', '81757ffffffffff', '81763ffffffffff',
        '81767ffffffffff', '8177bffffffffff', '81783ffffffffff',
        '81787ffffffffff', '8179bffffffffff', '817a3ffffffffff',
        '817a7ffffffffff', '817bbffffffffff', '817c3ffffffffff',
        '817c7ffffffffff', '817cbffffffffff', '817e3ffffffffff',
        '817ebffffffffff', '817efffffffffff', '817f7ffffffffff',
        '817fbffffffffff', '81807ffffffffff', '8180bffffffffff',
        '8180fffffffffff', '81827ffffffffff', '8182bffffffffff',
        '8182fffffffffff', '81853ffffffffff', '81857ffffffffff',
        '8186bffffffffff', '8186fffffffffff', '8188bffffffffff',
        '8188fffffffffff', '818a7ffffffffff', '818afffffffffff',
        '818cbffffffffff', '818cfffffffffff', '818f3ffffffffff',
        '81933ffffffffff', '81987ffffffffff', '81997ffffffffff',
        '819a7ffffffffff', '819b7ffffffffff', '81ac7ffffffffff',
        '81ba3ffffffffff', '81bafffffffffff', '81bb3ffffffffff',
        '81c07ffffffffff', '81c17ffffffffff', '81d0bffffffffff',
        '81d1bffffffffff', '81db3ffffffffff', '81dbbffffffffff',
        '81dcbffffffffff', '81ddbffffffffff', '81e67ffffffffff',
        '81eabffffffffff', '81eafffffffffff', '81ed7ffffffffff',
        '81eebffffffffff', '81efbffffffffff', '81f17ffffffffff',
        '81f2bffffffffff', '81f33ffffffffff', '81f3bffffffffff',
    ]

    with pytest.raises(H3FailedError):
        h3.cells_to_h3shape(cells)
