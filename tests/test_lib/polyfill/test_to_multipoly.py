import pytest

import h3
from h3._cy.error_system import H3DuplicateInputError, H3ResMismatchError

from .. import util as u


def assert_cells_roundtrip(cells):
    """Convert cells to multi-polygon and back, checking we recover the original set."""
    res = h3.get_resolution(cells[0])
    mpoly = h3.cells_to_h3shape(cells, tight=False)

    recovered = set()
    for poly in mpoly:
        recovered.update(h3.h3shape_to_cells(poly, res))

    assert u.same_set(recovered, cells)


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


def test_empty():
    mpoly = h3.cells_to_h3shape([], tight=False)
    assert len(mpoly) == 0


def test_all_res0_cells():
    """All 122 res-0 cells cover the globe.

    cellsToMultiPolygon returns 8 thin triangular octants that tile the
    globe correctly, but h3shape_to_cells misses cells whose centroids
    fall near the edges of these very thin slices (recovers only ~69/122).
    """
    cells = h3.get_res0_cells()
    assert len(cells) == 122
    h3.cells_to_h3shape(cells, tight=False)


def test_pentagon_cell():
    cells = [h3.get_pentagons(0)[0]]
    mpoly = h3.cells_to_h3shape(cells, tight=False)

    assert len(mpoly) == 1
    assert len(mpoly[0].holes) == 0
    assert len(mpoly[0].outer) == 5  # pentagon has 5 verts

    assert_cells_roundtrip(cells)


def test_duplicate_cells_error():
    cell = '8928308280fffff'
    with pytest.raises(H3DuplicateInputError):
        h3.cells_to_h3shape([cell, cell])


def test_mixed_resolution_error():
    with pytest.raises(H3ResMismatchError):
        h3.cells_to_h3shape(['8027fffffffffff', '81efbffffffffff'])


def test_three_polygons():
    cells = [
        '8027fffffffffff', '802bfffffffffff', '804dfffffffffff',
        '8067fffffffffff', '806dfffffffffff', '8049fffffffffff',
        '805ffffffffffff', '8057fffffffffff', '807dfffffffffff',
        '80a5fffffffffff', '80a9fffffffffff', '808bfffffffffff',
        '801bfffffffffff', '8035fffffffffff', '803ffffffffffff',
        '8053fffffffffff', '8043fffffffffff', '8021fffffffffff',
        '8011fffffffffff', '801ffffffffffff', '8097fffffffffff',
    ]

    mpoly = h3.cells_to_h3shape(cells, tight=False)

    assert len(mpoly) == 3
    hole_counts = sorted(len(p.holes) for p in mpoly)
    assert hole_counts == [0, 1, 3]

    assert_cells_roundtrip(cells)


