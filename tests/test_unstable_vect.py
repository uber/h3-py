import h3.api.numpy_int as h3
import h3.unstable.vect as h3_vect
import numpy as np  # only run this test suite if numpy is installed


def test_h3_to_parent():
    # At res 9
    h = np.array([617700169958555647], np.uint64)

    # Default to res - 1
    arr1 = h3_vect.h3_to_parent(h)
    arr2 = h3_vect.h3_to_parent(h, 8)
    assert np.array_equal(arr1, arr2)

    # Same as other h3 bindings
    arr1 = h3_vect.h3_to_parent(h)
    arr2 = np.array(list(map(h3.h3_to_parent, h)), dtype=np.uint64)
    assert np.array_equal(arr1, arr2)


def test_h3_to_parent_multiple_res():
    h = np.array([617700169958555647, 613196570331971583], np.uint64)

    # Cells at res 9, 8
    assert list(h3_vect.h3_get_resolution(h)) == [9, 8]

    # Same as other h3 bindings
    arr1 = h3_vect.h3_to_parent(h)
    arr2 = np.array(list(map(h3.h3_to_parent, h)), dtype=np.uint64)
    assert np.array_equal(arr1, arr2)

    # Parent cells are 8, 7
    parents = h3_vect.h3_to_parent(h)
    assert list(h3_vect.h3_get_resolution(parents)) == [8, 7]


def test_h3_get_resolution():
    h = np.array([617700169958555647], np.uint64)

    arr1 = h3_vect.h3_get_resolution(h)
    arr2 = np.array(list(map(h3.h3_get_resolution, h)), dtype=np.uint8)
    assert np.array_equal(arr1, arr2)
