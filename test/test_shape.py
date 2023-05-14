import unittest
import io

from svgelements import *


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
            'x1': "0",
            'y1': "0",
            'x2': "100",
            'y2': "100"
        }
        e = SimpleLine(values)
        e2 = SimpleLine(0, '0px', '100px', '100px')
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
        e2 = Ellipse(22.4, 33.33, 4, 8)
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
        e2 = Circle(22.4, 33.33, 4)
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
        self.assertEqual(Path(polyline_d), "M 0,100 L 50,25 L 50,75 L 100,0")

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
        self.assertEqual(Path(polygon_d), 'M 0,100 L 50,25 L 50,75 L 100,0 Z')

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
        shape = Circle()
        shape *= "translate(40,40) rotate(15deg) scale(2,1.5)"
        self.assertAlmostEqual(shape.implicit_rx, 2.0)
        self.assertAlmostEqual(shape.implicit_ry, 1.5)
        self.assertAlmostEqual(shape.rotation, Angle.degrees(15))
        self.assertEqual(shape.implicit_center, (40, 40))

    def test_rect_implicit(self):
        shape = Rect()
        shape *= "translate(40,40) rotate(15deg) scale(2,1.5)"
        self.assertAlmostEqual(shape.implicit_x, 40)
        self.assertAlmostEqual(shape.implicit_y, 40)
        self.assertAlmostEqual(shape.implicit_width, 2)
        self.assertAlmostEqual(shape.implicit_height, 1.5)
        self.assertAlmostEqual(shape.implicit_rx, 0)
        self.assertAlmostEqual(shape.implicit_ry, 0)
        self.assertAlmostEqual(shape.rotation, Angle.degrees(15))

    def test_line_implicit(self):
        shape = SimpleLine(0, 0, 1, 1)
        shape *= "translate(40,40) rotate(15deg) scale(2,1.5)"
        self.assertAlmostEqual(shape.implicit_x1, 40)
        self.assertAlmostEqual(shape.implicit_y1, 40)
        p = Point(1, 1) * "rotate(15deg) scale(2,1.5)"
        self.assertAlmostEqual(shape.implicit_x2, 40 + p[0])
        self.assertAlmostEqual(shape.implicit_y2, 40 + p[1])
        self.assertAlmostEqual(shape.rotation, Angle.degrees(15))

    def test_circle_equals_transformed_circle(self):
        shape1 = Circle(r=2)
        shape2 = Circle().set('vector-effect', 'non-scaling-stroke') * "scale(2)"
        self.assertEqual(shape1, shape2)
        shape2.reify()
        self.assertEqual(shape1, shape2)

    def test_rect_equals_transformed_rect(self):
        shape1 = Rect(x=0, y=0, width=2, height=2)
        shape2 = Rect(0, 0, 1, 1).set('vector-effect', 'non-scaling-stroke') * "scale(2)"
        self.assertEqual(shape1, shape2)
        shape2.reify()
        self.assertEqual(shape1, shape2)

    def test_rrect_equals_transformed_rrect(self):
        shape1 = Rect(0, 0, 2, 2, 1, 1)
        shape2 = Rect(0, 0, 1, 1, 0.5, 0.5).set('vector-effect', 'non-scaling-stroke') * "scale(2)"
        self.assertEqual(shape1, shape2)
        shape2.reify()
        self.assertEqual(shape1, shape2)

    def test_line_equals_transformed_line(self):
        shape1 = SimpleLine(0, 0, 2, 2)
        shape2 = SimpleLine(0, 0, 1, 1).set('vector-effect', 'non-scaling-stroke') * "scale(2)"
        self.assertEqual(shape1, shape2)
        shape2.reify()
        self.assertEqual(shape1, shape2)

    def test_polyline_equals_transformed_polyline(self):
        shape1 = Polyline(0, 0, 2, 2)
        shape2 = Polyline(0, 0, 1, 1).set('vector-effect', 'non-scaling-stroke') * "scale(2)"
        self.assertEqual(shape1, shape2)
        shape2.reify()
        self.assertEqual(shape1, shape2)

    def test_polygon_equals_transformed_polygon(self):
        shape1 = Polyline(0, 0, 2, 2)
        shape2 = Polyline(0, 0, 1, 1).set('vector-effect', 'non-scaling-stroke') * "scale(2)"
        self.assertEqual(shape1, shape2)
        shape2.reify()
        self.assertEqual(shape1, shape2)

    def test_polyline_not_equal_transformed_polygon(self):
        shape1 = Polyline(0, 0, 2, 2)
        shape2 = Polygon(0, 0, 1, 1) * "scale(2)"
        self.assertNotEqual(shape1, shape2)

    def test_polyline_closed_equals_transformed_polygon(self):
        shape1 = Path(Polyline(0, 0, 2, 2)) + "z"
        shape2 = Polygon(0, 0, 1, 1).set('vector-effect', 'non-scaling-stroke') * "scale(2)"
        self.assertEqual(shape1, shape2)

    def test_path_plus_shape(self):
        path = Path("M 0,0 z")
        path += Rect(0, 0, 1, 1)
        self.assertEqual(path, "M0,0zM0,0h1v1h-1z")

    def test_circle_not_equal_red_circle(self):
        shape1 = Circle()
        shape2 = Circle(stroke="red")
        self.assertNotEqual(shape1, shape2)
        shape1 = Circle()
        shape2 = Circle(fill="red")
        self.assertNotEqual(shape1, shape2)

    def test_rect_initialize(self):
        shapes = (
            Rect(),
            Rect(0),
            Rect(0, 0),
            Rect(0, 0, 1),
            Rect(0, 0, 1, 1),
            Rect(0, y=0),
            Rect(0, y=0, width=1),
            Rect(0, y=0, width=1, height=1),
            Rect(width=1, height=1, x=0, y=0),
            Rect(0, 0, 1, 1, 0, 0),
            Rect(0, 0, 1, 1, rx=0, ry=0)
        )
        for s in shapes:
            self.assertEqual(shapes[0], s)

    def test_circle_initialize(self):
        shapes = (
            Circle(),
            Circle(0, 0),
            Circle(center=(0, 0), r=1),
            Circle("0px", "0px", 1),
            Ellipse("0", "0", 1, 1),
            Ellipse("0", "0", rx=1, ry=1),
            Ellipse(0, 0, 1, ry=1),
            Circle(Circle()),
            Circle({"cx": 0, "cy": 0, "r": 1}),
            Ellipse({"cx": 0, "cy": 0, "rx": 1}),
            Ellipse({"cx": 0, "cy": 0, "ry": 1}),
            Ellipse({"cx": 0, "cy": 0, "rx": 1, "ry": 1.0}),
            Circle(Ellipse()),
            Ellipse(Circle())
        )
        for s in shapes:
            self.assertEqual(shapes[0], s)

    def test_polyline_initialize(self):
        shapes = (
            Polyline(0, 0, 1, 1),
            Polyline((0, 0), (1, 1)),
            Polyline(points=((0, 0), (1, 1))),
            Polyline("0,0", "1,1"),
            Polyline("0,0", (1, 1)),
            Polyline("0,0", Point(1, 1)),
            Polyline({"points": "0,0,1,1"}),
            Polyline(Polyline(0, 0, 1, 1)),
            Path("M0,0L1,1"),
            SimpleLine(0, 0, 1, 1),
        )
        for s in shapes:
            self.assertEqual(shapes[0], s)

    def test_polygon_initialize(self):
        shapes = (
            Polygon(0, 0, 1, 1),
            Polygon((0, 0), (1, 1)),
            Polygon(points=((0, 0), (1, 1))),
            Polygon("0,0", "1,1"),
            Polygon("0,0", (1, 1)),
            Polygon("0,0", Point(1, 1)),
            Polygon({"points": "0,0,1,1"}),
            Polygon(Polyline(0, 0, 1, 1)),
            Polygon("0,0,1,1"),
            Path("M0,0L1,1z"),
        )
        for s in shapes:
            self.assertEqual(shapes[0], s)

    def test_shapes_repr(self):
        s = Rect(fill='red')
        self.assertEqual(repr(s), "Rect(width=1, height=1, fill='#ff0000')")
        s = Ellipse(fill='red')
        self.assertEqual(repr(s), "Ellipse(cx=0, cy=0, r=1, fill='#ff0000')")
        s = Circle(fill='red')
        self.assertEqual(repr(s), "Circle(cx=0, cy=0, r=1, fill='#ff0000')")
        s = SimpleLine(fill='red')
        self.assertEqual(repr(s), "SimpleLine(x1=0.0, y1=0.0, x2=0.0, y2=0.0, fill='#ff0000')")
        s = Polygon(fill='red')
        self.assertEqual(repr(s), "Polygon(points='', fill='#ff0000')")
        s = Polyline(fill='red')
        self.assertEqual(repr(s), "Polyline(points='', fill='#ff0000')")
        s = Path(fill='red')
        self.assertEqual(repr(s), "Path(fill='#ff0000')")

    def test_shape_bbox(self):
        s = Rect() * 'scale(20)'
        self.assertEqual(s.bbox(False), (0, 0, 1, 1))
        self.assertEqual(s.bbox(True), (0, 0, 20, 20))
        self.assertNotEqual(s.bbox(False), (0, 0, 20, 20))
        self.assertNotEqual(s.bbox(True), (0, 0, 1, 1))
        s = Circle() * 'scale(20)'
        self.assertEqual(s.bbox(False), (-1, -1, 1, 1))
        self.assertEqual(s.bbox(True), (-20, -20, 20, 20))
        self.assertNotEqual(s.bbox(False), (-20, -20, 20, 20))
        self.assertNotEqual(s.bbox(True), (-1, -1, 1, 1))
        s = Ellipse() * 'scale(20)'
        self.assertEqual(s.bbox(False), (-1, -1, 1, 1))
        self.assertEqual(s.bbox(True), (-20, -20, 20, 20))
        self.assertNotEqual(s.bbox(False), (-20, -20, 20, 20))
        self.assertNotEqual(s.bbox(True), (-1, -1, 1, 1))
        s = Polygon() * 'scale(20)'
        self.assertEqual(s.bbox(False), None)
        self.assertEqual(s.bbox(True), None)
        self.assertNotEqual(s.bbox(False), (0, 0, 0, 0))
        self.assertNotEqual(s.bbox(True), (0, 0, 0, 0))
        s = Polyline() * 'scale(20)'
        self.assertEqual(s.bbox(False), None)
        self.assertEqual(s.bbox(True), None)
        self.assertNotEqual(s.bbox(False), (0, 0, 0, 0))
        self.assertNotEqual(s.bbox(True), (0, 0, 0, 0))
        s = Polygon("0,0 0,1 1,1 1,0 0,0") * 'scale(20)'
        self.assertEqual(s.bbox(False), (0, 0, 1, 1))
        self.assertEqual(s.bbox(True), (0, 0, 20, 20))
        self.assertNotEqual(s.bbox(False), (0, 0, 20, 20))
        self.assertNotEqual(s.bbox(True), (0, 0, 1, 1))
        s = Polyline("0,0 0,1 1,1 1,0 0,0") * 'scale(20)'
        self.assertEqual(s.bbox(False), (0, 0, 1, 1))
        self.assertEqual(s.bbox(True), (0, 0, 20, 20))
        self.assertNotEqual(s.bbox(False), (0, 0, 20, 20))
        self.assertNotEqual(s.bbox(True), (0, 0, 1, 1))
        s = SimpleLine(0, 0, 1, 1) * 'scale(20)'
        self.assertEqual(s.bbox(False), (0, 0, 1, 1))
        self.assertEqual(s.bbox(True), (0, 0, 20, 20))
        self.assertNotEqual(s.bbox(False), (0, 0, 20, 20))
        self.assertNotEqual(s.bbox(True), (0, 0, 1, 1))

    def test_rect_rot_equal_rect_path_rotate(self):
        r = Rect(10, 10, 8, 4)
        a = r.d()
        b = Path(a).d()
        self.assertEqual(a, b)
        a = (Path(r.d()) * "rotate(0.5turns)").d()
        b = (r * "rotate(0.5turns)").d()
        self.assertEqual(a, b)

    def test_rect_reify(self):
        """Reifying a rotated rect."""
        reification_checks(self, Rect())
        reification_checks(self, Rect(2, 2, 4, 4))

        shape = Rect() * "rotate(-90) translate(20,0)"
        t = Rect(0, -20, 1, 1)
        t *= "rotate(-90, 0, -20)"
        self.assertEqual(t, shape)

    def test_circle_reify(self):
        """Reifying a rotated circle."""
        reification_checks(self, Circle())
        reification_checks(self, Circle(2, 2, 4, 4))

    def test_ellipse_reify(self):
        """Reifying a rotated ellipse."""
        reification_checks(self, Ellipse(rx=1, ry=2))
        reification_checks(self, Ellipse(2, 2, 5, 8))

    def test_polyline_reify(self):
        """Reifying a rotated polyline."""
        reification_checks(self, Polyline("0,0 1,1 2,2"))
        reification_checks(self, Polyline("0,0 1,1 2,0"))

    def test_polygon_reify(self):
        """Reifying a rotated polygon."""
        reification_checks(self, Polygon("0,0 1,1 2,2"))
        reification_checks(self, Polygon("0,0 1,1 2,0"))

    def test_line_reify(self):
        """Reifying a rotated line."""
        reification_checks(self, SimpleLine(0, 0, 1, 1))
        reification_checks(self, SimpleLine(2, 2, 1, 0))

    def test_path_reify(self):
        """Reifying a path."""
        reification_checks(self, Path("M0,0L1,1L1,0z"))
        reification_checks(self, Path("M100,100L70,70L45,0z"))

    def test_shapes_degenerate(self):
        """Testing Degenerate Shapes"""
        self.assertEqual(Rect(0, 0, 0, 100).d(), '')
        self.assertEqual(Rect(0, 0, 100, 0).d(), '')
        self.assertEqual(Circle(0, 0, 0).d(), '')
        self.assertEqual(Ellipse(0,0,0,100).d(), '')
        self.assertEqual(Ellipse(0, 0, 100, 0).d(), '')
        self.assertEqual(Polygon(points='').d(), '')

    def test_issue_95(self):
        """Testing Issue 95 stroke-width"""
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg>
                        <ellipse style="stroke:#fc0000;stroke-width:1;fill:none" cx="0" cy="0" rx="1" ry="1" transform="scale(100) rotate(-90,0,0)"/>
                        <rect style="stroke:#fc0000;stroke-width:1;fill:none" x="0" y="0" width="10" height="10" transform="scale(100) rotate(-90,0,0)"/>
                        </svg>''')
        m = SVG.parse(q)
        ellipse = m[0]
        for i in range(5):
            ellipse = ellipse.reify()
        self.assertEqual(ellipse.stroke_width, 1.0)

        rect = m[1]
        for i in range(5):
            rect = rect.reify()
        self.assertEqual(rect.stroke_width, 1.0)

    def test_issue_99(self):
        """Test Issue of inverted circle reified location"""
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg
                            width="82.475mm"
                            height="35.215mm"
                            viewBox="24.766026 -242.607513 82.475082 35.214996"
                            version="1.1"
                        >
                        <circle
                            transform="scale(1,-1)"
                            style="opacity:0.99;fill:none;stroke:#ff0000;stroke-width:0.0264584;stroke-miterlimit:4;stroke-dasharray:none"
                            r="2"
                            cx="100.41245"
                            cy="211.59723"
                            id="circle2" /></svg>
        ''')
        m = SVG.parse(q, reify=False)
        q = copy(m[0])
        r = copy(m[0])
        self.assertEqual(q, r)
        q.reify()
        r = Path(r)
        q = Path(q)
        self.assertEqual(q, r)
        r.reify()
        q.reify()
        self.assertEqual(q, r)

    def test_issue_99b(self):
        """Test Issue of double inverted circle reified location"""
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg
                            width="82.475mm"
                            height="35.215mm"
                            viewBox="24.766026 -242.607513 82.475082 35.214996"
                            version="1.1"
                        >
                        <circle
                            transform="scale(-1,-1)"
                            style="opacity:0.99;fill:none;stroke:#ff0000;stroke-width:0.0264584;stroke-miterlimit:4;stroke-dasharray:none"
                            r="2"
                            cx="100.41245"
                            cy="211.59723"
                            id="circle2" /></svg>
        ''')
        m = SVG.parse(q, reify=False)
        q = copy(m[0])
        r = copy(m[0])
        self.assertEqual(q, r)
        q.reify()
        r = Path(r)
        q = Path(q)
        self.assertEqual(q, r)
        r.reify()
        q.reify()
        self.assertEqual(q, r)

    def test_issue_99c(self):
        """Test Issue of inverted rect reified location"""
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg
                            width="82.475mm"
                            height="35.215mm"
                            viewBox="24.766026 -242.607513 82.475082 35.214996"
                            version="1.1"
                        >
                        <rect
                            transform="scale(1,-1)"
                            style="opacity:0.99;fill:none;stroke:#ff0000;stroke-width:0.0264584;stroke-miterlimit:4;stroke-dasharray:none"
                            rx="2"
                            x="100.41245"
                            y="211.59723"
                            width="100"
                            height="100"
                            id="circle2" /></svg>
        ''')
        m = SVG.parse(q, reify=False)
        q = copy(m[0])
        r = copy(m[0])
        self.assertEqual(q, r)
        q.reify()
        r = Path(r)
        q = Path(q)
        self.assertEqual(q, r)
        r.reify()
        q.reify()
        self.assertEqual(q, r)

    def test_issue_99d(self):
        """Test Issue of double inverted rect reified location"""
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg
                            width="82.475mm"
                            height="35.215mm"
                            viewBox="24.766026 -242.607513 82.475082 35.214996"
                            version="1.1"
                        >
                        <rect
                            transform="scale(-1,-1)"
                            style="opacity:0.99;fill:none;stroke:#ff0000;stroke-width:0.0264584;stroke-miterlimit:4;stroke-dasharray:none"
                            rx="2"
                            x="100.41245"
                            y="211.59723"
                            width="100"
                            height="100"
                            id="circle2" /></svg>
        ''')
        m = SVG.parse(q, reify=False)
        q = copy(m[0])
        r = copy(m[0])
        self.assertEqual(q, r)
        q.reify()
        r = Path(r)
        q = Path(q)
        self.assertEqual(q, r)
        r.reify()
        q.reify()
        self.assertEqual(q, r)

    def test_issue_104(self):
        """Testing Issue 104 degenerate parsing"""
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg>
                        <polygon points=""/>
                        <polygon/>
                        <rect x="0" y="0" width="0" height="10"/>
                        <circle cx="0" cy="0" r="0"/>
                        </svg>''')
        m = SVG.parse(q)
        self.assertEqual(len(m), 0)

    def test_issue_172(self):
        """
        Polylines were checked whether the payload had a length of one and replaced them. However that was wrong
        as when the payload was *actually* 1 it made it a point and then did not produce the single point.
        """
        p = Polyline(0,0)
        q = Polyline(p)
        self.assertEqual(len(q), 1)

        p = Polygon(0, 0)
        q = Polygon(p)
        self.assertEqual(len(q), 1)

    def test_rect_strict(self):
        values = {
            'tag': 'rect',
            'rx': "-4",
            'x': "50",
            'y': "51",
            'width': "20",
            'height': "10"
        }
        e = Rect(values)
        e2 = Rect(50, 51, 20, 10)
        self.assertEqual(e, e2)

        e3 = Rect(values)
        e3._strict = False  # unstrict rx-negative rectangles, have scooped corners.
        self.assertNotEqual(e3, e2)

        values['ry'] = 4
        e4 = Rect(values)
        self.assertEqual(e, e4)

    def test_shape_npoints(self):
        import numpy as np
        shapes = [
            Rect(10, 20, 300, 340),
            Circle(10, 10, 5),
            Ellipse(50, 50, 30, 20),
            Polygon(points=((10, 10), (20, 30), (50, 20))),
            Polyline(points=((10, 10), (20, 30), (50, 20), (100, 120))),
        ]

        for shape in shapes:
            pos = np.linspace(0, 1, 1000)
            v1 = shape.npoint(pos)
            v2 = [shape.point(p) for p in pos]

            for p, p1, p2 in zip(pos, v1, v2):
                self.assertEqual(Point(p1), Point(p2))

    def test_shape_npoints_len0(self):
        """
        If the length of a shape is 0 the npoint code calls 0-length fallback which used an illegal round command
        """
        import numpy as np
        shapes = [
            Rect(0, 0, 0, 0),
            Circle(0, 0, 0),
            Ellipse(0, 0, 0, 0),
            Polygon(points=((0, 0), (0, 0), (0, 0))),
            Polyline(points=((0, 0), (0, 0), (0, 0), (0, 0))),
            Path("M0,0zM1,1z")
        ]

        for shape in shapes:
            pos = np.linspace(0, 1, 1000)
            v1 = shape.npoint(pos)
            if v1 is None:
                continue  # Degenerate shape had no segments
            v2 = [shape.point(p) for p in pos]

            for p, p1, p2 in zip(pos, v1, v2):
                self.assertEqual(Point(p1), Point(p2))

    def test_shape_npoints_points_issue_232(self):
        import numpy as np
        p = Path("M 4594.76424273,1787.94321633 C 4582.20211202,1787.86035528 4571.02257722,1787.8800841 4561.51723033,1788.01029433 C 4552.01148887,1788.14050456 4544.17164921,1788.39697926 4538.36624578,1788.75801672 C 4532.56044777,1789.12102706 4528.29783829,1789.91017998 4528.13803482,1789.96778814 C 4499.59674127,1800.20732345 4482.59365252,1807.33408452 4460.51078644,1822.22520278 C 4427.94718047,1844.1833827 4410.22517341,1855.51652611 4388.9239633,1876.84176593 C 4370.029275,1895.75784027 4345.39705043,1930.28225449 4336.63903135,1945.92081894 C 4328.01122251,1961.3264649 4304.48815236,2015.51609632 4294.15340576,2054.0867343 C 4287.16979702,2080.14929854 4284.79681419,2117.73112791 4281.09884363,2145.82220972 C 4279.62312767,2157.03133775 4279.82436166,2175.09268056 4280.27417883,2189.42961619 L 4289.87540779,2190.26611828 L 4288.916587,2201.39633102 L 4280.67901427,2200.68214763 C 4280.91576015,2206.22200111 4281.14066873,2210.21748233 4281.14066873,2210.21748233 L 4281.14066873,2210.4542282 L 4261.31122881,2937.51619918 L 4861.38942017,2992.84765596 L 4862.09176627,2532.61051811 L 4862.2890545,2532.61051811 L 4862.21013921,2529.7932422 C 4839.05994381,2460.37146008 4825.96039996,2381.42736429 4825.96039996,2297.62366484 C 4825.96039996,2280.80523787 4826.50491547,2264.18449371 4827.53476003,2247.79102559 L 4766.64924502,2242.54513157 L 4767.60412005,2231.44806325 L 4828.39059637,2236.6833037 C 4837.10876322,2123.48957674 4869.70590819,2021.87587968 4918.36586621,1944.8818202 C 4964.40228536,1872.03854724 5025.02659075,1821.03997401 5093.12575258,1803.84228015 C 5038.09614679,1801.52256515 4954.58680138,1798.09673397 4850.52988688,1794.49385632 C 4773.90550609,1791.84072421 4696.39174997,1789.49224459 4636.28670719,1788.46693766 C 4621.2604465,1788.21046297 4607.32006022,1788.02185542 4594.75792951,1787.93899436 L 4594.76424273,1787.94321633")
        space = np.linspace(0, 1, 101)
        points = p.npoint(space)
        for n in range(len(space)):
            npoint = points[n]
            point = p.point(space[n])

            self.assertAlmostEqual(npoint[0], point[0])
            self.assertAlmostEqual(npoint[1], point[1])


def reification_checks(test, shape):
    correct_reify(test, shape * "rotate(-90) translate(20,0)")
    correct_reify(test, shape * "rotate(12turn)")
    correct_reify(test, shape * "translate(20,0)")
    correct_reify(test, shape * "scale(2) translate(20,0)")
    correct_reify(test, shape * "rotate(90) scale(-1) translate(20,0)")
    correct_reify(test, shape * "rotate(90) translate(20,0)")
    correct_reify(test, shape * "skewX(10)")
    correct_reify(test, shape * "skewY(10)")


def correct_reify(test, shape):
    path = abs(Path(shape))
    reified = abs(copy(shape))
    test.assertEqual(path, shape)
    test.assertEqual(reified, shape)
    test.assertEqual(reified, path)
