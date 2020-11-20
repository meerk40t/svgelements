from __future__ import print_function

import unittest
from random import *

from svgelements import *


def get_random_quadratic_bezier():
    return QuadraticBezier((random() * 50, random() * 50), (random() * 50, random() * 50),
                           (random() * 50, random() * 50))


class TestElementQuadraticBezierPoint(unittest.TestCase):

    def test_quadratic_bezier_point_start_stop(self):
        for _ in range(1000):
            b = get_random_quadratic_bezier()
            self.assertEqual(b.start, b.point(0))
            self.assertEqual(b.end, b.point(1))
            self.assertEqual(b.start, b._point_numpy(np.array([0]))[0])
            self.assertEqual(b.end, b._point_numpy(np.array([1]))[0])

    def test_quadratic_bezier_point_implementations_match(self):
        for _ in range(1000):
            b = get_random_quadratic_bezier()

            pos = np.linspace(0, 1, 100)
            vec_res = b._point_numpy(pos)

            for p, v in zip(pos, vec_res):
                self.assertEqual(b.point(p), v)
