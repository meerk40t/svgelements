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
