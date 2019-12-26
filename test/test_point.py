from __future__ import print_function

import unittest
from random import random

from svgelements import *


class TestElementPoint(unittest.TestCase):

    def test_point_init_string(self):
        p = Point("(0,24)")
        self.assertEqual(p, (0, 24))
        self.assertEqual(p, 0 + 24j)
        self.assertEqual(p, [0, 24])
        self.assertEqual(p, "(0,24)")

    def test_polar_angle(self):
        for i in range(1000):
            p = Point(random() * 50, random() * 50)
            a = random() * tau - tau / 2
            r = random() * 50
            m = Point.polar(p, a, r)
            self.assertAlmostEqual(Point.angle(p, m), a)

    def test_not_equal_unparsed(self):
        self.assertNotEqual(Point(0,0), "string that doesn't parse to point")
