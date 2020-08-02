import numpy as np
import h3.api.basic_int as h3

from sphericalpolygon import create_polygon


def area_sp(h):
    earth_radius_km = 6371.007180918475
    
    poly = np.array(h3.h3_to_geo_boundary(h))
    poly = create_polygon(poly)
    
    return poly.area(earth_radius_km)
