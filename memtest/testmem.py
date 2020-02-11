import h3
import time

def foo():
    N = 5

    #h = h3.geo_to_h3(0,0,0)
    #out = h3.h3_to_children(h, N)
    #h2 = h3.compact(out)

    #assert {h} == h2

    # get s a weird asymptote
    #poly = h3.h3_set_to_multi_polygon(out)

    h = h3.geo_to_h3(0,0,10)
    out = h3.k_ring(h, 20)



time.sleep(1)

for _ in range(300):
    foo()
    time.sleep(.1)

time.sleep(1)
