"""
Exceptions from the h3-py library have three possible sources:

- the Python code
- the Cython code
- the underlying H3 C library code

The Python and Cython h3-py code will only raise standard Python
built-in exceptions; no custom exception classes will be used.

On the other hand, many functions in the H3 C library return a `uint32_t`
error code (aliased as type `H3Error`).
The Python/Cython code will pass along these errors if they occur (but can't be
recovered from), and convert them from `uint32_t` values to custom Python
exception types.
These custom exception classes all inherit from `H3BaseException`.

There is a 1-1 correspondence between the concrete subclasses of
`H3BaseException` and the H3 C library `H3ErrorCodes` values.
Thus, the user can refer to the C library documentation on these errors.

The (`uint32_t` <-> Exception) correspondence should be clear from the names
of each, but the explicit mapping is given by a dictionary in the code below.

Note that some "abstract" subclasses of `H3BaseException` are also included to
group the exceptions by type. (We say "abstract" because Python has no easy
way to make true abstract exception classes.)
These "abstract" exceptions will never be raised directly by h3-py, but they
allow the user to catch general groups of errors.

Summarizing, all exceptions originating from the C library inherit from
`H3BaseException`, which has both "abstract" and "concrete" subclasses.

**Abstract classes**:

- H3BaseException
- H3ValueError
- H3MemoryError
- H3GridNavigationError

**Concrete classes**:

- H3FailedError
- H3DomainError
- H3LatLngDomainError
- H3ResDomainError
- H3CellInvalidError
- H3DirEdgeInvalidError
- H3UndirEdgeInvalidError
- H3VertexInvalidError
- H3PentagonError
- H3DuplicateInputError
- H3NotNeighborsError
- H3ResMismatchError
- H3MemoryAllocError
- H3MemoryBoundsError
- H3OptionInvalidError


# TODO: add tests verifying that concrete exception classes have the right error codes associated with them
"""

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
    Syntactic maple syrup for grouping exception definitions, in the
    form of a `with` statement that ends up as a not-half-bad
    approximation of a valid sentence fragment.

    Sort of a pretend scope, in that it allows for block indentation to
    visually indicate the scoping of the `... as e`, even though Python
    doesn't treat it as a "true" block scope.

    Note that this doesn't actually do anything context-manager-y, outside
    of the variable assignment and block indentation.
    """
    yield obj


#
# Base exception for C library error codes
#
class H3BaseException(Exception):
    """ Base H3 exception class.

    Concrete subclasses of this class correspond to specific
    error codes from the C library.

    Base/abstract subclasses will have `h3_error_code = None`, while
    concrete subclasses will have `h3_error_code` equal to their associated
    C library error code.
    """
    h3_error_code = None


#
# A few more abstract exceptions; organizational.
#
with the_error(H3BaseException) as e:
    class H3ValueError(e, ValueError): ...
    class H3MemoryError(e, MemoryError): ...
    class H3GridNavigationError(e, RuntimeError): ...


#
# Concrete exceptions
#
with the_error(H3BaseException) as e:
    class H3FailedError(e): ...

with the_error(H3GridNavigationError) as e:
    class H3PentagonError(e): ...

with the_error(H3MemoryError) as e:
    class H3MemoryAllocError(e): ...
    class H3MemoryBoundsError(e): ...

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


#
# Something that should never happen
#
class UnknownH3ErrorCode(Exception):
    """
    Indicates that the h3-py Python bindings have received an
    unrecognized error code from the C library.

    This should never happen. Please report if you get this error.

    Note that this exception is *outside* of the
    H3BaseException class hierarchy.
    """
    pass


"""
This defines a mapping between uint32_t error codes and concrete Python
exception classes.
Note that we intentionally omit E_SUCCESS, as it is not an actual error.
"""
error_mapping = {
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

# Go back and modify the class definitions so that each concrete exception
# stores its associated error code.
for code, ex in error_mapping.items():
    ex.h3_error_code = code


#
# Helper functions
#

# TODO: Move the helpers to util?
# TODO: Unclear how/where to expose these functions. cdef/cpdef?

cdef code_to_exception(H3Error err):
    if err == E_SUCCESS:
        return None
    elif err in error_mapping:
        return error_mapping[err]
    else:
        raise UnknownH3ErrorCode(err)

cdef check_for_error(H3Error err):
    ex = code_to_exception(err)
    if ex:
        raise ex

cdef check_for_error_msg(H3Error err, str msg):
    ex = code_to_exception(err)
    if ex:
        raise ex(msg)
