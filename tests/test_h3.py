import pytest
from pytest import approx

import h3


def test_is_valid_cell():
    assert h3.is_valid_cell('85283473fffffff')
    assert h3.is_valid_cell('850dab63fffffff')
    assert not h3.is_valid_cell('lolwut')

    # H3 0.x Addresses are not considered valid
    assert not h3.is_valid_cell('5004295803a88')

    for res in range(16):
        assert h3.is_valid_cell(h3.latlng_to_cell(37, -122, res))


def test_latlng_to_cell():
    assert h3.latlng_to_cell(37.3615593, -122.0553238, 5) == '85283473fffffff'


def test_get_resolution():
    for res in range(16):
        h = h3.latlng_to_cell(37.3615593, -122.0553238, res)
        assert h3.get_resolution(h) == res


def test_silly_latlng_to_cell():
    lat, lng = 37.3615593, -122.0553238

    expected0 = '85283473fffffff'
    out0 = h3.latlng_to_cell(lat, lng, 5)
    assert out0 == expected0

    out1 = h3.latlng_to_cell(lat + 180.0, lng + 360.0, 5)
    expected1 = '85ca2d53fffffff'
    assert out1 == expected1


def test_cell_to_latlng():
    latlng = h3.cell_to_latlng('85283473fffffff')
    assert latlng == approx((37.34579337536848, -121.97637597255124))


def test_cell_to_boundary():
    out = h3.cell_to_boundary('85283473fffffff')

    expected = [
        [37.271355866731895, -121.91508032705622],
        [37.353926450852256, -121.86222328902491],
        [37.42834118609435, -121.9235499963016],
        [37.42012867767778, -122.0377349642703],
        [37.33755608435298, -122.09042892904395],
        [37.26319797461824, -122.02910130919],
    ]

    assert len(out) == len(expected)

    for o, e in zip(out, expected):
        assert o == approx(e)


def test_cell_to_boundary_geo_json():
    out = h3.cell_to_boundary('85283473fffffff', True)

    expected = [
        [-121.91508032705622, 37.271355866731895],
        [-121.86222328902491, 37.353926450852256],
        [-121.9235499963016, 37.42834118609435],
        [-122.0377349642703, 37.42012867767778],
        [-122.09042892904395, 37.33755608435298],
        [-122.02910130919, 37.26319797461824],
        [-121.91508032705622, 37.271355866731895],
    ]

    assert len(out) == len(expected)

    for o, e in zip(out, expected):
        assert o == approx(e)


def test_grid_disk():
    h = '8928308280fffff'
    out = h3.grid_disk(h, 1)

    assert len(out) == 1 + 6

    expected = {
        '8928308280bffff',
        '89283082807ffff',
        '89283082877ffff',
        h,
        '89283082803ffff',
        '89283082873ffff',
        '8928308283bffff',
    }

    assert out == expected


def test_grid_disk2():
    h = '8928308280fffff'
    out = h3.grid_disk(h, 2)

    assert len(out) == 1 + 6 + 12

    expected = {
        '89283082813ffff',
        '89283082817ffff',
        '8928308281bffff',
        '89283082863ffff',
        '89283082823ffff',
        '89283082873ffff',
        '89283082877ffff',
        h,
        '8928308287bffff',
        '89283082833ffff',
        '8928308282bffff',
        '8928308283bffff',
        '89283082857ffff',
        '892830828abffff',
        '89283082847ffff',
        '89283082867ffff',
        '89283082803ffff',
        '89283082807ffff',
        '8928308280bffff',
    }

    assert out == expected


def test_grid_disk_pentagon():
    h = '821c07fffffffff'  # a pentagon cell
    out = h3.grid_disk(h, 1)

    assert len(out) == 1 + 5

    expected = {
        '821c2ffffffffff',
        '821c27fffffffff',
        h,
        '821c17fffffffff',
        '821c1ffffffffff',
        '821c37fffffffff',
    }

    assert out == expected


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


