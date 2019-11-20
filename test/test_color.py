from __future__ import print_function

import unittest

from svg.elements import *


class TestElementColor(unittest.TestCase):

    def test_color(self):
        r0 = Color.parse('red')
        r1 = Color.parse('#F00')
        r2 = Color.parse('#FF0000')
        self.assertEqual(r0, r1)
        self.assertEqual(r0, r2)

