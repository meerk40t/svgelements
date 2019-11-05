from __future__ import print_function

import unittest

from svg.elements import *


class TestElementPoint(unittest.TestCase):

    def test_point_init_string(self):
        p = Point("(0,24)")
        self.assertEqual(p, (0,24))
        self.assertEqual(p, 0+24j)
        self.assertEqual(p, [0,24])
        self.assertEqual(p, "(0,24)")
