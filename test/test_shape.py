from __future__ import print_function

import unittest

from svg.elements import *


class TestElementShape(unittest.TestCase):

    def test_rect_dict(self):
        values = {
            'tag': 'rect',
            'rx': "4",
            'ry': "2",
            'x': "50",
            'y': "51",
            'width': "20",
            'height': "10"
        }
        e = Rect(values)
        e2 = Rect(50, 51, 20, 10, 4, 2)
        self.assertEqual(e, e2)
        e2 *= "translate(2)"
        e3 = Rect()
        self.assertNotEqual(e, e3)

    def test_line_dict(self):
        values = {
            'tag': 'rect',
            'x0': "0",
            'y0': "0",
            'x1': "100",
            'y1': "100"
        }
        e = SimpleLine(values)
        e2 = SimpleLine((0, 0), (100, 100))
        e3 = SimpleLine(0, 0, 100, 100)
        self.assertEqual(e, e2)
        self.assertEqual(e, e3)
        e4 = SimpleLine()
        self.assertNotEqual(e, e4)

    def test_ellipse_dict(self):
        values = {
            'tag': 'ellipse',
            'rx': "4.0",
            'ry': "8.0",
            'cx': "22.4",
            'cy': "33.33"
        }
        e = Ellipse(values)
        e2 = Ellipse((22.4, 33.33), 4, 8)
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
        circle_d = e.d()
        self.assertEqual(Path(circle_d),
                'M26.4,33.33A4,4 0 0,1 22.4,37.33 A4,4 0 0,1 18.4,33.33 A4,4 0 0,1 22.4,29.33 A4,4 0 0,1 26.4,33.33Z')

    def test_polyline_dict(self):
        values = {
            'tag': 'polyline',
            'points': '0,100 50,25 50,75 100,0',
        }
        e = Polyline(values)
        e2 = Polyline(0, 100, 50, 25, 50, 75, 100, 0)
        self.assertEqual(e, e2)
        e3 = Polyline()
        self.assertNotEqual(e, e3)
        polyline_d = e.d()
        self.assertEqual(Path(polyline_d), "M0, 100, 50, 25, 50, 75, 100, 0")

    def test_polygon_dict(self):
        values = {
            'tag': 'polyline',
            'points': '0,100 50,25 50,75 100,0',
        }
        e = Polygon(values)
        e2 = Polygon(0, 100, 50, 25, 50, 75, 100, 0)
        self.assertEqual(e, e2)
        e3 = Polygon()
        self.assertNotEqual(e, e3)
        polygon_d = e.d()
        self.assertEqual(Path(polygon_d), "M0,100 50,25 50,75 100,0z")

    def test_circle_ellipse_equal(self):
        self.assertTrue(Ellipse(center=(0, 0), rx=10, ry=10) == Circle(center="0,0", r=10.0))

    def test_transform_circle_to_ellipse(self):
        c = Circle(center="0,0", r=10.0)
        p = c * Matrix.skew_x(Angle.degrees(50))
        p.reify()
        p = c * "translate(10,1)"
        p.reify()
        p = c * "scale(10,1)"
        p.reify()
        p = c * "rotate(10deg)"
        p.reify()
        p = c * "skewy(10)"
        p.reify()
        self.assertFalse(isinstance(Circle(), Ellipse))
        self.assertFalse(isinstance(Ellipse(), Circle))

    def test_circle_decomp(self):
        circle = Circle()
        c = Path(circle.d())
        self.assertEqual(c, "M 1,0 A 1,1 0 0,1 0,1 A 1,1 0 0,1 -1,0 A 1,1 0 0,1 0,-1 A 1,1 0 0,1 1,0 Z")
        circle *= "scale(2,1)"
        c = Path(circle.d())
        self.assertEqual(c, "M 2,0 A 2,1 0 0,1 0,1 A 2,1 0 0,1 -2,0 A 2,1 0 0,1 0,-1 A 2,1 0 0,1 2,0 Z")
        circle *= "scale(0.5,1)"
        c = Path(circle.d())
        self.assertEqual(c, "M 1,0 A 1,1 0 0,1 0,1 A 1,1 0 0,1 -1,0 A 1,1 0 0,1 0,-1 A 1,1 0 0,1 1,0 Z")

    def test_circle_implicit(self):
        circle = Circle()
        circle *= "translate(40,40) rotate(15deg) scale(2,1.5)"
        self.assertAlmostEqual(circle.implicit_rx, 2.0)
        self.assertAlmostEqual(circle.implicit_ry, 1.5)
        self.assertAlmostEqual(circle.rotation, Angle.degrees(15))
        self.assertEqual(circle.implicit_center, (40,40))

    def test_circle_equals_tranformed_circle(self):
        circle1 = Circle(r=2)
        circle2 = Circle() * "scale(2)"
        self.assertEqual(circle1, circle2)