def test_issue_1049():
    cells = [
        '827487fffffffff', '82748ffffffffff', '827497fffffffff',
        '82749ffffffffff', '8274affffffffff', '8274c7fffffffff',
        '8274cffffffffff', '8274d7fffffffff', '8274e7fffffffff',
        '8274effffffffff', '8274f7fffffffff', '82754ffffffffff',
        '827c07fffffffff', '827c27fffffffff', '827c2ffffffffff',
        '827c37fffffffff', '827d87fffffffff', '827d8ffffffffff',
        '827d97fffffffff', '827d9ffffffffff', '827da7fffffffff',
        '827daffffffffff', '82801ffffffffff', '8280a7fffffffff',
        '8280affffffffff', '8280b7fffffffff', '828197fffffffff',
        '82819ffffffffff', '8281a7fffffffff', '8281b7fffffffff',
        '828207fffffffff', '82820ffffffffff', '828227fffffffff',
        '82822ffffffffff', '8282e7fffffffff', '828307fffffffff',
        '82830ffffffffff', '82831ffffffffff', '82832ffffffffff',
        '828347fffffffff', '82834ffffffffff', '828357fffffffff',
        '82835ffffffffff', '828367fffffffff', '828377fffffffff',
        '82a447fffffffff', '82a457fffffffff', '82a45ffffffffff',
        '82a467fffffffff', '82a46ffffffffff', '82a477fffffffff',
        '82a4c7fffffffff', '82a4cffffffffff', '82a4d7fffffffff',
        '82a4e7fffffffff', '82a4effffffffff', '82a4f7fffffffff',
        '82a547fffffffff', '82a54ffffffffff', '82a557fffffffff',
        '82a55ffffffffff', '82a567fffffffff', '82a577fffffffff',
        '82a837fffffffff', '82a897fffffffff', '82a8a7fffffffff',
        '82a8b7fffffffff', '82a917fffffffff', '82a927fffffffff',
        '82a937fffffffff', '82a987fffffffff', '82a98ffffffffff',
        '82a997fffffffff', '82a99ffffffffff', '82a9a7fffffffff',
        '82a9affffffffff', '82ac47fffffffff', '82ac57fffffffff',
        '82ac5ffffffffff', '82ac67fffffffff', '82ac6ffffffffff',
        '82ac77fffffffff', '82ad47fffffffff', '82ad4ffffffffff',
        '82ad57fffffffff', '82ad5ffffffffff', '82ad67fffffffff',
        '82ad77fffffffff', '82c207fffffffff', '82c217fffffffff',
        '82c227fffffffff', '82c237fffffffff', '82c287fffffffff',
        '82c28ffffffffff', '82c29ffffffffff', '82c2a7fffffffff',
        '82c2affffffffff', '82c2b7fffffffff', '82c307fffffffff',
        '82c317fffffffff', '82c31ffffffffff', '82c337fffffffff',
        '82cfb7fffffffff', '82d0c7fffffffff', '82d0d7fffffffff',
        '82d0dffffffffff', '82d0e7fffffffff', '82d0f7fffffffff',
        '82d147fffffffff', '82d157fffffffff', '82d15ffffffffff',
        '82d167fffffffff', '82d177fffffffff', '82d187fffffffff',
        '82d18ffffffffff', '82d197fffffffff', '82d19ffffffffff',
        '82d1a7fffffffff', '82d1affffffffff', '82dc47fffffffff',
        '82dc57fffffffff', '82dc5ffffffffff', '82dc67fffffffff',
        '82dc6ffffffffff', '82dc77fffffffff', '82dcc7fffffffff',
        '82dccffffffffff', '82dcd7fffffffff', '82dce7fffffffff',
        '82dceffffffffff', '82dcf7fffffffff', '82dd1ffffffffff',
        '82dd47fffffffff', '82dd4ffffffffff', '82dd57fffffffff',
        '82dd5ffffffffff', '82dd6ffffffffff', '82dd87fffffffff',
        '82dd8ffffffffff', '82dd97fffffffff', '82dd9ffffffffff',
        '82ddaffffffffff', '82ddb7fffffffff', '82dec7fffffffff',
        '82decffffffffff', '82ded7fffffffff', '82dee7fffffffff',
        '82deeffffffffff', '82def7fffffffff', '82df0ffffffffff',
        '82df1ffffffffff', '82df47fffffffff', '82df4ffffffffff',
        '82df57fffffffff', '82df5ffffffffff', '82df77fffffffff',
        '82df8ffffffffff', '82df9ffffffffff', '82e6c7fffffffff',
        '82e6cffffffffff', '82e6d7fffffffff', '82e6dffffffffff',
        '82e6effffffffff', '82e6f7fffffffff',
    ]

    mpoly = h3.cells_to_h3shape(cells, tight=False)

    assert len(mpoly) == 12
    for poly in mpoly:
        assert len(poly.holes) == 0

    assert_cells_roundtrip(cells)


def test_equator_cells():
    """Global polygon near the equator.

    cellsToMultiPolygon succeeds, but the output polygon spans the
    antimeridian so h3shape_to_cells can't fill it back (loses cells).
    """
    cells = [
        '81807ffffffffff', '817efffffffffff', '81723ffffffffff',
        '817ebffffffffff', '817c3ffffffffff', '817e3ffffffffff',
        '817a3ffffffffff', '8166fffffffffff', '8172bffffffffff',
        '816afffffffffff', '81933ffffffffff', '8168fffffffffff',
        '8188fffffffffff', '81853ffffffffff', '817f7ffffffffff',
        '8180bffffffffff', '81783ffffffffff', '81743ffffffffff',
        '8170bffffffffff', '8173bffffffffff', '8179bffffffffff',
        '817cbffffffffff', '8188bffffffffff', '81857ffffffffff',
        '816f7ffffffffff', '8177bffffffffff', '81617ffffffffff',
        '816f3ffffffffff', '8174bffffffffff', '8180fffffffffff',
        '817a7ffffffffff', '81767ffffffffff', '81757ffffffffff',
        '81957ffffffffff', '81787ffffffffff', '81847ffffffffff',
        '81653ffffffffff', '817bbffffffffff', '816cfffffffffff',
        '816abffffffffff', '815f3ffffffffff', '817c7ffffffffff',
        '8168bffffffffff', '818cbffffffffff', '818cfffffffffff',
        '818afffffffffff', '8174fffffffffff', '8172fffffffffff',
        '8170fffffffffff', '816fbffffffffff', '81657ffffffffff',
        '816c7ffffffffff', '8186bffffffffff', '81763ffffffffff',
        '818a7ffffffffff', '8186fffffffffff', '81707ffffffffff',
        '8182bffffffffff', '818f3ffffffffff', '8182fffffffffff',
    ]
    h3.cells_to_h3shape(cells, tight=False)


