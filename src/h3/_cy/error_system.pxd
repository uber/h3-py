from .h3lib cimport H3Error

# todo: does this really need to be a cdef? just normal python function? are we hitting python anyway with the exception objects?
cdef check_for_error(H3Error err)

