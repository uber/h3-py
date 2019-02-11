'''
 Copyright (c) 2018 Uber Technologies, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Bindings for the functions available in h3lib
'''

from __future__ import absolute_import

import math
import os
import platform
from ctypes import (
    cast,
    cdll,
    c_int,
    c_long,
    c_double,
    c_void_p,
    byref,
    Structure,
    POINTER,
)

_dirname = os.path.dirname(__file__)
libh3_path = ('out/libh3.1.dylib'
              if platform.system() == 'Darwin' else 'out/libh3.so.1')
libh3 = cdll.LoadLibrary('{}/{}'.format(_dirname, libh3_path))


class GeoCoord(Structure):
    """
    An instance of :class:`GeoCoord` will have attributes:

    :param float lat: Latitude
    :param float lng: Longitude
    """
    _fields_ = [('lat', c_double), ('lng', c_double)]


#: Collection of :class:`GeoCoord` 's that make up a :class:`GeoBoundary`
GeoCoordArrayTen = GeoCoord * 10


class GeoBoundary(Structure):
    """
    Vertices that create a single hexagonal cell in geo-coordinates.

    :param int num_verts: The number of vertices that make up this cell [1, 10]
    :param GeoCoordArrayTen verts: The vertices
    """
    _fields_ = [('num_verts', c_int), ('verts', GeoCoordArrayTen)]


class Geofence(Structure):
    """
    Vertices that create an arbitrary geofence. Similar to GeoBoundary.

    :param int num_verts: The number of vertices that make up this geofence.
    :param GeoCoord* verts: Pointer to the vertices
    """
    _fields_ = [('num_verts', c_int), ('verts', c_void_p)]


class GeoJsonLite(Structure):
    """
    Struct that mimicks the core of the Polygon GeoJSON definition.

    :param Geofence geofence: The primary geofence of the polygon.
    :param int num_holes: The number of holes in the polygon.
    :param Geofence* holes: Pointer to all of the holes.
    """
    _fields_ = [('geofence', Geofence), ('num_holes', c_int), ('holes',
                                                               c_void_p)]


class LinkedGeoCoord(Structure):
    pass


LinkedGeoCoord._fields_ = [('vertex', GeoCoord), ('next',
                                                  POINTER(LinkedGeoCoord))]


class LinkedGeoLoop(Structure):
    pass


LinkedGeoLoop._fields_ = [('first',
                           POINTER(LinkedGeoCoord)), ('last',
                                                      POINTER(LinkedGeoCoord)),
                          ('next', POINTER(LinkedGeoLoop))]


class LinkedGeoPolygon(Structure):
    pass


LinkedGeoPolygon._fields_ = [('first', POINTER(LinkedGeoLoop)),
                             ('last', POINTER(LinkedGeoLoop)),
                             ('next', POINTER(LinkedGeoPolygon))]

libh3.h3IsValid.restype = c_int
libh3.h3IsValid.argtypes = [c_long]

libh3.geoToH3.restype = c_long
libh3.geoToH3.argtypes = [c_void_p, c_int]

libh3.h3ToGeo.restype = None
libh3.h3ToGeo.argtypes = [c_long, c_void_p]

libh3.h3ToGeoBoundary.restype = None
libh3.h3ToGeoBoundary.argtypes = [c_long, c_void_p]

libh3.maxKringSize.restype = c_int
libh3.maxKringSize.argtypes = [c_int]

libh3.kRing.restype = None
libh3.kRing.argtypes = [c_long, c_int, c_void_p]

libh3.kRingDistances.restype = None
libh3.kRingDistances.argtypes = [c_long, c_int, c_void_p, c_void_p]

libh3.maxPolyfillSize.restype = c_int
libh3.maxPolyfillSize.argtypes = [c_void_p, c_int]

libh3.polyfill.restype = None
libh3.polyfill.argtypes = [c_void_p, c_int, c_void_p]

libh3.h3SetToLinkedGeo.restype = None
libh3.h3SetToLinkedGeo.argtypes = [c_void_p, c_int, c_void_p]

libh3.destroyLinkedPolygon.restype = None
libh3.destroyLinkedPolygon.argtypes = [c_void_p]

libh3.hexRing.restype = c_int
libh3.hexRing.argtypes = [c_long, c_int, c_void_p]

libh3.compact.restype = c_int
libh3.compact.argtypes = [c_void_p, c_void_p, c_int]

