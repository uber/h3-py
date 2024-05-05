import h3
import pytest

from h3 import (
    H3FailedError,
    H3ResDomainError,
    H3DomainError,
    H3ResMismatchError,
    H3CellInvalidError,
    H3NotNeighborsError,
)


from . import util as u


def test1():
    lat, lng = 37.7752702151959, -122.418307270836
    assert h3.latlng_to_cell(lat, lng, 9) == '8928308280fffff'


def test2():
    h = '8928308280fffff'
    expected = (37.77670234943567, -122.41845932318311)

    assert h3.cell_to_latlng(h) == pytest.approx(expected)


def test3():
    expected = (
        (37.775197782893386, -122.41719971841658),
        (37.77688044840226, -122.41612835779264),
        (37.778385004930925, -122.4173879761762),
        (37.77820687262238, -122.41971895414807),
        (37.77652420699321, -122.42079024541877),
        (37.775019673792606, -122.4195306280734),
    )

    out = h3.cell_to_boundary('8928308280fffff')
    assert u.approx2(out, expected)


def test_grid_disk_distance():
    with pytest.raises(H3DomainError):
        h3.grid_disk('8928308280fffff', -10)


def test_grid_ring_distance():
    with pytest.raises(H3DomainError):
        h3.grid_ring('8928308280fffff', -10)


def test5():
    expected = [
        '89283082873ffff',
        '89283082877ffff',
        '8928308283bffff',
        '89283082807ffff',
        '8928308280bffff',
        '8928308280fffff',
        '89283082803ffff'
    ]

    out = h3.grid_disk('8928308280fffff', 1)
    assert u.same_set(out, expected)


def test6():
    expected = ['8928308280fffff']
    out = h3.grid_ring('8928308280fffff', 0)
    assert u.same_set(out, expected)


def test7():
    expected = [
        '89283082803ffff',
        '89283082807ffff',
        '8928308280bffff',
        '8928308283bffff',
        '89283082873ffff',
        '89283082877ffff'
    ]

    out = h3.grid_ring('8928308280fffff', 1)
    assert u.same_set(out, expected)


def test8():
    assert h3.is_valid_cell('89283082803ffff')
    assert not h3.is_valid_cell('abc')

    # looks like it might be valid, but it isn't!
    h_bad = '8a28308280fffff'
    assert not h3.is_valid_cell(h_bad)

    # other methods should validate and raise exception if bad input
    with pytest.raises(H3CellInvalidError):
        h3.get_resolution(h_bad)


def test9():
    assert h3.get_resolution('8928308280fffff') == 9
    assert h3.get_resolution('8a28308280f7fff') == 10


def test_parent():
    h = '8928308280fffff'

    assert h3.cell_to_parent(h, 7) == '872830828ffffff'
    assert h3.cell_to_parent(h, 8) == '8828308281fffff'
    assert h3.cell_to_parent(h, 9) == h

    with pytest.raises(H3ResMismatchError):
        h3.cell_to_parent(h, 10)


def test_parent_err():
    # Test 1
    h = '8075fffffffffff'  # latlng_to_cell(0,0,0)

    with pytest.raises(H3ResDomainError):
        h3.cell_to_parent(h)

    # Test 2
    try:
        h3.cell_to_parent(h)
    except Exception as e:
        msg = str(e)

    # todo: revist this weird formatting stuff
    expected = 'Invalid parent resolution -1 for cell {}.'
    expected = expected.format(hex(h3.str_to_int(h)))

    assert msg == expected


def test_children():
    h = '8928308280fffff'

    with pytest.raises(H3ResDomainError):
        h3.cell_to_children(h, 8)

    # same resolution is set of just cell itself
    out = h3.cell_to_children(h, 9)
    assert out == [h]

    # one below should give children
    expected = [
        '8a28308280c7fff',
        '8a28308280cffff',
        '8a28308280d7fff',
        '8a28308280dffff',
        '8a28308280e7fff',
        '8a28308280effff',
        '8a28308280f7fff'
    ]
    out = h3.cell_to_children(h, 10)
    assert u.same_set(out, expected)

    # finest resolution cell should return error for children
    h = '8f04ccb2c45e225'
    with pytest.raises(H3ResDomainError):
        h3.cell_to_children(h)


