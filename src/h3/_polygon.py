class H3Poly:
    """
    Container for loops of lat/lng points describing a polygon.

    Attributes
    ----------
    outer : list[tuple[float, float]]
        List of lat/lng points describing the outer loop of the polygon

    holes : list[list[tuple[float, float]]]
        List of loops of lat/lng points describing the holes of the polygon

    Examples
    --------

    A polygon with a single outer ring consisting of 4 points, having no holes:

    >>> H3Poly(
    ...     [(37.68, -122.54), (37.68, -122.34), (37.82, -122.34), (37.82, -122.54)],
    ... )
    <H3Poly |outer|=4, |holes|=()>

    The same polygon, but with one hole consisting of 3 points:

    >>> H3Poly(
    ...     [(37.68, -122.54), (37.68, -122.34), (37.82, -122.34), (37.82, -122.54)],
    ...     [(37.76, -122.51), (37.76, -122.44), (37.81, -122.51)],
    ... )
    <H3Poly |outer|=4, |holes|=(3,)>

    The same as above, but with one additional hole, made up of 5 points:

    >>> H3Poly(
    ...     [(37.68, -122.54), (37.68, -122.34), (37.82, -122.34), (37.82, -122.54)],
    ...     [(37.76, -122.51), (37.76, -122.44), (37.81, -122.51)],
    ...     [(37.71, -122.43), (37.71, -122.37), (37.73, -122.37), (37.75, -122.41),
    ...      (37.73, -122.43)],
    ... )
    <H3Poly |outer|=4, |holes|=(3, 5)>

    Notes
    -----

    - TODO: Add GeoJSON translation support.
    """
    def __init__(self, outer, *holes):
        self.outer = outer
        self.holes = holes

        # todo: maybe add some validation

    def __repr__(self):
        s = '<H3Poly |outer|={}, |holes|={}>'.format(
            len(self.outer),
            tuple(map(len, self.holes)),
        )

        return s


class H3MultiPoly:
    def __init__(self, *polys):
        self.polys = tuple(polys)

    def __repr__(self):
        return 'H3MultiPoly' + str(self.polys)
