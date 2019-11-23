from __future__ import print_function

import unittest

from svg.elements import *


class TestElementDistance(unittest.TestCase):

    def test_distance(self):
        self.assertAlmostEqual(Distance.parse('10cm'), (Distance.parse('100mm')))
        self.assertNotEqual(Distance.parse("1mm"), 0)
        self.assertNotEqual(Distance.parse("1cm"), 0)
        self.assertNotEqual(Distance.parse("1in"), 0)
        self.assertNotEqual(Distance.parse("1px"), 0)
        self.assertNotEqual(Distance.parse("1pc"), 0)
        self.assertNotEqual(Distance.parse("1pt"), 0)
        self.assertNotEqual(Distance.parse("50%", default_distance=100),0)

    def test_distance_matrix(self):
        m = Matrix("Translate(20mm,50%)", ppi=1000, width=600, height=800)
        self.assertEqual(Matrix(1, 0, 0, 1, 787.402, 400), m)
