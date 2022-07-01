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

# todo: make note that these exceptions are only for the ones returned from C lib. how to ensure/enforce/guarantee?
#
# todo: separate file for the hierarchy of errors? separate them from the helper functions? nice, short file to define all the errors!
#
# should the internal nodes be ABC classes? separate what is actually raised from the possible grouping exceptions?
#
# "This file defines *all* custom h3-py errors."
#
# Move the helpers to util! (move -> banish?)
#
# Control where `E_*` can appear in the lib, and where `H3*Error` can appear. very limited!

from contextlib import contextmanager

from .h3lib cimport (
    H3Error,

    # H3ErrorCodes enum values
    E_SUCCESS,
    E_FAILED,
    E_DOMAIN,
    E_LATLNG_DOMAIN,
    E_RES_DOMAIN,
    E_CELL_INVALID,
    E_DIR_EDGE_INVALID,
    E_UNDIR_EDGE_INVALID,
    E_VERTEX_INVALID,
    E_PENTAGON,
    E_DUPLICATE_INPUT,
    E_NOT_NEIGHBORS,
    E_RES_MISMATCH,
    E_MEMORY,
    E_MEMORY_BOUNDS,
    E_OPTION_INVALID,
)


@contextmanager
def this_error_as_e(obj):
    """
    Syntactic maple syrup for grouping exception definitions.

    I.e., pretend scope.
    (This doesn't actually do anything context-manager-y.)
    """
    yield obj


class H3Exception(Exception):
    h3_error_code = None


with this_error_as_e(H3Exception) as e:
    class H3ValueError(e, ValueError): ...
    class H3MemoryError(e, MemoryError): ...
    class H3GridNavigationError(e, RuntimeError): ...
    class H3UnrecognizedException(e): ...  ## Note: Should never happen

    class H3FailedError(e):
        h3_error_code = E_FAILED


with this_error_as_e(H3GridNavigationError) as e:
    class H3PentagonError(e):
        h3_error_code = E_PENTAGON


with this_error_as_e(H3MemoryError) as e:
    class H3MemoryAllocError(e):
        h3_error_code = E_MEMORY

    class H3MemoryBoundsError(e):
        h3_error_code = E_MEMORY_BOUNDS


with this_error_as_e(H3ValueError) as e:
    class H3DomainError(e):
        h3_error_code = E_DOMAIN

    class H3LatLngDomainError(e):
        h3_error_code = E_LATLNG_DOMAIN

    class H3ResDomainError(e):
        h3_error_code = E_RES_DOMAIN

    class H3CellInvalidError(e):
        h3_error_code = E_CELL_INVALID

    class H3DirEdgeInvalidError(e):
        h3_error_code = E_DIR_EDGE_INVALID

    class H3UndirEdgeInvalidError(e):
        h3_error_code = E_UNDIR_EDGE_INVALID

    class H3VertexInvalidError(e):
        h3_error_code = E_VERTEX_INVALID

    class H3DuplicateInputError(e):
        h3_error_code = E_DUPLICATE_INPUT

    class H3NotNeighborsError(e):
        h3_error_code = E_NOT_NEIGHBORS

    class H3ResMismatchError(e):
        h3_error_code = E_RES_MISMATCH

    class H3OptionInvalidError(e):
        h3_error_code = E_OPTION_INVALID


error_dict = {
    # E_SUCCESS:           None,
    E_FAILED:              H3FailedError,
    E_DOMAIN:              H3DomainError,
    E_LATLNG_DOMAIN:       H3LatLngDomainError,
    E_RES_DOMAIN:          H3ResDomainError,
    E_CELL_INVALID:        H3CellInvalidError,
    E_DIR_EDGE_INVALID:    H3DirEdgeInvalidError,
    E_UNDIR_EDGE_INVALID:  H3UndirEdgeInvalidError,
    E_VERTEX_INVALID:      H3VertexInvalidError,
    E_PENTAGON:            H3PentagonError,
    E_DUPLICATE_INPUT:     H3DuplicateInputError,
    E_NOT_NEIGHBORS:       H3NotNeighborsError,
    E_RES_MISMATCH:        H3ResMismatchError,
    E_MEMORY:              H3MemoryAllocError,
    E_MEMORY_BOUNDS:       H3MemoryBoundsError,
    E_OPTION_INVALID:      H3OptionInvalidError,
}


cpdef code_to_exception(H3Error err):
    if err == E_SUCCESS:
        return None
    else:
        ex = error_dict.get(err, H3UnrecognizedException)
        return ex


cdef check_for_error(H3Error err):
    """
    todo: more descriptive message
    todo: add error codes as property
    todo: allow passing in extra args for the error message?
    """

    ex = code_to_exception(err)

    if ex is None:
        pass
    elif ex == H3UnrecognizedException:
        # pass along the C error code
        # todo: add a test
        raise H3UnrecognizedException(err)
    else:
        raise ex


cdef raise_with_msg(H3Error err, str msg):
    ex = code_to_exception(err)

    if ex is None:
        pass
    elif ex == H3UnrecognizedException:
        msg = 'Code: {}, msg: {}'.format(err, msg)
        raise H3UnrecognizedException(msg)
    else:
        raise ex(msg)
