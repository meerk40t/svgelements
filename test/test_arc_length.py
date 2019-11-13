from __future__ import print_function

import unittest
from random import *

from svg.elements import *


def get_random_arc():
    return Arc((random() * 50, random() * 50),
               random() * 50, random() * 50,
               int(random() * 180),
               int(random() * 2), int(random() * 2),
               (random() * 50, random() * 50))


def get_random_circle_arc():
    r = random() * 50
    return Arc((random() * 50, random() * 50),
               r, r,
               int(random() * 180),
               int(random() * 2), int(random() * 2),
               (random() * 50, random() * 50))


class TestElementArcLength(unittest.TestCase):

    def test_arc_angle_point(self):
        for i in range(1000):
            ellipse = Ellipse((0, 0), 2, 1)
            point = random() * tau / 2 - tau / 4

            p = ellipse.point_at_angle(point)
            a = ellipse.angle_at_point(p)
            self.assertAlmostEqual(point, a)

    def test_arc_angle_point_rotated(self):
        for i in range(1000):
            ellipse = Ellipse((0, 0), 2, 1, Angle.degrees(45))
            angle = random() * tau / 2 - tau / 4

            p = ellipse.point_at_angle(angle)
            a = ellipse.angle_at_point(p)
            self.assertAlmostEqual(angle, a)

    def test_arc_angles(self):
        for i in range(1000):
            ellipse = Ellipse((0, 0), 2, 1)
            start = random() * tau / 2 - tau / 4
            end = random() * tau / 2 - tau / 4

            p = ellipse.point_at_angle(start)
            a = ellipse.angle_at_point(p)
            self.assertAlmostEqual(start, a)

            p = ellipse.point_at_angle(end)
            a = ellipse.angle_at_point(p)
            self.assertAlmostEqual(end, a)

            arc = ellipse.arc_angle(start, end)
            self.assertAlmostEqual(arc.get_start_angle(), start)
            self.assertAlmostEqual(arc.get_end_angle(), end)

    def test_arc_t(self):
        for i in range(1000):
            ellipse = Ellipse((0, 0), 2, 1)
            start = random() * tau / 2 - tau / 4
            end = random() * tau / 2 - tau / 4

            p = ellipse.point_at_t(start)
            a = ellipse.t_at_point(p)
            self.assertAlmostEqual(start, a)

            p = ellipse.point_at_t(end)
            a = ellipse.t_at_point(p)
            self.assertAlmostEqual(end, a)

            arc = ellipse.arc_t(start, end)
            self.assertAlmostEqual(arc.get_start_t(), start)
            self.assertAlmostEqual(arc.get_end_t(), end)

    def test_arc_angles_rotated(self):
        for i in range(1000):
            ellipse = Ellipse((0, 0), 2, 1, Angle.degrees(90))
            start = random() * tau / 2 - tau / 4
            end = random() * tau / 2 - tau / 4

            p = ellipse.point_at_angle(start)
            a = ellipse.angle_at_point(p)
            self.assertAlmostEqual(start, a)

            p = ellipse.point_at_t(end)
            a = ellipse.t_at_point(p)
            self.assertAlmostEqual(end, a)

            p = ellipse.point_at_angle(end)
            a = ellipse.angle_at_point(p)
            self.assertAlmostEqual(end, a)

            arc = ellipse.arc_angle(start, end)
            self.assertAlmostEqual(arc.get_start_angle(), start)
            self.assertAlmostEqual(arc.get_end_angle(), end)

    def test_arc_t_rotated(self):
        for i in range(1000):
            ellipse = Ellipse((0, 0), 2, 1, Angle.degrees(90))
            start = random() * tau / 2 - tau / 4
            end = random() * tau / 2 - tau / 4

            p = ellipse.point_at_t(start)
            a = ellipse.t_at_point(p)
            self.assertAlmostEqual(start, a)

            arc = ellipse.arc_t(start, end)
            self.assertAlmostEqual(arc.get_start_t(), start)
            self.assertAlmostEqual(arc.get_end_t(), end)

    def test_arc_solve_produced(self):
        a = 3.05
        b = 2.23
        angle = atan(a * tan(radians(50)) / b)
        x = cos(angle) * a
        y = sin(angle) * b
        arc0 = Arc(start=3.05 + 0j, radius=3.05 + 2.23j, rotation=0, sweep=1, arc=0, end=x + 1j * y)

        ellipse = Ellipse((0, 0), 3.05, 2.23)
        arc1 = ellipse.arc_angle(0, Angle.degrees(50))

        self.assertEqual(arc0, arc1)

    def test_arc_solved_exact(self):
        ellipse = Ellipse((0, 0), 3.05, 2.23)
        arc = ellipse.arc_angle(0, Angle.degrees(50))
        arc *= "rotate(1)"
        exact = arc._exact_length()
        self.assertAlmostEqual(exact, 2.5314195265536624417, delta=1e-15)

    def test_arc_solved_integrated(self):
        ellipse = Ellipse((0, 0), 3.05, 2.23)
        arc = ellipse.arc_angle(0, Angle.degrees(50))
        length_calculated = arc._integral_length()
        self.assertAlmostEqual(length_calculated, 2.5314195265536624417, delta=1e-4)

    def test_arc_solved_lines(self):
        ellipse = Ellipse((0, 0), 3.05, 2.23)
        arc = ellipse.arc_angle(0, Angle.degrees(50))
        length_calculated = arc._line_length()
        self.assertAlmostEqual(length_calculated, 2.5314195265536624417, delta=1e-9)

    def test_arc_rotated_solved_exact(self):
        ellipse = Ellipse((0, 0), 3.05, 2.23)
        arc = ellipse.arc_angle(Angle.degrees(180), Angle.degrees(180 - 50))
        exact = arc._exact_length()
        self.assertAlmostEqual(exact, 2.5314195265536624417)

    def test_arc_position_0_ortho(self):
        arc = Ellipse(0, 3, 5).arc_angle(0, Angle.degrees(90))
        self.assertEqual(arc.point(0), (3, 0))

    def test_arc_position_0_rotate(self):
        arc = Ellipse(0, 3, 5).arc_angle(0, Angle.degrees(90))
        arc *= "rotate(90deg)"
        p = arc.point(0)
        self.assertEqual(p, (0, 3))
        p = arc.point(1)
        self.assertEqual(p, (-5, 0))

    def test_arc_position_0_angle(self):
        arc = Ellipse("0,0", 3, 5).arc_angle(0, Angle.degrees(90))
        arc *= "rotate(-33deg)"
        self.assertEqual(arc.get_start_angle(), Angle.degrees(-33))

    def test_arc_position_0(self):
        start = Point(13.152548373912, 38.873772319489)
        arc = Arc(start,
                  Point(14.324014604836, 24.436855715076),
                  Point(-14.750000067599, 25.169681093411),
                  Point(-43.558410063178, 28.706909065029),
                  Point(-19.42967575562, -12.943218880396),
                  5.89788464227)
        point_0 = arc.point(0)
        self.assertAlmostEqual(start, point_0)

    def test_arc_len_r0_lines(self):
        """Test error vs. random arc"""
        arc = Arc(Point(13.152548373912, 38.873772319489),
                  Point(14.324014604836, 24.436855715076),
                  Point(-14.750000067599, 25.169681093411),
                  Point(-43.558410063178, 28.706909065029),
                  Point(-19.42967575562, -12.943218880396),
                  5.89788464227)
        length = arc._line_length()
        self.assertAlmostEqual(198.3041678406902, length, places=3)

    def test_arc_len_r0_exact(self):
        """Test error vs. random arc"""
        arc = Arc(Point(13.152548373912, 38.873772319489),
                  Point(14.324014604836, 24.436855715076),
                  Point(-14.750000067599, 25.169681093411),
                  Point(-43.558410063178, 28.706909065029),
                  Point(-19.42967575562, -12.943218880396),
                  5.89788464227)
        length = arc._exact_length()
        self.assertAlmostEqual(198.3041678406902, length, places=3)

    def test_arc_len_r0_integral(self):
        """Test error vs. random arc"""
        arc = Arc(Point(13.152548373912, 38.873772319489),
                  Point(14.324014604836, 24.436855715076),
                  Point(-14.750000067599, 25.169681093411),
                  Point(-43.558410063178, 28.706909065029),
                  Point(-19.42967575562, -12.943218880396),
                  5.89788464227)
        length = arc._integral_length()
        self.assertAlmostEqual(198.3041678406902, length, places=3)

    def test_arc_len_circle_shortcut(self):
        """Test error vs. circles"""
        for i in range(1000):
            arc = get_random_circle_arc()
            chord = abs(arc.sweep * arc.rx)
            length = arc.length()
            self.assertAlmostEqual(chord, length)

    def test_arc_len_circle_int(self):
        """Test error vs. circles, arc_length"""
        for i in range(1000):
            arc = get_random_circle_arc()
            chord = abs(arc.sweep * arc.rx)
            length = arc._integral_length()
            self.assertAlmostEqual(chord, length)

    def test_arc_len_straight(self):
        """Test error at extreme eccentricities"""
        self.assertAlmostEqual(Arc(0, 1, 1e-10, 0, 1, 0, (0, 2e-10))._line_length(), 2, places=15)
        self.assertAlmostEqual(Arc(0, 1, 1e-10, 0, 1, 0, (0, 2e-10))._integral_length(), 2, places=5)
        self.assertEqual(Arc(0, 1, 1e-10, 0, 1, 0, (0, 2e-10))._exact_length(), 2)

    def test_unit_matrix(self):
        ellipse = Ellipse("20,20", 4, 8, Angle.turns(.45))
        matrix = ellipse.unit_matrix()
        ellipse2 = Circle()
        ellipse2 *= matrix
        self.assertEqual(ellipse, ellipse2)


    def test_arc_len_r0_exact(self):
        """Test error vs. random arc"""
        arc = Arc(Point(13.152548373912, 38.873772319489),
                  Point(14.324014604836, 24.436855715076),
                  Point(-14.750000067599, 25.169681093411),
                  Point(-43.558410063178, 28.706909065029),
                  Point(-19.42967575562, -12.943218880396),
                  5.89788464227)
        length = arc._exact_length()
        self.assertAlmostEqual(198.3041678406902, length, places=3)

    def test_arc_len_integral(self):
        """Test error vs. random arc"""
        error = 0
        for i in range(5):
            arc = get_random_arc()
            length = arc._integral_length()
            exact = arc._exact_length()
            c = length - exact
            error += c
            self.assertAlmostEqual(exact, length, places=1)
        print(error / 5)

    def test_arc_len_lines(self):
        """Test error vs. random arc"""
        error = 0
        for i in range(5):
            arc = get_random_arc()
            length = arc._line_length()
            exact = arc._exact_length()
            c = length - exact
            error += c
            self.assertAlmostEqual(exact, length, places=1)
        print(error / 5)