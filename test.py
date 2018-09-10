import h3core as h3
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
    assert h3.h3_is_valid('89283082803ffff')
    assert not h3.h3_is_valid('foo')

def test9():
    assert h3.h3_get_resolution('8928308280fffff') == 9
    assert h3.h3_get_resolution('8a28308280fffff') == 10

def test_parent():
    assert h3.h3_to_parent('8928308280fffff', 8) == '8828308281fffff'
    assert h3.h3_to_parent('8928308280fffff', 7) == '872830828ffffff'
    assert h3.h3_to_parent('8928308280fffff', 10) == '0'


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

    out = h3.h3_to_children('8928308280fffff', 10)

    assert out == expected

    expected = set()
    out = h3.h3_to_children('8928308280fffff', 8)

    assert out == expected

def test_distance():
    h = '8a28308280c7fff'
    assert h3.h3distance(h,h) == 0

    n = h3.hex_ring(h,1).pop()
    assert h3.h3distance(h,n) == 1

    n = h3.hex_ring(h,2).pop()
    assert h3.h3distance(h,n) == 2


