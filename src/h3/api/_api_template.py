"""
This module tries to DRY-up API code which is repeated across
modules. Not sure if this function closure is the best solution.
There doesn't seem to be any obvious best-practice for
programmatically/dynamically creating modules.

Another approach: we could also just use `exec()`


todo: look up numpydoc reccomendations on docstrings for modules

Definitions of types
--------------------
H3Index:
    An unsigned 64-bit integer representing a valid H3 cell or
    unidirectional edge.
    Depending on the API, an H3Index may be represented as an
    unsigned integer type, or as a hexadecimal string.

H3 cell:
    A pentagon or hexagon that can be represented by an H3Index.

H3Cell:
    H3Index representation of an H3 cell.

H3Edge:
    H3Index representation of an H3 unidirectional edge.

"""

from .. import _cy


# todo: how do we lint these functions and docstrings? it seems to currently
# be skipped due to it being inside the `_api_functions` function.


def _api_functions(
        _in_scalar,
        _out_scalar,
        _in_collection,
        _out_unordered,
        _out_ordered,
        _globals,
):
    def versions():
        """
        Return version numbers for both the Python library
        and the underlying H3 C library.

        Versions are output as strings of the form `'X.Y.Z'`.
        C and Python should match on `X` (major) and `Y` (minor),
        but may differ on `Z` (patch).

        Returns
        -------
        dict like `{'c': 'X.Y.Z', 'python': 'A.B.C'}`
        """
        from .._version import __version__

        v = {
            'c': _cy.c_version(),
            'python': __version__,
        }

        return v

    def string_to_h3(h):
        """
        Converts a hexadecimal string to an H3 64-bit integer index

        Parameters
        ----------
        h : str
            Hexadecimal string like `'89754e64993ffff'`

        Returns
        -------
        int
            Unsigned 64-bit integer
        """
        return _cy.hex2int(h)

    def h3_to_string(x):
        """
        Converts an H3 64-bit integer index to a hexadecimal string

        Parameters
        ----------
        x : int
            Unsigned 64-bit integer

        Returns
        -------
        str
            Hexadecimal string like `'89754e64993ffff'`
        """
        return _cy.int2hex(x)

    def num_hexagons(resolution):
        """
        Return the total number of *cells* (hexagons and pentagons)
        for the given resolution.

        Returns
        -------
        int
        """
        return _cy.num_hexagons(resolution)

    def hex_area(resolution, unit='km^2'):
        """
        Return the average area of an H3 *hexagon*
        for the given resolution.

        This average *excludes* pentagons.

        todo: `mean_hex_area` in 4.0

        Returns
        -------
        float
        """
        return _cy.mean_hex_area(resolution, unit)

    def edge_length(resolution, unit='km'):
        """
        Return the average *hexagon* edge length
        for the given resolution.

        This average *excludes* pentagons.

        todo: `mean_edge_length` in 4.0

        Returns
        -------
        float
        """
        return _cy.mean_edge_length(resolution, unit)

    def h3_is_valid(h):
        """
        Validates an H3 cell (hexagon or pentagon)

        Returns
        -------
        bool
        """
        try:
            h = _in_scalar(h)
            return _cy.is_cell(h)
        except (ValueError, TypeError):
            return False

    def h3_unidirectional_edge_is_valid(edge):
        """
        Validates an H3 unidirectional edge

        Returns
        -------
        bool
        """
        try:
            e = _in_scalar(edge)
            return _cy.is_edge(e)
        except (ValueError, TypeError):
            return False

    def geo_to_h3(lat, lng, resolution):
        """
        Return the cell containing the (lat, lng) point
        for a given resolution.

        Returns
        -------
        H3Index
            Either `str` or `int`, depending on API.

        """
        return _out_scalar(_cy.geo_to_h3(lat, lng, resolution))

    def h3_to_geo(h):
        """
        Return the center point of an H3 cell
        as a lat/lng pair

        Returns
        -------
        lat : float
            Latitude
        lng : float
            Longitude
        """
        return _cy.h3_to_geo(_in_scalar(h))

    def h3_get_resolution(h):
        """
        Returns the resolution of an H3 cell

        todo: would this work on edges, in addition to cells?

        Parameters
        ----------
        h : H3Index
            H3Index is a `str` or `int`, depending on API

        Returns
        -------
        int
        """
        return _cy.resolution(_in_scalar(h))

    def h3_to_parent(h, res=None):
        """
        Get the parent of a cell.

        Parameters
        ----------
        h : H3Index
            H3Index is a `str` or `int`, depending on API
        res : int or None, optional
            The resolution for the parent
            If `None`, then `res = resolution(h) - 1`

        Returns
        -------
        H3Index
            Specifically, an H3 cell.
            H3Index is a `str` or `int`, depending on API
        """
        h = _in_scalar(h)
        p = _cy.parent(h, res)
        p = _out_scalar(p)

        return p

    def h3_distance(h1, h2):
        """
        Compute the H3 distance between two cells.

        The H3 distance is defined as the length of the shortest
        path between the cells in the graph formed by connecting
        adjacent cells.

        Parameters
        ----------
        h1 : H3Index
        h2 : H3Index
            H3Index is a `str` or `int`, depending on API

        Returns
        -------
        int
        """
        h1 = _in_scalar(h1)
        h2 = _in_scalar(h2)

        d = _cy.distance(h1, h2)

        return d

    def h3_to_geo_boundary(h, geo_json=False):
        """
        Return tuple of lat/lng pairs describing
        the cell boundary.

        Parameters
        ----------
        h : H3Index
            H3Index is a `str` or `int`, depending on API
        geo_json : bool, optional
            If `True`, return output in GeoJson format:
            lng/lat pairs (opposite order), and
            have the last pair be the same as the first.
            If `False`, return lat/lng pairs, with the last
            pair distinct from the first.

        Returns
        -------
        tuple of (float, float) tuples

        """
        return _cy.cell_boundary(_in_scalar(h), geo_json)

    def k_ring(h, k=1):
        """
        Return unordered set of cells with H3 distance
        `<= k` from `h`. That is, the "filled-in" disk.

        Parameters
        ----------
        h : H3Index
            H3Index is a `str` or `int`, depending on API.
        k : int
            Size of disk.

        Returns
        -------
        unordered collection of H3Index
            Collection type varies with API: `set`, `numpy.ndarray`, etc.
        """
        mv = _cy.disk(_in_scalar(h), k)

        return _out_unordered(mv)

    def hex_range(h, k=1):
        """
        Alias for `k_ring`.
        "Filled-in" disk.

        Notes
        -----
        This name differs from the C API.

        """
        mv = _cy.disk(_in_scalar(h), k)

        return _out_unordered(mv)

    def hex_ring(h, k=1):
        """
        Return unordered set of cells with H3 distance
        `== k` from `h`. That is, the "hollow" ring.

        Parameters
        ----------
        h : H3Index
            H3Index is a `str` or `int`, depending on API.
        k : int
            Size of ring.

        Returns
        -------
        unordered collection of H3Index
            Collection type varies with API: `set`, `numpy.ndarray`, etc.
        """
        mv = _cy.ring(_in_scalar(h), k)

        return _out_unordered(mv)

    def hex_range_distances(h, K):
        """
        Ordered list of the "hollow" rings around `h`,
        up to and including distance `K`.

        Parameters
        ----------
        h : H3Index
            H3Index is a `str` or `int`, depending on API.
        K : int
            Largest distance considered.

        Returns
        -------
        ordered collection of (unordered collection of H3Index)
            Collection type varies with API: `list`, `numpy.ndarray`, etc.
        """
        h = _in_scalar(h)

        out = [
            _out_unordered(_cy.ring(h, k))
            for k in range(K + 1)
        ]

        return out

    def hex_ranges(hexes, K):
        """
        Return a dictionary like

        {h: h: hex_range_distances(h, K)}
        for each h in hexes

        todo: can we drop this function? the user can implement if needed.

        Returns
        -------
        Dict[H3Cell, List[ UnorderedCollection[H3Cell] ]]

        """
        out = {
            h: hex_range_distances(h, K)
            for h in hexes
        }

        return out

    def k_ring_distances(h, K):
        """ Alias for `hex_range_distances`.
        """
        return hex_range_distances(h, K)

    def h3_to_children(h, res=None):
        """
        Children of a hexagon.

        Parameters
        ----------
        h : H3Index
            H3Index is a `str` or `int`, depending on API.
        res : int or None, optional
            The resolution for the children.
            If `None`, then `res = resolution(h) + 1`

        Returns
        -------
        unordered collection of H3Index
            Collection type varies with API: `set`, `numpy.ndarray`, etc.
        """
        mv = _cy.children(_in_scalar(h), res)

        return _out_unordered(mv)

    # todo: nogil for expensive C operation?
    def compact(hexes):
        """
        Compact a collection of H3 cells by combining
        smaller cells into larger cells, if all child cells
        are present.

        todo: does compact work on mixed-resolution collections?

        Parameters
        ----------
        hexes : iterable of H3Index
            H3Index is a `str` or `int`, depending on API.

        Returns
        -------
        unordered collection of H3Index
            Collection type varies with API: `set`, `numpy.ndarray`, etc.
        """
        hu = _in_collection(hexes)
        hc = _cy.compact(hu)

        return _out_unordered(hc)

    def uncompact(hexes, res):
        """ Reverse the `compact` operation and return a collection
        of H3 cells, all of resolution `res`.

        what if uncompact input contains a hex samller than res?

        Parameters
        ----------
        hexes : iterable of H3Index
            H3Index is a `str` or `int`, depending on API.
        res : int
            Resolution of desired output cells.

        Returns
        -------
        unordered collection of H3Index
            Collection type varies with API: `set`, `numpy.ndarray`, etc.


        Raises
        ------
        todo: add test to make sure an error is returned when input
        contains hex smaller than output res.
        https://github.com/uber/h3/blob/master/src/h3lib/lib/h3Index.c#L425


        """
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
        Returns `True` if input is a valid H3 cell which is
        a pentagon.

        Parameters
        ----------
        h : H3Index
            H3Index is a `str` or `int`, depending on API.

        Returns
        -------
        bool

        Notes
        -----
        A pentagon should *also* pass `h3_is_cell()`.
        """
        return _cy.is_pentagon(_in_scalar(h))

    def h3_get_base_cell(h):
        """
        Return the parent cell, having resolution `0`.

        todo/question: overlap with the `get_parent()` function?

        Parameters
        ----------
        h : H3Index
            H3Index is a `str` or `int`, depending on API.

        Returns
        -------
        H3Index
        """
        return _cy.get_base_cell(_in_scalar(h))

    def h3_indexes_are_neighbors(h1, h2):
        """
        Returns true if `h1` and `h2` are neighboring cells.

        Parameters
        ----------
        h1 : H3Cell
        h2 : H3Cell
            H3Index is a `str` or `int`, depending on API.

        Returns
        -------
        bool
        """
        h1 = _in_scalar(h1)
        h2 = _in_scalar(h2)

        return _cy.are_neighbors(h1, h2)

    def get_h3_unidirectional_edge(origin, destination):
        """
        Return an H3 Index denoting the directed edge
        between neighboring cells `origin` and `destination`.

        Parameters
        ----------
        h1 : H3Index
            Must be an H3 cell.
        h2 : H3Index
            Must be an H3 cell.
            H3Index is a `str` or `int`, depending on API.

        Raises
        ------
        ValueError: when cells are not adjacent

        Returns
        -------
        H3Index
            Specifically, an H3 edge
        """
        o = _in_scalar(origin)
        d = _in_scalar(destination)
        e = _cy.edge(o, d)
        e = _out_scalar(e)

        return e

    def get_origin_h3_index_from_unidirectional_edge(e):
        """
        Origin cell from an H3 directed edge.

        Parameters
        ----------
        e : H3Index
            Must be an H3 edge.

        Returns
        -------
        H3Index
            Specifically, an H3 cell
        """
        e = _in_scalar(e)
        o = _cy.edge_origin(e)
        o = _out_scalar(o)

        return o

    def get_destination_h3_index_from_unidirectional_edge(e):
        """
        Destination cell from an H3 directed edge.

        Parameters
        ----------
        e : H3Index
            Must be an H3 edge.

        Returns
        -------
        H3Index
            Specifically, an H3 cell

        """
        e = _in_scalar(e)
        d = _cy.edge_destination(e)
        d = _out_scalar(d)

        return d

    def get_h3_indexes_from_unidirectional_edge(e):
        """
        Return (origin, destination) tuple from H3 directed edge

        Parameters
        ----------
        e : H3Index
            Must be an H3 edge.

        Returns
        -------
        H3Index
            Origin cell of edge
        H3Index
            Destination cell of edge
        """
        e = _in_scalar(e)
        o, d = _cy.edge_cells(e)
        o, d = _out_scalar(o), _out_scalar(d)

        return o, d

    def get_h3_unidirectional_edges_from_hexagon(origin):
        """
        Return all directed edges starting from `origin` cell.

        Parameters
        ----------
        origin : H3Cell

        Returns
        -------
        unordered collection of H3Edge
            Collection type varies with API: `set`, `numpy.ndarray`, etc.
        """
        mv = _cy.edges_from_cell(_in_scalar(origin))

        return _out_unordered(mv)

    def get_h3_unidirectional_edge_boundary(edge, geo_json=False):
        return _cy.edge_boundary(_in_scalar(edge), geo_json=geo_json)

    def h3_line(start, end):
        """
        Returns the ordered collection of cells denoting a
        minimum-length non-unique path between cells.

        Parameters
        ----------
        start : H3Cell
        end : H3Cell
            H3Cell is a `str` or `int`, depending on API.

        Returns
        -------
        ordered collection of H3Cell
            Starting with `start`, and ending with `end`.
            Collection type varies with API: `set`, `numpy.ndarray`, etc.
        """
        mv = _cy.line(_in_scalar(start), _in_scalar(end))

        return _out_ordered(mv)

    def h3_is_res_class_iii(h):
        return _cy.is_res_class_iii(_in_scalar(h))

    def h3_is_res_class_III(h):
        return _cy.is_res_class_iii(_in_scalar(h))

    _globals.update(locals())
