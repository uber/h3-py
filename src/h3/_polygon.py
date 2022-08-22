class Polygon:
    """ Container for loops of lat/lng points describing a polygon
    """
    def __init__(self, outer, *holes):
        self.outer = outer
        self.holes = holes
