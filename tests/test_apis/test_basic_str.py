import h3.api.basic_str as h3


def same_set(a, b):
    """Test if two collections are the same if taken as sets"""
    set_a = set(a)
    set_b = set(b)

    assert len(a) == len(b) == len(set_a) == len(set_b)

    return set_a == set_b


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
    assert same_set(out, expected)
