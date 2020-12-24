from __future__ import print_function

import io
import unittest

from svgelements import *


class TestElementLength(unittest.TestCase):
    """Tests the functionality of the Length Element."""

    def test_length_parsing(self):
        self.assertAlmostEqual(Length('10cm'), (Length('100mm')))
        self.assertNotEqual(Length("1mm"), 0)
        self.assertNotEqual(Length("1cm"), 0)
        self.assertNotEqual(Length("1in"), 0)
        self.assertNotEqual(Length("1px"), 0)
        self.assertNotEqual(Length("1pc"), 0)
        self.assertNotEqual(Length("1pt"), 0)
        self.assertNotEqual(Length("1%").value(relative_length=100), 0)
        self.assertEqual(Length("50%").value(relative_length=100), 50.0)

    def test_distance_matrix(self):
        m = Matrix("Translate(20mm,50%)", ppi=1000, width=600, height=800)
        self.assertEqual(Matrix(1, 0, 0, 1, 787.402, 400), m)
        m = Matrix("Translate(20mm,50%)")
        m.render(ppi=1000, width=600, height=800)
        self.assertEqual(Matrix(1, 0, 0, 1, 787.402, 400), m)

    def test_rect_distance_percent(self):
        rect = Rect("0%", "0%", "100%", "100%")
        rect.render(relative_length="1mm", ppi=DEFAULT_PPI)
        self.assertEqual(rect, Path("M 0,0 H 3.7795296 V 3.7795296 H 0 z"))
        rect = Rect("0%", "0%", "100%", "100%")
        rect.render(relative_length="1in", ppi=DEFAULT_PPI)
        self.assertEqual(rect, Path("M 0,0 H 96 V 96 H 0 z"))

    def test_circle_distance_percent(self):
        shape = Circle(0, 0, "50%")
        shape.render(relative_length="1in", ppi=DEFAULT_PPI)
        print(shape.d())
        self.assertEqual(
            shape,
            Path('M48,0A48,48 0 0,1 0,48A48,48 0 0,1-48,0A48,48 0 0,1 0,-48A48,48 0 0,1 48,0Z')
        )

    def test_length_division(self):
        self.assertEqual(Length("1mm") // Length('1mm'), 1.0)
        self.assertEqual(Length("1mm") / Length('1mm'), 1.0)
        self.assertEqual(Length('1in') / '1in', 1.0)
        self.assertEqual(Length('1cm') / '1mm', 10.0)

    def test_length_compare(self):
        self.assertTrue(Length('1in') < Length('2.6cm'))
        self.assertTrue(Length('1in') < '2.6cm')
        self.assertFalse(Length('1in') < '2.5cm')
        self.assertTrue(Length('10mm') >= '1cm')
        self.assertTrue(Length('10mm') <= '1cm')
        self.assertTrue(Length('11mm') >= '1cm')
        self.assertTrue(Length('10mm') <= '1.1cm')
        self.assertFalse(Length('11mm') <= '1cm')
        self.assertFalse(Length('10mm') >= '1.1cm')
        self.assertTrue(Length('20%') > '10%')
        self.assertRaises(ValueError, lambda: Length('20%') > '1in')
        self.assertRaises(ValueError, lambda: Length('20px') > '1in')
        self.assertRaises(ValueError, lambda: Length('20pc') > '1in')
        self.assertRaises(ValueError, lambda: Length('20em') > '1in')
        self.assertEqual(max(Length('1in'), Length('2.5cm')), '1in')

    def test_length_parsed(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg>
                        <rect x="1in" y="1in" width="10in" height="10in"/>
                        </svg>''')
        m = SVG.parse(q, ppi=96.0)
        q = list(m.elements())
        self.assertEqual(q[1].x, 96.0)
        self.assertEqual(q[1].y, 96.0)
        self.assertEqual(q[1].width, 960)
        self.assertEqual(q[1].height, 960)

    def test_length_parsed_percent(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg>
                        <rect x="25%" y="25%" width="50%" height="50%"/>
                        </svg>''')
        m = SVG.parse(q, width=1000, height=1000)
        q = list(m.elements())
        self.assertEqual(q[1].x, 250)
        self.assertEqual(q[1].y, 250)
        self.assertEqual(q[1].width, 500)
        self.assertEqual(q[1].height, 500)

    def test_length_parsed_percent2(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>\n
                        <svg width="1in" height="1in">
                        <rect x="25%" y="25%" width="50%" height="50%"/>
                        </svg>''')
        m = SVG.parse(q, width=1000, height=1000)
        q = list(m.elements())
        self.assertEqual(q[1].x, 24)
        self.assertEqual(q[1].y, 24)
        self.assertEqual(q[1].width, 48)
        self.assertEqual(q[1].height, 48)

    def test_length_parsed_percent3(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg width="1in" height="1in">
                        <rect x="25%" y="25%" width="50%" height="50%"/>
                        </svg>''')
        m = SVG.parse(q, width=500, height=500)
        q = list(m.elements())
        self.assertEqual(q[1].x, 24)
        self.assertEqual(q[1].y, 24)
        self.assertEqual(q[1].width, 48)
        self.assertEqual(q[1].height, 48)

    def test_length_parsed_percent4(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg viewbox="0 0 960 960" width="1in" height="1in">
                        <rect x="25%" y="25%" width="50%" height="50%"/>
                        </svg>''')
        m = SVG.parse(q, width="garbage", height=500)
        q = list(m.elements())
        self.assertEqual(q[1].x, 24)
        self.assertEqual(q[1].y, 24)
        self.assertEqual(q[1].width, 48)
        self.assertEqual(q[1].height, 48)

    def test_length_parsed_percent5(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg viewbox="0 0 960 960">
                        <rect x="25%" y="25%" width="50%" height="50%"/>
                        <rect x="240" y="240" width="480" height="480"/>
                        </svg>''')
        m = SVG.parse(q, width="1in", height="1in")
        q = list(m.elements())
        self.assertEqual(q[1].x, 24)
        self.assertEqual(q[1].y, 24)
        self.assertEqual(q[1].width, 48)
        self.assertEqual(q[1].height, 48)
        self.assertEqual(q[2].x, 240)
        self.assertEqual(q[2].y, 240)
        self.assertEqual(q[2].width, 480)
        self.assertEqual(q[2].height, 480)

    def test_length_parsed_percent6(self):
        q = io.StringIO(u'''<svg version="1.1" baseProfile="basic" id="svg-root"
                        width="100%" height="100%" viewBox="0 0 480 360"
                        xmlns="http://www.w3.org/2000/svg">
                        <g transform="translate(5, 50) scale(4)">
                        <circle cx="7.5" cy="7.5" r="2.5" fill="black"/>
                        <circle cx="1.563%" cy="2.083%" r=".3535%" fill="fuchsia"/>
                        </g>
                        <g transform="translate(30, 260)  skewX(45) scale(4)">
                        <circle cx="0" cy="0" r="3.536" fill="black"/>
                        <circle cx="10" cy="0" r="3.536px" fill="fuchsia"/>
                        <circle cx="20" cy="0" r=".8334%" fill="green"/>
                        </g>
                        </svg>''')
        m = SVG.parse(q, width="10000", height="10000")
        q = list(m.elements())
        self.assertAlmostEqual(q[2].cx, q[3].cx, delta=1)
        self.assertAlmostEqual(q[2].cy, q[3].cy, delta=1)
        self.assertAlmostEqual(q[5].rx, q[6].rx, delta=1)
        self.assertAlmostEqual(q[6].rx, q[7].rx, delta=1)
