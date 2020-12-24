from __future__ import print_function

import unittest
from random import *

from svgelements import *


def get_random_arc():
    return Arc((random() * 50, random() * 50),
               random() * 48 + 2, random() * 48 + 2,
               int(random() * 180),
               int(random() * 2), int(random() * 2),
               (random() * 50, random() * 50))


def get_random_circle_arc():
    r = random() * 48 + 2
    return Arc((random() * 50, random() * 50),
               r, r,
               int(random() * 180),
               int(random() * 2), int(random() * 2),
               (random() * 50, random() * 50))


class TestElementArcLength(unittest.TestCase):

    def test_arc_angle_point(self):
        for i in range(1000):
            ellipse = Ellipse((0, 0), 2, 1)
            angle = random() * tau / 2 - tau / 4

            p = ellipse.point_at_angle(angle)
            a = ellipse.angle_at_point(p)
            self.assertAlmostEqual(angle, a)

    def test_arc_angle_point_rotated(self):
        for i in range(1000):
            ellipse = Ellipse((0, 0), 2, 1, "rotate(45deg)")
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
            ellipse = Ellipse((0, 0), 2, 1, "rotate(90deg)")
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
            ellipse = Ellipse((0, 0), 2, 1,  "rotate(90deg)")
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
        arc0 = Arc(start=3.05 + 0j, radius=3.05 + 2.23j, rotation=0, sweep_flag=1, arc_flag=0, end=x + 1j * y)

        ellipse = Ellipse(0, 0, 3.05, 2.23)
        arc1 = ellipse.arc_angle(0, Angle.degrees(50))

        self.assertEqual(arc0, arc1)

    def test_arc_solved_exact(self):
        ellipse = Ellipse(0.0, 0.0, 3.05, 2.23)
        arc = ellipse.arc_angle(0, Angle.degrees(50))
        arc *= "rotate(1)"
        exact = arc._exact_length()
        self.assertAlmostEqual(exact, 2.5314195265536624417, delta=1e-10)

    def test_arc_solved_integrated(self):
        ellipse = Ellipse(0, 0, 3.05, 2.23)
        arc = ellipse.arc_angle(0, Angle.degrees(50))
        length_calculated = arc._integral_length()
        self.assertAlmostEqual(length_calculated, 2.5314195265536624417, delta=1e-4)

    def test_arc_solved_lines(self):
        ellipse = Ellipse(0, 0, 3.05, 2.23)
        arc = ellipse.arc_angle(0, Angle.degrees(50))
        length_calculated = arc._line_length()
        self.assertAlmostEqual(length_calculated, 2.5314195265536624417, delta=1e-9)

    def test_arc_rotated_solved_exact(self):
        ellipse = Ellipse(0, 0, 3.05, 2.23)
        arc = ellipse.arc_angle(Angle.degrees(180), Angle.degrees(180 - 50))
        exact = arc._exact_length()
        self.assertAlmostEqual(exact, 2.5314195265536624417)

        arc = ellipse.arc_angle(Angle.degrees(360 + 180 - 50), Angle.degrees(180))
        exact = arc._exact_length()
        self.assertAlmostEqual(exact, 14.156360641292059)

    def test_arc_position_0_ortho(self):
        arc = Ellipse(0, 0, 3, 5).arc_angle(0, Angle.degrees(90))
        self.assertEqual(arc.point(0), (3, 0))

    def test_arc_position_0_rotate(self):
        arc = Ellipse(0, 0, 3, 5).arc_angle(0, Angle.degrees(90))
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

    def test_arc_len_r0_default(self):
        """Test error vs. random arc"""
        arc = Arc(Point(13.152548373912, 38.873772319489),
                  Point(14.324014604836, 24.436855715076),
                  Point(-14.750000067599, 25.169681093411),
                  Point(-43.558410063178, 28.706909065029),
                  Point(-19.42967575562, -12.943218880396),
                  5.89788464227)
        length = arc.length()
        self.assertAlmostEqual(198.3041678406902, length, places=3)

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

    def test_arc_len_straight(self):
        """Test error at extreme eccentricities"""
        self.assertAlmostEqual(Arc(0, 1, 1e-10, 0, 1, 0, (0, 2e-10))._line_length(), 2, places=15)
        self.assertAlmostEqual(Arc(0, 1, 1e-10, 0, 1, 0, (0, 2e-10))._integral_length(), 2, places=5)
        self.assertEqual(Arc(0, 1, 1e-10, 0, 1, 0, (0, 2e-10))._exact_length(), 2)

    def test_unit_matrix(self):
        ellipse = Ellipse("20", "20", 4, 8, "rotate(45deg)")
        matrix = ellipse.unit_matrix()
        ellipse2 = Circle()
        ellipse2.values[SVG_ATTR_VECTOR_EFFECT] = SVG_VALUE_NON_SCALING_STROKE
        ellipse2 *= matrix
        p1 = ellipse.point_at_t(1)
        p2 = ellipse2.point_at_t(1)
        self.assertAlmostEqual(p1, p2)
        self.assertEqual(ellipse, ellipse2)

    def test_arc_len_circle_shortcut(self):
        """Known chord vs. shortcut"""
        error = 0
        for i in range(1000):
            arc = get_random_circle_arc()
            chord = abs(arc.sweep * arc.rx)
            length = arc.length()
            c = abs(length - chord)
            error += c
            self.assertAlmostEqual(chord, length)
        print("Average chord vs shortcut-length: %g" % (error / 1000))

    def test_arc_len_circle_int(self):
        """Known chord vs integral"""
        n = 10
        error = 0
        for i in range(n):
            arc = get_random_circle_arc()
            chord = abs(arc.sweep * arc.rx)
            length = arc._integral_length()
            c = abs(length - chord)
            error += c
            self.assertAlmostEqual(chord, length)
        print("Average chord vs integral: %g" % (error / n))

    def test_arc_len_circle_exact(self):
        """Known chord vs exact"""
        n = 1000
        error = 0
        for i in range(n):
            arc = get_random_circle_arc()
            chord = abs(arc.sweep * arc.rx)
            length = arc._exact_length()
            c = abs(length - chord)
            error += c
            self.assertAlmostEqual(chord, length)
        print("Average chord vs exact: %g" % (error / n))

    def test_arc_len_circle_line(self):
        """Known chord vs line"""
        n = 1
        error = 0
        for i in range(n):
            arc = get_random_circle_arc()
            chord = abs(arc.sweep * arc.rx)
            length = arc._line_length()
            c = abs(length - chord)
            error += c
            self.assertAlmostEqual(chord, length, places=6)
        print("Average chord vs line: %g" % (error / n))

    def test_arc_len_flat_line(self):
        """Known flat vs line"""
        n = 100
        error = 0
        for i in range(n):
            flat = 1 + random() * 50
            arc = Arc(0, flat, 1e-10, 0, 1, 0, (0, 2e-10))
            flat = 2*flat
            length = arc._line_length()
            c = abs(length - flat)
            error += c
            self.assertAlmostEqual(flat, length)
        print("Average flat vs line: %g" % (error / n))

    def test_arc_len_flat_integral(self):
        """Known flat vs integral"""
        n = 10
        error = 0
        for i in range(n):
            flat = 1 + random() * 50
            arc = Arc(0, flat, 1e-10, 0, 1, 0, (0, 2e-10))
            flat = 2*flat
            length = arc._integral_length()
            c = abs(length - flat)
            error += c
            self.assertAlmostEqual(flat, length)
        print("Average flat vs integral: %g" % (error / n))

    def test_arc_len_flat_exact(self):
        """Known flat vs exact"""
        n = 1000
        error = 0
        for i in range(n):
            flat = 1 + random() * 50
            arc = Arc(0, flat, 1e-10, 0, 1, 0, (0, 2e-10))
            flat = 2*flat
            length = arc._exact_length()
            c = abs(length - flat)
            error += c
            self.assertAlmostEqual(flat, length)
        print("Average flat vs line: %g" % (error / n))

    def test_arc_len_random_int(self):
        """Test error vs. random arc"""
        n = 5
        error = 0
        for i in range(n):
            arc = get_random_arc()
            length = arc._integral_length()
            exact = arc._exact_length()
            c = abs(length - exact)
            error += c
            self.assertAlmostEqual(exact, length, places=1)
        print("Average arc-integral error: %g" % (error / n))

    def test_arc_len_random_lines(self):
        """Test error vs. random arc"""
        n = 2
        error = 0
        for i in range(n):
            arc = get_random_arc()
            length = arc._line_length()
            exact = arc._exact_length()
            c = abs(length - exact)
            error += c
            self.assertAlmostEqual(exact, length, places=1)
        print("Average arc-line error: %g" % (error / n))