libh3.uncompact.restype = c_int
libh3.uncompact.argtypes = [c_void_p, c_int, c_void_p, c_int, c_int]

libh3.maxUncompactSize.restype = c_int
libh3.maxUncompactSize.argtypes = [c_void_p, c_int, c_int]

libh3.h3ToParent.restype = c_long
libh3.h3ToParent.argtypes = [c_long, c_int]

libh3.maxH3ToChildrenSize.restype = c_int
libh3.maxH3ToChildrenSize.argtypes = [c_long, c_int]

libh3.h3ToChildren.restype = None
libh3.h3ToChildren.argtypes = [c_long, c_int, c_void_p]

libh3.hexRange.restype = c_int
libh3.hexRange.argtypes = [c_long, c_int, c_void_p]

libh3.hexRangeDistances.restype = c_int
libh3.hexRangeDistances.argtypes = [c_long, c_int, c_void_p, c_void_p]

libh3.hexRanges.restype = c_int
libh3.hexRanges.argtypes = [c_void_p, c_int, c_int, c_void_p]

libh3.hexAreaKm2.restype = c_double
libh3.hexAreaKm2.argtypes = [c_int]

libh3.hexAreaM2.restype = c_double
libh3.hexAreaM2.argtypes = [c_int]

libh3.edgeLengthKm.restype = c_double
libh3.edgeLengthKm.argtypes = [c_int]

libh3.edgeLengthM.restype = c_double
libh3.edgeLengthM.argtypes = [c_int]

libh3.numHexagons.restype = c_long
libh3.numHexagons.argtypes = [c_int]

libh3.h3GetBaseCell.restype = c_int
libh3.h3GetBaseCell.argtypes = [c_long]

libh3.h3IsResClassIII.restype = c_int
libh3.h3IsResClassIII.argtypes = [c_long]

libh3.h3IsPentagon.restype = c_int
libh3.h3IsPentagon.argtypes = [c_long]

libh3.h3IndexesAreNeighbors.restype = c_int
libh3.h3IndexesAreNeighbors.argtypes = [c_long, c_long]

libh3.getH3UnidirectionalEdge.restype = c_long
libh3.getH3UnidirectionalEdge.argtypes = [c_long, c_long]

libh3.h3UnidirectionalEdgeIsValid.restype = c_int
libh3.h3UnidirectionalEdgeIsValid.argtypes = [c_long]

libh3.getOriginH3IndexFromUnidirectionalEdge.restype = c_long
libh3.getOriginH3IndexFromUnidirectionalEdge.argtypes = [c_long]

libh3.getDestinationH3IndexFromUnidirectionalEdge.restype = c_long
libh3.getDestinationH3IndexFromUnidirectionalEdge.argtypes = [c_long]

libh3.getH3IndexesFromUnidirectionalEdge.restype = None
libh3.getH3IndexesFromUnidirectionalEdge.argtypes = [c_long, c_void_p]

libh3.getH3UnidirectionalEdgesFromHexagon.restype = None
libh3.getH3UnidirectionalEdgesFromHexagon.argtypes = [c_long, c_void_p]

libh3.getH3UnidirectionalEdgeBoundary.restype = None
libh3.getH3UnidirectionalEdgeBoundary.argtypes = [c_long, c_void_p]

libh3.h3Distance.restype = c_int
libh3.h3Distance.argtypes = [c_long, c_long]


def string_to_h3(h3_address):
    return int(h3_address, 16)


def h3_to_string(h3_int):
    return hex(h3_int)[2:]


def h3_is_valid(h3_address):
    """Validates an `h3_address`

    :returns: boolean
    """
    try:
        return libh3.h3IsValid(string_to_h3(h3_address)) == 1
    except Exception:
        return False


def h3_get_resolution(h3_address):
    """Returns the resolution of an `h3_address`

    :return: nibble (0-15)
    """
    return int(h3_address[1], 16)


def degs_to_rads(deg):
    """Helper degrees to radians"""
    return deg * math.pi / 180.0


def rads_to_degs(rad):
    """Helper radians to degrees"""
    return rad * 180.0 / math.pi


def mercator_lat(lat):
    """Helper coerce lat range"""
    return lat - 180 if lat > 90 else lat


def mercator_lng(lng):
    """Helper coerce lng range"""
    return lng - 360 if lng > 180 else lng


def hexagon_c_array_to_set(h3_addresses):
    return {
        h3_to_string(hexagon_address)
        for hexagon_address in h3_addresses if hexagon_address != 0
    }  # Turn it into a regular python set


