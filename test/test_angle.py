from __future__ import print_function

import unittest

from svgelements import *


class TestElementAngle(unittest.TestCase):
    """These tests ensure the basic functions of the Angle element."""

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

    def test_orth(self):
        self.assertTrue(Angle.degrees(0).is_orthogonal())
        self.assertTrue(Angle.degrees(90).is_orthogonal())
        self.assertTrue(Angle.degrees(180).is_orthogonal())
        self.assertTrue(Angle.degrees(270).is_orthogonal())
        self.assertTrue(Angle.degrees(360).is_orthogonal())

        self.assertFalse(Angle.degrees(1).is_orthogonal())
        self.assertFalse(Angle.degrees(91).is_orthogonal())
        self.assertFalse(Angle.degrees(181).is_orthogonal())
        self.assertFalse(Angle.degrees(271).is_orthogonal())
        self.assertFalse(Angle.degrees(361).is_orthogonal())
