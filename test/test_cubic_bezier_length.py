from __future__ import print_function

import unittest
from random import *

from svgelements import *


def get_random_cubic_bezier():
    return CubicBezier((random() * 50, random() * 50), (random() * 50, random() * 50),
                       (random() * 50, random() * 50), (random() * 50, random() * 50))


class TestElementCubicBezierLength(unittest.TestCase):

    def test_cubic_bezier_length(self):
        for _ in range(100):
            b = get_random_cubic_bezier()
            l1 = b._length_scipy()
            l2 = b._length_default()
            self.assertAlmostEqual(l1, l2)