def geo_to_h3(lat, lng, res):
    """Index a geo-coordinate at a resolution into an h3 address"""
    geo_coord = GeoCoord(
        degs_to_rads(mercator_lat(lat)), degs_to_rads(mercator_lng(lng)))
    return h3_to_string(libh3.geoToH3(byref(geo_coord), res))


def h3_to_geo(h3_address):
    """Reverse lookup an h3 address into a geo-coordinate"""
    geo_coord = GeoCoord()
    libh3.h3ToGeo(string_to_h3(h3_address), byref(geo_coord))
    return [
        mercator_lat(rads_to_degs(geo_coord.lat)),
        mercator_lng(rads_to_degs(geo_coord.lng))
    ]


def h3_to_geo_boundary(h3_address, geo_json=False):
    """Compose an array of geo-coordinates that outlines a hexagonal cell"""
    geo_boundary = GeoBoundary()
    libh3.h3ToGeoBoundary(string_to_h3(h3_address), byref(geo_boundary))
    out = []
    for i in range(geo_boundary.num_verts):
        out.append([
            mercator_lng(rads_to_degs(geo_boundary.verts[i].lng)),
            mercator_lat(rads_to_degs(geo_boundary.verts[i].lat))
        ]) if geo_json else out.append([
            mercator_lat(rads_to_degs(geo_boundary.verts[i].lat)),
            mercator_lng(rads_to_degs(geo_boundary.verts[i].lng))
        ])
    if geo_json:
        out.append(out[0])
    return out


def k_ring(h3_address, ring_size):
    """Get K-Rings for a given hexagon"""
    array_len = libh3.maxKringSize(ring_size)
    KringArray = c_long * array_len
    # Initializes to zeroes by default, don't need to force
    krings = KringArray()
    libh3.kRing(string_to_h3(h3_address), ring_size, krings)
    return hexagon_c_array_to_set(krings)


def k_ring_distances(h3_address, ring_size):
    """Get K-Rings for a given hexagon properly split by ring"""
    array_len = libh3.maxKringSize(ring_size)
    KringArray = c_long * array_len
    DistanceArray = c_int * array_len
    # Initializes to zeroes by default, don't need to force
    krings = KringArray()
    distances = DistanceArray()
    libh3.kRingDistances(
        string_to_h3(h3_address), ring_size, krings, distances)
    out = []
    for i in range(0, ring_size + 1):
        out.append(set([]))
    for i in range(0, array_len):
        ring_index = distances[i]
        out[ring_index].add(h3_to_string(krings[i]))
    return out


def _coord_array_to_geo_coord(coord_array, geo_json_conformant=False):
    if geo_json_conformant:
        lng = coord_array[0]
        lat = coord_array[1]
    else:
        lat = coord_array[0]
        lng = coord_array[1]

    return GeoCoord(
        degs_to_rads(mercator_lat(lat)), degs_to_rads(mercator_lng(lng)))


def _polygon_array_to_geofence(polygon_array, geo_json_conformant=False):
    num_verts = len(polygon_array)
    GeoCoordArray = GeoCoord * num_verts
    geo_coord_array = GeoCoordArray()
    for i in range(num_verts):
        geo_coord_array[i] = _coord_array_to_geo_coord(polygon_array[i],
                                                       geo_json_conformant)

    return Geofence(num_verts, cast(geo_coord_array, c_void_p))


def _geo_json_to_geo_json_lite(geo_json, geo_json_conformant=False):
    if geo_json['type'] != 'Polygon':
        raise Exception('Only Polygon GeoJSON supported')
    num_holes = len(geo_json['coordinates']) - 1
    geofence = _polygon_array_to_geofence(geo_json['coordinates'][0],
                                          geo_json_conformant)
    holes = None
    if num_holes > 0:
        Holes = Geofence * num_holes
        holes = Holes()
        for i in range(num_holes):
            holes[i] = _polygon_array_to_geofence(
                geo_json['coordinates'][i + 1], geo_json_conformant)

    return GeoJsonLite(geofence, num_holes, cast(holes, c_void_p))


