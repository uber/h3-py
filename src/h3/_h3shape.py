from abc import ABCMeta, abstractmethod


class H3Shape(metaclass=ABCMeta):
    @property
    @abstractmethod
    def __geo_interface__(self):
        """ https://github.com/pytest-dev/pytest-cov/issues/428 """


class H3Poly(H3Shape):
    """
    Container for loops of lat/lng points describing a polygon.

    Attributes
    ----------
    outer : list[tuple[float, float]]
        List of lat/lng points describing the outer loop of the polygon

    holes : list[list[tuple[float, float]]]
        List of loops of lat/lng points describing the holes of the polygon

    Examples
    --------

    A polygon with a single outer ring consisting of 4 points, having no holes:

    >>> H3Poly(
    ...     [(37.68, -122.54), (37.68, -122.34), (37.82, -122.34), (37.82, -122.54)],
    ... )
    <H3Poly: [4]>

    The same polygon, but with one hole consisting of 3 points:

    >>> H3Poly(
    ...     [(37.68, -122.54), (37.68, -122.34), (37.82, -122.34), (37.82, -122.54)],
    ...     [(37.76, -122.51), (37.76, -122.44), (37.81, -122.51)],
    ... )
    <H3Poly: [4/(3,)]>

    The same as above, but with one additional hole, made up of 5 points:

    >>> H3Poly(
    ...     [(37.68, -122.54), (37.68, -122.34), (37.82, -122.34), (37.82, -122.54)],
    ...     [(37.76, -122.51), (37.76, -122.44), (37.81, -122.51)],
    ...     [(37.71, -122.43), (37.71, -122.37), (37.73, -122.37), (37.75, -122.41),
    ...      (37.73, -122.43)],
    ... )
    <H3Poly: [4/(3, 5)]>
    """
    def __init__(self, outer, *holes):
        loops = [outer] + list(holes)
        for loop in loops:
            if len(loop) in (1, 2):
                raise ValueError('Non-empty H3Poly loops need at least 3 points.')

        self.outer = tuple(_open_ring(outer))
        self.holes = tuple(
            _open_ring(hole)
            for hole in holes
        )

    def __repr__(self):
        return '<H3Poly: {}>'.format(self.loopcode)

    def __len__(self):
        """
        Should this be the number of points in the outer loop,
        the number of holes (or +1 for the outer loop)?
        """
        raise NotImplementedError('No clear definition of length for H3Poly.')

    @property
    def loopcode(self):
        """ Short code for describing the length of the outer loop and each hole

        Example: `[382/(18, 6, 6)]` indicates an outer loop of 382 points,
        along with 3 holes with 18, 6, and 6 points, respectively.

        Example: `[15]` indicates an outer loop of 15 points and no holes.
        """
        outer = len(self.outer)
        holes = tuple(map(len, self.holes))

        outer = str(outer)

        if holes:
            out = outer + '/' + str(holes)
        else:
            out = outer

        return '[' + out + ']'

    @property
    def __geo_interface__(self):
        ll2 = _polygon_to_LL2(self)
        gj_dict = _LL2_to_geojson_dict(ll2)

        return gj_dict


class H3MultiPoly(H3Shape):
    def __init__(self, *polys):
        self.polys = tuple(polys)

        for p in self.polys:
            if not isinstance(p, H3Poly):
                raise ValueError('H3MultiPoly requires each input to be an H3Poly object, instead got: ' + str(p)) # noqa

    def __repr__(self):
        out = [p.loopcode for p in self.polys]
        out = ', '.join(out)
        out = '<H3MultiPoly: {}>'.format(out)
        return out

    def __iter__(self):
        return iter(self.polys)

    def __len__(self):
        """ Give the number of polygons in this multi-polygon.
        """

        """
        TODO: Pandas series or dataframe representation changes depending
        on if __len__ is defined.

        I'd prefer the one that states `H3MultiPoly`. It seems like Pandas is assuming
        an iterable is best-described by its elements when choosing the representation.

        when __len__ *IS NOT* defined:

        0                      <H3MultiPoly: [368], [20], [6]>
        1    <H3MultiPoly: [632/(6, 6, 6, 6, 6)], [290/(6,)...
        2    <H3MultiPoly: [490/(6, 6, 10, 10, 14, 10, 6)],...
        3    <H3MultiPoly: [344/(6,)], [22], [6], [10], [6]...
        4    <H3MultiPoly: [382/(18, 6, 6)], [32], [6], [18...

        when __len__ *IS* defined:

        0     (<H3Poly: [368]>, <H3Poly: [20]>, <H3Poly: [6]>)
        1    (<H3Poly: [632/(6, 6, 6, 6, 6)]>, <H3Poly: [29...
        2    (<H3Poly: [490/(6, 6, 10, 10, 14, 10, 6)]>, <H...
        3    (<H3Poly: [344/(6,)]>, <H3Poly: [22]>, <H3Poly...
        4    (<H3Poly: [382/(18, 6, 6)]>, <H3Poly: [32]>, <...
        """
        return len(self.polys)

    def __getitem__(self, index):
        return self.polys[index]

    @property
    def __geo_interface__(self):
        ll3 = _mpoly_to_LL3(self)
        gj_dict = _LL3_to_geojson_dict(ll3)

        return gj_dict


