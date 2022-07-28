cimport h3lib
from .h3lib cimport bool, int64_t, H3int, H3ErrorCodes
from libc cimport stdlib

from .util cimport (
    check_cell,
    check_res,
    check_distance,
    create_ptr,
    create_mv,
    empty_memory_view, # want to drop this import if possible
)

from .error_system cimport (
    check_for_error,
    check_for_error_msg,
)

# todo: add notes about Cython exception handling


# bool is a python type, so we don't need the except clause
cpdef bool is_cell(H3int h):
    """Validates an H3 cell (hexagon or pentagon)

    Returns
    -------
    boolean
    """
    return h3lib.isValidCell(h) == 1


cpdef bool is_pentagon(H3int h):
    return h3lib.isPentagon(h) == 1


cpdef int get_base_cell(H3int h) except -1:
    check_cell(h)

    return h3lib.getBaseCellNumber(h)


cpdef int resolution(H3int h) except -1:
    """Returns the resolution of an H3 Index
    0--15
    """
    check_cell(h)

    return h3lib.getResolution(h)


cpdef int distance(H3int h1, H3int h2) except -1:
    """ Compute the grid distance between two cells
    """
    cdef:
        int64_t distance

    check_cell(h1)
    check_cell(h2)

    check_for_error(
        h3lib.gridDistance(h1, h2, &distance)
    ) # todo: should this raise a distance error?

    # s = 'Cells are too far apart to compute distance: {} and {}'

    return distance

cpdef H3int[:] disk(H3int h, int k):
    """ Return cells at grid distance `<= k` from `h`.
    """
    cdef:
        int64_t n

    check_cell(h)
    check_distance(k)

    check_for_error(
        h3lib.maxGridDiskSize(k, &n)
    )

    ptr = create_ptr(n) # todo: return a "smart" pointer that knows its length?

    err = h3lib.gridDisk(h, k, ptr)
    mv = create_mv(ptr, n)
    check_for_error(err)  # needs to be after, to ensure we clean up memory

    return mv


cpdef H3int[:] _ring_fallback(H3int h, int k):
    """
    `ring` tries to call `h3lib.hexRing` first; if that fails, we call
    this function, which relies on `h3lib.kRingDistances`.

    Failures for `h3lib.hexRing` happen when the algortihm runs into a pentagon.
    """
    cdef:
        int64_t n

    check_cell(h)
    check_distance(k)

    check_for_error(
        h3lib.maxGridDiskSize(k, &n)
    )
    # array of h3 cells
    ptr = create_ptr(n)

    # array of cell distances from `h`
    dist_ptr = <int*> stdlib.calloc(n, sizeof(int))
    if dist_ptr is NULL:
        raise MemoryError() #todo: H3 memory error?

    err = h3lib.gridDiskDistances(h, k, ptr, dist_ptr)

    distances = <int[:n]> dist_ptr
    distances.callback_free_data = stdlib.free

    for i,v in enumerate(distances):
        if v != k:
            ptr[i] = 0

    mv = create_mv(ptr, n)

    check_for_error(err)  # note: need to move this down here to make sure ptr gets freed
    # again, easier with a memory manager object

    return mv

cpdef H3int[:] ring(H3int h, int k):
    """ Return cells at grid distance `== k` from `h`.
    Collection is "hollow" for k >= 1.
    """
    check_cell(h)
    check_distance(k)

    n = 6*k if k > 0 else 1
    ptr = create_ptr(n)

    err = h3lib.gridRingUnsafe(h, k, ptr)

    if err == H3ErrorCodes.E_SUCCESS:
        mv = create_mv(ptr, n)
    elif err == H3ErrorCodes.E_PENTAGON:
        mv = create_mv(ptr, n)  # need to create this to guarantee memory is freed.
        # better done with a Cython object, i think.
        mv = _ring_fallback(h, k)
    else:
        mv = create_mv(ptr, n)  # need to create this to guarantee memory is freed.
        # definitely better done with a Cython "memory manager" object.
        check_for_error(err)

    return mv

cpdef H3int parent(H3int h, res=None) except 0:
    cdef:
        H3int parent

    check_cell(h) # todo: do we want to check for validity here? or leave correctness to the user?

    if res is None:
        res = resolution(h) - 1

    err = h3lib.cellToParent(h, res, &parent)
    if err:
        msg = 'Invalid parent resolution {} for cell {}.'
        msg = msg.format(res, hex(h))
        check_for_error_msg(err, msg)

    return parent


cpdef H3int[:] children(H3int h, res=None):
    cdef:
        H3int child
        int64_t N

    check_cell(h)

    if res is None:
        res = resolution(h) + 1

    err = h3lib.cellToChildrenSize(h, res, &N)
    if err:
        msg = 'Invalid child resolution {} for cell {}.'
        msg = msg.format(res, hex(h))
        check_for_error_msg(err, msg)

    ptr = create_ptr(N)
    err = h3lib.cellToChildren(h, res, ptr)
    mv = create_mv(ptr, N)
    check_for_error(err)  # needs to be after, to ensure memory is freed!

    return mv


