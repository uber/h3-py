from ... import _cy


def _in_scalar(x):
    return x


def _out_scalar(x):
    return x


def _in_collection(cells):
    it = list(cells)

    return _cy.iter_to_mv(it)


_out_unordered = set
_out_ordered = list
