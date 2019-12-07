from h3.api._api_template import _api_functions
import h3._internal_api as _a


# todo: how to write documentation once and have it carry over to each interface?

def _id(x):
    return x


def _in_collection(hexes):
    it = list(hexes)

    return _a.from_iter(it)


_api_functions(
    _in_scalar = _id,
    _out_scalar = _id,
    _in_collection = _in_collection,
    _out_unordered = set,
    _out_ordered = list,
    _globals = globals(),
)
