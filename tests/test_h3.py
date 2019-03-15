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
'''

import pytest
import unittest

from h3 import h3


class TestH3Core(unittest.TestCase):
    def shift_circular_list(self, start_element, elements_list):
        # We shift the circular list so that it starts from start_element,
        start_index = elements_list.index(start_element)
        return elements_list[start_index:] + elements_list[:start_index]

    def test_h3_is_valid(self):
        self.assertTrue(
            h3.h3_is_valid('85283473fffffff'),
            'H3 Address is considered an address'
        )
        self.assertTrue(
            h3.h3_is_valid('850dab63fffffff'),
            'H3 Address from Java test also valid'
        )
        self.assertFalse(
            h3.h3_is_valid('lolwut'),
            'Random string is not considered an address'
        )
        self.assertFalse(
            h3.h3_is_valid('5004295803a88'),
            'H3 0.x Addresses are not considered valid'
        )
        for res in range(16):
            self.assertTrue(
                h3.h3_is_valid(h3.geo_to_h3(37, -122, res)),
                'H3 Address is considered an address'
            )

    def test_geo_to_h3(self):
        self.assertEqual(
            h3.geo_to_h3(37.3615593, -122.0553238, 5), '85283473fffffff',
            'Got the expected H3 address back'
        )

    def test_h3_get_resolution(self):
        for res in range(16):
            h3_address = h3.geo_to_h3(37.3615593, -122.0553238, res)
            self.assertEqual(
                h3.h3_get_resolution(h3_address), res,
                'Got the expected H3 resolution back'
            )

    def test_silly_geo_to_h3(self):
        self.assertEqual(
            h3.geo_to_h3(37.3615593 + 180.0, -122.0553238 + 360.0, 5),
            '85283473fffffff', 'world-wrapping lat, lng corrected'
        )

    def test_h3_to_geo(self):
        latlng = h3.h3_to_geo('85283473fffffff')
        self.assertAlmostEqual(
            latlng[0], 37.34579337536848, None, 'lat center is ok'
        )
        self.assertAlmostEqual(
            latlng[1], -121.97637597255124, None, 'lng center is ok'
        )

    def test_h3_to_geo_boundary(self):
        latlngs = h3.h3_to_geo_boundary('85283473fffffff')
        expectedlatlngs = [
            [37.271355866731895,
             -121.91508032705622], [37.353926450852256, -121.86222328902491], [
                37.42834118609435, -121.9235499963016
            ], [37.42012867767778,
                -122.0377349642703], [37.33755608435298, -122.09042892904395],
            [37.26319797461824, -122.02910130919]
        ]
        self.assertEqual(
            len(latlngs), len(expectedlatlngs),
            'got the expected number of vertices'
        )
        for i in range(len(latlngs)):
            self.assertAlmostEqual(
                latlngs[i][0], expectedlatlngs[i][0], None, 'lat is ok'
            )
            self.assertAlmostEqual(
                latlngs[i][1], expectedlatlngs[i][1], None, 'lng is ok'
            )

    def test_h3_to_geo_boundary_geo_json(self):
        lnglats = h3.h3_to_geo_boundary('85283473fffffff', True)
        expectedlnglats = [
            [-121.91508032705622, 37.271355866731895],
            [-121.86222328902491, 37.353926450852256],
            [-121.9235499963016, 37.42834118609435],
            [-122.0377349642703, 37.42012867767778],
            [-122.09042892904395, 37.33755608435298],
            [-122.02910130919, 37.26319797461824],
            [-121.91508032705622, 37.271355866731895],
        ]
        self.assertEqual(
            len(lnglats), len(expectedlnglats),
            'got the expected number of vertices'
        )
        for i in range(len(lnglats)):
            self.assertAlmostEqual(
                lnglats[i][0], expectedlnglats[i][0], None, 'lng is ok'
            )
            self.assertAlmostEqual(
                lnglats[i][1], expectedlnglats[i][1], None, 'lat is ok'
            )

    def test_k_ring(self):
        hexagons = h3.k_ring('8928308280fffff', 1)
        self.assertEqual(
            1 + 6, len(hexagons),
            'got the expected number of hexagons for a single ring'
        )
        expected_hexagons = [
            '8928308280fffff',
            '8928308280bffff',
            '89283082807ffff',
            '89283082877ffff',
            '89283082803ffff',
            '89283082873ffff',
            '8928308283bffff',
        ]
        for hexagon in expected_hexagons:
            self.assertIn(hexagon, hexagons, 'found an expected hexagon')

    def test_k_ring2(self):
        hexagons = h3.k_ring('8928308280fffff', 2)
        self.assertEqual(
            1 + 6 + 12, len(hexagons),
            'got the expected number of hexagons for two rings'
        )
        expected_hexagons = [
            '89283082813ffff',
            '89283082817ffff',
            '8928308281bffff',
            '89283082863ffff',
            '89283082823ffff',
            '89283082873ffff',
            '89283082877ffff',
            '8928308287bffff',
            '89283082833ffff',
            '8928308282bffff',
            '8928308283bffff',
            '89283082857ffff',
            '892830828abffff',
            '89283082847ffff',
            '89283082867ffff',
            '89283082803ffff',
            '89283082807ffff',
            '8928308280bffff',
            '8928308280fffff',
        ]
        for hexagon in expected_hexagons:
            self.assertIn(hexagon, hexagons, 'found an expected hexagon')

    def test_k_ring_pentagon(self):
        hexagons = h3.k_ring('821c07fffffffff', 1)
        self.assertEqual(
            1 + 5, len(hexagons),
            'got the expected number for a single ring around a pentagon'
        )
        expected_hexagons = [
            '821c2ffffffffff',
            '821c27fffffffff',
            '821c07fffffffff',
            '821c17fffffffff',
            '821c1ffffffffff',
            '821c37fffffffff',
        ]
        for hexagon in expected_hexagons:
            self.assertIn(hexagon, hexagons, 'found an expected hexagon')

    def test_k_ring_distances(self):
        hexagons = h3.k_ring_distances('8928308280fffff', 1)

        self.assertEqual(2, len(hexagons))
        self.assertEqual(1, len(hexagons[0]))
        self.assertEqual(6, len(hexagons[1]))

        self.assertTrue('8928308280fffff' in hexagons[0])
        self.assertTrue('8928308280bffff' in hexagons[1])
        self.assertTrue('89283082807ffff' in hexagons[1])
        self.assertTrue('89283082877ffff' in hexagons[1])
        self.assertTrue('89283082803ffff' in hexagons[1])
        self.assertTrue('89283082873ffff' in hexagons[1])
        self.assertTrue('8928308283bffff' in hexagons[1])

    def test_polyfill(self):
        hexagons = h3.polyfill(
            {
                'type':
                    'Polygon',
                'coordinates': [
                    [
                        [37.813318999983238, -122.4089866999972145], [
                        37.7866302000007224, -122.3805436999997056
                    ], [37.7198061999978478, -122.3544736999993603], [
                        37.7076131999975672, -122.5123436999983966
                    ], [37.7835871999971715, -122.5247187000021967],
                        [37.8151571999998453, -122.4798767000009008]
                    ]
                ]
            }, 9
        )
        self.assertGreater(
            len(hexagons), 1000, 'got an appropriate number of hexagons back'
        )

    def test_polyfill_bogus_geo_json(self):
        self.assertRaises(
            Exception,
            lambda: h3.polyfill({'type': 'whatwhat'}, 9)
        )

    def test_polyfill_with_hole(self):
        hexagons = h3.polyfill(
            {
                'type':
                    'Polygon',
                'coordinates': [
                    [
                        [37.813318999983238, -122.4089866999972145], [
                        37.7866302000007224, -122.3805436999997056
                    ], [37.7198061999978478, -122.3544736999993603], [
                        37.7076131999975672, -122.5123436999983966
                    ], [37.7835871999971715, -122.5247187000021967],
                        [37.8151571999998453, -122.4798767000009008]
                    ], [
                        [37.7869802, -122.4471197], [37.7664102, -122.4590777],
                        [37.7710682, -122.4137097]
                    ]
                ]
            }, 9
        )
        self.assertGreater(
            len(hexagons), 1000, 'got an appropriate number of hexagons back'
        )

    def test_polyfill_with_two_holes(self):
        hexagons = h3.polyfill(
            {
                'type':
                    'Polygon',
                'coordinates': [
                    [
                        [37.813318999983238, -122.4089866999972145], [
                        37.7866302000007224, -122.3805436999997056
                    ], [37.7198061999978478, -122.3544736999993603], [
                        37.7076131999975672, -122.5123436999983966
                    ], [37.7835871999971715, -122.5247187000021967],
                        [37.8151571999998453, -122.4798767000009008]
                    ], [
                        [37.7869802, -122.4471197], [37.7664102, -122.4590777],
                        [37.7710682, -122.4137097]
                    ], [
                        [37.747976, -122.490025], [37.731550, -122.503758],
                        [37.725440, -122.452603]
                    ]
                ]
            }, 9
        )
        self.assertGreater(
            len(hexagons), 1000, 'got an appropriate number of hexagons back'
        )

    def test_polyfill_geo_json_compliant(self):
        hexagons = h3.polyfill(
            {
                'type':
                    'Polygon',
                'coordinates': [
                    [
                        [-122.4089866999972145, 37.813318999983238], [
                        -122.3805436999997056, 37.7866302000007224
                    ], [-122.3544736999993603, 37.7198061999978478], [
                        -122.5123436999983966, 37.7076131999975672
                    ], [-122.5247187000021967, 37.7835871999971715],
                        [-122.4798767000009008, 37.8151571999998453]
                    ]
                ]
            }, 9, True
        )
        self.assertGreater(
            len(hexagons), 1000, 'got an appropriate number of hexagons back'
        )

    def test_polyfill_down_under(self):
        hexagons = h3.polyfill(
            {
                'type':
                    'Polygon',
                'coordinates': [
                    [
                        [151.1979259, -33.8555555], [151.2074556, -33.8519779],
                        [151.224743, -33.8579597], [151.2254986, -33.8582212], [
                        151.235313348, -33.8564183032
                    ], [151.234799568, -33.8594049408], [
                        151.233485084, -33.8641069037
                    ], [151.233181742, -33.8715791334], [
                        151.223980353, -33.8876967719
                    ], [151.219388501, -33.8873877027], [
                        151.2189209, -33.8869995
                    ], [151.2181177, -33.886283399999996
                        ], [151.2157995, -33.8851287],
                        [151.2156925, -33.8852471], [151.2141233, -33.8851287],
                        [151.2116267, -33.8847438], [151.2083456, -33.8834707],
                        [151.2080246, -33.8827601], [151.2059204, -33.8816053],
                        [151.2043868, -33.8827601], [151.2028176, -33.8838556],
                        [151.2022826, -33.8839148], [151.2011057, -33.8842405],
                        [151.1986114, -33.8842819], [151.1986091, -33.8842405],
                        [151.1948287, -33.8773416], [151.1923322, -33.8740845],
                        [151.1850566, -33.8697019], [151.1902636, -33.8625354],
                        [151.1986805, -33.8612915], [151.1979259, -33.8555555]
                    ]
                ]
            }, 9, True
        )
        self.assertGreater(
            len(hexagons), 10, 'got an appropriate number of hexagons back'
        )

    def test_polyfill_far_east(self):
        hexagons = h3.polyfill(
            {
                "type":
                    "Polygon",
                "coordinates": [
                    [
                        [142.86483764648438, 41.92578147109541], [
                        142.86483764648438, 42.29965889253408
                    ], [143.41552734375, 42.29965889253408], [
                        143.41552734375, 41.92578147109541
                    ], [142.86483764648438, 41.92578147109541]
                    ]
                ]
            }, 9, True
        )
        self.assertGreater(
            len(hexagons), 10, 'got an appropriate number of hexagons back'
        )

    def test_polyfill_southern_tip(self):
        hexagons = h3.polyfill(
            {
                "type":
                    "Polygon",
                "coordinates": [
                    [
                        [-67.642822265625, -55.41654360858007], [
                        -67.642822265625, -54.354955689554096
                    ], [-64.742431640625, -54.354955689554096], [
                        -64.742431640625, -55.41654360858007
                    ], [-67.642822265625, -55.41654360858007]
                    ]
                ]
            }, 9, True
        )
        self.assertGreater(
            len(hexagons), 10, 'got an appropriate number of hexagons back'
        )

    def test_polyfill_null_island(self):
        hexagons = h3.polyfill(
            {
                "type":
                    "Polygon",
                "coordinates": [
                    [
                        [-3.218994140625, -3.0856655287215378], [
                        -3.218994140625, 3.6888551431470478
                    ], [3.5815429687499996, 3.6888551431470478], [
                        3.5815429687499996, -3.0856655287215378
                    ], [-3.218994140625, -3.0856655287215378]
                    ]
                ]
            }, 4, True
        )
        self.assertGreater(
            len(hexagons), 10, 'got an appropriate number of hexagons back'
        )

    def test_h3_set_to_multi_polygon_empty(self):
        h3_addresses = []
        multi_polygon = h3.h3_set_to_multi_polygon(h3_addresses)

        self.assertEqual(multi_polygon, [], 'no hexagons yields an empty array')

    def test_h3_set_to_multi_polygon_single(self):
        h3_addresses = ['89283082837ffff']
        multi_polygon = h3.h3_set_to_multi_polygon(h3_addresses)
        vertices = h3.h3_to_geo_boundary(h3_addresses[0])

        # We shift the expected circular list so that it starts from multi_polygon[0][0][0],
        # since output starting from any vertex would be correct as long as it's in order.
        expected_coords = self.shift_circular_list(multi_polygon[0][0][0],
                                                   [
                                                       vertices[2], vertices[3], vertices[4], vertices[5],
                                                       vertices[0], vertices[1]
                                                   ])
        expected = [
            [
                expected_coords
            ]
        ]

        self.assertEqual(multi_polygon, expected, 'outline matches expected')

    def test_h3_set_to_multi_polygon_single_geo_json(self):
        h3_addresses = ['89283082837ffff']
        multi_polygon = h3.h3_set_to_multi_polygon(h3_addresses, True)
        vertices = h3.h3_to_geo_boundary(h3_addresses[0], True)

        # We shift the expected circular list so that it starts from multi_polygon[0][0][0],
        # since output starting from any vertex would be correct as long as it's in order.
        expected_coords = self.shift_circular_list(multi_polygon[0][0][0],
                                                   [
                                                       vertices[2], vertices[3], vertices[4], vertices[5],
                                                       vertices[0], vertices[1]
                                                   ])
        expected = [
            [
                expected_coords
            ]
        ]

        self.assertEqual(
            len(multi_polygon), 1, 'polygon count matches expected'
        )
        self.assertEqual(
            len(multi_polygon[0]), 1, 'loop count matches expected'
        )
        self.assertEqual(
            len(multi_polygon[0][0]), 7,
            'coord count 7 matches expected according to geojson format'
        )
        self.assertEqual(
            multi_polygon[0], multi_polygon[-1],
            'first coord should be the same as last coord according to geojson format'
        )
        self.assertAlmostEqual(
            multi_polygon[0][0][0][0], -122.42778275313199, None,
            'the coord should be (lng, lat) according to geojson format (1)'
        )
        self.assertAlmostEqual(
            multi_polygon[0][0][0][1], 37.77598951883773, None,
            'the coord should be (lng, lat) according to geojson format (2)'
        )
        # Discard last coord for testing below, since last coord is the same as the first one
        multi_polygon[0][0].pop()

        self.assertEqual(multi_polygon, expected, 'outline matches expected')

    def test_h3_set_to_multi_polygon_contiguous(self):
        # the second hexagon shares v0 and v1 with the first
        h3_addresses = ['89283082837ffff', '89283082833ffff']

        multi_polygon = h3.h3_set_to_multi_polygon(h3_addresses)
        vertices0 = h3.h3_to_geo_boundary(h3_addresses[0])
        vertices1 = h3.h3_to_geo_boundary(h3_addresses[1])

        # We shift the expected circular list so that it starts from multi_polygon[0][0][0],
        # since output starting from any vertex would be correct as long as it's in order.
        expected_coords = self.shift_circular_list(multi_polygon[0][0][0],
                                                   [
                                                       vertices1[0], vertices1[1], vertices1[2], vertices0[1],
                                                       vertices0[2],
                                                       vertices0[3], vertices0[4], vertices0[5], vertices1[4],
                                                       vertices1[5],
                                                   ])
        expected = [
            [
                expected_coords
            ]
        ]

        self.assertEqual(
            len(multi_polygon), 1, 'polygon count matches expected'
        )
        self.assertEqual(
            len(multi_polygon[0]), 1, 'loop count matches expected'
        )
        self.assertEqual(
            len(multi_polygon[0][0]), 10, 'coord count 10 matches expected'
        )

        self.assertTrue(multi_polygon == expected, 'outline matches expected')

    def test_h3_set_to_multi_polygon_non_contiguous(self):
        # the second hexagon does not touch the first
        h3_addresses = ['89283082837ffff', '8928308280fffff']
        multi_polygon = h3.h3_set_to_multi_polygon(h3_addresses)

        self.assertEqual(
            len(multi_polygon), 2, 'polygon count matches expected'
        )
        self.assertEqual(
            len(multi_polygon[0]), 1, 'loop count matches expected'
        )
        self.assertEqual(
            len(multi_polygon[0][0]), 6, 'coord count 1 matches expected'
        )
        self.assertEqual(
            len(multi_polygon[1][0]), 6, 'coord count 2 matches expected'
        )

    def test_h3_set_to_multi_polygon_hole(self):
        # Six hexagons in a ring around a hole
        h3_addresses = [
            '892830828c7ffff', '892830828d7ffff', '8928308289bffff',
            '89283082813ffff', '8928308288fffff', '89283082883ffff'
        ]
        multi_polygon = h3.h3_set_to_multi_polygon(h3_addresses)

        self.assertEqual(
            len(multi_polygon), 1, 'polygon count matches expected'
        )
        self.assertEqual(
            len(multi_polygon[0]), 2, 'loop count matches expected'
        )
        self.assertEqual(
            len(multi_polygon[0][0]), 6 * 3,
            'outer coord count matches expected'
        )
        self.assertEqual(
            len(multi_polygon[0][1]), 6, 'inner coord count matches expected'
        )

    def test_h3_set_to_multi_polygon_2k_ring(self):
        # 2-ring in order returned by algo
        h3_addresses = h3.k_ring('8930062838bffff', 2)
        multi_polygon = h3.h3_set_to_multi_polygon(h3_addresses)

        self.assertEqual(
            len(multi_polygon), 1, 'polygon count matches expected'
        )
        self.assertEqual(
            len(multi_polygon[0]), 1, 'loop count matches expected'
        )
        self.assertEqual(
            len(multi_polygon[0][0]), 6 * (2 * 2 + 1),
            'coord count matches expected'
        )

        # Same k-ring in random order
        h3_addresses = [
            '89300628393ffff', '89300628383ffff', '89300628397ffff',
            '89300628067ffff', '89300628387ffff', '893006283bbffff',
            '89300628313ffff', '893006283cfffff', '89300628303ffff',
            '89300628317ffff', '8930062839bffff', '8930062838bffff',
            '8930062806fffff', '8930062838fffff', '893006283d3ffff',
            '893006283c3ffff', '8930062831bffff', '893006283d7ffff',
            '893006283c7ffff'
        ]

        multi_polygon = h3.h3_set_to_multi_polygon(h3_addresses)

        self.assertEqual(
            len(multi_polygon), 1, 'polygon count matches expected'
        )
        self.assertEqual(
            len(multi_polygon[0]), 1, 'loop count matches expected'
        )
        self.assertEqual(
            len(multi_polygon[0][0]), 6 * (2 * 2 + 1),
            'coord count matches expected'
        )

        h3_addresses = list(h3.k_ring('8930062838bffff', 6))
        h3_addresses.sort()
        multi_polygon = h3.h3_set_to_multi_polygon(h3_addresses)

        self.assertEqual(
            len(multi_polygon[0]), 1, 'loop count matches expected'
        )

    def test_hex_ring(self):
        hexagons = h3.hex_ring('8928308280fffff', 1)
        self.assertEqual(
            6, len(hexagons),
            'got the expected number of hexagons for a single ring'
        )
        expected_hexagons = [
            '8928308280bffff',
            '89283082807ffff',
            '89283082877ffff',
            '89283082803ffff',
            '89283082873ffff',
            '8928308283bffff',
        ]
        for hexagon in expected_hexagons:
            self.assertIn(hexagon, hexagons, 'found an expected hexagon')
        self.assertEqual(
            hexagons,
            h3.k_ring('8928308280fffff', 1) - h3.k_ring('8928308280fffff', 0),
            'the fast and slow hex ring paths match'
        )

    def test_hex_ring2(self):
        hexagons = h3.hex_ring('8928308280fffff', 2)
        self.assertEqual(
            12, len(hexagons),
            'got the expected number of hexagons for the second ring'
        )
        expected_hexagons = [
            '89283082813ffff',
            '89283082817ffff',
            '8928308281bffff',
            '89283082863ffff',
            '89283082823ffff',
            '8928308287bffff',
            '89283082833ffff',
            '8928308282bffff',
            '89283082857ffff',
            '892830828abffff',
            '89283082847ffff',
            '89283082867ffff',
        ]
        for hexagon in expected_hexagons:
            self.assertIn(hexagon, hexagons, 'found an expected hexagon')
        self.assertEqual(
            hexagons,
            h3.k_ring('8928308280fffff', 2) - h3.k_ring('8928308280fffff', 1),
            'the fast and slow hex ring paths match'
        )

    def test_hex_ring_pentagon(self):
        try:
            hexagons = h3.hex_ring('821c07fffffffff', 1)
        except Exception as err:
            self.assertEqual(
                str(err),
                "Failed to get hexagon ring for pentagon 821c07fffffffff"
            )

    def test_compact_and_uncompact(self):
        hexagons = h3.polyfill(
            {
                'type':
                    'Polygon',
                'coordinates': [
                    [
                        [37.813318999983238, -122.4089866999972145], [
                        37.7866302000007224, -122.3805436999997056
                    ], [37.7198061999978478, -122.3544736999993603], [
                        37.7076131999975672, -122.5123436999983966
                    ], [37.7835871999971715, -122.5247187000021967],
                        [37.8151571999998453, -122.4798767000009008]
                    ]
                ]
            }, 9
        )
        compactedHexagons = h3.compact(hexagons)
        self.assertEqual(
            len(compactedHexagons), 209,
            'got an appropriate number of hexagons back'
        )
        uncompactedHexagons = h3.uncompact(compactedHexagons, 9)
        self.assertEqual(
            len(uncompactedHexagons), 1253,
            'got an appropriate number of hexagons back'
        )

    def test_compact_and_uncompact_nothing(self):
        compactedNothing = h3.compact([])
        self.assertEqual(len(compactedNothing), 0, 'still nothing')

        uncompactedNothing = h3.uncompact([], 9)
        self.assertEqual(len(uncompactedNothing), 0, 'still nothing')

    def test_uncompact_error(self):
        hexagons = [h3.geo_to_h3(37, -122, 10)]
        with pytest.raises(Exception) as e_info:
            h3.uncompact(hexagons, 5)
        self.assertTrue(isinstance(e_info.value, Exception))

    def test_compact_malformed_input(self):
        with pytest.raises(Exception) as e_info:
            h3.compact(
                [
                    '89283082813ffff',
                    '89283082813ffff',
                    '89283082813ffff',
                    '89283082813ffff',
                    '89283082813ffff',
                    '89283082813ffff',
                    '89283082813ffff',
                    '89283082813ffff',
                    '89283082813ffff',
                    '89283082813ffff',
                    '89283082813ffff',
                    '89283082813ffff',
                    '89283082813ffff',
                ]
            )

        self.assertTrue(isinstance(e_info.value, Exception))

    def test_h3_to_parent(self):
        test_hexagon = '89283082813ffff'
        parent_hexagon = h3.h3_to_parent(test_hexagon, 8)
        self.assertEqual(
            parent_hexagon, '8828308281fffff', 'got the parent back'
        )

    def test_h3_to_children(self):
        test_hexagon = '8828308281fffff'
        children = h3.h3_to_children(test_hexagon, 9)
        self.assertEqual(len(children), 7, 'got all 7 children back')

    def test_hex_range(self):
        hexagons = h3.hex_range('8928308280fffff', 1)
        self.assertEqual(
            1 + 6, len(hexagons),
            'got the expected number of hexagons for a single ring'
        )
        expected_hexagons = [
            '8928308280fffff',
            '8928308280bffff',
            '89283082807ffff',
            '89283082877ffff',
            '89283082803ffff',
            '89283082873ffff',
            '8928308283bffff',
        ]
        for hexagon in expected_hexagons:
            self.assertIn(hexagon, hexagons, 'found an expected hexagon')

    def test_hex_range2(self):
        hexagons = h3.hex_range('8928308280fffff', 2)
        self.assertEqual(
            1 + 6 + 12, len(hexagons),
            'got the expected number of hexagons for two rings'
        )
        expected_hexagons = [
            '89283082813ffff',
            '89283082817ffff',
            '8928308281bffff',
            '89283082863ffff',
            '89283082823ffff',
            '89283082873ffff',
            '89283082877ffff',
            '8928308287bffff',
            '89283082833ffff',
            '8928308282bffff',
            '8928308283bffff',
            '89283082857ffff',
            '892830828abffff',
            '89283082847ffff',
            '89283082867ffff',
            '89283082803ffff',
            '89283082807ffff',
            '8928308280bffff',
            '8928308280fffff',
        ]
        for hexagon in expected_hexagons:
            self.assertIn(hexagon, hexagons, 'found an expected hexagon')

    def test_hex_range_pentagon(self):
        with pytest.raises(ValueError) as e_info:
            h3.hex_range('821c07fffffffff', 1)

        self.assertTrue(isinstance(e_info.value, ValueError))

    def test_hex_range_distances(self):
        hexagons = h3.hex_range_distances('8928308280fffff', 1)

        self.assertEqual(2, len(hexagons))
        self.assertEqual(1, len(hexagons[0]))
        self.assertEqual(6, len(hexagons[1]))

        self.assertTrue('8928308280fffff' in hexagons[0])
        self.assertTrue('8928308280bffff' in hexagons[1])
        self.assertTrue('89283082807ffff' in hexagons[1])
        self.assertTrue('89283082877ffff' in hexagons[1])
        self.assertTrue('89283082803ffff' in hexagons[1])
        self.assertTrue('89283082873ffff' in hexagons[1])
        self.assertTrue('8928308283bffff' in hexagons[1])

    def test_hex_range_distances_pentagon(self):
        with pytest.raises(ValueError) as e_info:
            h3.hex_range_distances('821c07fffffffff', 1)

        self.assertTrue(isinstance(e_info.value, ValueError))

    def test_hex_ranges(self):
        hex_ranges = h3.hex_ranges(['8928308280fffff'], 1)

        self.assertEqual(1, len(list(hex_ranges.keys())))

        hexagons = hex_ranges['8928308280fffff']

        self.assertEqual(2, len(hexagons))
        self.assertEqual(1, len(hexagons[0]))
        self.assertEqual(6, len(hexagons[1]))

        self.assertTrue('8928308280fffff' in hexagons[0])
        self.assertTrue('8928308280bffff' in hexagons[1])
        self.assertTrue('89283082807ffff' in hexagons[1])
        self.assertTrue('89283082877ffff' in hexagons[1])
        self.assertTrue('89283082803ffff' in hexagons[1])
        self.assertTrue('89283082873ffff' in hexagons[1])
        self.assertTrue('8928308283bffff' in hexagons[1])

    def test_hex_ranges_pentagon(self):
        with pytest.raises(ValueError) as e_info:
            h3.hex_ranges(['821c07fffffffff'], 1)

        self.assertTrue(isinstance(e_info.value, ValueError))

    def test_many_hex_ranges(self):
        hex_ranges = h3.hex_ranges(list(h3.k_ring('8928308280fffff', 2)), 2)

        self.assertEqual(19, len(list(hex_ranges.keys())))

        hexagons = hex_ranges['8928308280fffff']

        self.assertEqual(3, len(hexagons))
        self.assertEqual(1, len(hexagons[0]))
        self.assertEqual(6, len(hexagons[1]))
        self.assertEqual(12, len(hexagons[2]))

        hex_ranges_even_larger = h3.hex_ranges(
            list(h3.k_ring('8928308280fffff', 5)), 5
        )
        self.assertEqual(91, len(list(hex_ranges_even_larger.keys())))

        hexagons_larger = hex_ranges_even_larger['8928308280fffff']

        self.assertEqual(6, len(hexagons_larger))
        self.assertEqual(1, len(hexagons_larger[0]))
        self.assertEqual(6, len(hexagons_larger[1]))
        self.assertEqual(12, len(hexagons_larger[2]))
        self.assertEqual(18, len(hexagons_larger[3]))
        self.assertEqual(24, len(hexagons_larger[4]))
        self.assertEqual(30, len(hexagons_larger[5]))

    def test_hex_area(self):
        for i in range(0, 15):
            self.assertTrue(isinstance(h3.hex_area(i), float))
            self.assertTrue(isinstance(h3.hex_area(i, 'm^2'), float))

        with pytest.raises(ValueError) as e_info:
            h3.hex_area(5, 'ft^2')

        self.assertTrue(isinstance(e_info.value, ValueError))

    def test_edge_length(self):
        for i in range(0, 15):
            self.assertTrue(isinstance(h3.edge_length(i), float))
            self.assertTrue(isinstance(h3.edge_length(i, 'm'), float))

        with pytest.raises(ValueError) as e_info:
            h3.edge_length(5, 'ft')

        self.assertTrue(isinstance(e_info.value, ValueError))

    def test_num_hexagons(self):
        for i in range(0, 15):
            self.assertTrue(isinstance(h3.num_hexagons(i), int))

    def test_h3_get_base_cell(self):
        self.assertTrue(isinstance(h3.h3_get_base_cell('8928308280fffff'), int))

    def test_h3_is_res_class_iiiIII(self):
        self.assertTrue(h3.h3_is_res_class_iii('8928308280fffff'))
        self.assertFalse(h3.h3_is_res_class_iii('8828308280fffff'))
        self.assertTrue(h3.h3_is_res_class_III('8928308280fffff'))

    def test_h3_is_pentagon(self):
        self.assertTrue(h3.h3_is_pentagon('821c07fffffffff'))
        self.assertFalse(h3.h3_is_pentagon('8928308280fffff'))

    def test_h3_indexes_are_neighbors(self):
        self.assertTrue(
            h3.h3_indexes_are_neighbors('8928308280fffff', '8928308280bffff')
        )
        self.assertFalse(
            h3.h3_indexes_are_neighbors('821c07fffffffff', '8928308280fffff')
        )

    def test_get_h3_unidirectional_edge(self):
        self.assertTrue(
            isinstance(
                h3.get_h3_unidirectional_edge(
                    '8928308280fffff', '8928308280bffff'
                ), str
            )
        )

        with pytest.raises(ValueError) as e_info:
            h3.get_h3_unidirectional_edge('821c07fffffffff', '8928308280fffff')

        self.assertTrue(isinstance(e_info.value, ValueError))

    def test_h3_unidirectional_edge_is_valid(self):
        self.assertFalse(h3.h3_unidirectional_edge_is_valid('8928308280fffff'))
        self.assertTrue(h3.h3_unidirectional_edge_is_valid('11928308280fffff'))

    def test_get_origin_h3_index_from_unidirectional_edge(self):
        self.assertEqual(
            '8928308280fffff',
            h3.get_origin_h3_index_from_unidirectional_edge('11928308280fffff')
        )

    def test_get_destination_h3_index_from_unidirectional_edge(self):
        self.assertEqual(
            '8928308283bffff',
            h3.get_destination_h3_index_from_unidirectional_edge(
                '11928308280fffff'
            )
        )

    def test_get_h3_indexes_from_unidirectional_edge(self):
        h3_indexes = h3.get_h3_indexes_from_unidirectional_edge(
            '11928308280fffff'
        )

        self.assertEqual(2, len(h3_indexes))
        self.assertEqual('8928308280fffff', h3_indexes[0])
        self.assertEqual('8928308283bffff', h3_indexes[1])

    def test_get_h3_unidirectional_edges_from_hexagon(self):
        h3_uni_edges = h3.get_h3_unidirectional_edges_from_hexagon(
            '8928308280fffff'
        )

        self.assertEqual(6, len(h3_uni_edges))

        h3_uni_edge_pentagon = h3.get_h3_unidirectional_edges_from_hexagon(
            '821c07fffffffff'
        )

        self.assertEqual(5, len(h3_uni_edge_pentagon))

    def test_get_h3_unidirectional_edge_boundary(self):
        boundary = h3.get_h3_unidirectional_edge_boundary('11928308280fffff')

        self.assertEqual(2, len(boundary))

        boundary_geo_json = h3.get_h3_unidirectional_edge_boundary(
            '11928308280fffff', True
        )

        self.assertEqual(3, len(boundary_geo_json))

    def test_h3_distance(self):
        self.assertEqual(
            0, h3.h3_distance('89283082993ffff', '89283082993ffff')
        )
        self.assertEqual(
            1, h3.h3_distance('89283082993ffff', '8928308299bffff')
        )
        self.assertEqual(
            5, h3.h3_distance('89283082993ffff', '89283082827ffff')
        )
