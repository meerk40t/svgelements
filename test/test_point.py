import unittest
from random import random

from svgelements import *


class TestElementPoint(unittest.TestCase):

    def test_point_init_string(self):
        p = Point("(0,24)")
        self.assertEqual(p, (0, 24))
        self.assertEqual(p, 0 + 24j)
        self.assertEqual(p, [0, 24])
        self.assertEqual(p, "(0,24)")

    def test_polar_angle(self):
        for i in range(1000):
            p = Point(random() * 50, random() * 50)
            a = random() * tau - tau / 2
            r = random() * 50
            m = Point.polar(p, a, r)
            self.assertAlmostEqual(Point.angle(p, m), a)

    def test_not_equal_unparsed(self):
        self.assertNotEqual(Point(0, 0), "string that doesn't parse to point")

    def test_dunder_iadd(self):
        p = Point(0)
        p += (1, 0)
        self.assertEqual(p, (1, 0))
        p += Point(1, 1)
        self.assertEqual(p, (2, 1))
        p += 1 + 2j
        self.assertEqual(p, (3, 3))

        class c:
            def __init__(self):
                self.x = 1
                self.y = 1

        p += c()
        self.assertEqual(p, (4, 4))
        p += Point("-4,-4")
        self.assertEqual(p, (0, 0))
        p += 1
        self.assertEqual(p, (1, 0))
        self.assertRaises(TypeError, 'p += "hello"')

    def test_dunder_isub(self):
        p = Point(0)
        p -= (1, 0)
        self.assertEqual(p, (-1, 0))
        p -= Point(1, 1)
        self.assertEqual(p, (-2, -1))
        p -= 1 + 2j
        self.assertEqual(p, (-3, -3))

        class c:
            def __init__(self):
                self.x = 1
                self.y = 1

        p -= c()
        self.assertEqual(p, (-4, -4))
        p -= Point("-4,-4")
        self.assertEqual(p, (0, 0))
        p -= 1
        self.assertEqual(p, (-1, 0))
        r = p - 1
        self.assertEqual(r, (-2, 0))
        self.assertRaises(TypeError, 'p -= "hello"')

    def test_dunder_add(self):
        p = Point(0)
        p = p + (1, 0)
        self.assertEqual(p, (1, 0))
        p = p + Point(1, 1)
        self.assertEqual(p, (2, 1))
        p = p + 1 + 2j
        self.assertEqual(p, (3, 3))

        class c:
            def __init__(self):
                self.x = 1
                self.y = 1

        p = p + c()
        self.assertEqual(p, (4, 4))
        p = p + Point("-4,-4")
        self.assertEqual(p, (0, 0))
        p = p + 1
        self.assertEqual(p, (1, 0))
        self.assertRaises(TypeError, 'p = p + "hello"')

    def test_dunder_sub(self):
        p = Point(0)
        p = p - (1, 0)
        self.assertEqual(p, (-1, 0))
        p = p - Point(1, 1)
        self.assertEqual(p, (-2, -1))
        p = p - (1 + 2j)
        self.assertEqual(p, (-3, -3))

        class c:
            def __init__(self):
                self.x = 1
                self.y = 1

        p = p - c()
        self.assertEqual(p, (-4, -4))
        p = p - Point("-4,-4")
        self.assertEqual(p, (0, 0))
        p = p - 1
        self.assertEqual(p, (-1, 0))
        self.assertRaises(TypeError, 'p = p - "hello"')

    def test_dunder_rsub(self):
        p = Point(0)
        p = (1, 0) - p
        self.assertEqual(p, (1, 0))
        p = Point(1, 1) - p
        self.assertEqual(p, (0, 1))
        p = (1 + 2j) - p
        self.assertEqual(p, (1, 1))

        class c:
            def __init__(self):
                self.x = 1
                self.y = 1

        p = c() - p
        self.assertEqual(p, (0, 0))
        p = Point("-4,-4") - p
        self.assertEqual(p, (-4, -4))
        p = 1 - p
        self.assertEqual(p, (5, 4))
        self.assertRaises(TypeError, 'p = "hello" - p')

    def test_dunder_mult(self):
        """
        For backwards compatibility multiplication of points works like multiplication of complex variables.

        :return:
        """
        p = Point(2, 2)
        p *= (1, 0)
        self.assertEqual(p, (2, 2))
        p *= Point(1, 1)
        self.assertEqual(p, (0, 4))
        p *= 1 + 2j
        self.assertEqual(p, (-8, 4))

        class c:
            def __init__(self):
                self.x = 1
                self.y = 1

        p *= c()
        self.assertEqual(p, (-12, -4))
        p *= Point("-4,-4")
        self.assertEqual(p, (32, 64))
        p *= 1
        self.assertEqual(p, (32, 64))
        r = p * 1
        self.assertEqual(r, (32, 64))
        r *= "scale(0.1)"
        self.assertEqual(r, (3.2, 6.4))

    def test_dunder_transform(self):
        p = Point(4, 4)
        m = Matrix("scale(4)")
        p.matrix_transform(m)
        self.assertEqual(p, (16, 16))

    def test_move_towards(self):
        p = Point(4, 4)
        p.move_towards((6, 6), 0.5)
        self.assertEqual(p, (5, 5))

    def test_distance_to(self):
        p = Point(4, 4)
        m = p.distance_to((6, 6))
        self.assertEqual(m, 2 * sqrt(2))
        m = p.distance_to(4)
        self.assertEqual(m, 4)

    def test_angle_to(self):
        p = Point(0)
        a = p.angle_to((3, 3))
        self.assertEqual(a, Angle.parse("45deg"))
        a = p.angle_to((0, 3))
        self.assertEqual(a, Angle.parse("0.25turn"))
        a = p.angle_to((-3, 0))
        self.assertEqual(a, Angle.parse("200grad"))

    def test_polar(self):
        p = Point(0)
        q = p.polar_to(Angle.parse("45deg"), 10)
        self.assertEqual(q, (sqrt(2)/2 * 10, sqrt(2)/2 * 10))

    def test_reflected_across(self):
        p = Point(0)
        r = p.reflected_across((10,10))
        self.assertEqual(r, (20,20))