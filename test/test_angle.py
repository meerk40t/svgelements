from __future__ import print_function

import unittest
from random import random

from svg.elements import *


class TestElementAngle(unittest.TestCase):

    def test_angle_init(self):
        self.assertEqual(Angle.degrees(90).as_turns, 0.25)
        self.assertEqual(Angle.degrees(180).as_turns, 0.50)
        self.assertEqual(Angle.degrees(360).as_turns, 1.0)
        self.assertEqual(Angle.degrees(720).as_turns, 2.0)
        self.assertEqual(Angle.radians(tau).as_turns, 1.0)
        self.assertEqual(Angle.radians(tau / 50.0).as_turns, 1.0 / 50.0)
        self.assertEqual(Angle.gradians(100).as_turns, 0.25)
        self.assertEqual(Angle.turns(100).as_turns, 100)
        self.assertEqual(Angle.gradians(100).as_gradians, 100)
        self.assertEqual(Angle.degrees(100).as_degrees, 100)
        self.assertEqual(Angle.radians(100).as_radians, 100)
        self.assertEqual(Angle.parse("90deg").as_radians, tau / 4.0)
        self.assertEqual(Angle.parse("90turn").as_radians, tau * 90)

    def test_angle_equal(self):
        self.assertEqual(Angle.degrees(0), Angle.degrees(-360))
        self.assertEqual(Angle.degrees(0), Angle.degrees(360))
        self.assertEqual(Angle.degrees(0), Angle.degrees(1080))
        self.assertNotEqual(Angle.degrees(0), Angle.degrees(180))
        self.assertEqual(Angle.degrees(0), Angle.turns(5))