def test_prime_meridian():
    """Global polygon near the prime meridian.

    cellsToMultiPolygon succeeds, but the output polygon spans the
    antimeridian so h3shape_to_cells raises H3FailedError.
    """
    cells = [
        '81efbffffffffff', '81c07ffffffffff', '81d1bffffffffff',
        '81097ffffffffff', '8109bffffffffff', '81d0bffffffffff',
        '81987ffffffffff', '81017ffffffffff', '81e67ffffffffff',
        '81ddbffffffffff', '81ac7ffffffffff', '8158bffffffffff',
        '81397ffffffffff', '81593ffffffffff', '81c17ffffffffff',
        '81827ffffffffff', '81197ffffffffff', '81eebffffffffff',
        '81383ffffffffff', '81dcbffffffffff', '81757ffffffffff',
        '81093ffffffffff', '81073ffffffffff', '8159bffffffffff',
        '81f17ffffffffff', '81187ffffffffff', '81007ffffffffff',
        '81997ffffffffff', '81753ffffffffff', '81033ffffffffff',
        '81f2bffffffffff', '8138bffffffffff',
    ]
    h3.cells_to_h3shape(cells, tight=False)


def test_anti_meridian():
    """Global polygon near the anti-meridian.

    cellsToMultiPolygon succeeds, but the output polygon spans the
    antimeridian so h3shape_to_cells raises H3FailedError.
    """
    cells = [
        '817ebffffffffff', '8133bffffffffff', '81047ffffffffff',
        '81f3bffffffffff', '81dbbffffffffff', '8132bffffffffff',
        '810cbffffffffff', '81bb3ffffffffff', '81db3ffffffffff',
        '81bafffffffffff', '81177ffffffffff', '817fbffffffffff',
        '81ba3ffffffffff', '815abffffffffff', '815bbffffffffff',
        '81eafffffffffff', '81ed7ffffffffff', '81057ffffffffff',
        '819a7ffffffffff', '81eabffffffffff', '819b7ffffffffff',
        '81167ffffffffff', '81227ffffffffff', '8171bffffffffff',
        '81237ffffffffff', '810dbffffffffff', '81033ffffffffff',
        '81f2bffffffffff', '8147bffffffffff', '81f33ffffffffff',
    ]
    h3.cells_to_h3shape(cells, tight=False)


def test_issue_482_with_antimeridian():
    """https://github.com/uber/h3-py/issues/482

    Previously raised ValueError ('loops need at least 3 points').
    cellsToMultiPolygon now succeeds, but the output polygon spans the
    antimeridian so it can't roundtrip through h3shape_to_cells.
    """
    cells = [
        '8001fffffffffff', '8005fffffffffff', '8009fffffffffff', '800bfffffffffff',
        '8011fffffffffff', '8015fffffffffff', '8017fffffffffff', '801ffffffffffff',
        '8021fffffffffff', '8025fffffffffff', '802dfffffffffff', '802ffffffffffff',
        '8031fffffffffff', '8033fffffffffff', '803dfffffffffff', '803ffffffffffff',
        '8041fffffffffff', '8043fffffffffff', '804bfffffffffff', '804ffffffffffff',
        '8053fffffffffff', '8059fffffffffff', '8061fffffffffff', '8063fffffffffff',
        '8065fffffffffff', '8069fffffffffff', '806bfffffffffff', '8073fffffffffff',
        '8077fffffffffff',
    ]
    h3.cells_to_h3shape(cells, tight=False)


def test_issue_482_without_antimeridian():
    """https://github.com/uber/h3-py/issues/482

    Same issue but with antimeridian-crossing cells removed.
    Previously raised H3FailedError. cellsToMultiPolygon now succeeds,
    but the output polygon spans the antimeridian so it can't roundtrip
    through h3shape_to_cells.
    """
    cells = [
        '8001fffffffffff', '8009fffffffffff', '800bfffffffffff', '8011fffffffffff',
        '8015fffffffffff', '801ffffffffffff', '8021fffffffffff', '8025fffffffffff',
        '802dfffffffffff', '802ffffffffffff', '8031fffffffffff', '803dfffffffffff',
        '803ffffffffffff', '8041fffffffffff', '8043fffffffffff', '804bfffffffffff',
        '804ffffffffffff', '8053fffffffffff', '8059fffffffffff', '8061fffffffffff',
        '8063fffffffffff', '8065fffffffffff', '8069fffffffffff', '806bfffffffffff',
        '8073fffffffffff', '8077fffffffffff',
    ]
    h3.cells_to_h3shape(cells, tight=False)
