import h3
import pytest


class MockGeoInterface:
    def __init__(self, dictionary):
        assert isinstance(dictionary, dict)
        self.dictionary = dictionary

    @property
    def __geo_interface__(self):
        return self.dictionary


def loop_open():
    return [
        [-122.408, 37.813],
        [-122.512, 37.707],
        [-122.479, 37.815],
    ]


def loop_closed():
    loop = loop_open()
    loop += [loop[0]]
    return loop


def get_mocked(loop):
    geo = MockGeoInterface({
        'type': 'Polygon',
        'coordinates': [loop]
    })

    return geo


sf_7x7 = [
    (37.813319, -122.408987),
    (37.786630, -122.380544),
    (37.719806, -122.354474),
    (37.707613, -122.512344),
    (37.783587, -122.524719),
    (37.815157, -122.479877),
]

sf_hole1 = [
    (37.786980, -122.447120),
    (37.766410, -122.459078),
    (37.771068, -122.413710),
]

sf_hole2 = [
    (37.747976, -122.490025),
    (37.731550, -122.503758),
    (37.725440, -122.452603),
]


def test_geo_interface():
    poly = h3.H3Poly(sf_hole1)
    mpoly = h3.H3MultiPoly(poly)

    assert poly.__geo_interface__['type'] == 'Polygon'
    assert mpoly.__geo_interface__['type'] == 'MultiPolygon'

    assert (
        poly.__geo_interface__['coordinates']
        ==
        mpoly.__geo_interface__['coordinates'][0]
    )


def test_shape_repr():
    poly = h3.H3Poly(sf_hole1)
    mpoly = h3.H3MultiPoly(poly)

    assert (
        'H3MultiPoly(<H3Poly |outer|=3, |holes|=()>,)'
        == str(mpoly)
        == repr(mpoly)
    )


def test_polyfill():
    poly = h3.H3Poly(sf_7x7)
    out = h3.h3shape_to_cells(poly, res=9)

    assert len(out) == 1253
    assert '89283080527ffff' in out
    assert '89283095edbffff' in out


def test_polyfill_with_hole():
    poly = h3.H3Poly(sf_7x7, sf_hole1)

    out = h3.h3shape_to_cells(poly, res=9)
    assert len(out) == 1214

    foo = lambda x: h3.h3shape_to_cells(h3.H3Poly(x), 9)
    # todo: foo = lambda x: h3.H3Poly(x).to_cells(9)
    assert out == foo(sf_7x7) - foo(sf_hole1)


def test_polyfill_with_two_holes():

    poly = h3.H3Poly(sf_7x7, sf_hole1, sf_hole2)
    out = h3.h3shape_to_cells(poly, 9)
    assert len(out) == 1172

    foo = lambda x: h3.h3shape_to_cells(h3.H3Poly(x), 9)
    assert out == foo(sf_7x7) - (foo(sf_hole1) | foo(sf_hole2))


def test_polyfill_geo_json_compliant():
    geo = get_mocked(loop_open()).__geo_interface__
    out = h3.geo_to_cells(geo, 9)
    assert len(out) > 300


def test_polyfill_geo_interface_compliant():
    geo = get_mocked(loop_open())
    out = h3.geo_to_cells(geo, 9)
    assert len(out) > 300


def test_poly_opens_loop():
    loop = loop_closed()
    poly = h3.H3Poly(loop)

    assert loop[0] == loop[-1]
    assert len(poly.outer) == len(loop) - 1

#
#
#
# add test to ensure polygon constructor opens the loop
#
#
#
# def test_geo_to_h3shape():
#     geo = get_mocked()
#     h3shape = h3.geo_to_h3shape(geo)


def test_polyfill_down_under():
    sydney = [
        (-33.8556, 151.1979),
        (-33.8520, 151.2075),
        (-33.8580, 151.2247),
        (-33.8582, 151.2255),
        (-33.8564, 151.2353),
        (-33.8594, 151.2348),
        (-33.8641, 151.2335),
        (-33.8716, 151.2332),
        (-33.8877, 151.2240),
        (-33.8874, 151.2194),
        (-33.8870, 151.2189),
        (-33.8863, 151.2181),
        (-33.8851, 151.2158),
        (-33.8852, 151.2157),
        (-33.8851, 151.2141),
        (-33.8847, 151.2116),
        (-33.8835, 151.2083),
        (-33.8828, 151.2080),
        (-33.8816, 151.2059),
        (-33.8828, 151.2044),
        (-33.8839, 151.2028),
        (-33.8839, 151.2023),
        (-33.8842, 151.2011),
        (-33.8843, 151.1986),
        (-33.8842, 151.1986),
        (-33.8773, 151.1948),
        (-33.8741, 151.1923),
        (-33.8697, 151.1851),
        (-33.8625, 151.1903),
        (-33.8613, 151.1987),
        (-33.8556, 151.1979),
    ]

    poly = h3.H3Poly(sydney)
    out = h3.h3shape_to_cells(poly, 9)
    assert len(out) == 92
    assert '89be0e34207ffff' in out
    assert '89be0e35ddbffff' in out


