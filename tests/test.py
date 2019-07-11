import h3py.api.set_str as h3
import pytest


def approx2(a,b):
    if len(a) != len(b):
        return False

    return all(
    x == pytest.approx(y)
    for x,y in zip(a,b)
    )

def test1():
    assert h3.geo_to_h3(37.7752702151959, -122.418307270836, 9) == '8928308280fffff'

def test2():
    assert h3.h3_to_geo('8928308280fffff') == pytest.approx((37.77670234943567, -122.41845932318311))


def test3():
    expected = (
        (37.775197782893386, -122.41719971841658),
        (37.77688044840226, -122.41612835779264),
        (37.778385004930925, -122.4173879761762),
        (37.77820687262238, -122.41971895414807),
        (37.77652420699321, -122.42079024541877),
        (37.775019673792606, -122.4195306280734)
     )

    out = h3.h3_to_geo_boundary('8928308280fffff')
    assert approx2(out, expected)


def test4():
    expected = (
        (-122.41719971841658, 37.775197782893386),
        (-122.41612835779264, 37.77688044840226),
        (-122.4173879761762, 37.778385004930925),
        (-122.41971895414807, 37.77820687262238),
        (-122.42079024541877, 37.77652420699321),
        (-122.4195306280734, 37.775019673792606),
        (-122.41719971841658, 37.775197782893386)
    )

    out = h3.h3_to_geo_boundary('8928308280fffff', geo_json=True)
    assert approx2(out, expected)


def test5():
    expected = {
        '89283082873ffff',
        '89283082877ffff',
        '8928308283bffff',
        '89283082807ffff',
        '8928308280bffff',
        '8928308280fffff',
        '89283082803ffff'
    }

    out = h3.k_ring('8928308280fffff', 1)
    assert out == expected


def test6():
    expected = {'8928308280fffff'}
    out = h3.hex_ring('8928308280fffff', 0)
    assert out == expected

def test7():
    expected = {
        '89283082803ffff',
        '89283082807ffff',
        '8928308280bffff',
        '8928308283bffff',
        '89283082873ffff',
        '89283082877ffff'
    }

    out = h3.hex_ring('8928308280fffff', 1)
    assert out == expected

def test8():
    assert h3.is_valid('89283082803ffff')
    assert not h3.is_valid('abc')

    # looks like it might be valid, but it isn't!
    h_bad = '8a28308280fffff'
    assert not h3.is_valid(h_bad)

    # other methods should validate and raise exception if bad input
    with pytest.raises(Exception):
        h3.resolution(h_bad)

def test9():
    assert h3.resolution('8928308280fffff') == 9
    assert h3.resolution('8a28308280f7fff') == 10

def test_parent():
    assert h3.parent('8928308280fffff', 8) == '8828308281fffff'
    assert h3.parent('8928308280fffff', 7) == '872830828ffffff'
    assert h3.parent('8928308280fffff', 10) == '0' # todo: thsi should probably return None, eh?


def test_children():
    expected = {
        '8a28308280c7fff',
        '8a28308280cffff',
        '8a28308280d7fff',
        '8a28308280dffff',
        '8a28308280e7fff',
        '8a28308280effff',
        '8a28308280f7fff'
    }

    out = h3.children('8928308280fffff', 10)

    assert out == expected

    expected = set()
    out = h3.children('8928308280fffff', 8)

    assert out == expected

def test_distance():
    h = '8a28308280c7fff'
    assert h3.distance(h,h) == 0

    n = h3.hex_ring(h,1).pop()
    assert h3.distance(h,n) == 1

    n = h3.hex_ring(h,2).pop()
    assert h3.distance(h,n) == 2


