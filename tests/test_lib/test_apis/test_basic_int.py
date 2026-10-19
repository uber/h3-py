import h3.api.basic_int as h3


from .. import util as u


def test_int_output():
    lat = 37.7752702151959
    lng = -122.418307270836

    assert h3.latlng_to_cell(lat, lng, 9) == 617700169958293503
    assert h3.latlng_to_cell(lat, lng, 9) == 0x8928308280fffff


def test_grid_disk():
    expected = [
        617700169957507071,
        617700169957769215,
        617700169958031359,
        617700169958293503,
        617700169961177087,
        617700169964847103,
        617700169965109247,
    ]

    out = h3.grid_disk(617700169958293503, 1)
    assert u.same_set(out, expected)


def test_compact_cells():
    h = 617700169958293503
    cells = h3.cell_to_children(h)

    assert h3.compact_cells(cells) == [h]


def test_identity_scalar_bindings():
    """
    Ensure scalar functions in int APIs are bound directly to _cy implementations
    to eliminate wrapper and identity call overhead (Issue #501).
    """
    from h3 import _cy

    assert h3.latlng_to_cell is _cy.latlng_to_cell
    assert h3.cell_to_parent is _cy.cell_to_parent
    assert h3.cell_to_center_child is _cy.cell_to_center_child
    assert h3.cells_to_directed_edge is _cy.cells_to_directed_edge
    assert h3.get_directed_edge_origin is _cy.get_directed_edge_origin
    assert h3.get_directed_edge_destination is _cy.get_directed_edge_destination
    assert h3.directed_edge_to_cells is _cy.directed_edge_to_cells
    assert h3.local_ij_to_cell is _cy.local_ij_to_cell
    assert h3.cell_to_vertex is _cy.cell_to_vertex

    # Ensure docstrings and signatures are intact
    assert h3.latlng_to_cell.__doc__ is not None
    assert 'latlng_to_cell' in h3.latlng_to_cell.__name__
