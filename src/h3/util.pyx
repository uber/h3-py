from libc cimport stdlib
from cython.view cimport array
from .h3lib cimport H3int, H3str, h3IsValid, h3UnidirectionalEdgeIsValid

# todo: should we use C API functions instead? (stringToH3 and h3ToString)
cpdef H3int hex2int(H3str h):
    return int(h, 16)

cpdef H3str int2hex(H3int x):
    """ Convert H3 integer to hex string representation
    The `.rstrip('L')` is needed in Python 2 because "long"
    integers (even in hex form) are represented with a trailing `L` character
    The final `str` conversion converts from `unicode` to `str` in Python 2
    """
    return str(hex(x)[2:].rstrip('L'))


class H3ValueError(ValueError):
    pass

class H3CellError(H3ValueError):
    pass

class H3EdgeError(H3ValueError):
    pass

class H3ResolutionError(H3ValueError):
    pass

cdef check_cell(H3int h):
    """ Check if valid H3 "cell" (hexagon or pentagon).

    Does not check if a valid H3 edge, for example.
    """
    if h3IsValid(h) == 0:
        raise H3CellError(h)

cdef check_edge(H3int e):
    if h3UnidirectionalEdgeIsValid(e) == 0:
        raise H3EdgeError(e)

cdef check_res(int res):
    if (res < 0) or (res > 15):
        raise H3ResolutionError(res)



## todo: can i turn these two into a context manager?
cdef H3int* create_ptr(size_t n) except *:
    cdef H3int* ptr = <H3int*> stdlib.calloc(n, sizeof(H3int))
    if (n > 0) and (not ptr):
        raise MemoryError()

    return ptr

cdef H3int[:] create_mv(H3int* ptr, size_t n):
    cdef:
        array x

    n = move_nonzeros(ptr, n)
    if n <= 0:
        stdlib.free(ptr)
        return empty_memory_view()

    ptr = <H3int*> stdlib.realloc(ptr, n*sizeof(H3int))

    if ptr is NULL:
        raise MemoryError()

    x = <H3int[:n]> ptr
    x.callback_free_data = stdlib.free

    return x


cpdef H3int[:] from_iter(hexes):
    """ hexes needs to be an iterable that knows its size...
    or should we have it match the np.fromiter function, which infers if not available?
    """
    cdef:
        array x
        size_t n
    n = len(hexes)
    x = <H3int[:n]> create_ptr(n)
    x.callback_free_data = stdlib.free

    for i,h in enumerate(hexes):
        x[i] = h

    return x


cdef size_t move_nonzeros(H3int* a, size_t n):
    """ Move nonzero elements to front of array `a` of length `n`.
    Return the number of nonzero elements.

    | a | b | 0 | c | d | ... |
            ^           ^
            i           j


    | a | b | d | c | d | ... |
            ^       ^
            i       j
    """
    cdef:
        size_t i = 0
        size_t j = n

    while i < j:
        if a[j-1] == 0:
            j -= 1
            continue

        if a[i] != 0:
            i += 1
            continue

        # if we're here, we know:
        # a[i] == 0
        # a[j-1] != 0
        # i < j
        # so we can swap!
        a[i] = a[j-1]
        j -= 1

    return i


cdef inline H3int[:] empty_memory_view():
    # there's gotta be a better way to do this...
    # create an empty cython.view.array?
    cdef:
        H3int a[1]

    return (<H3int[:]>a)[:0]
