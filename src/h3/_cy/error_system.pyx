"""
todo: use module docs to describe new error system

- less aggressive correctness checking for indices
- hierarchy?
- error codes from C
"""

from .h3lib cimport H3ErrorCodes, H3Error

# todo: do we want valueerror hierarchy or memory error from Python?

class H3Exception(Exception):
    h3_error_code = None

class H3UnrecognizedException(H3Exception):
    h3_error_code = None


class H3FailedError(H3Exception):
    h3_error_code = H3ErrorCodes.E_FAILED

class H3DomainError(H3Exception):
    h3_error_code = H3ErrorCodes.E_DOMAIN

class H3LatLngDomainError(H3Exception):
    h3_error_code = H3ErrorCodes.E_LATLNG_DOMAIN

class H3ResDomainError(H3Exception):
    h3_error_code = H3ErrorCodes.E_RES_DOMAIN

class H3CellInvalidError(H3Exception):
    h3_error_code = H3ErrorCodes.E_CELL_INVALID

class H3DirEdgeInvalidError(H3Exception):
    h3_error_code = H3ErrorCodes.E_DIR_EDGE_INVALID

class H3UndirEdgeInvalidError(H3Exception):
    h3_error_code = H3ErrorCodes.E_UNDIR_EDGE_INVALID

class H3VertexInvalidError(H3Exception):
    h3_error_code = H3ErrorCodes.E_VERTEX_INVALID

class H3PentagonError(H3Exception):
    h3_error_code = H3ErrorCodes.E_PENTAGON

class H3DuplicateInputError(H3Exception):
    h3_error_code = H3ErrorCodes.E_DUPLICATE_INPUT

class H3NotNeighborsError(H3Exception):
    h3_error_code = H3ErrorCodes.E_NOT_NEIGHBORS

class H3ResMismatchError(H3Exception):
    h3_error_code = H3ErrorCodes.E_RES_MISMATCH

class H3MemoryAllocError(H3Exception):
    h3_error_code = H3ErrorCodes.E_MEMORY

class H3MemoryBoundsError(H3Exception):
    h3_error_code = H3ErrorCodes.E_MEMORY_BOUNDS

class H3OptionInvalidError(H3Exception):
    h3_error_code = H3ErrorCodes.E_OPTION_INVALID


# todo: remove these
class H3ValueError(H3Exception, ValueError):
    pass

class H3DistanceError(H3ValueError):
    pass

error_dict = {
    H3ErrorCodes.E_SUCCESS: None,
    H3ErrorCodes.E_FAILED:              H3Exception,
    H3ErrorCodes.E_DOMAIN:              H3ValueError,
    H3ErrorCodes.E_LATLNG_DOMAIN:       H3ValueError,
    H3ErrorCodes.E_RES_DOMAIN:          H3ResDomainError,
    H3ErrorCodes.E_CELL_INVALID:        H3CellInvalidError,
    H3ErrorCodes.E_DIR_EDGE_INVALID:    H3DirEdgeInvalidError,
    H3ErrorCodes.E_UNDIR_EDGE_INVALID:  H3UndirEdgeInvalidError,
    H3ErrorCodes.E_VERTEX_INVALID:      H3ValueError,
    H3ErrorCodes.E_PENTAGON:            H3ValueError,
    H3ErrorCodes.E_DUPLICATE_INPUT:     H3ValueError,
    H3ErrorCodes.E_NOT_NEIGHBORS:       H3ValueError,
    H3ErrorCodes.E_RES_MISMATCH:        H3ResMismatchError,
    H3ErrorCodes.E_MEMORY:              H3Exception,
    H3ErrorCodes.E_MEMORY_BOUNDS:       H3Exception,
    H3ErrorCodes.E_OPTION_INVALID:      H3Exception,
}


cpdef code_to_exception(H3Error err):
    ex = error_dict.get(err, H3UnrecognizedException)

    return ex


cdef check_for_error(H3Error err):
    """
    todo: more descriptive message
    todo: add error codes as property
    todo: allow passing in extra args for the error message?
    """

    ex = code_to_exception(err)

    if ex:
        raise ex
