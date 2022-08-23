from .h3lib cimport H3Error
cdef check_for_error(H3Error err)
cdef check_for_error_msg(H3Error err, str msg)
