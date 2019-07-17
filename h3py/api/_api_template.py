import h3py.h3core as h3core
import h3py.util as u

# this module tries to DRY-up API code which is repeated across
# modules. Not sure if this function closure is the best solution.
# There doesn't seem to be any obvious best-practice for
# programattically/dynamically creating modules

# another approach: we could also just use `exec()`


def api_functions(
    _in_scalar,
    _out_scalar,
    _in_collection,
    _out_collection,
):
    def hex2int(h):
        return u.hex2int(h)

    def int2hex(x):
        return u.int2hex(x)

    def num_hexagons(resolution):
        return h3core.num_hexagons(resolution)

    def hex_area(resolution, unit='km'):
        return h3core.hex_area(resolution, unit)

    def edge_length(resolution, unit='km'):
        return h3core.edge_length(resolution, unit)

    def is_valid(h):
        """Validates an H3 address

        :returns: boolean
        """
        # todo: might think about renaming this function, since we can check if something is a valid hex or a valid edge (or if it is a pentagon...)
        # `is_h3_address()`?

        try:
            h = _in_scalar(h)
            return h3core.is_valid(h)
        except: # todo: maybe make a special Exception type?
            return False

    def is_uni_edge(edge):
        try:
            e = _in_scalar(edge)
            return h3core.is_uni_edge(e)
        except: # todo: maybe make a special Exception type?
            return False


    def geo_to_h3(lat, lng, resolution):
        return _out_scalar(h3core.geo_to_h3(lat, lng, resolution))


    def h3_to_geo(h):
        """Reverse lookup an h3 address into a geo-coordinate"""
        return h3core.h3_to_geo(_in_scalar(h))

    def resolution(h):
        """Returns the resolution of an `h3_address`

        :return: nibble (0-15)
        """
        return h3core.resolution(_in_scalar(h))

    def parent(h, res=None):
        h = _in_scalar(h)
        p = h3core.parent(h, res)
        p = _out_scalar(p)

        return p

    def distance(h1, h2):
        """ compute the hex-distance between two hexagons

        todo: figure out string typing.
        had to drop typing due to errors like
        `TypeError: Argument 'h2' has incorrect type (expected str, got numpy.str_)`
        """
        d = h3core.distance(
                _in_scalar(h1),
                _in_scalar(h2)
            )

        return d

    def h3_to_geo_boundary(h, geo_json=False):
        return h3core.h3_to_geo_boundary(_in_scalar(h), geo_json)


    def k_ring(h, k):
        mv = h3core.k_ring(_in_scalar(h), k)

        return _out_collection(mv)

    def hex_ring(h, k):
        mv = h3core.hex_ring(_in_scalar(h), k)

        return _out_collection(mv)

    def children(h, res=None):
        mv = h3core.children(_in_scalar(h), res)

        return _out_collection(mv)

    # todo: nogil for expensive C operation?
    def compact(hexes):
        hu = _in_collection(hexes)
        hc = h3core.compact(hu)

        return _out_collection(hc)

    def uncompact(hexes, res):
        hc = _in_collection(hexes)
        hu = h3core.uncompact(hc, res)

        return _out_collection(hu)


    def polyfill(geos, res):
        mv = h3core.polyfill(geos, res)

        return _out_collection(mv)

    def is_pentagon(h):
        """
        a pentagon should still pass is_valid(), right?

        :returns: boolean
        """
        return h3core.is_pentagon(_in_scalar(h))

    def base_cell(h):
        """
        :returns: boolean
        """
        return h3core.base_cell(_in_scalar(h))

    def are_neighbors(h1, h2):
        """
        :returns: boolean
        """
        return h3core.are_neighbors(_in_scalar(h1), _in_scalar(h2))

    def uni_edge(origin, destination):
        o = _in_scalar(origin)
        d = _in_scalar(destination)
        e = h3core.uni_edge(o, d)
        e = _out_scalar(e)

        return e

    def uni_edge_origin(e):
        e = _in_scalar(e)
        o = h3core.uni_edge_origin(e)
        o = _out_scalar(o)

        return o

    def uni_edge_destination(e):
        e = _in_scalar(e)
        d = h3core.uni_edge_destination(e)
        d = _out_scalar(d)

        return d


    def uni_edge_hexes(e):
        e = _in_scalar(e)
        o,d = h3core.uni_edge_hexes(e)
        o,d = _out_scalar(o), _out_scalar(d)

        return o,d

    def uni_edges_from_hex(origin):
        mv = h3core.uni_edges_from_hex(_in_scalar(origin))

        return _out_collection(mv)

    def uni_edge_boundary(edge):
        return h3core.uni_edge_boundary(_in_scalar(edge))

    return locals()

