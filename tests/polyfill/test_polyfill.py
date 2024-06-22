import h3
import pytest

from h3 import H3ResDomainError

from .. import util as u


def get_us_box_coords():

    # big center chunk of the US in lat/lng order
    outer = [
        [42.68, -110.61],
        [32.17, -109.02],
        [31.57,  -94.26],
        [42.94,  -89.38],
        [42.68, -110.61]
    ]

    hole1 = [
        [39.77, -105.07],
        [34.81, -104.72],
        [34.77,  -98.39],
        [40.14,  -96.72],
        [39.77, -105.07]
    ]

    hole2 = [
        [41.37, -98.61],
        [40.04, -91.80],
        [42.32, -91.80],
        [41.37, -98.61]
    ]

    return outer, hole1, hole2


def test_h3shape_to_cells():

    # approximate lat/lngs for State of Maine
    maine = [
        (45.137, -67.137),
        (44.810, -66.965),
        (44.325, -68.033),
        (43.980, -69.060),
        (43.684, -70.116),
        (43.090, -70.646),
        (43.080, -70.751),
        (43.220, -70.798),
        (43.368, -70.982),
        (43.466, -70.944),
        (45.305, -71.085),
        (45.460, -70.660),
        (45.915, -70.305),
        (46.693, -70.000),
        (47.448, -69.237),
        (47.185, -68.905),
        (47.355, -68.234),
        (47.066, -67.790),
        (45.703, -67.791),
        (45.137, -67.137),
    ]

    # a very rough hexagonal approximation to the State of Maine
    expected = {
        '832b13fffffffff',
        '832b18fffffffff',
        '832b1afffffffff',
        '832b1efffffffff',
        '832ba9fffffffff',
        '832badfffffffff'
    }

    poly = h3.LatLngPoly(maine)
    out = h3.h3shape_to_cells(poly, 3)

    assert u.same_set(out, expected)


def test_h3shape_to_cells2():
    lnglat, _, _ = get_us_box_coords()

    poly = h3.LatLngPoly(lnglat)
    out = h3.h3shape_to_cells(poly, 5)

    assert len(out) == 7063


# todo: we can generate segfaults with malformed input data to polyfill
# need to test for this and avoid segfault
# def test_polyfill_segfault():
#     pass


def test_h3shape_to_cells_holes():

    outer, hole1, hole2 = get_us_box_coords()

    assert 7063 == len(
        h3.h3shape_to_cells(h3.LatLngPoly(outer), 5)
    )

    for res in 1, 2, 3, 4, 5:
        cells_all = h3.h3shape_to_cells(h3.LatLngPoly(outer), res)
        poly = h3.LatLngPoly(outer, hole1, hole2)
        cells_holes = set(h3.h3shape_to_cells(poly, res=res))

        cells_1 = set(h3.h3shape_to_cells(h3.LatLngPoly(hole1), res))
        cells_2 = set(h3.h3shape_to_cells(h3.LatLngPoly(hole2), res))

        assert len(cells_all) == len(cells_holes) + len(cells_1) + len(cells_2)
        assert u.same_set(
            cells_all,
            set.union(cells_holes, cells_1, cells_2)
        )


def test_resolution():
    poly = h3.LatLngPoly([])

    assert h3.h3shape_to_cells(poly, 0) == []
    assert h3.h3shape_to_cells(poly, 15) == []

    with pytest.raises(H3ResDomainError):
        h3.h3shape_to_cells(poly, -1)

    with pytest.raises(H3ResDomainError):
        h3.h3shape_to_cells(poly, 16)


def test_invalid_polygon():
    """
    We were previously seeing segfaults on data like
    this because we weren't raising errors inside
    some `cdef` functions.
    """
    with pytest.raises(TypeError):
        h3.LatLngPoly([1, 2, 3])

    with pytest.raises(ValueError):
        h3.LatLngPoly([[1, 2, 3]])


def test_bad_geo_input():
    with pytest.raises(ValueError):
        h3.h3shape_to_cells('not a shape', 9)

    with pytest.raises(ValueError):
        h3.geo_to_cells({'type': 'not a shape', 'coordinates': None}, 9)


def test_cells_to_geo():
    h = '89754e64993ffff'
    res = h3.get_resolution(h)

    geo = h3.cells_to_geo([h], tight=False)
    coord = geo['coordinates']

    assert geo['type'] == 'MultiPolygon'  # todo: TBD
    assert len(coord) == 1
    coord = coord[0]
    assert len(coord[0]) == 7
    assert coord[0][0] == coord[0][-1]

    assert h3.geo_to_cells(geo, res) == [h]
