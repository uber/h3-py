"""
This module tries to DRY-up API code which is repeated across
modules. Not sure if this function closure is the best solution.
There doesn't seem to be any obvious best-practice for
programmatically/dynamically creating modules.

Another approach: we could also just use `exec()`
"""

from .. import _cy


def _api_functions(
        _in_scalar,
        _out_scalar,
        _in_collection,
        _out_unordered,
        _out_ordered,
        _globals,
):
    def versions():
        """ Return version numbers for both the Python library
        and the underlying H3 C library.

        Versions are output as strings of the form `'X.Y.Z'`.
        C and Python should match on `X` (major) and `Y` (minor),
        but may differ on `Z` (patch).

        Returns
        -------
        Dict[str, str]
            Consists of keys `'c'` and `'python'`.
        """
        from .._version import __version__

        v = {
            'c': _cy.c_version(),
            'python': __version__,
        }

        return v

    def string_to_h3(h):
        """ Converts a hexadecimal string to an H3 64-bit integer index
        """
        return _cy.hex2int(h)

    def h3_to_string(x):
        """ Converts an H3 64-bit integer index to a hexadecimal string
        """
        return _cy.int2hex(x)

    def num_hexagons(resolution):
        """ Return the total number of *cells* (hexagons and pentagons)
        for the given resolution.

        Returns
        -------
        int
        """
        return _cy.num_hexagons(resolution)

    def hex_area(resolution, unit='km^2'):
        return _cy.mean_hex_area(resolution, unit)

    def edge_length(resolution, unit='km'):
        return _cy.mean_edge_length(resolution, unit)

    def h3_is_valid(h):
        """Validates an H3 cell (hexagon or pentagon)

        Returns
        -------
        boolean
        """
        try:
            h = _in_scalar(h)
            return _cy.is_cell(h)
        except (ValueError, TypeError):
            return False

    def h3_unidirectional_edge_is_valid(edge):
        try:
            e = _in_scalar(edge)
            return _cy.is_edge(e)
        except (ValueError, TypeError):
            return False

    def geo_to_h3(lat, lng, resolution):
        return _out_scalar(_cy.geo_to_h3(lat, lng, resolution))

    def h3_to_geo(h):
        """Reverse lookup an h3 address into a geo-coordinate"""
        return _cy.h3_to_geo(_in_scalar(h))

    def h3_get_resolution(h):
        """Returns the resolution of an `h3_address`
        :return: nibble (0-15)
        """
        return _cy.resolution(_in_scalar(h))

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
        p = _cy.parent(h, res)
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
        h1 = _in_scalar(h1)
        h2 = _in_scalar(h2)

        d = _cy.distance(h1, h2)

        return d

    def h3_to_geo_boundary(h, geo_json=False):
        return _cy.cell_boundary(_in_scalar(h), geo_json)

    def k_ring(h, k=1):
        mv = _cy.disk(_in_scalar(h), k)

        return _out_unordered(mv)

    def hex_range(h, k=1):
        mv = _cy.disk(_in_scalar(h), k)

        return _out_unordered(mv)

    def hex_ring(h, k=1):
        mv = _cy.ring(_in_scalar(h), k)

        return _out_unordered(mv)

    def hex_range_distances(h, K):
        h = _in_scalar(h)

        out = [
            _out_unordered(_cy.ring(h, k))
            for k in range(K + 1)
        ]

        return out

    def hex_ranges(hexes, K):
        out = {
            h: hex_range_distances(h, K)
            for h in hexes
        }

        return out

    def k_ring_distances(h, K):
        return hex_range_distances(h, K)

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
        mv = _cy.children(_in_scalar(h), res)

        return _out_unordered(mv)

    # todo: nogil for expensive C operation?
    def compact(hexes):
        hu = _in_collection(hexes)
        hc = _cy.compact(hu)

        return _out_unordered(hc)

    def uncompact(hexes, res):
        hc = _in_collection(hexes)
        hu = _cy.uncompact(hc, res)

        return _out_unordered(hu)

    def h3_set_to_multi_polygon(hexes, geo_json=False):
        hexes = _in_collection(hexes)
        return _cy.h3_set_to_multi_polygon(hexes, geo_json=geo_json)

    def polyfill_polygon(outer, res, holes=None, lnglat_order=False):
        mv = _cy.polyfill_polygon(outer, res, holes=holes, lnglat_order=lnglat_order)

        return _out_unordered(mv)

    def polyfill_geojson(geojson, res):
        mv = _cy.polyfill_geojson(geojson, res)

        return _out_unordered(mv)

    def polyfill(geojson, res, geo_json_conformant=False):
        mv = _cy.polyfill(geojson, res, geo_json_conformant=geo_json_conformant)

        return _out_unordered(mv)

    def h3_is_pentagon(h):
        """
        a pentagon should still pass is_cell(), right?
        :returns: boolean
        """
        return _cy.is_pentagon(_in_scalar(h))

    def h3_get_base_cell(h):
        """
        :returns: boolean
        """
        return _cy.get_base_cell(_in_scalar(h))

    def h3_indexes_are_neighbors(h1, h2):
        """
        :returns: boolean
        """
        h1 = _in_scalar(h1)
        h2 = _in_scalar(h2)

        return _cy.are_neighbors(h1, h2)

    def get_h3_unidirectional_edge(origin, destination):
        o = _in_scalar(origin)
        d = _in_scalar(destination)
        e = _cy.edge(o, d)
        e = _out_scalar(e)

        return e

    def get_origin_h3_index_from_unidirectional_edge(e):
        e = _in_scalar(e)
        o = _cy.edge_origin(e)
        o = _out_scalar(o)

        return o

    def get_destination_h3_index_from_unidirectional_edge(e):
        e = _in_scalar(e)
        d = _cy.edge_destination(e)
        d = _out_scalar(d)

        return d

    def get_h3_indexes_from_unidirectional_edge(e):
        e = _in_scalar(e)
        o, d = _cy.edge_cells(e)
        o, d = _out_scalar(o), _out_scalar(d)

        return o, d

    def get_h3_unidirectional_edges_from_hexagon(origin):
        mv = _cy.edges_from_cell(_in_scalar(origin))

        return _out_unordered(mv)

    def get_h3_unidirectional_edge_boundary(edge, geo_json=False):
        return _cy.edge_boundary(_in_scalar(edge), geo_json=geo_json)

    def h3_line(start, end):
        mv = _cy.line(_in_scalar(start), _in_scalar(end))

        return _out_ordered(mv)

    def h3_is_res_class_iii(h):
        return _cy.is_res_class_iii(_in_scalar(h))

    def h3_is_res_class_III(h):
        return _cy.is_res_class_iii(_in_scalar(h))

    _globals.update(locals())
