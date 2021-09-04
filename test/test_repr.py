import io
import unittest

from svgelements import *


class TestElementsRepr(unittest.TestCase):
    """Tests the functionality of the repr for elements."""

    def test_repr_length(self):
        obj = Length("10cm")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_color(self):
        obj = Color("red")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_point(self):
        obj = Point("20.3,3.1615926535")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_angle(self):
        obj = Angle.parse("1.1turn")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertAlmostEqual(obj, obj2)

    def test_repr_matrix(self):
        obj = Matrix("rotate(20)")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_viewbox(self):
        obj = Viewbox("0 0 100 60")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_move(self):
        obj = Move(0.1, 50)
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_close(self):
        obj = Close(0.1, 50)
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_line(self):
        obj = Line(start=(0.2, 0.99), end=(0.1, 22.9996))
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

        obj = Line(end=(0.1, 22.9996))
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_qbez(self):
        obj = QuadraticBezier(start=(0.2, 0.99), control=(-3,-3), end=(0.1, 22.9996))
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_cbez(self):
        obj = CubicBezier(start=(0.2, 0.99), control1=(-3, -3), control2=(-4, -4), end=(0.1, 22.9996))
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_arc(self):
        obj = Arc(start=(0,0), end=(0,100), control=(50,50))
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_path(self):
        obj = Path("M0,0Z")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

        obj = Path("M0,0L100,100Z")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

        obj = Path("M0,0L100,100Z", transform="scale(4)")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_rect(self):
        obj = Rect(x=100, y=100, width=500, height=500)
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

        obj = Rect(x=100, y=100, width=500, height=500, transform="scale(2)", stroke="red", fill="blue")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_ellipse(self):
        obj = Ellipse(cx=100, cy=100, rx=500, ry=500)
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

        obj = Ellipse(cx=100, cy=100, rx=500, ry=500, transform="scale(2)", stroke="red", fill="blue")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_circle(self):
        obj = Circle(cx=100, cy=100, r=500)
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

        obj = Circle(cx=100, cy=100, r=500, transform="scale(2)", stroke="red", fill="blue")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_simpleline(self):
        obj = SimpleLine(start=(0,0), end=(100,100))
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

        obj = SimpleLine(start=(0, 0), end=(100, 100), transform="scale(2)", stroke="red", fill="blue")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_polyline(self):
        obj = Polyline("0,0 7,7 10,10 0 20")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

        obj = Polyline("0,0 7,7 10,10 0 20", transform="scale(2)", stroke="red", fill="blue")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_polygon(self):
        obj = Polygon("0,0 7,7 10,10 0 20")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

        obj = Polygon("0,0 7,7 10,10 0 20", transform="scale(2)", stroke="red", fill="blue")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_group(self):
        obj = Group()
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

        obj = Group(transform="scale(2)", stroke="red", fill="blue")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_clippath(self):
        obj = ClipPath()
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_pattern(self):
        obj = Pattern()
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_text(self):
        obj = SVGText(x=0, y=0, text="Hello")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

        obj = SVGText(x=0, y=0, text="Hello", transform="scale(2)", stroke="red", fill="blue")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_image(self):
        obj = SVGImage(href="test.png", transform="scale(2)")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_desc(self):
        obj = Desc("Describes Object")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

    def test_repr_title(self):
        obj = Title(title="SVG Description")
        repr_obj = repr(obj)
        obj2 = eval(repr_obj)
        self.assertTrue(obj == obj2)
        self.assertFalse(obj != obj2)

