from h3.api._api_template import _api_functions


def _id(x):
    return x


_funcs = _api_functions(
    _in_scalar = _id,
    _out_scalar = _id,
    _in_collection = _id,
    _out_unordered = _id,
    _out_ordered = _id,
)

globals().update(_funcs)
