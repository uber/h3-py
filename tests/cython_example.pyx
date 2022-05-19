# from cython cimport boundscheck, wraparound

# from h3._cy.h3lib cimport H3int
# from h3._cy.geo cimport geo_to_h3

# @boundscheck(False)
# @wraparound(False)
# cpdef void geo_to_h3_vect(
#     const double[:] lat,
#     const double[:] lng,
#     int res,
#     H3int[:] out
# ):

#     cdef Py_ssize_t i

#     for i in range(len(lat)):
#         out[i] = geo_to_h3(lat[i], lng[i], res)
