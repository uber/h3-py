"""
todo: use module docs to describe new error system

- less aggressive correctness checking for indices
- hierarchy?
- error codes from C
"""

from .h3lib cimport H3Error

class H3Exception(Exception):
    pass

class H3ValueError(H3Exception, ValueError):
    pass

class H3CellError(H3ValueError):
    pass

class H3EdgeError(H3ValueError):
    pass

class H3ResolutionError(H3ValueError):
    pass

class H3DistanceError(H3ValueError):
    pass

cdef check_for_error(H3Error err):
    """
    todo: more descriptive message
    todo: add error codes as property
    todo: allow passing in extra args for the error message?
    """

    d = {
        H3Error.E_SUCCESS: None,
        H3Error.E_FAILED: H3ValueError(), # H3Exception(),
        H3Error.E_DOMAIN: H3ValueError(),
        H3Error.E_LATLNG_DOMAIN: H3ValueError(),
        H3Error.E_RES_DOMAIN: H3ResolutionError(),
        H3Error.E_CELL_INVALID: H3CellError(),
        H3Error.E_DIR_EDGE_INVALID: H3EdgeError(),
        H3Error.E_UNDIR_EDGE_INVALID: H3EdgeError(),
        H3Error.E_VERTEX_INVALID: H3ValueError(),
        H3Error.E_PENTAGON: H3ValueError(),
        H3Error.E_DUPLICATE_INPUT: H3ValueError(),
        H3Error.E_NOT_NEIGHBORS: H3ValueError(),
        H3Error.E_RES_MISMATCH: H3ResolutionError(),
        H3Error.E_MEMORY: H3Exception(),
        H3Error.E_MEMORY_BOUNDS: H3Exception(),
        H3Error.E_OPTION_INVALID: H3Exception(),
    }

    e = d[err]

    if e:
        raise e
