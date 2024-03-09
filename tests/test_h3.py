import pytest
from pytest import approx

import h3

from . import util as u


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

    assert u.same_set(out, expected)


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

    assert u.same_set(out, expected)


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

    assert u.same_set(out, expected)


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

    assert u.same_set(out, expected)
    assert u.same_set(
        out,
        set(h3.grid_disk(h, 1)) - set(h3.grid_disk(h, 0))
    )


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

    assert u.same_set(out, expected)
    assert u.same_set(
        out,
        set(h3.grid_disk(h, 2)) - set(h3.grid_disk(h, 1))
    )


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

    assert u.same_set(out, expected)


def test_compact_and_uncompact_cells():
    sf_7x7 = [
        (37.813318999983238, -122.4089866999972145),
        (37.7866302000007224, -122.3805436999997056),
        (37.7198061999978478, -122.3544736999993603),
        (37.7076131999975672, -122.5123436999983966),
        (37.7835871999971715, -122.5247187000021967),
        (37.8151571999998453, -122.4798767000009008),
    ]

    poly = h3.H3Poly(sf_7x7)
    cells = h3.h3shape_to_cells(poly, 9)

    compact_cells = h3.compact_cells(cells)
    assert len(compact_cells) == 209

    uncompact_cells = h3.uncompact_cells(compact_cells, 9)
    assert len(uncompact_cells) == 1253

    assert u.same_set(uncompact_cells, cells)


def test_compact_cells_and_uncompact_cells_nothing():
    assert h3.compact_cells([]) == []
    assert h3.uncompact_cells([], 9) == []


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