def test_polyfill():

    #lat/lngs for State of Maine
    geos = [
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

    out = h3.polyfill(geos, 3)

    assert out == expected


def test_compact():

    #lat/lngs for State of Maine
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

    res = 5

    h_uncomp = h3.polyfill(maine, res)
    h_comp = h3.compact(h_uncomp)

    expected = {'852b114ffffffff', '852b189bfffffff', '852b1163fffffff', '842ba9bffffffff', '842bad3ffffffff', '852ba9cffffffff', '842badbffffffff', '852b1e8bfffffff', '852a346ffffffff', '842b1e3ffffffff', '852b116ffffffff', '842b185ffffffff', '852b1bdbfffffff', '852bad47fffffff', '852ba9c3fffffff', '852b106bfffffff', '852a30d3fffffff', '842b1edffffffff', '852b12a7fffffff', '852b1027fffffff', '842baddffffffff', '852a349bfffffff', '852b1227fffffff', '852a3473fffffff', '852b117bfffffff', '842ba99ffffffff', '852a341bfffffff', '852ba9d3fffffff', '852b1067fffffff', '852a3463fffffff', '852baca7fffffff', '852b116bfffffff', '852b1c6bfffffff', '852a3493fffffff', '852ba9dbfffffff', '852b180bfffffff', '842bad7ffffffff', '852b1063fffffff', '842ba93ffffffff', '852a3693fffffff', '852ba977fffffff', '852b1e9bfffffff', '852bad53fffffff', '852b100ffffffff', '852b102bfffffff', '852a3413fffffff', '852ba8b7fffffff', '852bad43fffffff', '852b1c6ffffffff', '852a340bfffffff', '852b103bfffffff', '852b1813fffffff', '852b12affffffff', '842a34dffffffff', '852b1873fffffff', '852b106ffffffff', '852b115bfffffff', '852baca3fffffff', '852b114bfffffff', '852b1143fffffff', '852a348bfffffff', '852a30d7fffffff', '852b181bfffffff', '842a345ffffffff', '852b1e8ffffffff', '852b1883fffffff', '852b1147fffffff', '852a3483fffffff', '852b12a3fffffff', '852a346bfffffff', '852ba9d7fffffff', '842b18dffffffff', '852b188bfffffff', '852a36a7fffffff', '852bacb3fffffff', '852b187bfffffff', '852bacb7fffffff', '842b1ebffffffff', '842b1e5ffffffff', '852ba8a7fffffff', '842bad9ffffffff', '852a36b7fffffff', '852a347bfffffff', '832b13fffffffff', '852ba9c7fffffff', '832b1afffffffff', '842ba91ffffffff', '852bad57fffffff', '852ba8affffffff', '852b1803fffffff', '842b1e7ffffffff', '852bad4ffffffff', '852b102ffffffff', '852b1077fffffff', '852b1237fffffff', '852b1153fffffff', '852a3697fffffff', '852a36b3fffffff', '842bad1ffffffff', '842b1e1ffffffff', '852b186bfffffff', '852b1023fffffff'}

    assert h_comp == expected

    return h_uncomp, h_comp, res

def test_uncompact():

    h_uncomp, h_comp, res = test_compact()

    out = h3.uncompact(h_comp, res)

    assert out == h_uncomp


def test_num_hexagons():
    expected = {
        0: 122,
        1: 842,
        2: 5882,
        9: 4842432842,
        15: 569707381193162,
    }

    out = {
        k: h3.num_hexagons(k)
        for k in expected
    }

    assert expected == out

def test_hex_area():
    expected_in_km2 = {
        0: 4250546.848,
        1: 607220.9782,
        2: 86745.85403,
        9: 0.1053325,
        15: 9e-07,
    }

    out = {
        k: h3.hex_area(k, unit='km')
        for k in expected_in_km2
    }

    assert out == pytest.approx(expected_in_km2)

def test_hex_edge_length():
    expected_in_km = {
        0: 1107.712591000,
        1: 418.676005500,
        2: 158.244655800,
        9: 0.174375668,
        15: 0.000509713,
    }

    out = {
        res: h3.edge_length(res, unit='km')
        for res in expected_in_km
    }

    assert out == pytest.approx(expected_in_km)


def test_uni_edge():
    h1 = '8928308280fffff'
    h2 = '89283082873ffff'

    assert not h3.are_neighbors(h1, h1)
    assert h3.are_neighbors(h1, h2)

    e = h3.uni_edge(h1,h2)

    assert e == '12928308280fffff'
    assert h3.is_uni_edge(e)
    assert not h3.is_valid(e)

    assert h3.uni_edge_origin(e) == h1
    assert h3.uni_edge_destination(e) == h2

    assert h3.uni_edge_hexes(e) == (h1,h2)

def test_uni_edges_from_hex():
    h = '8928308280fffff'
    edges = h3.uni_edges_from_hex(h)
    destinations = {h3.uni_edge_destination(e) for e in edges}
    neighbors = h3.hex_ring(h, 1)

    assert neighbors == destinations

def test_uni_edge_boundary():
    h1 = '8928308280fffff'
    h2 = '89283082873ffff'
    e = h3.uni_edge(h1,h2)

    expected = (
        (37.77688044840226, -122.41612835779266),
        (37.778385004930925, -122.41738797617619)
    )

    out = h3.uni_edge_boundary(e)

    assert out[0] == pytest.approx(expected[0])
    assert out[1] == pytest.approx(expected[1])



