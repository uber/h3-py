import h3
import pytest

from h3 import H3ResDomainError


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

    # lat/lngs for State of Maine
    maine = [
        (45.137451890638886, -67.13734351262877),
        (44.8097, -66.96466),
        (44.3252, -68.03252),
        (43.98, -69.06),
        (43.68405, -70.11617),
        (43.090083319667144, -70.64573401557249),
        (43.08003225358635, -70.75102474636725),
        (43.21973948828747, -70.79761105007827),
        (43.36789581966826, -70.98176001655037),
        (43.46633942318431, -70.94416541205806),
        (45.3052400000002, -71.08482),
        (45.46022288673396, -70.6600225491012),
        (45.914794623389355, -70.30495378282376),
        (46.69317088478567, -70.00014034695016),
        (47.44777598732787, -69.23708614772835),
        (47.184794623394396, -68.90478084987546),
        (47.35462921812177, -68.23430497910454),
        (47.066248887716995, -67.79035274928509),
        (45.702585354182816, -67.79141211614706),
        (45.137451890638886, -67.13734351262877)
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

    poly = h3.H3Poly(maine)
    out = h3.h3shape_to_cells(poly, 3)

    assert out == expected


def test_h3shape_to_cells2():
    lnglat, _, _ = get_us_box_coords()

    poly = h3.H3Poly(lnglat)
    out = h3.h3shape_to_cells(poly, 5)

    assert len(out) == 7063


# todo: we can generate segfaults with malformed input data to polyfill
# need to test for this and avoid segfault
# def test_polyfill_segfault():
#     pass


def test_h3shape_to_cells_holes():

    outer, hole1, hole2 = get_us_box_coords()

    assert 7063 == len(
        h3.h3shape_to_cells(h3.H3Poly(outer), 5)
    )

    for res in 1, 2, 3, 4, 5:
        cells_all = h3.h3shape_to_cells(h3.H3Poly(outer), res)
        cells_holes = h3.h3shape_to_cells(h3.H3Poly(outer, hole1, hole2), res=res)

        cells_1 = h3.h3shape_to_cells(h3.H3Poly(hole1), res)
        cells_2 = h3.h3shape_to_cells(h3.H3Poly(hole2), res)

        assert len(cells_all) == len(cells_holes) + len(cells_1) + len(cells_2)
        assert cells_all == set.union(cells_holes, cells_1, cells_2)


def test_resolution():
    poly = h3.H3Poly([])

    assert h3.h3shape_to_cells(poly, 0) == set()
    assert h3.h3shape_to_cells(poly, 15) == set()

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
        poly = h3.H3Poly([1, 2, 3])
        h3.h3shape_to_cells(poly, 4)

    with pytest.raises(ValueError):
        poly = h3.H3Poly([[1, 2, 3]])
        h3.h3shape_to_cells(poly, 4)


def test_bad_geo_input():
    with pytest.raises(ValueError):
        h3.h3shape_to_cells('not a shape', 9)

    with pytest.raises(ValueError):
        h3.geo_to_cells({'type': 'not a shape', 'coordinates': None}, 9)


def test_cells_to_geo():
    h = '89754e64993ffff'
    res = h3.get_resolution(h)

    geo = h3.cells_to_geo([h])
    coord = geo['coordinates']

    assert geo['type'] == 'MultiPolygon'  # todo: TBD
    assert len(coord) == 1
    coord = coord[0]
    assert len(coord[0]) == 7
    assert coord[0][0] == coord[0][-1]

    assert h3.geo_to_cells(geo, res) == {h}
