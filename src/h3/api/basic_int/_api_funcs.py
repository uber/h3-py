from ... import _cy


def _id(x):
    return x


def _in_collection(cells):
    it = list(cells)

    return _cy.iter_to_mv(it)


_in_scalar = _id
_out_scalar = _id
_in_collection = _in_collection
_out_unordered = set
_out_ordered = list