def test_polyfill():
    poly = h3.Polygon(sf_7x7)
    out = h3.polygon_to_cells(poly, res=9)

    assert len(out) == 1253
    assert '89283080527ffff' in out
    assert '89283095edbffff' in out


# def test_polyfill_bogus_geo_json():
#     with pytest.raises(ValueError):
#         bad_geo = {'type': 'whatwhat'}
#         h3.polyfill(bad_geo, 9)


def test_polyfill_with_hole():
    poly = h3.Polygon(sf_7x7, sf_hole1)

    out = h3.polygon_to_cells(poly, res=9)
    assert len(out) == 1214

    foo = lambda x: h3.polygon_to_cells(h3.Polygon(x), 9)
    # todo: foo = lambda x: h3.Polygon(x).to_cells(9)
    assert out == foo(sf_7x7) - foo(sf_hole1)


def test_polyfill_with_two_holes():

    poly = h3.Polygon(sf_7x7, sf_hole1, sf_hole2)
    out = h3.polygon_to_cells(poly, 9)
    assert len(out) == 1172

    foo = lambda x: h3.polygon_to_cells(h3.Polygon(x), 9)
    assert out == foo(sf_7x7) - (foo(sf_hole1) | foo(sf_hole2))

# def test_polyfill_geo_json_compliant():
#     geo = {
#         'type': 'Polygon',
#         'coordinates': [
#             [
#                 [-122.4089866999972145, 37.813318999983238],
#                 [-122.3805436999997056, 37.7866302000007224],
#                 [-122.3544736999993603, 37.7198061999978478],
#                 [-122.5123436999983966, 37.7076131999975672],
#                 [-122.5247187000021967, 37.7835871999971715],
#                 [-122.4798767000009008, 37.8151571999998453],
#             ]
#         ]
#     }

#     out = h3.polyfill(geo, 9, True)
#     assert len(out) > 1000


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

    poly = h3.Polygon(sydney)
    out = h3.polygon_to_cells(poly, 9)
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

    poly = h3.Polygon(geo)
    out = h3.polygon_to_cells(poly, 9)
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

    poly = h3.Polygon(geo)
    out = h3.polygon_to_cells(poly, 9)
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

    poly = h3.Polygon(geo)
    out = h3.polygon_to_cells(poly, 4)
    assert len(out) == 345
    assert '847421bffffffff' in out
    assert '84825ddffffffff' in out


def test_cells_to_polygons_empty():
    polys = h3.cells_to_polygons([])
    assert polys == []


def test_cells_to_polygons_single():
    h = '89283082837ffff'
    cells = {h}

    polys = h3.cells_to_polygons(cells)
    assert len(polys) == 1
    poly = polys[0]

    vertices = h3.cell_to_boundary(h)
    expected_poly = h3.Polygon(vertices)

    assert set(poly.outer) == set(expected_poly.outer)
    assert poly.holes == expected_poly.holes == ()


def test_cells_to_polygons_contiguous():
    a = '89283082837ffff'
    b = '89283082833ffff'
    assert h3.are_neighbor_cells(a, b)

    polys = h3.cells_to_polygons([a, b])
    assert len(polys) == 1
    poly = polys[0]

    assert len(poly.outer) == 10
    assert poly.holes == ()

    verts_a = h3.cell_to_boundary(a)
    verts_b = h3.cell_to_boundary(b)
    assert set(poly.outer) == set(verts_a) | set(verts_b)


def test_cells_to_polygons_non_contiguous():
    a = '89283082837ffff'
    b = '8928308280fffff'
    assert not h3.are_neighbor_cells(a, b)

    polys = h3.cells_to_polygons([a, b])
    assert len(polys) == 2

    assert all(poly.holes == () for poly in polys)
    assert all(len(poly.outer) == 6 for poly in polys)

    verts_a = h3.cell_to_boundary(a)
    verts_b = h3.cell_to_boundary(b)

    verts_both = set.union(*[set(poly.outer) for poly in polys])
    assert verts_both == set(verts_a) | set(verts_b)