"""
Helpers for cells_to_geojson and geojson_to_cells.

Dealing with GeoJSON Polygons and MultiPolygons can be confusing because
there are so many nested lists. To help keep track, we use the following
symbols to denote different levels of nesting.

LL0: lat/lng or lng/lat pair
LL1: list of LL0s
LL2: list of LL1s (i.e., a polygon with holes)
LL3: list of LL2s (i.e., several polygons with holes)


## TODO

- Allow user to specify "container" in `cells_to_geojson`.
    - That is, they may want a MultiPolygon even if the output fits in a Polygon
    - 'auto', Polygon, MultiPolygon, FeatureCollection, GeometryCollection, ...
"""


def _mpoly_to_LL3(mpoly):
    ll3 = tuple(
        _polygon_to_LL2(poly)
        for poly in mpoly
    )

    return ll3


def _LL3_to_mpoly(ll3):
    polys = [
        _LL2_to_polygon(ll2)
        for ll2 in ll3
    ]

    mpoly = H3MultiPoly(*polys)

    return mpoly


def _polygon_to_LL2(h3poly):
    ll2 = [h3poly.outer] + list(h3poly.holes)
    ll2 = tuple(
        _close_ring(_swap_latlng(ll1))
        for ll1 in ll2
    )

    return ll2


def _LL2_to_polygon(ll2):
    ll2 = [
        _swap_latlng(ll1)
        for ll1 in ll2
    ]
    h3poly = H3Poly(*ll2)

    return h3poly


def _LL2_to_geojson_dict(ll2):
    gj_dict = {
        'type': 'Polygon',
        'coordinates': ll2,
    }

    return gj_dict


def _LL3_to_geojson_dict(ll3):
    gj_dict = {
        'type': 'MultiPolygon',
        'coordinates': ll3,
    }

    return gj_dict


def _swap_latlng(ll1):
    ll1 = tuple(
        (b, a) for a, b in ll1
    )
    return ll1


def _close_ring(ll1):
    """
    Idempotent
    """
    if ll1 and (ll1[0] != ll1[-1]):
        ll1 = tuple(ll1) + (ll1[0],)

    return ll1


def _open_ring(ll1):
    """
    Idempotent
    """
    if ll1 and (ll1[0] == ll1[-1]):
        ll1 = ll1[:-1]

    return ll1


def geo_to_h3shape(geo):
    """
    Translate from __geo_interface__ to H3Shape.

    `geo` either implements `__geo_interface__` or is a dict matching the format

    Returns
    -------
    H3Shape
    """

    # geo can be dict, a __geo_interface__, a string, H3Poly or H3MultiPoly
    if isinstance(geo, H3Shape):
        return geo

    if hasattr(geo, '__geo_interface__'):
        # get dict
        geo = geo.__geo_interface__

    assert isinstance(geo, dict)  # todo: remove

    t = geo['type']
    coord = geo['coordinates']

    if t == 'Polygon':
        ll2 = coord
        h3shape = _LL2_to_polygon(ll2)
    elif t == 'MultiPolygon':
        ll3 = coord
        h3shape = _LL3_to_mpoly(ll3)
    else:
        raise ValueError('Unrecognized type: ' + str(t))

    return h3shape


def h3shape_to_geo(h3shape):
    """
    Translate from H3Shape to a __geo_interface__ dict.

    `h3shape` should be either H3Poly or H3MultiPoly

    Returns
    -------
    dict
    """
    return h3shape.__geo_interface__
