import h3
import time
import numpy as np

# todo: some of these functions have a much cleaner memory profile... leaks?

def dummy():
    a = np.zeros(100000)
    h = h3.geo_to_h3(0, 0, 10)
    hexes = h3.k_ring(h, 70)

def to_mulitpoly():
    res = 10

    h = h3.geo_to_h3(0, 0, res)
    hexes = h3.k_ring(h, 70)

    poly = h3.h3_set_to_multi_polygon(hexes)

def compact():
    res = 10
    h = h3.geo_to_h3(0, 0, res)
    hexes = h3.k_ring(h, 70)

    hc = h3.compact(hexes)
    hu = h3.uncompact(hc, res)

    assert hu == hexes



#time.sleep(1)

for _ in range(100):
    #compact()
    #to_mulitpoly()
    dummy()
    time.sleep(.1)

#time.sleep(1)