def test_center_child():
    h = '8928308280fffff'

    # one above should raise an exception
    with pytest.raises(H3ResDomainError):
        h3.cell_to_center_child(h, 8)

    # same resolution should be same cell
    assert h3.cell_to_center_child(h, 9) == h

    # one below should give direct child
    expected = '8a28308280c7fff'
    assert h3.cell_to_center_child(h, 10) == expected

    # finest resolution hex should return error for child
    h = '8f04ccb2c45e225'
    with pytest.raises(H3ResDomainError):
        h3.cell_to_center_child(h)


def test_distance():
    h = '8a28308280c7fff'
    assert h3.grid_distance(h, h) == 0

    n = h3.grid_ring(h, 1).pop()
    assert h3.grid_distance(h, n) == 1

    n = h3.grid_ring(h, 2).pop()
    assert h3.grid_distance(h, n) == 2


def test_distance_error():
    """ Two valid cells, but they are too far apart compute the distance

    todo: make sure this raises a E_TOO_FAR error (when we add it in the future)
    """
    h1 = '8353b0fffffffff'
    h2 = '835804fffffffff'

    with pytest.raises(H3FailedError):
        h3.grid_distance(h1, h2)


def get_maine_cells():
    # lat/lngs for State of Maine
    poly = h3.LatLngPoly([
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
    ])

    res = 5
    cells_uncomp = h3.h3shape_to_cells(poly, res=res)

    # the expected result from h3.compact_cells(cells_uncomp)
    cells_comp = ['852b114ffffffff', '852b189bfffffff', '852b1163fffffff', '842ba9bffffffff', '842bad3ffffffff', '852ba9cffffffff', '842badbffffffff', '852b1e8bfffffff', '852a346ffffffff', '842b1e3ffffffff', '852b116ffffffff', '842b185ffffffff', '852b1bdbfffffff', '852bad47fffffff', '852ba9c3fffffff', '852b106bfffffff', '852a30d3fffffff', '842b1edffffffff', '852b12a7fffffff', '852b1027fffffff', '842baddffffffff', '852a349bfffffff', '852b1227fffffff', '852a3473fffffff', '852b117bfffffff', '842ba99ffffffff', '852a341bfffffff', '852ba9d3fffffff', '852b1067fffffff', '852a3463fffffff', '852baca7fffffff', '852b116bfffffff', '852b1c6bfffffff', '852a3493fffffff', '852ba9dbfffffff', '852b180bfffffff', '842bad7ffffffff', '852b1063fffffff', '842ba93ffffffff', '852a3693fffffff', '852ba977fffffff', '852b1e9bfffffff', '852bad53fffffff', '852b100ffffffff', '852b102bfffffff', '852a3413fffffff', '852ba8b7fffffff', '852bad43fffffff', '852b1c6ffffffff', '852a340bfffffff', '852b103bfffffff', '852b1813fffffff', '852b12affffffff', '842a34dffffffff', '852b1873fffffff', '852b106ffffffff', '852b115bfffffff', '852baca3fffffff', '852b114bfffffff', '852b1143fffffff', '852a348bfffffff', '852a30d7fffffff', '852b181bfffffff', '842a345ffffffff', '852b1e8ffffffff', '852b1883fffffff', '852b1147fffffff', '852a3483fffffff', '852b12a3fffffff', '852a346bfffffff', '852ba9d7fffffff', '842b18dffffffff', '852b188bfffffff', '852a36a7fffffff', '852bacb3fffffff', '852b187bfffffff', '852bacb7fffffff', '842b1ebffffffff', '842b1e5ffffffff', '852ba8a7fffffff', '842bad9ffffffff', '852a36b7fffffff', '852a347bfffffff', '832b13fffffffff', '852ba9c7fffffff', '832b1afffffffff', '842ba91ffffffff', '852bad57fffffff', '852ba8affffffff', '852b1803fffffff', '842b1e7ffffffff', '852bad4ffffffff', '852b102ffffffff', '852b1077fffffff', '852b1237fffffff', '852b1153fffffff', '852a3697fffffff', '852a36b3fffffff', '842bad1ffffffff', '842b1e1ffffffff', '852b186bfffffff', '852b1023fffffff'] # noqa

    return cells_uncomp, cells_comp, res


def test_compact_cells():
    cells_uncomp, cells_comp, _ = get_maine_cells()
    out = h3.compact_cells(cells_uncomp)

    assert u.same_set(out, cells_comp)


def test_uncompact_cells():
    cells_uncomp, cells_comp, res = get_maine_cells()
    out = h3.uncompact_cells(cells_comp, res)
    assert u.same_set(out, cells_uncomp)


