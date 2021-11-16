import unittest
from random import *

from svgelements import *


def get_random_quadratic_bezier():
    return QuadraticBezier((random() * 50, random() * 50), (random() * 50, random() * 50),
                           (random() * 50, random() * 50))


class TestElementQuadraticBezierPoint(unittest.TestCase):

    def test_quadratic_bezier_point_start_stop(self):
        import numpy as np
        for _ in range(1000):
            b = get_random_quadratic_bezier()
            self.assertEqual(b.start, b.point(0))
            self.assertEqual(b.end, b.point(1))
            self.assertTrue(np.all(np.array([list(b.start), list(b.end)])
                                   == b.npoint([0, 1])))

    def test_quadratic_bezier_point_implementations_match(self):
        import numpy as np
        for _ in range(1000):
            b = get_random_quadratic_bezier()

            pos = np.linspace(0, 1, 100)

            v1 = b.npoint(pos)
            v2 = []
            for i in range(len(pos)):
                v2.append(b.point(pos[i]))

            for p, p1, p2 in zip(pos, v1, v2):
                self.assertEqual(b.point(p), Point(p1))
                self.assertEqual(Point(p1), Point(p2))
