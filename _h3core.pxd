from libc cimport stdint

cdef extern from "h3api.h":
    ctypedef stdint.uint64_t H3Index

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

    H3Index geoToH3(const GeoCoord *g, int res)

    void h3ToGeo(H3Index h3, GeoCoord *g)

    void h3ToGeoBoundary(H3Index h3, GeoBoundary *gp)

    int maxKringSize(int k)

    int hexRange(H3Index origin, int k, H3Index *out)

    int hexRangeDistances(H3Index origin, int k, H3Index *out, int *distances)

    int h3Distance(H3Index origin, H3Index h3)

    int hexRanges(H3Index *h3Set, int length, int k, H3Index *out)

    void kRing(H3Index origin, int k, H3Index *out)

    void kRingDistances(H3Index origin, int k, H3Index *out, int *distances)

    int hexRing(H3Index origin, int k, H3Index *out)

    int maxPolyfillSize(const GeoPolygon *geoPolygon, int res)

    void polyfill(const GeoPolygon *geoPolygon, int res, H3Index *out)

    void h3SetToLinkedGeo(const H3Index *h3Set, const int numHexes, LinkedGeoPolygon *out)

    void destroyLinkedPolygon(LinkedGeoPolygon *polygon)

    double degsToRads(double degrees)

    double radsToDegs(double radians)

    double hexAreaKm2(int res)

    double hexAreaM2(int res)

    double edgeLengthKm(int res)

    double edgeLengthM(int res)

    stdint.int64_t numHexagons(int res)

    int h3GetResolution(H3Index h)

    int h3GetBaseCell(H3Index h)

    H3Index stringToH3(const char *str)

    void h3ToString(H3Index h, char *str, size_t sz)

    int h3IsValid(H3Index h)

    H3Index h3ToParent(H3Index h, int parentRes)

    int maxH3ToChildrenSize(H3Index h, int childRes)

    void h3ToChildren(H3Index h, int childRes, H3Index *children)

    int compact(const H3Index *h3Set, H3Index *compactedSet, const int numHexes)

    int maxUncompactSize(const H3Index *compactedSet, const int numHexes, const int res)

    int uncompact(const H3Index *compactedSet, const int numHexes, H3Index *h3Set, const int maxHexes, const int res)

    int h3IsResClassIII(H3Index h)

    int h3IsPentagon(H3Index h)

    int h3IndexesAreNeighbors(H3Index origin, H3Index destination)

    H3Index getH3UnidirectionalEdge(H3Index origin, H3Index destination)

    int h3UnidirectionalEdgeIsValid(H3Index edge)

    H3Index getOriginH3IndexFromUnidirectionalEdge(H3Index edge)

    H3Index getDestinationH3IndexFromUnidirectionalEdge(H3Index edge)

    void getH3IndexesFromUnidirectionalEdge(H3Index edge, H3Index *originDestination)

    void getH3UnidirectionalEdgesFromHexagon(H3Index origin, H3Index *edges)

    void getH3UnidirectionalEdgeBoundary(H3Index edge, GeoBoundary *gb)
