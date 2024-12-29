import h3.api.memview_int as h3


def test1():
    lat, lng = 37.7752702151959, -122.418307270836
    assert h3.latlng_to_cell(lat, lng, 9) == 617700169958293503


def test_line():
    h1 = '8928308280fffff'
    h2 = '8928308287bffff'
    h1, h2 = h3.str_to_int(h1), h3.str_to_int(h2)

    out = h3.grid_path_cells(h1, h2)

    # todo: are we outputting `memoryviewslice`? should we just output a memoryview?
    assert 'memoryview' in str(type(out))

    expected = [
        617700169958293503,
        617700169964847103,
        617700169965371391,
    ]

    assert list(out) == expected
