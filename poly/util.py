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

import h3
import json


if True:  # functions below should be inverses of each other
    def cells_to_geojson(cells):
        mpoly = h3.cells_to_shape(cells)
        ll3 = _mpoly_to_LL3(mpoly)
        gj_dict = _LL3_to_geojson_dict(ll3)
        gj_str = json.dumps(gj_dict)

        return gj_str

    def geojson_to_cells(gj_str, res):
        gj_dict = json.loads(gj_str)
        ll3 = _geojson_dict_to_LL3(gj_dict)
        mpoly = _LL3_to_mpoly(ll3)
        cells = h3.shape_to_cells(mpoly, res)

        return cells


if True:  # functions below should be inverses of each other
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

        mpoly = h3.H3MultiPoly(*polys)

        return mpoly


if True:  # functions below should be inverses of each other
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
        h3poly = h3.H3Poly(*ll2)

        return h3poly


if True:  # functions below should be inverses of each other
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
            ll3 = [ ll2 ]
        elif t == 'MultiPolygon':
            ll3 = coord
        else:
            raise ValueError(f'Unrecognized type: {t}')

        return ll3


def _swap_latlng(ll1):
    ll1 = [(lng, lat) for lat, lng in ll1]

    return ll1

def _close_ring(ll1):
    if ll1[0] != ll1[-1]:
        ll1.append(ll1[0])

    return ll1