import pytest
from h3._h3shape import LatLngPoly, h3shape_to_geo, LatLngMultiPoly


def test_h3shape_to_geo_containers():
    # Create a basic dummy polygon for testing
    poly = LatLngPoly(
        [(37.68, -122.54), (37.68, -122.34), (37.82, -122.34), (37.82, -122.54)]
    )

    # Test 'auto' (Default behavior should return a Polygon)
    auto_geo = h3shape_to_geo(poly, container='auto')
    assert auto_geo['type'] == 'Polygon'

    # Test MultiPolygon wrapper
    mp_geo = h3shape_to_geo(poly, container='MultiPolygon')
    assert mp_geo['type'] == 'MultiPolygon'
    assert len(mp_geo['coordinates']) == 1

    # Test Feature wrapper
    feat_geo = h3shape_to_geo(poly, container='Feature')
    assert feat_geo['type'] == 'Feature'
    assert feat_geo['geometry']['type'] == 'Polygon'

    # Test FeatureCollection wrapper
    fc_geo = h3shape_to_geo(poly, container='FeatureCollection')
    assert fc_geo['type'] == 'FeatureCollection'
    assert len(fc_geo['features']) == 1
    assert fc_geo['features'][0]['type'] == 'Feature'
    assert fc_geo['features'][0]['geometry']['type'] == 'Polygon'

    # Test GeometryCollection wrapper
    gc_geo = h3shape_to_geo(poly, container='GeometryCollection')
    assert gc_geo['type'] == 'GeometryCollection'
    assert len(gc_geo['geometries']) == 1
    assert gc_geo['geometries'][0]['type'] == 'Polygon'


def test_h3shape_to_geo_invalid_containers():
    # 1. Test an unknown container string
    poly = LatLngPoly([(37.68, -122.54), (37.68, -122.34), (37.82, -122.34)])
    with pytest.raises(ValueError, match='invalid or insufficient'):
        h3shape_to_geo(poly, container='InvalidString')

    # 2. Test an insufficient container (MultiPolygon data into a Polygon container)
    mpoly = LatLngMultiPoly([
        [(37.68, -122.54), (37.68, -122.34), (37.82, -122.34)]
    ])
    with pytest.raises(ValueError, match='invalid or insufficient'):
        h3shape_to_geo(mpoly, container='Polygon')


def test_h3shape_to_geo_exact_match():
    # Test that requesting a MultiPolygon for MultiPolygon data succeeds
    mpoly = LatLngMultiPoly([
        [(37.68, -122.54), (37.68, -122.34), (37.82, -122.34)]
    ])

    mp_geo = h3shape_to_geo(mpoly, container='MultiPolygon')

    assert mp_geo['type'] == 'MultiPolygon'
    assert len(mp_geo['coordinates']) == 1
