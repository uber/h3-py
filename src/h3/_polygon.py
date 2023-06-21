# todo: rename file to _shape.py
import json


class H3Shape:
    pass


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
    <H3Poly |outer|=4, |holes|=()>

    The same polygon, but with one hole consisting of 3 points:

    >>> H3Poly(
    ...     [(37.68, -122.54), (37.68, -122.34), (37.82, -122.34), (37.82, -122.54)],
    ...     [(37.76, -122.51), (37.76, -122.44), (37.81, -122.51)],
    ... )
    <H3Poly |outer|=4, |holes|=(3,)>

    The same as above, but with one additional hole, made up of 5 points:

    >>> H3Poly(
    ...     [(37.68, -122.54), (37.68, -122.34), (37.82, -122.34), (37.82, -122.54)],
    ...     [(37.76, -122.51), (37.76, -122.44), (37.81, -122.51)],
    ...     [(37.71, -122.43), (37.71, -122.37), (37.73, -122.37), (37.75, -122.41),
    ...      (37.73, -122.43)],
    ... )
    <H3Poly |outer|=4, |holes|=(3, 5)>

    Notes
    -----

    - TODO: Add GeoJSON translation support.
    """
    def __init__(self, outer, *holes):
        if isinstance(outer, H3Poly):
            # Since the object being copied contains a tuple, we can copy it directly
            if len(holes) != 0:
                raise ValueError(
                    "When copying another polygon, holes cannot be specified"
                )
            self.outer = outer.outer
            self.holes = outer.holes
        elif isinstance(outer, dict) or hasattr(outer, "__geo_interface__"):
            to_import = outer if isinstance(outer, dict) else outer.__geo_interface__
            ll3 = _geojson_dict_to_LL3(to_import)
            to_copy = _LL3_to_mpoly(ll3)
            if len(to_copy.polys) != 1:
                raise ValueError(
                    "H3Poly must be constructed with a single polygon, "
                    "but got " + str(len(to_copy.polys))
                )
            # Check that conflicting arguments (GeoJSON, and also holes)
            # aren't specified.
            if len(holes) != 0:
                raise ValueError("When copying from GeoJSON, holes cannot be specified")
            self.outer = to_copy.polys[0].outer
            self.holes = to_copy.polys[0].holes
        else:
            self.outer = tuple(outer)
            self.holes = tuple(holes)

        # todo: maybe add some validation

    def __repr__(self):
        s = '<H3Poly |outer|={}, |holes|={}>'.format(
            len(self.outer),
            tuple(map(len, self.holes)),
        )

        return s

    @property
    def __geo_interface__(self):
        ll2 = _polygon_to_LL2(self)
        ll3 = [ll2]
        gj_dict = _LL3_to_geojson_dict(ll3)

        return gj_dict


class H3MultiPoly(H3Shape):
    def __init__(self, *polys):
        if len(polys) and isinstance(polys[0], H3MultiPoly):
            # Since the object being copied contains a tuple, we can copy it directly
            if len(polys) != 1:
                raise ValueError(
                    "When copying from another H3MultiPoly, "
                    "only one may be specified but got " + str(len(polys))
                )
            self.polys = polys[0].polys
        elif (len(polys)
              and not isinstance(polys[0], H3Shape)
              and (isinstance(polys[0], dict)
                   or hasattr(polys[0], '__geo_interface__'))):
            to_import = (
                polys[0] if isinstance(polys[0], dict) else polys[0].__geo_interface__
            )
            if len(polys) != 1:
                raise ValueError(
                    "When copying from GeoJSON, only one may be specified"
                )
            ll3 = _geojson_dict_to_LL3(to_import)
            to_copy = _LL3_to_mpoly(ll3)
            self.polys = to_copy.polys
        else:
            self.polys = tuple(polys)

    def __repr__(self):
        return 'H3MultiPoly' + str(self.polys)

    def __iter__(self):
        return iter(self.polys)

    def __len__(self):
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
    ll3 = [
        _polygon_to_LL2(poly)
        for poly in mpoly
    ]

    return ll3


def _LL3_to_mpoly(ll3):
    polys = [
        _LL2_to_polygon(ll2)
        for ll2 in ll3
    ]

    mpoly = H3MultiPoly(*polys)

    return mpoly


# functions below should be inverses of each other
def _polygon_to_LL2(h3poly):
    ll2 = [h3poly.outer] + list(h3poly.holes)
    ll2 = [
        _close_ring(_swap_latlng(ll1))
        for ll1 in ll2
    ]

    return ll2


def _LL2_to_polygon(ll2):
    ll2 = [
        _swap_latlng(ll1)
        for ll1 in ll2
    ]
    h3poly = H3Poly(*ll2)

    return h3poly


# functions below should be inverses of each other
def _LL3_to_geojson_dict(ll3):
    if len(ll3) == 1:
        gj_dict = {
            'type': 'Polygon',
            'coordinates': ll3[0],
        }
    else:
        gj_dict = {
            'type': 'MultiPolygon',
            'coordinates': ll3,
        }

    return gj_dict


def _geojson_dict_to_LL3(gj_dict):
    t = gj_dict['type']
    coord = gj_dict['coordinates']

    if t == 'Polygon':
        ll2 = coord
        ll3 = [ll2]
    elif t == 'MultiPolygon':
        ll3 = coord
    else:
        raise ValueError('Unrecognized type: ' + str(t))

    return ll3


def _swap_latlng(ll1):
    ll1 = [(lng, lat) for lat, lng in ll1]

    return ll1


def _close_ring(ll1):
    if ll1[0] != ll1[-1]:
        ll1.append(ll1[0])

    return ll1


def check_geo_interface(x):
    return any(
        isinstance(x, str),
        hasattr(x, '__geo_interface__'),
        isinstance(x, dict) and 'type' in x,
    )


def from_geo_interface(x):
    if isinstance(x, str):
        x = json.loads(x)

    if hasattr(x, '__geo_interface__'):
        x = x.__geo_interface__

    if isinstance(x, dict) and 'type' in x:
        ll3 = _geojson_dict_to_LL3(x)
        mpoly = _LL3_to_mpoly(ll3)
        return mpoly
