#cython: language_level=3
from cython cimport boundscheck, wraparound

from h3._cy.h3lib cimport H3int
from h3._cy.latlng cimport latlng_to_cell

@boundscheck(False)
@wraparound(False)
cpdef void latlng_to_cell_vect(
    const double[:] lat,
    const double[:] lng,
    int res,
    H3int[:] out
):

    cdef Py_ssize_t i

    for i in range(len(lat)):
        out[i] = latlng_to_cell(lat[i], lng[i], res)
