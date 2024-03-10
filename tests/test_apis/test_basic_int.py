import h3.api.basic_int as h3


from .. import util as u


def test_int_output():
    lat = 37.7752702151959
    lng = -122.418307270836

    assert h3.latlng_to_cell(lat, lng, 9) == 617700169958293503
    assert h3.latlng_to_cell(lat, lng, 9) == 0x8928308280fffff


def test_grid_disk():
    expected = [
        617700169957507071,
        617700169957769215,
        617700169958031359,
        617700169958293503,
        617700169961177087,
        617700169964847103,
        617700169965109247,
    ]

    out = h3.grid_disk(617700169958293503, 1)
    assert u.same_set(out, expected)


def test_compact_cells():
    h = 617700169958293503
    cells = h3.cell_to_children(h)

    assert h3.compact_cells(cells) == [h]
