import h3.api.basic_str as h3


from .. import util as u


def test1():
    lat, lng = 37.7752702151959, -122.418307270836
    assert h3.latlng_to_cell(lat, lng, 9) == '8928308280fffff'


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


def test_string_subtypes():

    class my_str(str):
        pass

    expected = [
        '89283082873ffff',
        '89283082877ffff',
        '8928308283bffff',
        '89283082807ffff',
        '8928308280bffff',
        '8928308280fffff',
        '89283082803ffff'
    ]

    out = h3.grid_disk(my_str('8928308280fffff'), 1)
    assert u.same_set(out, expected)