class TestElementArcPoint(unittest.TestCase):

    def test_arc_point_start_stop(self):
        import numpy as np
        for _ in range(1000):
            arc = get_random_arc()
            self.assertEqual(arc.start, arc.point(0))
            self.assertEqual(arc.end, arc.point(1))
            self.assertTrue(np.all(np.array([list(arc.start), list(arc.end)])
                                   == arc.npoint([0, 1])))

    # def test_arc_point_implementations_match(self):
    #     import numpy as np
    #     for _ in range(1000):
    #         arc = get_random_arc()
    #
    #         pos = np.linspace(0, 1, 100)
    #
    #         v1 = arc.npoint(pos)
    #         # with disable_numpy():
    #         v2 = arc.npoint(pos)  # test is rendered pointless.
    #
    #         for p, p1, p2 in zip(pos, v1, v2):
    #             self.assertEqual(arc.point(p), Point(p1))
    #             self.assertEqual(Point(p1), Point(p2))


class TestElementArcApproximation(unittest.TestCase):

    def test_approx_quad(self):
        n = 100
        for i in range(n):
            arc = get_random_arc()
            path1 = Path([Move(), arc])
            path2 = Path(path1)
            path2.approximate_arcs_with_quads(error=0.05)
            d = abs(path1.length() - path2.length())
            # Error less than 1% typically less than 0.5%
            if d > 10:
                print(arc)
            self.assertAlmostEqual(d, 0.0, delta=20)

    def test_approx_cubic(self):
        n = 100
        for i in range(n):
            arc = get_random_arc()
            path1 = Path([Move(), arc])
            path2 = Path(path1)
            path2.approximate_arcs_with_cubics(error=0.1)
            d = abs(path1.length() - path2.length())
            # Error less than 0.1% typically less than 0.001%
            if d > 1:
                print(arc)
            self.assertAlmostEqual(d, 0.0, delta=2)