def polyfill(geo_json, res, geo_json_conformant=False):
    """
    Get hexagons for a given GeoJSON region

    :param geo_json dict: A GeoJSON dictionary
    :param res int: The hexagon resolution to use (0-15)
    :param geo_json_conformant bool: Determines (lat, lng) vs (lng, lat)
        ordering Default is false, which is (lat, lng) ordering, violating
        the spec http://geojson.org/geojson-spec.html#id2 which is (lng, lat)

    :returns: Set of hex addresses
    """
    geo_json_lite = _geo_json_to_geo_json_lite(geo_json, geo_json_conformant)
    array_len = libh3.maxPolyfillSize(byref(geo_json_lite), res)
    HexagonArray = c_long * array_len
    hexagons = HexagonArray()
    libh3.polyfill(byref(geo_json_lite), res, hexagons)
    return hexagon_c_array_to_set(hexagons)


def h3_set_to_multi_polygon(h3_addresses, geo_json=False):
    """
    Get the outlines of a set of H3 hexagons, returned in GeoJSON MultiPolygon
    format (an array of polygons, each with an array of loops, each an array of
    coordinates). Coordinates are returned as [lat, lng] pairs unless GeoJSON
    is requested.

    :param h3_addresses string[]: H3 addresses to get outlines for
    :param geo_json bool: Whether to follow GeoJSON: [lng, lat], closed loops
    :returns: MultiPolygon-style output.
    """
    # Early exit on empty input
    if not h3_addresses or not len(h3_addresses):
        return []
    # Set up input set
    address_count = len(h3_addresses)
    HexagonArray = c_long * address_count
    hexagons = HexagonArray()
    for i, address in enumerate(h3_addresses):
        hexagons[i] = int(address, 16)
    # Allocate memory for output linked polygon (3 pointers: first, last, next)
    polygon = LinkedGeoPolygon()
    # Store a reference to the first polygon - that's the one we need for
    # memory deallocation
    original_polygon = polygon
    libh3.h3SetToLinkedGeo(hexagons, address_count, byref(polygon))
    # Loop through the linked structure, building the output
    output = []
    lat_index = 1 if geo_json else 0
    lng_index = 0 if geo_json else 1
    loops = None
    coords = None
    pair = None
    loop = None
    coord = None
    while polygon:
        loops = []
        output.append(loops)
        # Follow ->first pointer
        loop_ptr = cast(polygon.first, POINTER(LinkedGeoLoop))
        loop = loop_ptr.contents if loop_ptr else None
        while loop:
            coords = []
            loops.append(coords)
            # Follow ->first pointer
            coord_ptr = cast(loop.first, POINTER(LinkedGeoCoord))
            coord = coord_ptr.contents if coord_ptr else None
            while coord:
                pair = [None, None]
                coords.append(pair)
                pair[lat_index] = mercator_lat(rads_to_degs(coord.vertex.lat))
                pair[lng_index] = mercator_lng(rads_to_degs(coord.vertex.lng))
                # Follow ->next pointer
                coord_ptr = cast(coord.next, POINTER(LinkedGeoCoord))
                coord = coord_ptr.contents if coord_ptr else None
            if geo_json:
                # Close loop if GeoJSON is requested
                coords.append(coords[0])
            # Follow ->next pointer
            loop_ptr = cast(loop.next, POINTER(LinkedGeoLoop))
            loop = loop_ptr.contents if loop_ptr else None
        # Follow ->next pointer
        polygon_ptr = cast(polygon.next, POINTER(LinkedGeoPolygon))
        polygon = polygon_ptr.contents if polygon_ptr else None
    # Clean up
    libh3.destroyLinkedPolygon(byref(original_polygon))
    return output


def hex_ring(h3_address, ring_size):
    """
    Get a hexagon ring for a given hexagon.
    Returns individual rings, unlike `k_ring`.

    If a pentagon is reachable, falls back to a
    MUCH slower form based on `k_ring`.
    """

    # This technically should be defined in the C code,
    # but this is much faster
    array_len = 6 * ring_size
    HexRingArray = c_long * array_len
    hex_rings = HexRingArray()
    success = libh3.hexRing(string_to_h3(h3_address), ring_size, hex_rings)
    if success != 0:
        raise Exception(
            'Failed to get hexagon ring for pentagon {}'.format(h3_address))

    return hexagon_c_array_to_set(hex_rings)


