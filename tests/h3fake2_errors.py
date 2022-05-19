# flake8: noqa
"""
Some of the tests expect to catch certain errors.
As we transition, we'll have errors of each type.
pytest functions can accept tuples of errors to check for either one.
"""

import h3
import h3fake2

H3ValueError      = (h3.H3ValueError,      h3fake2.H3ValueError)
H3CellError       = (h3.H3CellError,       h3fake2.H3CellError)
H3ResolutionError = (h3.H3ResolutionError, h3fake2.H3ResolutionError)
H3EdgeError       = (h3.H3EdgeError,       h3fake2.H3EdgeError)
H3DistanceError   = (h3.H3DistanceError,   h3fake2.H3DistanceError)
