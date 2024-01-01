from ... import _cy

_in_scalar = _cy.str_to_int
_out_scalar = _cy.int_to_str


def _in_collection(cells):
    it = [_cy.str_to_int(h) for h in cells]

    return _cy.iter_to_mv(it)


def _out_unordered(mv):
    # todo: should this be an (immutable) frozenset?
    return set(_cy.int_to_str(h) for h in mv)


def _out_ordered(mv):
    # todo: should this be an (immutable) tuple?
    return list(_cy.int_to_str(h) for h in mv)