def compact(h3_addresses):
    if not h3_addresses or not len(h3_addresses):
        return set()

    num_hexagons = len(h3_addresses)
    HexSetArray = c_long * num_hexagons
    hex_set = HexSetArray()
    compacted_hex_set = HexSetArray()
    for i, address in enumerate(h3_addresses):
        hex_set[i] = int(address, 16)

    ret_val = libh3.compact(hex_set, compacted_hex_set, num_hexagons)
    if ret_val != 0:
        raise Exception(
            'Failed to compact, malformed input data (duplicate hexagons?)')

    return hexagon_c_array_to_set(compacted_hex_set)


def uncompact(h3_addresses, res):
    if not h3_addresses or not len(h3_addresses):
        return set()

    num_hexagons = len(h3_addresses)
    HexSetArray = c_long * num_hexagons
    hex_set = HexSetArray()
    for i, address in enumerate(h3_addresses):
        hex_set[i] = int(address, 16)

    max_uncompacted_num = libh3.maxUncompactSize(hex_set, num_hexagons, res)
    if max_uncompacted_num < 0:
        raise Exception(
            'Failed to determine max uncompact output size (bad resolution?)')
    HexOutSetArray = c_long * max_uncompacted_num
    uncompacted_hex_set = HexOutSetArray()

    ret_val = libh3.uncompact(hex_set, num_hexagons, uncompacted_hex_set,
                              max_uncompacted_num, res)
    if ret_val != 0:  # pragma: no cover
        raise Exception('Failed to uncompact (bad resolution?)')

    return hexagon_c_array_to_set(uncompacted_hex_set)


def h3_to_parent(h3_address, res):
    h3_address_num = string_to_h3(h3_address)
    return h3_to_string(libh3.h3ToParent(h3_address_num, res))


def h3_to_children(h3_address, res):
    h3_address_num = string_to_h3(h3_address)
    max_children = libh3.maxH3ToChildrenSize(h3_address_num, res)
    ChildrenArray = c_long * max_children
    children = ChildrenArray()
    libh3.h3ToChildren(h3_address_num, res, children)

    return hexagon_c_array_to_set(children)


def hex_range(h3_address, ring_size):
    array_len = libh3.maxKringSize(ring_size)
    KringArray = c_long * array_len
    krings = KringArray()
    success = libh3.hexRange(string_to_h3(h3_address), ring_size, krings)
    if success != 0:
        raise ValueError('Specified hexagon range contains a pentagon')
    return hexagon_c_array_to_set(krings)


def hex_range_distances(h3_address, ring_size):
    """
    Get K-Rings for a given hexagon properly split by ring,
    aborting if a pentagon is reached
    """
    array_len = libh3.maxKringSize(ring_size)
    KringArray = c_long * array_len
    DistanceArray = c_int * array_len
    # Initializes to zeroes by default, don't need to force
    krings = KringArray()
    distances = DistanceArray()
    success = libh3.hexRangeDistances(
        string_to_h3(h3_address),
        ring_size,
        krings,
        distances,
    )
    if success != 0:
        raise ValueError('Specified hexagon range contains a pentagon')
    out = []
    for i in range(0, ring_size + 1):
        out.append(set([]))
    for i in range(0, array_len):
        ring_index = distances[i]
        out[ring_index].add(h3_to_string(krings[i]))
    return out


def hex_ranges(h3_address_list, ring_size):
    """
    Get K-Rings for all hexagons properly split by ring,
    aborting if a pentagon is reached
    """
    num_hexagons = len(h3_address_list)
    array_len = num_hexagons * libh3.maxKringSize(ring_size)
    HexArray = c_long * num_hexagons
    KringArray = c_long * array_len
    # Initializes to zeroes by default, don't need to force
    hex_array = HexArray(
        *[string_to_h3(h3_address) for h3_address in h3_address_list])
    krings = KringArray()
    success = libh3.hexRanges(
        hex_array,
        num_hexagons,
        ring_size,
        krings,
    )
    if success != 0:
        raise ValueError(
            'One of the specified hexagon ranges contains a pentagon')
    out = {}
    for i in range(0, num_hexagons):
        h3_address = h3_address_list[i]
        hex_range_list = []
        out[h3_address] = hex_range_list
        for j in range(0, ring_size + 1):
            hex_range_list.append(set([]))
        ring_index = 0
        ring_end = 0
        range_size = int(array_len / num_hexagons)
        for j in range(0, range_size):
            if j > ring_end:
                ring_index = ring_index + 1
                ring_end = ring_end + 6 * ring_index
            # hexRanges doesn't return distance array
            hex_range_list[ring_index].add(
                h3_to_string(krings[i * range_size + j]))
    return out


