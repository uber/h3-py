import h3.api.numpy_int as h3
import numpy as np  # only run this test suite if numpy is installed

from .. import util as u


def test1():
    lat, lng = (
        37.7752702151959,
        -122.418307270836,
    )
    assert h3.latlng_to_cell(lat, lng, 9) == 617700169958293503


def test5():
    expected = {
        617700169957507071,
        617700169957769215,
        617700169958031359,
        617700169958293503,
        617700169961177087,
        617700169964847103,
        617700169965109247,
    }

    out = h3.grid_disk(617700169958293503, 1)
    assert isinstance(out, np.ndarray)
    assert u.same_set(out, expected)


def test_compact_cells():
    h = 617700169958293503
    cells = h3.cell_to_children(h)
    assert isinstance(cells, np.ndarray)

    assert h3.compact_cells(cells) == [h]


def test_numpy_str():
    expected = [
        617700169957507071,
        617700169957769215,
        617700169958031359,
        617700169958293503,
        617700169961177087,
        617700169964847103,
        617700169965109247,
    ]
    cells = np.array([h3.int_to_str(h) for h in expected])
    got = [h3.str_to_int(c) for c in cells]

    assert expected == got
