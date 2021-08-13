import unittest
import io

from svgelements import *


class TestElementCopy(unittest.TestCase):
    """These tests test the validity of object copy."""

    def test_copy_objects(self):
        # CSS OBJECTS

        length = Length('1in')
        length_copy = copy(length)
        self.assertEqual(length, length_copy)

        color = Color('red')
        color_copy = copy(color)
        self.assertEqual(color, color_copy)

        point = Point("2,4.58")
        point_copy = copy(point)
        self.assertEqual(point, point_copy)

        angle = Angle.parse('1.2grad')
        angle_copy = copy(angle)
        self.assertEqual(angle, angle_copy)

        matrix = Matrix("scale(4.5) translate(2,2.4) rotate(40grad)")
        matrix_copy = copy(matrix)
        self.assertEqual(matrix, matrix_copy)

        # SVG OBJECTS
        viewbox = Viewbox('0 0 103 109', preserveAspectRatio="xMaxyMin slice")
        viewbox_copy = copy(viewbox)
        # self.assertEqual(viewbox, viewbox_copy)

        svgelement = SVGElement({'tag': "element", 'id': 'testelement1234'})
        svgelement_copy = copy(svgelement)
        self.assertIsNotNone(svgelement_copy.values)
        # self.assertEqual(svgelement, svgelement_copy)

        # PATH SEGMENTS
        move = Move((8,8.78))
        move_copy = copy(move)
        self.assertEqual(move, move_copy)

        close = Close()
        close_copy = copy(close)
        self.assertEqual(close, close_copy)

        line = Line((8, 8.78))
        line_copy = copy(line)
        self.assertEqual(line, line_copy)

        quad = QuadraticBezier((8, 8.78), (50, 50.78), (50, 5))
        quad_copy = copy(quad)
        self.assertEqual(quad, quad_copy)

        cubic = CubicBezier((8, 8.78), (1, 6.78), (8, 9.78), (50, 5))
        cubic_copy = copy(cubic)
        self.assertEqual(cubic, cubic_copy)

        arc = Arc(start=(0,0), end=(25,0), control=(10,10))
        arc_copy = copy(arc)
        self.assertEqual(arc, arc_copy)

        # SHAPES
        path = Path("M5,5V10Z")
        path_copy = copy(path)
        self.assertEqual(path, path_copy)
        self.assertIsNotNone(path_copy.values)

        rect = Rect(0, 0, 1000, 1000, ry=20)
        rect_copy = copy(rect)
        self.assertEqual(rect, rect_copy)
        self.assertIsNotNone(rect_copy.values)

        ellipse = Ellipse(0, 0, 1000, 1000)
        ellipse_copy = copy(ellipse)
        self.assertEqual(ellipse, ellipse_copy)
        self.assertIsNotNone(ellipse_copy.values)

        circle = Circle(x=0, y=0, r=1000)
        circle_copy = copy(circle)
        self.assertEqual(circle, circle_copy)
        self.assertIsNotNone(circle_copy.values)

        sline = SimpleLine((0, 0), (1000, 1000))
        sline_copy = copy(sline)
        self.assertEqual(sline, sline_copy)
        self.assertIsNotNone(sline_copy.values)

        rect = Rect(0, 0, 1000, 1000, ry=20)
        rect_copy = copy(rect)
        self.assertEqual(rect, rect_copy)
        self.assertIsNotNone(rect_copy.values)

        pline = Polyline((0, 0), (1000, 1000), (0,1000), (0,0))
        pline_copy = copy(pline)
        self.assertEqual(pline, pline_copy)
        self.assertIsNotNone(pline_copy.values)

        pgon = Polygon((0, 0), (1000, 1000), (0,1000))
        pgon_copy = copy(pgon)
        self.assertEqual(pgon, pgon_copy)
        self.assertIsNotNone(pgon_copy.values)

        group = Group(stroke="cornflower")
        group_copy = copy(group)
        self.assertEqual(group, group_copy)
        self.assertIsNotNone(group_copy.values)

        cpath = ClipPath(stroke="blue")
        cpath_copy = copy(cpath)
        self.assertEqual(cpath, cpath_copy)
        self.assertIsNotNone(cpath_copy.values)

        text = SVGText("HelloWorld")
        text_copy = copy(text)
        # self.assertEqual(text,text_copy)
        self.assertIsNotNone(text_copy.values)

        image = SVGImage(viewbox=viewbox)
        image_copy = copy(image)
        # self.assertEqual(image,image_copy)
        self.assertIsNotNone(image_copy.values)

        desc = Desc({"apple": 7}, desc="Some description")
        desc_copy = copy(desc)
        # self.assertEqual(desc, desc_copy)
        self.assertIsNotNone(desc_copy.values)

        title = Title({"apple": 3}, title="Some Title")
        title_copy = copy(title)
        # self.assertEqual(title, title_copy)
        self.assertIsNotNone(title_copy.values)

        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg>
                        <path d="M0 36c0 128.082 96 214 251 214c153.639 0 293 -37 293 -264c0 -220 -158.05 -325.976 -254 -391c-121 -82 -200.248 -117.634 -339 -171c-5.93907 -2.28437 -11.3166 -3.27496 -15.9795 -3.27496c-11.9348 0 -19.1871 6.48977 -19.1871 14.3854 c0 7.04844 5.77949 15.2172 19.1666 20.8896c118 50 225 86 316 200c91 113 125 205.913 125 350c0 135 -33 224 -145 224c-46.615 0 -77.452 -12.593 -112 -44c-8.09234 -7.35667 -11.3121 -13.0296 -11.3121 -17.4022c0 -13.4585 30.5027 -14.5978 43.3121 -14.5978 c69 0 123 -64.8867 123 -136c0 -75 -48 -132 -139 -132c-79.1582 0 -135 74 -135 150zM572 128c0 35 29 64 64 64s63 -29 63 -64s-28 -63 -63 -63s-64 28 -64 63zM572 -131c0 35 29 64 64 64s63 -29 63 -64s-28 -63 -63 -63s-64 28 -64 63z" transform="rotate(45deg)"/>
                        </svg>''')
        svg = SVG.parse(q)
        svg_copy = copy(svg)
        self.assertEqual(svg, svg_copy)
        self.assertIsNotNone(svg_copy.values)
