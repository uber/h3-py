import h3py.h3core as h3core
import h3py.util as u
from .._version import __version__

# this module tries to DRY-up API code which is repeated across
# modules. Not sure if this function closure is the best solution.
# There doesn't seem to be any obvious best-practice for
# programattically/dynamically creating modules

# another approach: we could also just use `exec()`


def _api_functions(
    _in_scalar,
    _out_scalar,
    _in_collection,
    _out_collection,
):
    def versions():
        v = {
            'c': h3core._c_version(),
            'python': __version__,
        }

        return v


    def string_to_h3(h):
        return u.hex2int(h)

    def h3_to_string(x):
        return u.int2hex(x)

    def num_hexagons(resolution):
        return h3core.num_hexagons(resolution)

    def mean_hex_area(resolution, unit='km2'):
        return h3core.mean_hex_area(resolution, unit)

    def mean_edge_length(resolution, unit='km'):
        return h3core.mean_edge_length(resolution, unit)

    def h3_is_valid(h):
        """Validates an H3 cell (hexagon or pentagon)

        Returns
        -------
        boolean
        """
        try:
            h = _in_scalar(h)
            return h3core.is_cell(h)
        except:
            return False

    def h3_unidirectional_edge_is_valid(edge):
        try:
            e = _in_scalar(edge)
            return h3core.is_edge(e)
        except: # todo: maybe make a special Exception type?
            return False


    def geo_to_h3(lat, lng, resolution):
        return _out_scalar(h3core.geo_to_h3(lat, lng, resolution))


    def h3_to_geo(h):
        """Reverse lookup an h3 address into a geo-coordinate"""
        return h3core.h3_to_geo(_in_scalar(h))

    def h3_get_resolution(h):
        """Returns the resolution of an `h3_address`

        :return: nibble (0-15)
        """
        return h3core.resolution(_in_scalar(h))

    def h3_to_parent(h, res=None):
        """ Get the parent of a hexagon.

        Parameters
        ----------
        h : H3 address
        res : int or None, optional
            The resolution for the parent
            If `None`, then `res = resolution(h) - 1`

        Returns
        -------
        H3 address

        """
        h = _in_scalar(h)
        p = h3core.parent(h, res)
        p = _out_scalar(p)

        return p

    def h3_distance(h1, h2):
        """ Compute the hex-distance between two hexagons

        Parameters
        ----------
        h1, h2 : H3 address

        Returns
        -------
        int

        """
        d = h3core.distance(
                _in_scalar(h1),
                _in_scalar(h2)
            )

        return d

    def h3_to_geo_boundary(h, geo_json=False):
        return h3core.cell_boundary(_in_scalar(h), geo_json)


    def k_ring(h, k=1):
        mv = h3core.disk(_in_scalar(h), k)

        return _out_collection(mv)

    def hex_ring(h, k=1):
        mv = h3core.ring(_in_scalar(h), k)

        return _out_collection(mv)

    def h3_to_children(h, res=None):
        """ Get the children of a hexagon.

        Parameters
        ----------
        h : H3 address
        res : int or None, optional
            The resolution for the children.
            If `None`, then `res = resolution(h) + 1`

        Returns
        -------
        collection of h3 addresses
        """
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

    def h3_is_pentagon(h):
        """
        a pentagon should still pass is_cell(), right?

        :returns: boolean
        """
        return h3core.is_pentagon(_in_scalar(h))

    def h3_get_base_cell(h):
        """
        :returns: boolean
        """
        return h3core.get_base_cell(_in_scalar(h))

    def h3_indexes_are_neighbors(h1, h2):
        """
        :returns: boolean
        """
        return h3core.are_neighbors(_in_scalar(h1), _in_scalar(h2))

    def get_h3_unidirectional_edge(origin, destination):
        o = _in_scalar(origin)
        d = _in_scalar(destination)
        e = h3core.edge(o, d)
        e = _out_scalar(e)

        return e

    def get_origin_h3_index_from_unidirectional_edge(e):
        e = _in_scalar(e)
        o = h3core.edge_origin(e)
        o = _out_scalar(o)

        return o

    def get_destination_h3_index_from_unidirectional_edge(e):
        e = _in_scalar(e)
        d = h3core.edge_destination(e)
        d = _out_scalar(d)

        return d


    def get_h3_indexes_from_unidirectional_edge(e):
        e = _in_scalar(e)
        o,d = h3core.edge_cells(e)
        o,d = _out_scalar(o), _out_scalar(d)

        return o,d

    def get_h3_unidirectional_edges_from_hexagon(origin):
        mv = h3core.edges_from_cell(_in_scalar(origin))

        return _out_collection(mv)

    def get_h3_unidirectional_edge_boundary(edge):
        return h3core.edge_boundary(_in_scalar(edge))

    def h3_line(start, end):
        mv = h3core.line(_in_scalar(start), _in_scalar(end))

        return _out_collection(mv)

    return locals()

