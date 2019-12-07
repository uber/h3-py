cimport h3lib
from .h3lib cimport bool, int64_t, H3int
from libc cimport stdlib

from .util cimport (
    check_cell,
    check_res,
    create_ptr,
    create_mv,
    empty_memory_view, # want to drop this import if possible
)

from .util import H3ValueError

# todo: add notes about Cython exception handling


# bool is a python type, so we don't need the except clause
cpdef bool is_cell(H3int h):
    """Validates an H3 cell (hexagon or pentagon)

    Returns
    -------
    boolean
    """
    return h3lib.h3IsValid(h) == 1

cpdef bool is_pentagon(H3int h):
    return h3lib.h3IsPentagon(h) == 1

cpdef int get_base_cell(H3int h) except -1:
    check_cell(h)

    return h3lib.h3GetBaseCell(h)


cpdef int resolution(H3int h) except -1:
    """Returns the resolution of an H3 Index
    0--15
    """
    check_cell(h)

    return h3lib.h3GetResolution(h)


cpdef H3int parent(H3int h, res=None) except 1:
    check_cell(h)

    if res is None:
        res = resolution(h) - 1
    # todo: actually, do we want to raise an error if there are no children, or just return an empty set?
    check_res(res)

    return h3lib.h3ToParent(h, res)


cpdef int distance(H3int h1, H3int h2) except -1:
    """ compute the hex-distance between two hexagons
    """
    check_cell(h1)
    check_cell(h2)

    d = h3lib.h3Distance(h1,h2)

    return d

cpdef H3int[:] disk(H3int h, int k):
    """ Return cells at grid distance `<= k` from `h`.
    """
    check_cell(h)
    if k < 0:
        raise H3ValueError('Invalid ring size: {}'.format(k))

    n = h3lib.maxKringSize(k)

    ptr = create_ptr(n) # todo: return a "smart" pointer that knows its length?
    h3lib.kRing(h, k, ptr)
    mv = create_mv(ptr, n)

    return mv


cpdef H3int[:] _ring_fallback(H3int h, int k):
    """
    `ring` tries to call `h3lib.hexRing` first; if that fails, we call
    this function, which relies on `h3lib.kRingDistances`.

    Failures for `h3lib.hexRing` happen when that alg runs into a pentagon.
    """
    check_cell(h)

    n = h3lib.maxKringSize(k)
    # array of h3 cells
    ptr = create_ptr(n)

    # array of cell distances from `h`
    dist_ptr = <int*> stdlib.calloc(n, sizeof(int))
    if dist_ptr is NULL:
        raise MemoryError()

    h3lib.kRingDistances(h, k, ptr, dist_ptr)

    distances = <int[:n]> dist_ptr
    distances.callback_free_data = stdlib.free

    for i,v in enumerate(distances):
        if v != k:
            ptr[i] = 0

    mv = create_mv(ptr, n)

    return mv

cpdef H3int[:] ring(H3int h, int k):
    """ Return cells at grid distance `== k` from `h`.
    Collection is "hollow" for k >= 1.
    """
    check_cell(h)

    n = 6*k if k > 0 else 1
    ptr = create_ptr(n)

    flag = h3lib.hexRing(h, k, ptr)

    # if we drop into the failure state, we might be tempted to not create
    # this mv, but creating the mv is exactly what guarantees that we'll free
    # the memory. context manager would be better here, if we can figure out
    # how to do that
    mv = create_mv(ptr, n)

    if flag != 0:
        mv = _ring_fallback(h, k)

    return mv



cpdef H3int[:] children(H3int h, res=None):
    check_cell(h)

    if res is None:
        res = resolution(h) + 1
    # todo: actually, do we want to raise an error if there are no children, or just return an empty set?
    check_res(res)

    n = h3lib.maxH3ToChildrenSize(h, res)

    ptr = create_ptr(n)
    h3lib.h3ToChildren(h, res, ptr)
    mv = create_mv(ptr, n)

    return mv



cpdef H3int[:] compact(const H3int[:] hu):
    # todo: the Clib can handle 0-len arrays because it **avoids**
    # dereferencing the pointer, but Cython's syntax of
    # `&hu[0]` **requires** a dereference. For Cython, checking for array
    # length of zero and returning early seems like the easiest solution.
    # note: open to better ideas!
    if len(hu) == 0:
        return empty_memory_view()

    for h in hu: ## todo: should we have an array version? would that be faster?
        check_cell(h)

    ptr = create_ptr(len(hu))
    flag = h3lib.compact(&hu[0], ptr, len(hu))
    mv = create_mv(ptr, len(hu))

    if flag != 0:
        raise H3ValueError('Could not compact set of hexagons!')

    return mv

# todo: https://stackoverflow.com/questions/50684977/cython-exception-type-for-a-function-returning-a-typed-memoryview
# apparently, memoryviews are python objects, so we don't need to do the except clause
cpdef H3int[:] uncompact(const H3int[:] hc, int res):
    # todo: the Clib can handle 0-len arrays because it **avoids**
    # dereferencing the pointer, but Cython's syntax of
    # `&hc[0]` **requires** a dereference. For Cython, checking for array
    # length of zero and returning early seems like the easiest solution.
    # note: open to better ideas!
    if len(hc) == 0:
        return empty_memory_view()

    for h in hc:
        check_cell(h)

    N = h3lib.maxUncompactSize(&hc[0], len(hc), res)

    ptr = create_ptr(N)
    flag = h3lib.uncompact(
        &hc[0], len(hc),
           ptr, N,
        res
    )
    mv = create_mv(ptr, N)

    if flag != 0:
        raise H3ValueError('Could not uncompact set of hexagons!')

    return mv


cpdef int64_t num_hexagons(int resolution) except -1:
    check_res(resolution)

    return h3lib.numHexagons(resolution)


cpdef double mean_hex_area(int resolution, unit='km^2') except -1:
    check_res(resolution)

    area = h3lib.hexAreaKm2(resolution)

    # todo: multiple units
    convert = {
        'km^2': 1.0,
        'm^2': 1000*1000.0
    }

    try:
        area *= convert[unit]
    except:
        raise H3ValueError('Unknown unit: {}'.format(unit))

    return area

cpdef double mean_edge_length(int resolution, unit='km') except -1:
    check_res(resolution)

    length = h3lib.edgeLengthKm(resolution)

    # todo: multiple units
    convert = {
        'km': 1.0,
        'm': 1000.0
    }

    try:
        length *= convert[unit]
    except:
        raise H3ValueError('Unknown unit: {}'.format(unit))

    return length


cpdef H3int[:] line(H3int start, H3int end):
    check_cell(start)
    check_cell(end)

    n = h3lib.h3LineSize(start, end)

    if n < 0:
        raise H3ValueError("Couldn't find line between cells {} and {}".format(start, end))

    ptr = create_ptr(n)
    flag = h3lib.h3Line(start, end, ptr)
    mv = create_mv(ptr, n)

    if flag != 0:
        raise H3ValueError("Couldn't find line between cells {} and {}".format(start, end))

    return mv

cpdef bool is_res_class_iii(H3int h):
    return h3lib.h3IsResClassIII(h) == 1
