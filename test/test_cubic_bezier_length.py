from __future__ import print_function

import unittest
from random import *

from svgelements import *


def get_random_cubic_bezier():
    return CubicBezier((random() * 50, random() * 50), (random() * 50, random() * 50),
                       (random() * 50, random() * 50), (random() * 50, random() * 50))


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
