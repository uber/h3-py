from libc cimport stdint

ctypedef stdint.uint64_t H3int
ctypedef str H3str

cdef extern from "h3api.h":
    ctypedef struct GeoCoord:
        double lat
        double lng "lon"

    ctypedef struct GeoBoundary:
        int num_verts "numVerts"
        GeoCoord verts[10]  # MAX_CELL_BNDRY_VERTS

    ctypedef struct Geofence:
        int numVerts
        GeoCoord *verts

    ctypedef struct GeoPolygon:
        Geofence geofence
        int numHoles
        Geofence *holes

    ctypedef struct GeoMultiPolygon:
        int numPolygons
        GeoPolygon *polygons

    ctypedef struct LinkedGeoCoord:
        GeoCoord vertex
        LinkedGeoCoord *next

    ctypedef struct LinkedGeoLoop:
        LinkedGeoCoord *first
        LinkedGeoCoord *last
        LinkedGeoLoop *next

    ctypedef struct LinkedGeoPolygon:
        LinkedGeoLoop *first
        LinkedGeoLoop *last
        LinkedGeoPolygon *next

    H3int geoToH3(const GeoCoord *g, int res)

    void h3ToGeo(H3int h3, GeoCoord *g)

    void h3ToGeoBoundary(H3int h3, GeoBoundary *gp)

    int maxKringSize(int k)

    int hexRange(H3int origin, int k, H3int *out)

    int hexRangeDistances(H3int origin, int k, H3int *out, int *distances)

    int h3Distance(H3int origin, H3int h3)

    int hexRanges(H3int *h3Set, int length, int k, H3int *out)

    void kRing(H3int origin, int k, H3int *out)

    void kRingDistances(H3int origin, int k, H3int *out, int *distances)

    int hexRing(H3int origin, int k, H3int *out)

    int maxPolyfillSize(const GeoPolygon *geoPolygon, int res)

    void polyfill(const GeoPolygon *geoPolygon, int res, H3int *out)

    void h3SetToLinkedGeo(const H3int *h3Set, const int numHexes, LinkedGeoPolygon *out)

    void destroyLinkedPolygon(LinkedGeoPolygon *polygon)

    double degsToRads(double degrees)

    double radsToDegs(double radians)

    double hexAreaKm2(int res)

    double hexAreaM2(int res)

    double edgeLengthKm(int res)

    double edgeLengthM(int res)

    stdint.int64_t numHexagons(int res)

    int h3GetResolution(H3int h)

    int h3GetBaseCell(H3int h)

    H3int stringToH3(const char *str)

    void h3ToString(H3int h, char *str, size_t sz)

    int h3IsValid(H3int h)

    H3int h3ToParent(H3int h, int parentRes)

    int maxH3ToChildrenSize(H3int h, int childRes)

    void h3ToChildren(H3int h, int childRes, H3int *children)

    int compact(const H3int *h3Set, H3int *compactedSet, const int numHexes)

    int maxUncompactSize(const H3int *compactedSet, const int numHexes, const int res)

    int uncompact(const H3int *compactedSet, const int numHexes, H3int *h3Set, const int maxHexes, const int res)

    int h3IsResClassIII(H3int h)

    int h3IsPentagon(H3int h)

    int h3IndexesAreNeighbors(H3int origin, H3int destination)

    H3int getH3UnidirectionalEdge(H3int origin, H3int destination)

    int h3UnidirectionalEdgeIsValid(H3int edge)

    H3int getOriginH3IndexFromUnidirectionalEdge(H3int edge)

    H3int getDestinationH3IndexFromUnidirectionalEdge(H3int edge)

    void getH3IndexesFromUnidirectionalEdge(H3int edge, H3int *originDestination)

    void getH3UnidirectionalEdgesFromHexagon(H3int origin, H3int *edges)

    void getH3UnidirectionalEdgeBoundary(H3int edge, GeoBoundary *gb)

    int h3LineSize(H3int start, H3int end)

    int h3Line(H3int start, H3int end, H3int *out)
