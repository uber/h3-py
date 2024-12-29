""" Test that `h3shape_to_cells` can take in polygon inputs
where the LinearRings may or may not follow the right hand rule,
and they may or may not be closed loops (where the last element
is equal to the first).

Test all permutations of these rules on polygons with
0, 1, and 2 holes. Ensure that for any polygon, each LinearRing
may follow a different subset of rules.
"""

import h3
import itertools


def reverse(loop):
    return list(reversed(loop))


def drop_last(loop):
    return loop[:-1]


def toggle_map(func, poly):
    """ Return all permutations of `func` being applied or not
    to each element of `poly`

    returns iterable of length 2**len(poly)
    """
    mapped = (list(func(loop)) for loop in poly)

    return itertools.product(*zip(poly, mapped))


def chain_toggle_map(func, seq):
    seq = (toggle_map(func, p) for p in seq)
    seq = itertools.chain(*seq)

    return seq


def input_permutations(geo, res=5):
    g = [geo]
    g = chain_toggle_map(drop_last, g)
    g = chain_toggle_map(reverse, g)

    for p in g:
        poly = h3.LatLngPoly(*p)
        cells = h3.h3shape_to_cells(poly, res=res)
        yield cells


def get_us_box_coords():

    # big center chunk of the US in lat/lng order
    outer = [
        [42.68, -110.61],
        [32.17, -109.02],
        [31.57,  -94.26],
        [42.94,  -89.38],
        [42.68, -110.61]
    ]

    hole1 = [
        [39.77, -105.07],
        [34.81, -104.72],
        [34.77,  -98.39],
        [40.14,  -96.72],
        [39.77, -105.07]
    ]

    hole2 = [
        [41.37, -98.61],
        [40.04, -91.80],
        [42.32, -91.80],
        [41.37, -98.61]
    ]

    return outer, hole1, hole2


def test_input_format():
    geo = get_us_box_coords()

    assert len(geo) == 3

    # two holes
    for cells in input_permutations(geo[:3]):
        assert len(cells) == 5437

    # one hole
    for cells in input_permutations(geo[:2]):
        assert len(cells) == 5726

    # zero holes
    for cells in input_permutations(geo[:1]):
        assert len(cells) == 7063
