from cpython cimport bool
from libc.stdint cimport uint64_t, int64_t, uint32_t

ctypedef uint64_t H3int
ctypedef basestring H3str

# todo: extern version of this?
cdef enum H3Error:
    E_SUCCESS = 0
    E_FAILED = 1
    E_DOMAIN = 2
    E_LATLNG_DOMAIN = 3
    E_RES_DOMAIN = 4
    E_CELL_INVALID = 5
    E_DIR_EDGE_INVALID = 6
    E_UNDIR_EDGE_INVALID = 7
    E_VERTEX_INVALID = 8
    E_PENTAGON = 9
    E_DUPLICATE_INPUT = 10
    E_NOT_NEIGHBORS = 11
    E_RES_MISMATCH = 12
    E_MEMORY = 13
    E_MEMORY_BOUNDS = 14
    E_OPTION_INVALID = 15

cdef extern from "h3api.h":
    cdef int H3_VERSION_MAJOR
    cdef int H3_VERSION_MINOR
    cdef int H3_VERSION_PATCH

    ctypedef uint64_t H3Index

    ctypedef struct LatLng:
        double lat  # in radians
        double lng  # in radians

    ctypedef struct CellBoundary:
        int num_verts "numVerts"
        LatLng verts[10]  # MAX_CELL_BNDRY_VERTS

    ctypedef struct CoordIJ:
        int i
        int j

    ctypedef struct LinkedLatLng:
        LatLng data "vertex"
        LinkedLatLng *next

    # renaming these for clarity
    ctypedef struct LinkedGeoLoop:
        LinkedLatLng *data "first"
        LinkedLatLng *_data_last "last"  # not needed in Cython bindings
        LinkedGeoLoop *next

    ctypedef struct LinkedGeoPolygon:
        LinkedGeoLoop *data "first"
        LinkedGeoLoop *_data_last "last"  # not needed in Cython bindings
        LinkedGeoPolygon *next

    ctypedef struct GeoLoop:
        int numVerts
        LatLng *verts

    ctypedef struct GeoPolygon:
        GeoLoop geoloop
        int numHoles
        GeoLoop *holes

    int isValidCell(H3Index h) nogil
    int isPentagon(H3Index h) nogil
    int isResClassIII(H3Index h) nogil
    int isValidDirectedEdge(H3Index edge) nogil

    double degsToRads(double degrees) nogil
    double radsToDegs(double radians) nogil

    int getResolution(H3Index h) nogil
    int getBaseCellNumber(H3Index h) nogil

    H3Error latLngToCell(const LatLng *g, int res, H3Index *out) nogil
    H3Error cellToLatLng(H3Index h, LatLng *) nogil
    H3Error gridDistance(H3Index h1, H3Index h2, int64_t *distance) nogil

    H3Error maxGridDiskSize(int k, int64_t *out) nogil # num/out/N?
    H3Error gridDisk(H3Index h, int k, H3Index *out) nogil

    H3Error cellToParent(     H3Index h, int parentRes, H3Index *parent) nogil
    H3Error cellToCenterChild(H3Index h, int childRes,  H3Index *child) nogil

    H3Error cellToChildrenSize(H3Index h, int childRes, int64_t *num) nogil # num/out/N?
    H3Error cellToChildren(    H3Index h, int childRes, H3Index *children) nogil

    H3Error compactCells(
        const H3Index *cells_u,
              H3Index *cells_c,
        const int num_u
    ) nogil
    H3Error uncompactCellsSize(
        const H3Index *cells_c,
        const int64_t    num_c,
        const int res,
        int64_t *num_u
    ) nogil
    H3Error uncompactCells(
        const H3Index *cells_c,
        const int        num_c,
        H3Index       *cells_u,
        const int        num_u,
        const int res
    ) nogil

    H3Error getNumCells(int res, int64_t *out) nogil
    int pentagonCount() nogil
    int res0CellCount() nogil
    H3Error getPentagons(int res, H3Index *out) nogil
    H3Error getRes0Cells(H3Index *out) nogil

    H3Error gridPathCellsSize(H3Index start, H3Index end, int64_t *size) nogil
    H3Error gridPathCells(H3Index start, H3Index end, H3Index *out) nogil

    H3Error getHexagonAreaAvgKm2(int res, double *out) nogil
    H3Error getHexagonAreaAvgM2(int res, double *out) nogil

    H3Error cellAreaRads2(H3Index h, double *out) nogil
    H3Error cellAreaKm2(H3Index h, double *out) nogil
    H3Error cellAreaM2(H3Index h, double *out) nogil

    H3Error maxFaceCount(H3Index h, int *out) nogil
    H3Error getIcosahedronFaces(H3Index h3, int *out) nogil

    H3Error cellToLocalIj(H3Index origin, H3Index h3, uint32_t mode, CoordIJ *out) nogil
    H3Error localIjToCell(H3Index origin, const CoordIJ *ij, uint32_t mode, H3Index *out) nogil

    H3Error gridDiskDistances(H3Index origin, int k, H3Index *out, int *distances) nogil
    H3Error gridRingUnsafe(H3Index origin, int k, H3Index *out) nogil

    H3Error areNeighborCells(H3Index origin, H3Index destination, int *out) nogil
    H3Error cellsToDirectedEdge(H3Index origin, H3Index destination, H3Index *out) nogil
    H3Error getDirectedEdgeOrigin(H3Index edge, H3Index *out) nogil
    H3Error getDirectedEdgeDestination(H3Index edge, H3Index *out) nogil
    H3Error originToDirectedEdges(H3Index origin, H3Index *edges) nogil

    H3Error getHexagonEdgeLengthAvgKm(int res, double *out) nogil
    H3Error getHexagonEdgeLengthAvgM(int res, double *out) nogil

    H3Error exactEdgeLengthRads(H3Index edge, double *out) nogil
    H3Error exactEdgeLengthKm(H3Index edge, double *out) nogil
    H3Error exactEdgeLengthM(H3Index edge, double *out) nogil

    H3Error cellToBoundary(H3Index h3, CellBoundary *gp) nogil
    H3Error directedEdgeToBoundary(H3Index edge, CellBoundary *gb) nogil

    double distanceRads(const LatLng *a, const LatLng *b) nogil
    double distanceKm(const LatLng *a, const LatLng *b) nogil
    double distanceM(const LatLng *a, const LatLng *b) nogil

    H3Error cellsToLinkedMultiPolygon(const H3Index *h3Set, const int numHexes, LinkedGeoPolygon *out)
    void destroyLinkedMultiPolygon(LinkedGeoPolygon *polygon)

    H3Error maxPolygonToCellsSize(const GeoPolygon *geoPolygon, int res, uint32_t flags, uint64_t *count)
    H3Error polygonToCells(const GeoPolygon *geoPolygon, int res, uint32_t flags, H3Index *out)

    # ctypedef struct GeoMultiPolygon:
    #     int numPolygons
    #     GeoPolygon *polygons

    # int hexRange(H3Index origin, int k, H3Index *out)

    # int hexRangeDistances(H3Index origin, int k, H3Index *out, int *distances)

    # int hexRanges(H3Index *h3Set, int length, int k, H3Index *out)

    # void h3SetToLinkedGeo(const H3Index *h3Set, const int numHexes, LinkedGeoPolygon *out)

    # void destroyLinkedPolygon(LinkedGeoPolygon *polygon)

    # H3Index stringToH3(const char *str)

    # void h3ToString(H3Index h, char *str, size_t sz)

    # void getH3IndexesFromUnidirectionalEdge(H3Index edge, H3Index *originDestination)
