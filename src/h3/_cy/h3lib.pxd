from cpython cimport bool
from libc.stdint cimport uint64_t, int64_t, uint32_t

ctypedef uint64_t H3int
ctypedef uint32_t H3Error
ctypedef basestring H3str

cdef extern from "h3api.h":
    cdef int H3_VERSION_MAJOR
    cdef int H3_VERSION_MINOR
    cdef int H3_VERSION_PATCH

    ctypedef uint64_t H3Index

    ctypedef struct LatLng:
        double lat  # in radians
        double lng  # in radians

    ctypedef struct CoordIJ:
        int i
        int j

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

    H3Error maxPolygonToCellsSize(const GeoPolygon *geoPolygon, int res, uint32_t flags, uint64_t *count)
    H3Error polygonToCells(const GeoPolygon *geoPolygon, int res, uint32_t flags, H3Index *out)

    # ctypedef struct GeoBoundary:
    #     int num_verts "numVerts"
    #     GeoCoord verts[10]  # MAX_CELL_BNDRY_VERTS

    # ctypedef struct GeoMultiPolygon:
    #     int numPolygons
    #     GeoPolygon *polygons

    # ctypedef struct LinkedGeoCoord:
    #     GeoCoord data "vertex"
    #     LinkedGeoCoord *next

    # # renaming these for clarity
    # ctypedef struct LinkedGeoLoop:
    #     LinkedGeoCoord *data "first"
    #     LinkedGeoCoord *_data_last "last"  # not needed in Cython bindings
    #     LinkedGeoLoop *next

    # ctypedef struct LinkedGeoPolygon:
    #     LinkedGeoLoop *data "first"
    #     LinkedGeoLoop *_data_last "last"  # not needed in Cython bindings
    #     LinkedGeoPolygon *next

    # void h3ToGeoBoundary(H3Index h3, GeoBoundary *gp)

    # int hexRange(H3Index origin, int k, H3Index *out)

    # int hexRangeDistances(H3Index origin, int k, H3Index *out, int *distances)

    # int hexRanges(H3Index *h3Set, int length, int k, H3Index *out)

    # void h3SetToLinkedGeo(const H3Index *h3Set, const int numHexes, LinkedGeoPolygon *out)

    # void destroyLinkedPolygon(LinkedGeoPolygon *polygon)

    # H3Index stringToH3(const char *str)

    # void h3ToString(H3Index h, char *str, size_t sz)

    # int h3IndexesAreNeighbors(H3Index origin, H3Index destination)

    # H3Index getH3UnidirectionalEdge(H3Index origin, H3Index destination)

    # H3Index getOriginH3IndexFromUnidirectionalEdge(H3Index edge)

    # H3Index getDestinationH3IndexFromUnidirectionalEdge(H3Index edge)

    # void getH3IndexesFromUnidirectionalEdge(H3Index edge, H3Index *originDestination)

    # void getH3UnidirectionalEdgesFromHexagon(H3Index origin, H3Index *edges)

    # void getH3UnidirectionalEdgeBoundary(H3Index edge, GeoBoundary *gb)

    # double edgeLengthKm(int res) nogil
    # double edgeLengthM(int res) nogil

    # double exactEdgeLengthRads(H3Index edge) nogil
    # double exactEdgeLengthKm(H3Index edge) nogil
    # double exactEdgeLengthM(H3Index edge) nogil

    # double pointDistRads(const GeoCoord *a, const GeoCoord *b) nogil
    # double pointDistKm(const GeoCoord *a, const GeoCoord *b) nogil
    # double pointDistM(const GeoCoord *a, const GeoCoord *b) nogil
