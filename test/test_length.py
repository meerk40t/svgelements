from __future__ import print_function

import unittest

from svg.elements import *


class TestElementLength(unittest.TestCase):

    def test_length_parsing(self):
        self.assertAlmostEqual(Length('10cm'), (Length('100mm')))
        self.assertNotEqual(Length("1mm"), 0)
        self.assertNotEqual(Length("1cm"), 0)
        self.assertNotEqual(Length("1in"), 0)
        self.assertNotEqual(Length("1px"), 0)
        self.assertNotEqual(Length("1pc"), 0)
        self.assertNotEqual(Length("1pt"), 0)
        self.assertNotEqual(Length("1%").value(relative_length=100), 0)
        self.assertEqual(Length("50%").value(relative_length=100), 50.0)

    def test_distance_matrix(self):
        m = Matrix("Translate(20mm,50%)", ppi=1000, width=600, height=800)
        self.assertEqual(Matrix(1, 0, 0, 1, 787.402, 400), m)
