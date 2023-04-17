import random
import unittest
from random import *

from svgelements import *


def get_random_cubic_bezier():
    return CubicBezier(
        (random() * 50, random() * 50),
        (random() * 50, random() * 50),
        (random() * 50, random() * 50),
        (random() * 50, random() * 50),
    )


class TestElementCubicBezierLength(unittest.TestCase):
    def test_cubic_bezier_length(self):
        n = 100
        error = 0
        for _ in range(n):
            b = get_random_cubic_bezier()
            l1 = b._length_scipy()
            l2 = b._length_default(error=1e-6)
            c = abs(l1 - l2)
            error += c
            self.assertAlmostEqual(l1, l2, places=1)
        print("Average cubic-line error: %g" % (error / n))


class TestElementCubicBezierPoint(unittest.TestCase):
    def test_cubic_bezier_point_start_stop(self):
        import numpy as np

        for _ in range(1000):
            b = get_random_cubic_bezier()
            self.assertEqual(b.start, b.point(0))
            self.assertEqual(b.end, b.point(1))
            self.assertTrue(
                np.all(np.array([list(b.start), list(b.end)]) == b.npoint([0, 1]))
            )

    def test_cubic_bezier_point_implementations_match(self):
        import numpy as np

        for _ in range(1000):
            b = get_random_cubic_bezier()

            pos = np.linspace(0, 1, 100)

            v1 = b.npoint(pos)
            v2 = []
            for i in range(len(pos)):
                v2.append(b.point(pos[i]))

            for p, p1, p2 in zip(pos, v1, v2):
                self.assertEqual(b.point(p), Point(p1))
                self.assertEqual(Point(p1), Point(p2))

    def test_cubic_bounds_issue_214(self):
        cubic = CubicBezier(0, -2 - 3j, -1 - 4j, -3j)
        bbox = cubic.bbox()
        self.assertLess(bbox[1], -3)

    def test_cubic_bounds_issue_214_random(self):
        for i in range(100):
            a = random() * 5
            b = random() * 5
            c = random() * 5
            d = a - 3 * b + 3 * c
            cubic1 = CubicBezier(a, b, c, d)
            bbox1 = cubic1.bbox()
            cubic2 = CubicBezier(a, b, c, d + 1e-11)
            bbox2 = cubic2.bbox()
            for a, b in zip(bbox1, bbox2):
                self.assertAlmostEqual(a, b, delta=1e-5)

    def test_cubic_bounds_issue_220(self):
        p = Path(transform=Matrix(682.657124793113, 0.000000000003, -0.000000000003, 682.657124793113, 257913.248909660178, -507946.354527872754))
        p += CubicBezier(start=Point(-117.139521365,1480.99923469), control1=Point(-41.342266634,1505.62725567), control2=Point(40.3422666342,1505.62725567), end=Point(116.139521365,1480.99923469))
        bounds = p.bbox()
        self.assertNotAlmostEquals(bounds[1], bounds[3], delta=100)