def test_polyfill_far_east():
    geo = [
        (41.925781, 142.864838),
        (42.299659, 142.864838),
        (42.299659, 143.415527),
        (41.925781, 143.415527),
        (41.925781, 142.864838),
    ]

    poly = h3.H3Poly(geo)
    out = h3.h3shape_to_cells(poly, 9)
    assert len(out) == 18507
    assert '892e18d16c3ffff' in out
    assert '892e1ebb5a7ffff' in out


def test_polyfill_southern_tip():
    geo = [
        (-55.416544, -67.642822),
        (-54.354956, -67.642822),
        (-54.354956, -64.742432),
        (-55.416544, -64.742432),
        (-55.416544, -67.642822),
    ]

    poly = h3.H3Poly(geo)
    out = h3.h3shape_to_cells(poly, 9)
    assert len(out) == 223247
    assert '89df4000003ffff' in out
    assert '89df4636b27ffff' in out


def test_polyfill_null_island():
    geo = [
        (-3, -3),
        (+3, -3),
        (+3, +3),
        (-3, +3),
        (-3, -3),
    ]

    poly = h3.H3Poly(geo)
    out = h3.h3shape_to_cells(poly, 4)
    assert len(out) == 345
    assert '847421bffffffff' in out
    assert '84825ddffffffff' in out


def test_cells_to_h3shape_empty():
    mpoly = h3.cells_to_h3shape([])
    assert list(mpoly) == []


def test_cells_to_h3shape_single():
    h = '89283082837ffff'
    cells = {h}

    mpoly = h3.cells_to_h3shape(cells)
    assert len(mpoly) == 1
    poly = mpoly[0]

    vertices = h3.cell_to_boundary(h)
    expected_poly = h3.H3Poly(vertices)

    assert set(poly.outer) == set(expected_poly.outer)
    assert poly.holes == expected_poly.holes == ()


def test_cells_to_h3shape_contiguous():
    a = '89283082837ffff'
    b = '89283082833ffff'
    assert h3.are_neighbor_cells(a, b)

    mpoly = h3.cells_to_h3shape([a, b])
    assert len(mpoly) == 1
    poly = mpoly[0]

    assert len(poly.outer) == 10
    assert poly.holes == ()

    verts_a = h3.cell_to_boundary(a)
    verts_b = h3.cell_to_boundary(b)
    assert set(poly.outer) == set(verts_a) | set(verts_b)


def test_cells_to_h3shape_non_contiguous():
    a = '89283082837ffff'
    b = '8928308280fffff'
    assert not h3.are_neighbor_cells(a, b)

    mpoly = h3.cells_to_h3shape([a, b])
    assert len(mpoly) == 2

    assert all(poly.holes == () for poly in mpoly)
    assert all(len(poly.outer) == 6 for poly in mpoly)

    verts_a = h3.cell_to_boundary(a)
    verts_b = h3.cell_to_boundary(b)

    verts_both = set.union(*[set(poly.outer) for poly in mpoly])
    assert verts_both == set(verts_a) | set(verts_b)


def test_cells_to_h3shape_hole():
    # Six hexagons in a ring around a hole
    cells = [
        '892830828c7ffff', '892830828d7ffff', '8928308289bffff',
        '89283082813ffff', '8928308288fffff', '89283082883ffff',
    ]
    mpoly = h3.cells_to_h3shape(cells)

    assert len(mpoly) == 1
    poly = mpoly[0]

    assert len(poly.holes) == 1
    assert len(poly.holes[0]) == 6
    assert len(poly.outer) == 6 * 3


def test_cells_to_h3shape_2grid_disk():
    h = '8930062838bffff'
    cells = h3.grid_disk(h, 2)
    mpoly = h3.cells_to_h3shape(cells)

    assert len(mpoly) == 1
    poly = mpoly[0]

    assert len(poly.holes) == 0
    assert len(poly.outer) == 6 * (2 * 2 + 1)


def test_multipoly_checks():

    with pytest.raises(ValueError):
        h3.H3MultiPoly('foo')

    with pytest.raises(ValueError):
        h3.H3MultiPoly(1)

    with pytest.raises(ValueError):
        h3.H3MultiPoly([[(1, 2), (3, 4)]])
