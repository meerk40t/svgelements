import unittest
from random import *

from svgelements import *


def get_random_cubic_bezier():
    return CubicBezier((random() * 50, random() * 50), (random() * 50, random() * 50),
                       (random() * 50, random() * 50), (random() * 50, random() * 50))


class TestElementApproximation(unittest.TestCase):

    def test_cubic_bezier_arc_approximation(self):
        n = 50
        for _ in range(n):
            b = get_random_cubic_bezier()
            path = Move(b.start) + Path([b])
            path2 = Path(path)
            path2.approximate_bezier_with_circular_arcs(error=0.001)
            path2.approximate_arcs_with_cubics(error=0.001)
