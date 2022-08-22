class Polygon:
    """ Container for loops of lat/lng points describing a polygon
    """
    def __init__(self, outer, *holes):
        self.outer = outer
        self.holes = holes

    def __repr__(self):
        s = '<h3.Polygon |outer|={}, |holes|={}>'.format(
            len(self.outer),
            tuple(map(len, self.holes)),
        )

        return s
