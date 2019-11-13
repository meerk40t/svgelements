from __future__ import print_function

import unittest

from svg.elements import *


class TestElementShape(unittest.TestCase):

    def test_ellipse_dict(self):
        values = {
            'tag': 'ellipse',
            'rx': "4.0",
            'ry': "8.0",
            'cx': "22.4",
            'cy': "33.33"
        }
        e = Ellipse(values)
        e2 = Ellipse((22.4, 33.33), 4, 8, 0)
        self.assertEqual(e, e2)
        e3 = Ellipse()
        self.assertNotEqual(e, e3)

    def test_circle_dict(self):
        values = {
            'tag': 'circle',
            'r': "4.0",
            'cx': "22.4",
            'cy': "33.33"
        }
        e = Circle(values)
        e2 = Circle((22.4, 33.33), 4)
        self.assertEqual(e, e2)
        e3 = Circle()
        self.assertNotEqual(e, e3)
