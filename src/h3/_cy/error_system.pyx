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
from contextlib import contextmanager

from .h3lib cimport H3ErrorCodes as ec
from .h3lib cimport H3Error


@contextmanager
def err_block(obj):
    'Syntactic maple syrup for grouping exception definitions. (pretend scope)'
    yield obj


class H3Exception(Exception):
    h3_error_code = None


with err_block(H3Exception) as e:
    class H3ValueError(e, ValueError): ...
    class H3MemoryError(e, MemoryError): ...
    class H3UnrecognizedException(e): ...

    class H3FailedError(e):
        h3_error_code = ec.E_FAILED

    class H3PentagonError(e):
        # todo: more-specific error type here?
        h3_error_code = ec.E_PENTAGON



with err_block(H3MemoryError) as e:
    class H3MemoryAllocError(e):
        h3_error_code = ec.E_MEMORY

    class H3MemoryBoundsError(e):
        h3_error_code = ec.E_MEMORY_BOUNDS



with err_block(H3ValueError) as e:
    class H3DomainError(e):
        h3_error_code = ec.E_DOMAIN

    class H3LatLngDomainError(e):
        h3_error_code = ec.E_LATLNG_DOMAIN

    class H3ResDomainError(e):
        h3_error_code = ec.E_RES_DOMAIN

    class H3CellInvalidError(e):
        h3_error_code = ec.E_CELL_INVALID

    class H3DirEdgeInvalidError(e):
        h3_error_code = ec.E_DIR_EDGE_INVALID

    class H3UndirEdgeInvalidError(e):
        h3_error_code = ec.E_UNDIR_EDGE_INVALID

    class H3VertexInvalidError(e):
        h3_error_code = ec.E_VERTEX_INVALID

    class H3DuplicateInputError(e):
        h3_error_code = ec.E_DUPLICATE_INPUT

    class H3NotNeighborsError(e):
        h3_error_code = ec.E_NOT_NEIGHBORS

    class H3ResMismatchError(e):
        h3_error_code = ec.E_RES_MISMATCH

    class H3OptionInvalidError(e):
        h3_error_code = ec.E_OPTION_INVALID


error_dict = {
    # ec.E_SUCCESS:           None,
    ec.E_FAILED:              H3FailedError,
    ec.E_DOMAIN:              H3DomainError,
    ec.E_LATLNG_DOMAIN:       H3LatLngDomainError,
    ec.E_RES_DOMAIN:          H3ResDomainError,
    ec.E_CELL_INVALID:        H3CellInvalidError,
    ec.E_DIR_EDGE_INVALID:    H3DirEdgeInvalidError,
    ec.E_UNDIR_EDGE_INVALID:  H3UndirEdgeInvalidError,
    ec.E_VERTEX_INVALID:      H3VertexInvalidError,
    ec.E_PENTAGON:            H3PentagonError,
    ec.E_DUPLICATE_INPUT:     H3DuplicateInputError,
    ec.E_NOT_NEIGHBORS:       H3NotNeighborsError,
    ec.E_RES_MISMATCH:        H3ResMismatchError,
    ec.E_MEMORY:              H3MemoryAllocError,
    ec.E_MEMORY_BOUNDS:       H3MemoryBoundsError,
    ec.E_OPTION_INVALID:      H3OptionInvalidError,
}


cpdef code_to_exception(H3Error err):
    if err == ec.E_SUCCESS:
        return None

    ex = error_dict.get(err, H3UnrecognizedException)

    return ex


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
