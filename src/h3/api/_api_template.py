"""
Module to DRY-up code which is repeated across API modules.

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


Definitions of collections
--------------------------
Collection types vary between APIs. We'll use the following terms:

unordered collection:
    Inputs and outputs are interpreted as *unordered* collections.
    Examples: `set`, `numpy.ndarray`.

ordered collection:
    Inputs and outputs are interpreted as *ordered* collections.
    Examples: `list`, `numpy.ndarray`.

Notes
--------------------
todo: how do we lint these functions and docstrings? it seems to currently
be skipped due to it being inside the `_api_functions` function.
"""

from .. import _cy
from .._polygon import Polygon


class _API_FUNCTIONS(object):
    def __init__(
        self,
        _in_scalar,
        _out_scalar,
        _in_collection,
        _out_unordered,
        _out_ordered,
    ):
        self._in_scalar = _in_scalar
        self._out_scalar = _out_scalar
        self._in_collection = _in_collection
        self._out_unordered = _out_unordered
        self._out_ordered = _out_ordered

    @staticmethod
    def versions():
        """
        Version numbers for the Python (wrapper) and C (wrapped) libraries.

        Versions are output as strings of the form ``'X.Y.Z'``.
        C and Python should match on ``X`` (major) and ``Y`` (minor),
        but may differ on ``Z`` (patch).

        Returns
        -------
        dict like ``{'c': 'X.Y.Z', 'python': 'A.B.C'}``
        """
        from .._version import __version__

        v = {
            'c': _cy.c_version(),
            'python': __version__,
        }

        return v

    @staticmethod
    def str_to_int(h):
        """
        Converts a hexadecimal string to an H3 64-bit integer index.

        Parameters
        ----------
        h : str
            Hexadecimal string like ``'89754e64993ffff'``

        Returns
        -------
        int
            Unsigned 64-bit integer
        """
        return _cy.str_to_int(h)

    @staticmethod
    def int_to_str(x):
        """
        Converts an H3 64-bit integer index to a hexadecimal string.

        Parameters
        ----------
        x : int
            Unsigned 64-bit integer

        Returns
        -------
        str
            Hexadecimal string like ``'89754e64993ffff'``
        """
        return _cy.int_to_str(x)

    @staticmethod
    def get_num_cells(res):
        """
        Return the total number of *cells* (hexagons and pentagons)
        for the given resolution.

        Returns
        -------
        int
        """
        return _cy.get_num_cells(res)

    @staticmethod
    def average_hexagon_area(res, unit='km^2'):
        """
        Return the average area of an H3 *hexagon*
        for the given resolution.

        This average *excludes* pentagons.

        Returns
        -------
        float
        """
        return _cy.average_hexagon_area(res, unit)

    @staticmethod
    def average_hexagon_edge_length(res, unit='km'):
        """
        Return the average *hexagon* edge length
        for the given resolution.

        This average *excludes* pentagons.

        Returns
        -------
        float
        """
        return _cy.average_hexagon_edge_length(res, unit)

    def is_valid_cell(self, h):
        """
        Validates an H3 cell (hexagon or pentagon).

        Returns
        -------
        bool
        """
        try:
            h = self._in_scalar(h)
            return _cy.is_valid_cell(h)
        except (ValueError, TypeError):
            return False

    def is_valid_directed_edge(self, edge):
        """
        Validates an H3 unidirectional edge.

        Returns
        -------
        bool
        """
        try:
            e = self._in_scalar(edge)
            return _cy.is_valid_directed_edge(e)
        except (ValueError, TypeError):
            return False

    def latlng_to_cell(self, lat, lng, res):
        """
        Return the cell containing the (lat, lng) point
        for a given resolution.

        Returns
        -------
        H3Cell

        """
        return self._out_scalar(_cy.latlng_to_cell(lat, lng, res))

    def cell_to_latlng(self, h):
        """
        Return the center point of an H3 cell as a lat/lng pair.

        Parameters
        ----------
        h : H3Cell

        Returns
        -------
        lat : float
            Latitude
        lng : float
            Longitude
        """
        return _cy.cell_to_latlng(self._in_scalar(h))

    def get_resolution(self, h):
        """
        Return the resolution of an H3 cell.

        Parameters
        ----------
        h : H3Cell

        Returns
        -------
        int
        """
        # todo: could also work for edges
        return _cy.get_resolution(self._in_scalar(h))

    def cell_to_parent(self, h, res=None):
        """
        Get the parent of a cell.

        Parameters
        ----------
        h : H3Cell
        res : int or None, optional
            The resolution for the parent
            If ``None``, then ``res = resolution(h) - 1``

        Returns
        -------
        H3Cell
        """
        h = self._in_scalar(h)
        p = _cy.cell_to_parent(h, res)
        p = self._out_scalar(p)

        return p

    def grid_distance(self, h1, h2):
        """
        Compute the H3 distance between two cells.

        The H3 distance is defined as the length of the shortest
        path between the cells in the graph formed by connecting
        adjacent cells.

        This function will raise an exception if the
        cells are too far apart to compute the distance.

        Parameters
        ----------
        h1 : H3Cell
        h2 : H3Cell

        Returns
        -------
        int
        """
        h1 = self._in_scalar(h1)
        h2 = self._in_scalar(h2)

        d = _cy.grid_distance(h1, h2)

        return d

    def cell_to_boundary(self, h, geo_json=False):
        """
        Return tuple of lat/lng pairs describing the cell boundary.

        Parameters
        ----------
        h : H3Cell
        geo_json : bool, optional
            If ``True``, return output in GeoJson format:
            lng/lat pairs (opposite order), and
            have the last pair be the same as the first.
            If ``False`` (default), return lat/lng pairs, with the last
            pair distinct from the first.

        Returns
        -------
        tuple of (float, float) tuples
        """
        return _cy.cell_to_boundary(self._in_scalar(h), geo_json)

    def grid_disk(self, h, k=1):
        """
        Return unordered set of cells with H3 distance ``<= k`` from ``h``.
        That is, the "filled-in" disk.

        Parameters
        ----------
        h : H3Cell
        k : int
            Size of disk.

        Returns
        -------
        unordered collection of H3Cell
        """
        mv = _cy.grid_disk(self._in_scalar(h), k)

        return self._out_unordered(mv)

    def grid_ring(self, h, k=1):
        """
        Return unordered set of cells with H3 distance ``== k`` from ``h``.
        That is, the "hollow" ring.

        Parameters
        ----------
        h : H3Cell
        k : int
            Size of ring.

        Returns
        -------
        unordered collection of H3Cell
        """
        mv = _cy.grid_ring(self._in_scalar(h), k)

        return self._out_unordered(mv)

    def cell_to_children(self, h, res=None):
        """
        Children of a cell.

        Parameters
        ----------
        h : H3Cell
        res : int or None, optional
            The resolution for the children.
            If ``None``, then ``res = resolution(h) + 1``

        Returns
        -------
        unordered collection of H3Cell
        """
        mv = _cy.cell_to_children(self._in_scalar(h), res)

        return self._out_unordered(mv)

    # todo: nogil for expensive C operation?
    def compact_cells(self, cells):
        """
        Compact a collection of H3 cells by combining
        smaller cells into larger cells, if all child cells
        are present.

        Parameters
        ----------
        cells : iterable of H3 Cells

        Returns
        -------
        unordered collection of H3Cell
        """
        # todo: does compact_cells work on mixed-resolution collections?
        hu = self._in_collection(cells)
        hc = _cy.compact_cells(hu)

        return self._out_unordered(hc)

    def uncompact_cells(self, cells, res):
        """
        Reverse the `compact_cells` operation.

        Return a collection of H3 cells, all of resolution ``res``.

        Parameters
        ----------
        cells : iterable of H3Cell
        res : int
            Resolution of desired output cells.

        Returns
        -------
        unordered collection of H3Cell

        Raises
        ------
        todo: add test to make sure an error is returned when input
        contains cell smaller than output res.
        https://github.com/uber/h3/blob/master/src/h3lib/lib/h3Index.c#L425
        """
        hc = self._in_collection(cells)
        hu = _cy.uncompact_cells(hc, res)

        return self._out_unordered(hu)

    def polygon_to_cells(self, polygon, res):
        """
        Return the set of H3 cells at a given resolution whose center points
        are contained within a `h3.Polygon`

        Parameters
        ----------
        Polygon : h3.Polygon
            A polygon described by an outer ring and optional holes

        res : int
            Resolution of the output cells

        Examples
        --------

        >>> poly = h3.Polygon(
        ...     [(37.68, -122.54), (37.68, -122.34), (37.82, -122.34),
        ...      (37.82, -122.54)],
        ... )
        >>> h3.polygon_to_cells(poly, 6)
        {'862830807ffffff',
         '862830827ffffff',
         '86283082fffffff',
         '862830877ffffff',
         '862830947ffffff',
         '862830957ffffff',
         '86283095fffffff'}
        """
        mv = _cy.polygon_to_cells(polygon.outer, res, holes=polygon.holes)

        return self._out_unordered(mv)

    # def polygons_to_cells(self, polygons, res):
    #     # todo: have to figure out how to concat memoryviews cleanly
    #     # or some other approach
    #     pass

    def cells_to_polygons(self, cells):
        """
        Return a list of h3.Polygon objects describing the area
        covered by a set of H3 cells.

        Parameters
        ----------
        cells : iterable of H3 cells

        Returns
        -------
        list[h3.Polygon]
            List of h3.Polygon objects

        Examples
        --------

        >>> cells = ['8428309ffffffff', '842830dffffffff']
        >>> h3.cells_to_polygons(cells)
        [<h3.Polygon |outer|=10, |holes|=()>]

        """
        cells = self._in_collection(cells)
        geos = _cy.cells_to_multi_polygon(cells)

        polys = [Polygon(*geo) for geo in geos]

        return polys

    def is_pentagon(self, h):
        """
        Identify if an H3 cell is a pentagon.

        Parameters
        ----------
        h : H3Index

        Returns
        -------
        bool
            ``True`` if input is a valid H3 cell which is a pentagon.

        Notes
        -----
        A pentagon should *also* pass ``is_valid_cell()``.
        Will return ``False`` for valid H3Edge.
        """
        return _cy.is_pentagon(self._in_scalar(h))

    def get_base_cell_number(self, h):
        """
        Return the base cell *number* (``0`` to ``121``) of the given cell.

        The base cell *number* and the H3Index are two different representations
        of the same cell: the parent cell of resolution ``0``.

        The base cell *number* is encoded within the corresponding
        H3Index.

        todo: could work with edges

        Parameters
        ----------
        h : H3Cell

        Returns
        -------
        int
        """
        return _cy.get_base_cell_number(self._in_scalar(h))

    def are_neighbor_cells(self, h1, h2):
        """
        Returns ``True`` if ``h1`` and ``h2`` are neighboring cells.

        Parameters
        ----------
        h1 : H3Cell
        h2 : H3Cell

        Returns
        -------
        bool
        """
        h1 = self._in_scalar(h1)
        h2 = self._in_scalar(h2)

        return _cy.are_neighbor_cells(h1, h2)

    def cells_to_directed_edge(self, origin, destination):
        """
        Create an H3 Index denoting a unidirectional edge.

        The edge is constructed from neighboring cells ``origin`` and
        ``destination``.

        Parameters
        ----------
        origin : H3Cell
        destination : H3Cell

        Raises
        ------
        ValueError
            When cells are not adjacent.

        Returns
        -------
        H3Edge
        """
        o = self._in_scalar(origin)
        d = self._in_scalar(destination)
        e = _cy.cells_to_directed_edge(o, d)
        e = self._out_scalar(e)

        return e

    def get_directed_edge_origin(self, e):
        """
        Origin cell from an H3 directed edge.

        Parameters
        ----------
        e : H3Edge

        Returns
        -------
        H3Cell
        """
        e = self._in_scalar(e)
        o = _cy.get_directed_edge_origin(e)
        o = self._out_scalar(o)

        return o

    def get_directed_edge_destination(self, e):
        """
        Destination cell from an H3 directed edge.

        Parameters
        ----------
        e : H3Edge

        Returns
        -------
        H3Cell
        """
        e = self._in_scalar(e)
        d = _cy.get_directed_edge_destination(e)
        d = self._out_scalar(d)

        return d

    def directed_edge_to_cells(self, e):
        """
        Return (origin, destination) tuple from H3 directed edge

        Parameters
        ----------
        e : H3Edge

        Returns
        -------
        H3Cell
            Origin cell of edge
        H3Cell
            Destination cell of edge
        """
        e = self._in_scalar(e)
        o, d = _cy.directed_edge_to_cells(e)
        o, d = self._out_scalar(o), self._out_scalar(d)

        return o, d

    def origin_to_directed_edges(self, origin):
        """
        Return all directed edges starting from ``origin`` cell.

        Parameters
        ----------
        origin : H3Cell

        Returns
        -------
        unordered collection of H3Edge
        """
        mv = _cy.origin_to_directed_edges(self._in_scalar(origin))

        return self._out_unordered(mv)

    def directed_edge_to_boundary(self, edge, geo_json=False):
        return _cy.directed_edge_to_boundary(self._in_scalar(edge), geo_json=geo_json)

    def grid_path_cells(self, start, end):
        """
        Returns the ordered collection of cells denoting a
        minimum-length non-unique path between cells.

        Parameters
        ----------
        start : H3Cell
        end : H3Cell

        Returns
        -------
        ordered collection of H3Cell
            Starting with ``start``, and ending with ``end``.
        """
        mv = _cy.grid_path_cells(self._in_scalar(start), self._in_scalar(end))

        return self._out_ordered(mv)

    def is_res_class_III(self, h):
        """
        Determine if cell has orientation "Class II" or "Class III".

        The orientation of pentagons/hexagons on the icosahedron can be one
        of two types: "Class II" or "Class III".

        All cells within a resolution have the same type, and the type
        alternates between resolutions.

        "Class II" cells have resolutions:  0,2,4,6,8,10,12,14
        "Class III" cells have resolutions: 1,3,5,7,9,11,13,15

        Parameters
        ----------
        h : H3Cell

        Returns
        -------
        bool
            ``True`` if ``h`` is "Class III".
            ``False`` if ``h`` is "Class II".

        References
        ----------
        1. https://uber.github.io/h3/#/documentation/core-library/coordinate-systems
        """
        return _cy.is_res_class_iii(self._in_scalar(h))

    def get_pentagons(self, res):
        """
        Return all pentagons at a given resolution.

        Parameters
        ----------
        res : int
            Resolution of the pentagons

        Returns
        -------
        unordered collection of H3Cell
        """
        mv = _cy.get_pentagons(res)

        return self._out_unordered(mv)

    def get_res0_cells(self):
        """
        Return all cells at resolution 0.

        Parameters
        ----------
        None

        Returns
        -------
        unordered collection of H3Cell
        """
        mv = _cy.get_res0_cells()

        return self._out_unordered(mv)

    def cell_to_center_child(self, h, res=None):
        """
        Get the center child of a cell at some finer resolution.

        Parameters
        ----------
        h : H3Cell
        res : int or None, optional
            The resolution for the child cell
            If ``None``, then ``res = resolution(h) + 1``

        Returns
        -------
        H3Cell
        """
        h = self._in_scalar(h)
        p = _cy.cell_to_center_child(h, res)
        p = self._out_scalar(p)

        return p

    def get_icosahedron_faces(self, h):
        """
        Return icosahedron faces intersecting a given H3 cell.

        There are twenty possible faces, ranging from 0--19.

        Note: Every interface returns a Python ``set`` of ``int``.

        Parameters
        ----------
        h : H3Cell

        Returns
        -------
        Python ``set`` of ``int``
        """
        h = self._in_scalar(h)
        faces = _cy.get_icosahedron_faces(h)

        return faces

    def cell_to_local_ij(self, origin, h):
        """
        Return local (i,j) coordinates of cell ``h`` in relation to ``origin`` cell


        Parameters
        ----------
        origin : H3Cell
            Origin/central cell for defining i,j coordinates.
        h: H3Cell
            Destination cell whose i,j coordinates we'd like, based off
            of the origin cell.


        Returns
        -------
        Tuple (i, j) of integer local coordinates of cell ``h``


        Notes
        -----

        The ``origin`` cell does not define (0, 0) for the IJ coordinate space.
        (0, 0) refers to the center of the base cell containing origin at the
        resolution of `origin`.
        Subtracting the IJ coordinates of ``origin`` from every cell would get
        you the property of (0, 0) being the ``origin``.

        This is done so we don't need to keep recomputing the coordinates of
        ``origin`` if not needed.
        """
        origin = self._in_scalar(origin)
        h = self._in_scalar(h)

        i, j = _cy.cell_to_local_ij(origin, h)

        return i, j

    def local_ij_to_cell(self, origin, i, j):
        """
        Return cell at local (i,j) position relative to the ``origin`` cell.

        Parameters
        ----------
        origin : H3Cell
            Origin/central cell for defining i,j coordinates.
        i, j: int
            Integer coordinates with respect to ``origin`` cell.


        Returns
        -------
        H3Cell at local (i,j) position relative to the ``origin`` cell


        Notes
        -----

        The ``origin`` cell does not define (0, 0) for the IJ coordinate space.
        (0, 0) refers to the center of the base cell containing origin at the
        resolution of ``origin``.
        Subtracting the IJ coordinates of ``origin`` from every cell would get
        you the property of (0, 0) being the ``origin``.

        This is done so we don't need to keep recomputing the coordinates of
        ``origin`` if not needed.
        """
        origin = self._in_scalar(origin)

        h = _cy.local_ij_to_cell(origin, i, j)
        h = self._out_scalar(h)

        return h

    def cell_area(self, h, unit='km^2'):
        """
        Compute the spherical surface area of a specific H3 cell.

        Parameters
        ----------
        h : H3Cell
        unit: str
            Unit for area result (``'km^2'``, 'm^2', or 'rads^2')


        Returns
        -------
        The area of the H3 cell in the given units


        Notes
        -----
        This function breaks the cell into spherical triangles, and computes
        their spherical area.
        The function uses the spherical distance calculation given by
        `great_circle_distance`.
        """
        h = self._in_scalar(h)

        return _cy.cell_area(h, unit=unit)

    def edge_length(self, e, unit='km'):
        """
        Compute the spherical length of a specific H3 edge.

        Parameters
        ----------
        h : H3Cell
        unit: str
            Unit for length result ('km', 'm', or 'rads')


        Returns
        -------
        The length of the edge in the given units


        Notes
        -----
        This function uses the spherical distance calculation given by
        `great_circle_distance`.
        """
        e = self._in_scalar(e)

        return _cy.edge_length(e, unit=unit)

    @staticmethod
    def great_circle_distance(latlng1, latlng2, unit='km'):
        """
        Compute the spherical distance between two (lat, lng) points.
        AKA: great circle distance or "haversine" distance.

        todo: overload to allow two cell inputs?

        Parameters
        ----------
        latlng1 : tuple
            (lat, lng) tuple in degrees
        latlng2 : tuple
            (lat, lng) tuple in degrees
        unit: str
            Unit for distance result ('km', 'm', or 'rads')


        Returns
        -------
        The spherical distance between the points in the given units
        """
        lat1, lng1 = latlng1
        lat2, lng2 = latlng2
        return _cy.great_circle_distance(
            lat1, lng1,
            lat2, lng2,
            unit = unit
        )