def test_cells_to_polygons_hole():
    # Six hexagons in a ring around a hole
    cells = [
        '892830828c7ffff', '892830828d7ffff', '8928308289bffff',
        '89283082813ffff', '8928308288fffff', '89283082883ffff',
    ]
    polys = h3.cells_to_polygons(cells)

    assert len(polys) == 1
    poly = polys[0]

    assert len(poly.holes) == 1
    assert len(poly.holes[0]) == 6
    assert len(poly.outer) == 6 * 3


def test_cells_to_polygons_2grid_disk():
    h = '8930062838bffff'
    cells = h3.grid_disk(h, 2)
    polys = h3.cells_to_polygons(cells)

    assert len(polys) == 1
    poly = polys[0]

    assert len(poly.holes) == 0
    assert len(poly.outer) == 6 * (2 * 2 + 1)


def test_grid_ring():
    h = '8928308280fffff'
    out = h3.grid_ring(h, 1)
    expected = {
        '8928308280bffff',
        '89283082807ffff',
        '89283082877ffff',
        '89283082803ffff',
        '89283082873ffff',
        '8928308283bffff',
    }

    assert out == expected
    assert out == h3.grid_disk(h, 1) - h3.grid_disk(h, 0)


def test_grid_ring2():
    h = '8928308280fffff'
    out = h3.grid_ring(h, 2)

    expected = {
        '89283082813ffff',
        '89283082817ffff',
        '8928308281bffff',
        '89283082863ffff',
        '89283082823ffff',
        '8928308287bffff',
        '89283082833ffff',
        '8928308282bffff',
        '89283082857ffff',
        '892830828abffff',
        '89283082847ffff',
        '89283082867ffff',
    }

    assert out == expected
    assert out == h3.grid_disk(h, 2) - h3.grid_disk(h, 1)


def test_grid_ring_pentagon():
    h = '821c07fffffffff'
    out = h3.grid_ring(h, 1)

    expected = {
        '821c17fffffffff',
        '821c1ffffffffff',
        '821c27fffffffff',
        '821c2ffffffffff',
        '821c37fffffffff',
    }

    assert out == expected


def test_compact_and_uncompact_cells():
    poly = h3.Polygon(sf_7x7)
    cells = h3.polygon_to_cells(poly, 9)

    compact_cells = h3.compact_cells(cells)
    assert len(compact_cells) == 209

    uncompact_cells = h3.uncompact_cells(compact_cells, 9)
    assert len(uncompact_cells) == 1253

    assert uncompact_cells == cells


def test_compact_cells_and_uncompact_cells_nothing():
    assert h3.compact_cells([]) == set()
    assert h3.uncompact_cells([], 9) == set()


def test_uncompact_cells_error():
    hexagons = [h3.latlng_to_cell(37, -122, 10)]

    with pytest.raises(Exception):
        h3.uncompact_cells(hexagons, 5)


def test_compact_cells_malformed_input():
    cells = ['89283082813ffff'] * 13

    with pytest.raises(Exception):
        h3.compact_cells(cells)


def test_cell_to_parent():
    h = '89283082813ffff'
    assert h3.cell_to_parent(h, 8) == '8828308281fffff'


def test_cell_to_children():
    h = '8828308281fffff'
    children = h3.cell_to_children(h, 9)

    assert len(children) == 7


def test_average_hexagon_area():
    for i in range(0, 15):
        assert isinstance(h3.average_hexagon_area(i), float)
        assert isinstance(h3.average_hexagon_area(i, 'm^2'), float)

    with pytest.raises(ValueError):
        h3.average_hexagon_area(5, 'ft^2')


def test_average_hexagon_edge_length():
    for i in range(0, 15):
        assert isinstance(h3.average_hexagon_edge_length(i), float)
        assert isinstance(h3.average_hexagon_edge_length(i, 'm'), float)

    with pytest.raises(ValueError):
        h3.average_hexagon_edge_length(5, 'ft')


