# flake8: noqa

from .api.basic_str import *
from ._version import __version__

#todo: remove in 4.0; only here for backward compatibility
from .api import basic_str as h3


from ._cy import (
    H3BaseException,
    UnknownH3ErrorCode,
    H3FailedError,
    H3DomainError,
    H3LatLngDomainError,
    H3ResDomainError,
    H3CellInvalidError,
    H3DirEdgeInvalidError,
    H3UndirEdgeInvalidError,
    H3VertexInvalidError,
    H3PentagonError,
    H3DuplicateInputError,
    H3NotNeighborsError,
    H3ResMismatchError,
    H3MemoryAllocError,
    H3MemoryBoundsError,
    H3OptionInvalidError,
)
