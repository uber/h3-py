from libc cimport stdlib
from h3py.h3api cimport H3int, H3str
from cython.view cimport array


# todo:  not sure this is the most intuitive place to have these conversion functions...
# todo: should we use C API functions instead? (stringToH3 and h3ToString)
cpdef H3int hex2int(h):  # we get typing problems if we try to type input as `H3str h`
    return int(h, 16)


cpdef H3str int2hex(H3int x):
    return hex(x)[2:]


## todo: can i turn these two into a context manager?
cdef H3int* create_ptr(size_t n):
    cdef H3int* ptr = <H3int*> stdlib.calloc(n, sizeof(H3int))
    if not ptr:
        raise MemoryError()

    return ptr


cdef H3int[:] create_mv(H3int* ptr, size_t n):
    cdef:
        array x

    n = move_nonzeros(ptr, n)
    ptr = <H3int*> stdlib.realloc(ptr, n*sizeof(H3int))

    if ptr is NULL:
        raise MemoryError()

    if n > 0:
        x = <H3int[:n]> ptr
        x.callback_free_data = stdlib.free

        return x
    else:
        return empty_memory_view()


cpdef H3int[:] from_iter(hexes):
    """ hexes needs to be an iterable that knows its size...
    or should we have it match the np.fromiter function, which infers if not available?
    """
    cdef:
        array x
        size_t n
    n = len(hexes)
    x = <H3int[:n]> stdlib.calloc(n, sizeof(H3int))
    x.callback_free_data = stdlib.free

    for i,h in enumerate(hexes):
        x[i] = h

    return x


cdef size_t move_nonzeros(H3int* a, size_t n):
    """ Move nonzero elements to front of array `a` of length `n`.

    Return the number of nonzero elements.
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
        # todo: what about j vs j-1 ....?
        a[i] = a[j-1]
        j -= 1

    return i


cdef inline H3int[:] empty_memory_view():
    # there's gotta be a better way to do this...
    # create an empty cython.view.array?
    cdef:
        H3int a[1]

    return (<H3int[:]>a)[:0]