def test_get_num_cells():
    expected = {
        0: 122,
        1: 842,
        2: 5882,
        9: 4842432842,
        15: 569707381193162,
    }

    out = {
        k: h3.get_num_cells(k)
        for k in expected
    }

    assert expected == out


def test_average_hexagon_area():
    expected_in_km2 = {
        0: 4357449.416078381,
        1:  609788.441794133,
        2:   86801.780398997,
        9:       0.105332513,
        15:      8.95311e-07,
    }

    out = {
        k: h3.average_hexagon_area(k, unit='km^2')
        for k in expected_in_km2
    }

    assert out == pytest.approx(expected_in_km2)


def test_average_hexagon_edge_length():
    expected_in_km = {
        0: 1107.712591000,
        1: 418.676005500,
        2: 158.244655800,
        9: 0.174375668,
        15: 0.000509713,
    }

    out = {
        res: h3.average_hexagon_edge_length(res, unit='km')
        for res in expected_in_km
    }

    assert out == pytest.approx(expected_in_km)


def test_edge():
    h1 = '8928308280fffff'
    h2 = '89283082873ffff'

    assert not h3.are_neighbor_cells(h1, h1)
    assert h3.are_neighbor_cells(h1, h2)

    e = h3.cells_to_directed_edge(h1, h2)

    assert e == '12928308280fffff'
    assert h3.is_valid_directed_edge(e)
    assert not h3.is_valid_cell(e)

    assert h3.get_directed_edge_origin(e) == h1
    assert h3.get_directed_edge_destination(e) == h2

    assert h3.directed_edge_to_cells(e) == (h1, h2)


def test_origin_to_directed_edges():
    h = '8928308280fffff'
    edges = h3.origin_to_directed_edges(h)
    destinations = {
        h3.get_directed_edge_destination(e)
        for e in edges
    }
    neighbors = h3.grid_ring(h, 1)

    assert u.same_set(neighbors, destinations)


def test_edge_boundary():
    h1 = '8928308280fffff'
    h2 = '89283082873ffff'
    e = h3.cells_to_directed_edge(h1, h2)

    expected = (
        (37.77688044840226, -122.41612835779266),
        (37.778385004930925, -122.41738797617619)
    )

    out = h3.directed_edge_to_boundary(e)

    assert out[0] == pytest.approx(expected[0])
    assert out[1] == pytest.approx(expected[1])


def test_validation():
    h = '8a28308280fffff'  # invalid cell

    with pytest.raises(H3CellInvalidError):
        h3.get_base_cell_number(h)

    with pytest.raises(H3CellInvalidError):
        h3.get_resolution(h)

    with pytest.raises(H3CellInvalidError):
        h3.cell_to_parent(h, 9)

    with pytest.raises(H3CellInvalidError):
        h3.grid_distance(h, h)

    with pytest.raises(H3CellInvalidError):
        h3.grid_disk(h, 1)

    with pytest.raises(H3CellInvalidError):
        h3.grid_ring(h, 1)

    with pytest.raises(H3CellInvalidError):
        h3.cell_to_children(h, 11)

    with pytest.raises(H3CellInvalidError):
        h3.compact_cells({h})

    with pytest.raises(H3CellInvalidError):
        h3.uncompact_cells({h}, 10)


def test_validation2():
    h = '8928308280fffff'

    with pytest.raises(H3ResDomainError):
        h3.cell_to_children(h, 17)

    assert not h3.are_neighbor_cells(h, h)


def test_validation_geo():
    h = '8a28308280fffff'  # invalid cell

    with pytest.raises(H3CellInvalidError):
        h3.cell_to_latlng(h)

    with pytest.raises(H3ResDomainError):
        h3.latlng_to_cell(0, 0, 17)

    with pytest.raises(H3CellInvalidError):
        h3.cell_to_boundary(h)

    # note: this won't raise an exception on bad input, but it does
    # *correctly* say that two invalid indexes are not neighbors
    assert not h3.are_neighbor_cells(h, h)


def test_edges():
    h = '8928308280fffff'

    with pytest.raises(H3NotNeighborsError):
        h3.cells_to_directed_edge(h, h)

    h2 = h3.grid_ring(h, 2).pop()
    with pytest.raises(H3NotNeighborsError):
        h3.cells_to_directed_edge(h, h2)

    e_bad = '14928308280ffff1'
    assert not h3.is_valid_directed_edge(e_bad)

    # note: won't raise an error on bad input
    h3.get_directed_edge_origin(e_bad)
    h3.get_directed_edge_destination(e_bad)
    h3.directed_edge_to_cells(e_bad)


