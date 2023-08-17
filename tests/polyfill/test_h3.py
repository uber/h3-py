import h3


class MockGeoInterface:
    def __init__(self, dictionary):
        assert isinstance(dictionary, dict)
        self.dictionary = dictionary

    @property
    def __geo_interface__(self):
        return self.dictionary


sf_7x7 = [
    (37.813318999983238, -122.4089866999972145),
    (37.7866302000007224, -122.3805436999997056),
    (37.7198061999978478, -122.3544736999993603),
    (37.7076131999975672, -122.5123436999983966),
    (37.7835871999971715, -122.5247187000021967),
    (37.8151571999998453, -122.4798767000009008),
]

sf_hole1 = [
    (37.7869802, -122.4471197),
    (37.7664102, -122.4590777),
    (37.7710682, -122.4137097),
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
    out = h3.shape_to_cells(poly, res=9)

    assert len(out) == 1253
    assert '89283080527ffff' in out
    assert '89283095edbffff' in out


def test_polyfill_with_hole():
    poly = h3.H3Poly(sf_7x7, sf_hole1)

    out = h3.shape_to_cells(poly, res=9)
    assert len(out) == 1214

    foo = lambda x: h3.shape_to_cells(h3.H3Poly(x), 9)
    # todo: foo = lambda x: h3.H3Poly(x).to_cells(9)
    assert out == foo(sf_7x7) - foo(sf_hole1)


def test_polyfill_with_two_holes():

    poly = h3.H3Poly(sf_7x7, sf_hole1, sf_hole2)
    out = h3.shape_to_cells(poly, 9)
    assert len(out) == 1172

    foo = lambda x: h3.shape_to_cells(h3.H3Poly(x), 9)
    assert out == foo(sf_7x7) - (foo(sf_hole1) | foo(sf_hole2))


def test_polyfill_geo_json_compliant():
    geo = {
        'type': 'Polygon',
        'coordinates': [
            [
                [-122.4089866999972145, 37.813318999983238],
                [-122.3805436999997056, 37.7866302000007224],
                [-122.3544736999993603, 37.7198061999978478],
                [-122.5123436999983966, 37.7076131999975672],
                [-122.5247187000021967, 37.7835871999971715],
                [-122.4798767000009008, 37.8151571999998453],
            ]
        ]
    }

    out = h3.geo_to_cells(geo, 9)
    assert len(out) > 1000


def test_polyfill_geo_interface_compliant():
    geo = MockGeoInterface({
        'type': 'Polygon',
        'coordinates': [
            [
                [-122.4089866999972145, 37.813318999983238],
                [-122.3805436999997056, 37.7866302000007224],
                [-122.3544736999993603, 37.7198061999978478],
                [-122.5123436999983966, 37.7076131999975672],
                [-122.5247187000021967, 37.7835871999971715],
                [-122.4798767000009008, 37.8151571999998453],
            ]
        ]
    })

    out = h3.geo_to_cells(geo, 9)
    assert len(out) > 1000


def test_polyfill_down_under():
    sydney = [
        (-33.8555555, 151.1979259),
        (-33.8519779, 151.2074556),
        (-33.8579597, 151.224743),
        (-33.8582212, 151.2254986),
        (-33.8564183032, 151.235313348),
        (-33.8594049408, 151.234799568),
        (-33.8641069037, 151.233485084),
        (-33.8715791334, 151.233181742),
        (-33.8876967719, 151.223980353),
        (-33.8873877027, 151.219388501),
        (-33.8869995, 151.2189209),
        (-33.886283399999996, 151.2181177),
        (-33.8851287, 151.2157995),
        (-33.8852471, 151.2156925),
        (-33.8851287, 151.2141233),
        (-33.8847438, 151.2116267),
        (-33.8834707, 151.2083456),
        (-33.8827601, 151.2080246),
        (-33.8816053, 151.2059204),
        (-33.8827601, 151.2043868),
        (-33.8838556, 151.2028176),
        (-33.8839148, 151.2022826),
        (-33.8842405, 151.2011057),
        (-33.8842819, 151.1986114),
        (-33.8842405, 151.1986091),
        (-33.8773416, 151.1948287),
        (-33.8740845, 151.1923322),
        (-33.8697019, 151.1850566),
        (-33.8625354, 151.1902636),
        (-33.8612915, 151.1986805),
        (-33.8555555, 151.1979259),
    ]

    poly = h3.H3Poly(sydney)
    out = h3.shape_to_cells(poly, 9)
    assert len(out) == 92
    assert '89be0e34207ffff' in out
    assert '89be0e35ddbffff' in out


def test_polyfill_far_east():
    geo = [
        (41.92578147109541, 142.86483764648438),
        (42.29965889253408, 142.86483764648438),
        (42.29965889253408, 143.41552734375),
        (41.92578147109541, 143.41552734375),
        (41.92578147109541, 142.86483764648438),
    ]

    poly = h3.H3Poly(geo)
    out = h3.shape_to_cells(poly, 9)
    assert len(out) == 18507
    assert '892e18d16c3ffff' in out
    assert '892e1ebb5a7ffff' in out


def test_polyfill_southern_tip():
    geo = [
        (-55.41654360858007, -67.642822265625),
        (-54.354955689554096, -67.642822265625),
        (-54.354955689554096, -64.742431640625),
        (-55.41654360858007, -64.742431640625),
        (-55.41654360858007, -67.642822265625),
    ]

    poly = h3.H3Poly(geo)
    out = h3.shape_to_cells(poly, 9)
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
    out = h3.shape_to_cells(poly, 4)
    assert len(out) == 345
    assert '847421bffffffff' in out
    assert '84825ddffffffff' in out


def test_cells_to_shape_empty():
    mpoly = h3.cells_to_shape([])
    assert list(mpoly) == []


def test_cells_to_shape_single():
    h = '89283082837ffff'
    cells = {h}

    mpoly = h3.cells_to_shape(cells)
    assert len(mpoly) == 1
    poly = mpoly[0]

    vertices = h3.cell_to_boundary(h)
    expected_poly = h3.H3Poly(vertices)

    assert set(poly.outer) == set(expected_poly.outer)
    assert poly.holes == expected_poly.holes == ()


def test_cells_to_shape_contiguous():
    a = '89283082837ffff'
    b = '89283082833ffff'
    assert h3.are_neighbor_cells(a, b)

    mpoly = h3.cells_to_shape([a, b])
    assert len(mpoly) == 1
    poly = mpoly[0]

    assert len(poly.outer) == 10
    assert poly.holes == ()

    verts_a = h3.cell_to_boundary(a)
    verts_b = h3.cell_to_boundary(b)
    assert set(poly.outer) == set(verts_a) | set(verts_b)


def test_cells_to_shape_non_contiguous():
    a = '89283082837ffff'
    b = '8928308280fffff'
    assert not h3.are_neighbor_cells(a, b)

    mpoly = h3.cells_to_shape([a, b])
    assert len(mpoly) == 2

    assert all(poly.holes == () for poly in mpoly)
    assert all(len(poly.outer) == 6 for poly in mpoly)

    verts_a = h3.cell_to_boundary(a)
    verts_b = h3.cell_to_boundary(b)

    verts_both = set.union(*[set(poly.outer) for poly in mpoly])
    assert verts_both == set(verts_a) | set(verts_b)


def test_cells_to_shape_hole():
    # Six hexagons in a ring around a hole
    cells = [
        '892830828c7ffff', '892830828d7ffff', '8928308289bffff',
        '89283082813ffff', '8928308288fffff', '89283082883ffff',
    ]
    mpoly = h3.cells_to_shape(cells)

    assert len(mpoly) == 1
    poly = mpoly[0]

    assert len(poly.holes) == 1
    assert len(poly.holes[0]) == 6
    assert len(poly.outer) == 6 * 3


def test_cells_to_shape_2grid_disk():
    h = '8930062838bffff'
    cells = h3.grid_disk(h, 2)
    mpoly = h3.cells_to_shape(cells)

    assert len(mpoly) == 1
    poly = mpoly[0]

    assert len(poly.holes) == 0
    assert len(poly.outer) == 6 * (2 * 2 + 1)
