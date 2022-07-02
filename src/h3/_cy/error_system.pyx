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
def the_error(obj):
    """
    Syntactic maple syrup for grouping exception definitions.

    I.e., pretend scope.
    (This doesn't actually do anything context-manager-y.)
    """
    yield obj

# H3ErrorCodeBaseException
class H3Exception(Exception):
    """ Base H3 exception class.

    Concrete subclasses of this class correspond to specific
    error codes from the C library.
    """
    h3_error_code = None

# A few more base exceptions; organizational.
with the_error(H3Exception) as e:
    class H3ValueError(e, ValueError): ...
    class H3MemoryError(e, MemoryError): ...
    class H3GridNavigationError(e, RuntimeError): ...


# Concrete exceptions
with the_error(H3Exception) as e:
    class H3FailedError(e): ...

# Concrete exceptions
with the_error(H3GridNavigationError) as e:
    class H3PentagonError(e): ...

# Concrete exceptions
with the_error(H3MemoryError) as e:
    class H3MemoryAllocError(e): ...
    class H3MemoryBoundsError(e): ...

# Concrete exceptions
with the_error(H3ValueError) as e:
    class H3DomainError(e): ...
    class H3LatLngDomainError(e): ...
    class H3ResDomainError(e): ...
    class H3CellInvalidError(e): ...
    class H3DirEdgeInvalidError(e): ...
    class H3UndirEdgeInvalidError(e): ...
    class H3VertexInvalidError(e): ...
    class H3DuplicateInputError(e): ...
    class H3NotNeighborsError(e): ...
    class H3ResMismatchError(e): ...
    class H3OptionInvalidError(e): ...

# class UnknownH3ErrorCode
class UnrecognizedH3ErrorCode(Exception):
    """
    Indicates that the h3-py Python bindings have received an
    unrecognized error code from the C library.

    This should never happen. Please report if you get this error.

    Note that this exception is *outside* of the H3Exception class hierarchy.
    """
    ...

"""
Map C int error code to h3-py concrete exception
We intentionally omit E_SUCCESS.
"""
error_dict = {
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

# Each concrete exception stores its associated error code
for code, ex in error_dict.items():
    ex.h3_error_code = code


cdef code_to_exception(H3Error err):
    if err == E_SUCCESS:
        return None
    elif err in error_dict:
        return error_dict[err]
    else:
        raise UnrecognizedH3ErrorCode(err)


SENTINEL_VAL = '__h3-py_sentinel__'
cdef check_for_error(H3Error err, str msg=SENTINEL_VAL):
    ex = code_to_exception(err)

    if ex:
        if msg == SENTINEL_VAL:
            raise ex
        else:
            raise ex(msg)
