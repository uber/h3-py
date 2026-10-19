import h3.api.memview_int as h3


def test1():
    lat, lng = 37.7752702151959, -122.418307270836
    assert h3.latlng_to_cell(lat, lng, 9) == 617700169958293503


def test_line():
    h1 = '8928308280fffff'
    h2 = '8928308287bffff'
    h1, h2 = h3.str_to_int(h1), h3.str_to_int(h2)

    out = h3.grid_path_cells(h1, h2)

    # todo: are we outputting `memoryviewslice`? should we just output a memoryview?
    assert 'memoryview' in str(type(out))

    expected = [
        617700169958293503,
        617700169964847103,
        617700169965371391,
    ]

    assert list(out) == expected


def test_identity_scalar_bindings():
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