def test_get_num_cells():
    h0 = 122
    assert h3.get_num_cells(0) == h0

    for i in range(0, 15):
        n = h3.get_num_cells(i) * 1.0 / h0

        assert 6**i <= n <= 7**i


def test_get_base_cell_number():
    assert h3.get_base_cell_number('8928308280fffff') == 20


def test_is_res_class_III():
    assert h3.is_res_class_III('8928308280fffff')
    assert not h3.is_res_class_III('8828308280fffff')


def test_is_pentagon():
    assert h3.is_pentagon('821c07fffffffff')
    assert not h3.is_pentagon('8928308280fffff')


def test_are_neighbor_cells():
    assert h3.are_neighbor_cells('8928308280fffff', '8928308280bffff')

    assert not h3.are_neighbor_cells('821c07fffffffff', '8928308280fffff')


def test_cells_to_directed_edge():
    out = h3.cells_to_directed_edge('8928308280fffff', '8928308280bffff')
    assert h3.is_valid_directed_edge(out)

    with pytest.raises(h3.H3NotNeighborsError):
        h3.cells_to_directed_edge('821c07fffffffff', '8928308280fffff')


def test_is_valid_directed_edge():
    assert not h3.is_valid_directed_edge('8928308280fffff')
    assert h3.is_valid_directed_edge('11928308280fffff')


def test_get_directed_edge_origin():
    out = h3.get_directed_edge_origin('11928308280fffff')
    assert out == '8928308280fffff'


def test_get_directed_edge_destination():
    h = '11928308280fffff'
    out = h3.get_directed_edge_destination(h)

    assert out == '8928308283bffff'


def test_directed_edge_to_cells():
    e = h3.directed_edge_to_cells('11928308280fffff')

    assert e == ('8928308280fffff', '8928308283bffff')


def test_origin_to_directed_edges():
    h3_uni_edges = h3.origin_to_directed_edges(
        '8928308280fffff'
    )
    assert len(h3_uni_edges) == 6

    h3_uni_edge_pentagon = h3.origin_to_directed_edges(
        '821c07fffffffff'
    )
    assert len(h3_uni_edge_pentagon) == 5


def test_directed_edge_to_boundary():
    e = '11928308280fffff'
    boundary = h3.directed_edge_to_boundary(e)
    assert len(boundary) == 2

    boundary_geo_json = h3.directed_edge_to_boundary(e, True)
    assert len(boundary_geo_json) == 3


def test_grid_distance():
    h = '89283082993ffff'

    assert 0 == h3.grid_distance(h, h)
    assert 1 == h3.grid_distance(h, '8928308299bffff')
    assert 5 == h3.grid_distance(h, '89283082827ffff')


def test_grid_path_cells():
    h1 = '8a2a84730587fff'
    h2 = '8a2a8471414ffff'

    out = h3.grid_path_cells(h1, h2)

    expected = [
        h1,
        '8a2a8473059ffff',
        '8a2a847304b7fff',
        '8a2a84730487fff',
        '8a2a8473049ffff',
        '8a2a84732b37fff',
        '8a2a84732b17fff',
        '8a2a84732baffff',
        '8a2a84732a37fff',
        '8a2a84732a17fff',
        '8a2a84732aaffff',
        '8a2a84732a8ffff',
        '8a2a84732327fff',
        '8a2a8473232ffff',
        '8a2a8473230ffff',
        '8a2a84732227fff',
        '8a2a84732207fff',
        '8a2a8473221ffff',
        '8a2a847322e7fff',
        '8a2a847322c7fff',
        '8a2a847322dffff',
        '8a2a84714977fff',
        '8a2a84714957fff',
        '8a2a8471495ffff',
        '8a2a84714877fff',
        '8a2a84714857fff',
        '8a2a847148effff',
        '8a2a847148cffff',
        '8a2a84714b97fff',
        '8a2a8471416ffff',
        h2,
    ]

    assert out == expected

    with pytest.raises(h3.H3ResMismatchError):
        h3.grid_path_cells(h1, '8001fffffffffff')