def test_line():
    h1 = '8928308280fffff'
    h2 = '8928308287bffff'

    out = h3.grid_path_cells(h1, h2)

    expected = [
        '8928308280fffff',
        '89283082873ffff',
        '8928308287bffff'
    ]

    assert out == expected


def test_versions():
    from packaging.version import Version

    v = h3.versions()

    assert v['python'] == h3.__version__

    v_c = Version(v['c'])
    v_p = Version(v['python'])

    # of X.Y.Z, X and Y must match
    assert v_c.release[:2] == v_p.release[:2]


def test_str_int_convert():
    s = '8928308280fffff'
    i = h3.str_to_int(s)

    assert h3.int_to_str(i) == s


def test_str_to_int_fail():
    h_invalid = {}

    assert not h3.is_valid_cell(h_invalid)


def test_edge_is_valid_fail():
    e_invalid = {}
    assert not h3.is_valid_directed_edge(e_invalid)


def test_get_pentagons():
    out = h3.get_pentagons(0)

    expected = [
        '8009fffffffffff',
        '801dfffffffffff',
        '8031fffffffffff',
        '804dfffffffffff',
        '8063fffffffffff',
        '8075fffffffffff',
        '807ffffffffffff',
        '8091fffffffffff',
        '80a7fffffffffff',
        '80c3fffffffffff',
        '80d7fffffffffff',
        '80ebfffffffffff',
    ]

    assert u.same_set(out, expected)

    out = h3.get_pentagons(5)

    expected = [
        '85080003fffffff',
        '851c0003fffffff',
        '85300003fffffff',
        '854c0003fffffff',
        '85620003fffffff',
        '85740003fffffff',
        '857e0003fffffff',
        '85900003fffffff',
        '85a60003fffffff',
        '85c20003fffffff',
        '85d60003fffffff',
        '85ea0003fffffff',
    ]

    assert u.same_set(out, expected)

    for i in range(16):
        assert len(h3.get_pentagons(i)) == 12


def test_uncompact_cell_input():
    # `uncompact_cells` takes in a collection of cells, not a single cell.
    # Since a python string is seen as a Iterable collection,
    # inputting a single cell string can raise weird errors.

    # Ensure we get a reasonably helpful answer
    with pytest.raises(H3CellInvalidError):
        h3.uncompact_cells('8001fffffffffff', 1)


def test_get_res0_cells():
    out = h3.get_res0_cells()

    assert len(out) == 122

    # subset
    pentagons = h3.get_pentagons(0)
    assert set(pentagons) < set(out)

    # all valid
    assert all(map(h3.is_valid_cell, out))

    # resolution
    assert all(map(
        lambda h: h3.get_resolution(h) == 0,
        out
    ))

    # verify a few concrete cells
    sub = {
        '8001fffffffffff',
        '8003fffffffffff',
        '8005fffffffffff',
    }
    assert sub < set(out)


def test_to_local_ij_error():
    h = h3.latlng_to_cell(0, 0, 0)

    # error if we cross a face
    nb = h3.grid_ring(h, k=2)

    # todo: should this be the E_TOO_FAR guy?
    with pytest.raises(H3FailedError):
        [h3.cell_to_local_ij(h, p) for p in nb]

    # should be fine if we do not cross a face
    nb = h3.grid_ring(h, k=1)
    out = {h3.cell_to_local_ij(h, p) for p in nb}
    expected = {(-1, 0), (0, -1), (0, 1), (1, 0), (1, 1)}

    assert out == expected


def test_from_local_ij_error():
    h = h3.latlng_to_cell(0, 0, 0)

    baddies = [(1, -1), (-1, 1), (-1, -1)]
    for i, j in baddies:
        with pytest.raises(H3FailedError):
            h3.local_ij_to_cell(h, i, j)

    # inverting output should give good data
    nb = h3.grid_ring(h, k=1)
    goodies = {h3.cell_to_local_ij(h, p) for p in nb}

    out = {
        h3.local_ij_to_cell(h, i, j)
        for i, j in goodies
    }

    assert u.same_set(out, nb)


def test_to_local_ij_self():
    h = h3.latlng_to_cell(0, 0, 9)
    out = h3.cell_to_local_ij(h, h)

    assert out == (-858, -2766)