cpdef H3int center_child(H3int h, res=None) except 0:
    cdef:
        H3int child

    check_cell(h)

    if res is None:
        res = resolution(h) + 1

    err = h3lib.cellToCenterChild(h, res, &child)
    if err:
        msg = 'Invalid child resolution {} for cell {}.'
        msg = msg.format(res, hex(h))
        check_for_error_msg(err, msg)

    return child



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
    err = h3lib.compactCells(&hu[0], ptr, len(hu))
    mv = create_mv(ptr, len(hu))

    # todo: fix weird error ordering due to memory freeing...
    check_for_error(err)

    return mv


# todo: https://stackoverflow.com/questions/50684977/cython-exception-type-for-a-function-returning-a-typed-memoryview
# apparently, memoryviews are python objects, so we don't need to do the except clause
cpdef H3int[:] uncompact(const H3int[:] hc, int res):
    # todo: the Clib can handle 0-len arrays because it **avoids**
    # dereferencing the pointer, but Cython's syntax of
    # `&hc[0]` **requires** a dereference. For Cython, checking for array
    # length of zero and returning early seems like the easiest solution.
    # note: open to better ideas!
    cdef:
        int64_t N

    if len(hc) == 0:
        return empty_memory_view()

    for h in hc:
        check_cell(h)

    # ignoring error for now
    err = h3lib.uncompactCellsSize(&hc[0], len(hc), res, &N)

    ptr = create_ptr(N)
    err = h3lib.uncompactCells(
        &hc[0],
        len(hc),
        ptr,
        N,
        res
    )
    mv = create_mv(ptr, N)

    # todo: fix weird error ordering due to memory freeing...
    check_for_error(err)

    return mv


cpdef int64_t num_hexagons(int resolution) except -1:
    cdef:
        int64_t num_cells

    check_for_error(
        h3lib.getNumCells(resolution, &num_cells)
    )

    return num_cells


cpdef double mean_hex_area(int resolution, unit='km^2') except -1:
    cdef:
        double area

    check_for_error(
        h3lib.getHexagonAreaAvgKm2(resolution, &area)
    )

    # todo: multiple units
    convert = {
        'km^2': 1.0,
        'm^2': 1000*1000.0
    }

    try:
        area *= convert[unit]
    except:
        raise ValueError('Unknown unit: {}'.format(unit))

    return area


cpdef double cell_area(H3int h, unit='km^2') except -1:
    cdef:
        double area

    if unit == 'rads^2':
        err = h3lib.cellAreaRads2(h, &area)
    elif unit == 'km^2':
        err = h3lib.cellAreaKm2(h, &area)
    elif unit == 'm^2':
        err = h3lib.cellAreaM2(h, &area)
    else:
        raise ValueError('Unknown unit: {}'.format(unit))

    check_for_error(err)

    return area


cdef could_not_find_line(err, start, end):
    msg = "Couldn't find line between cells {} and {}"
    msg = msg.format(hex(start), hex(end))

    check_for_error_msg(err, msg)

cpdef H3int[:] line(H3int start, H3int end):
    cdef:
        int64_t n

    # todo: can we segfault here with invalid inputs?
    # Can we trust the c library to validate the start/end cells?
    # probably applies to all size/work pairs of functions...
    err = h3lib.gridPathCellsSize(start, end, &n)

    could_not_find_line(err, start, end)

    ptr = create_ptr(n)
    err = h3lib.gridPathCells(start, end, ptr)
    mv = create_mv(ptr, n)

    could_not_find_line(err, start, end)

    return mv

cpdef bool is_res_class_iii(H3int h):
    return h3lib.isResClassIII(h) == 1


cpdef H3int[:] get_pentagon_indexes(int res):
    n = h3lib.pentagonCount()

    # todo note: this is the tricky situation where we need the memory manager
    ptr = create_ptr(n)
    err = h3lib.getPentagons(res, ptr)
    mv = create_mv(ptr, n)

    check_for_error(err)

    return mv


cpdef H3int[:] get_res0_indexes():
    n = h3lib.res0CellCount()

    # todo note: this is the tricky situation where we need the memory manager
    ptr = create_ptr(n)
    err = h3lib.getRes0Cells(ptr)
    mv = create_mv(ptr, n)

    check_for_error(err)

    return mv

cpdef get_faces(H3int h):
    cdef:
        int n

    check_for_error(
        h3lib.maxFaceCount(h, &n)
    )

    cdef int* ptr = <int*> stdlib.calloc(n, sizeof(int))
    if (n > 0) and (not ptr):
        raise MemoryError()

    check_for_error(
        h3lib.getIcosahedronFaces(h, ptr)
    )

    faces = <int[:n]> ptr
    faces = {f for f in faces if f >= 0}
    stdlib.free(ptr)

    return faces


cpdef (int, int) experimental_h3_to_local_ij(H3int origin, H3int h) except *:
    cdef:
        h3lib.CoordIJ c

    err = h3lib.cellToLocalIj(origin, h, 0, &c)
    if err:
        msg = "Couldn't find local (i,j) between cells {} and {}."
        msg = msg.format(hex(origin), hex(h))
        check_for_error_msg(err, msg)

    return c.i, c.j

cpdef H3int experimental_local_ij_to_h3(H3int origin, int i, int j) except 0:
    cdef:
        h3lib.CoordIJ c
        H3int out

    c.i, c.j = i, j

    err = h3lib.localIjToCell(origin, &c, 0, &out)
    if err:
        msg = "Couldn't find cell at local ({},{}) from cell {}."
        msg = msg.format(i, j, hex(origin))
        check_for_error_msg(err, msg)

    return out
