from __future__ import print_function

import unittest

from svgelements import *


class TestElementLinear(unittest.TestCase):

    def test_linear_nearest(self):
        line = Line((0,0),(5,0))
        r = line.closest_segment_point((17,0))
        self.assertEqual(r, (5,0))
        r = line.closest_segment_point((2, 2))
        self.assertEqual(r, (2, 0))


class TestBoundingBox(unittest.TestCase):

    def test_linear_bbox(self):
        line = Line((0,0), (5,0))
        r = line.bbox()
        self.assertEqual(r, (0, 0, 5, 0))

    def test_qbezier_bbox(self):
        line = QuadraticBezier((0,0), (2,2), (5,0))
        r = line.bbox()
        self.assertEqual(r, (0, 0, 5, 1))

    def test_cbezier_bbox(self):
        line = CubicBezier((0,0), (2,2), (2,-2), (5,0))
        r = line.bbox()
        for z in zip(r, (0.0, -0.5773502691896257, 5.0, 0.5773502691896257)):
            self.assertAlmostEqual(*z)

    def test_arc_bbox(self):
        line = Arc((0,0), (5,0), control=(2.5, 2.5))
        r = line.bbox()
        for z in zip(r, (0.0, 0, 5.0, 2.5)):
            self.assertAlmostEqual(*z)

    def test_null_arc_bbox(self):
        self.assertEqual(Path("M0,0A0,0 0 0 0 0,0z").bbox(), (0,0,0,0))

