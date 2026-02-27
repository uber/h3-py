cimport h3lib
from h3lib cimport H3int
from .util cimport check_cell, coord2deg
from .error_system cimport check_for_error


cdef _loop_to_list(const h3lib.GeoLoop *loop):
    return [coord2deg(loop.verts[v]) for v in range(loop.numVerts)]


def _to_multi_polygon(const H3int[:] cells):
    cdef:
        h3lib.GeoMultiPolygon mpoly
        h3lib.GeoPolygon *poly
        H3int cell

    for cell in cells:
        check_cell(cell)

    check_for_error(
        h3lib.cellsToMultiPolygon(&cells[0], len(cells), &mpoly)
    )

    try:
        out = []
        for p in range(mpoly.numPolygons):
            poly = &mpoly.polygons[p]
            # maybe a helper function here let's us avoid the `append`
            out.append(
                [_loop_to_list(&poly.geoloop)]
                + [_loop_to_list(&poly.holes[h]) for h in range(poly.numHoles)]
            )
    finally:
        h3lib.destroyGeoMultiPolygon(&mpoly)

    return out


def cells_to_multi_polygon(const H3int[:] cells):
    if len(cells) == 0:
        return []

    return _to_multi_polygon(cells)
