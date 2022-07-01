"""
todo: use module docs to describe new error system

- less aggressive correctness checking for indices
- hierarchy?
- error codes from C
"""

'''
Idea: Use normal Python exceptions whenever possible.
Only use these H3 exceptions to refer to H3Error output from the C library.
Would it then follow that these should only appear from the check_for_error function?


Philosophy question: should we aggressively check input values for the user? or assume
they know what they're doing (as long as we don't allow a segfault)?
Maybe the main Python lib checks aggressively, but we expose the Cython
functions if they want to get risky?

can we use a factory pattern to simplify the creation of these errors?
'''

from .h3lib cimport H3ErrorCodes, H3Error

# todo: do we want value error hierarchy or memory error from Python?

class H3Exception(Exception):
    h3_error_code = None

class H3UnrecognizedException(H3Exception):
    h3_error_code = None


# class H3Success(H3Exception):
#     h3_error_code = H3ErrorCodes.E_SUCCESS

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


error_dict = {
    # H3ErrorCodes.E_SUCCESS:             None,
    H3ErrorCodes.E_FAILED:              H3FailedError,
    H3ErrorCodes.E_DOMAIN:              H3DomainError,
    H3ErrorCodes.E_LATLNG_DOMAIN:       H3LatLngDomainError,
    H3ErrorCodes.E_RES_DOMAIN:          H3ResDomainError,
    H3ErrorCodes.E_CELL_INVALID:        H3CellInvalidError,
    H3ErrorCodes.E_DIR_EDGE_INVALID:    H3DirEdgeInvalidError,
    H3ErrorCodes.E_UNDIR_EDGE_INVALID:  H3UndirEdgeInvalidError,
    H3ErrorCodes.E_VERTEX_INVALID:      H3VertexInvalidError,
    H3ErrorCodes.E_PENTAGON:            H3PentagonError,
    H3ErrorCodes.E_DUPLICATE_INPUT:     H3DuplicateInputError,
    H3ErrorCodes.E_NOT_NEIGHBORS:       H3NotNeighborsError,
    H3ErrorCodes.E_RES_MISMATCH:        H3ResMismatchError,
    H3ErrorCodes.E_MEMORY:              H3MemoryAllocError,
    H3ErrorCodes.E_MEMORY_BOUNDS:       H3MemoryBoundsError,
    H3ErrorCodes.E_OPTION_INVALID:      H3OptionInvalidError,
}


cpdef code_to_exception(H3Error err):
    if err == H3ErrorCodes.E_SUCCESS:
        return None

    ex = error_dict.get(err, H3UnrecognizedException)

    return ex


# todo: rename to `raise_if_error`
cdef check_for_error(H3Error err):
    """
    todo: more descriptive message
    todo: add error codes as property
    todo: allow passing in extra args for the error message?
    """

    ex = code_to_exception(err)

    # pass along the C error code
    # todo: add a test
    if ex == H3UnrecognizedException:
        ex = H3UnrecognizedException(err)

    if ex:
        raise ex