def hex_area(resolution, unit='km^2'):
    if unit == 'km^2':
        return libh3.hexAreaKm2(resolution)
    elif unit == 'm^2':
        return libh3.hexAreaM2(resolution)
    else:
        raise ValueError(
            'Provided unit not supported, must be "km^2" or "m^2"')


def edge_length(resolution, unit='km'):
    if unit == 'km':
        return libh3.edgeLengthKm(resolution)
    elif unit == 'm':
        return libh3.edgeLengthM(resolution)
    else:
        raise ValueError('Provided unit not supported, must be "km" or "m"')


def num_hexagons(resolution):
    return libh3.numHexagons(resolution)


def h3_get_base_cell(h3_address):
    return libh3.h3GetBaseCell(string_to_h3(h3_address))


def h3_is_res_class_iii(h3_address):
    return libh3.h3IsResClassIII(string_to_h3(h3_address)) == 1


def h3_is_res_class_III(h3_address):
    return h3_is_res_class_iii(h3_address)


def h3_is_pentagon(h3_address):
    return libh3.h3IsPentagon(string_to_h3(h3_address)) == 1


def h3_indexes_are_neighbors(a, b):
    return libh3.h3IndexesAreNeighbors(string_to_h3(a), string_to_h3(b)) == 1


def get_h3_unidirectional_edge(a, b):
    edge_int = libh3.getH3UnidirectionalEdge(
        string_to_h3(a),
        string_to_h3(b),
    )
    if edge_int == 0:
        raise ValueError(
            'Provided H3Indexes are not hexagons or not neighbors')
    return h3_to_string(edge_int)


def h3_unidirectional_edge_is_valid(h3_address):
    return libh3.h3UnidirectionalEdgeIsValid(string_to_h3(h3_address)) == 1


def get_origin_h3_index_from_unidirectional_edge(h3_address):
    origin_int = libh3.getOriginH3IndexFromUnidirectionalEdge(
        string_to_h3(h3_address))
    if origin_int == 0:
        raise ValueError('Provided H3Index is not a Unidirectional Edge index')
    return h3_to_string(origin_int)


def get_destination_h3_index_from_unidirectional_edge(h3_address):
    destination_int = libh3.getDestinationH3IndexFromUnidirectionalEdge(
        string_to_h3(h3_address))
    if destination_int == 0:
        raise ValueError('Provided H3Index is not a Unidirectional Edge index')
    return h3_to_string(destination_int)


def get_h3_indexes_from_unidirectional_edge(h3_address):
    IndexArray = c_long * 2
    index_array = IndexArray()
    libh3.getH3IndexesFromUnidirectionalEdge(
        string_to_h3(h3_address), index_array)
    if index_array[0] == 0 or index_array[1] == 0:
        raise ValueError('Provided H3Index is not a Unidirectional Edge index')
    return [h3_to_string(h3_int) for h3_int in index_array]


def get_h3_unidirectional_edges_from_hexagon(h3_address):
    IndexArray = c_long * 6
    index_array = IndexArray()
    libh3.getH3UnidirectionalEdgesFromHexagon(
        string_to_h3(h3_address), index_array)
    zero_count = 0
    for h3_int in index_array:
        if h3_int == 0:
            zero_count = zero_count + 1
    if zero_count > 1:
        raise ValueError('Provided H3Index is not a Hexagon index')
    return [h3_to_string(h3_int) for h3_int in index_array if h3_int != 0]


def get_h3_unidirectional_edge_boundary(h3_address, geo_json=False):
    """Compose an array of geo-coordinates that defines a hexagonal edge"""
    geo_boundary = GeoBoundary()
    libh3.getH3UnidirectionalEdgeBoundary(
        string_to_h3(h3_address), byref(geo_boundary))
    out = []
    for i in range(geo_boundary.num_verts):
        out.append([
            mercator_lng(rads_to_degs(geo_boundary.verts[i].lng)),
            mercator_lat(rads_to_degs(geo_boundary.verts[i].lat))
        ]) if geo_json else out.append([
            mercator_lat(rads_to_degs(geo_boundary.verts[i].lat)),
            mercator_lng(rads_to_degs(geo_boundary.verts[i].lng))
        ])
    if geo_json:
        out.append(out[0])
    return out


def h3_distance(h3_address_origin, h3_address_h3):
    return libh3.h3Distance(
        string_to_h3(h3_address_origin), string_to_h3(h3_address_h3))
