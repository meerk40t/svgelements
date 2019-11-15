from __future__ import print_function

import unittest

from svg.elements import *


class TestElementColor(unittest.TestCase):

    def test_color(self):
        c = 0
        self.assertEqual(Color.parse('red'), Color.parse('#F00'))

