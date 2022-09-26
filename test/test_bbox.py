import unittest
import io

from svgelements import *


class TestElementBbox(unittest.TestCase):

    def test_bbox_rect(self):
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
        self.assertEqual(e.bbox(), (50,51,70,61))
        e *= "translate(2)"
        self.assertEqual(e.bbox(), (52, 51, 72, 61))

    def test_bbox_rect_stroke(self):
        values = {
            'tag': 'rect',
            'rx': "4",
            'ry': "2",
            'x': "50",
            'y': "51",
            'width': "20",
            'height': "10",
            'stroke-width': "5",
            'stroke': 'red',
        }
        e = Rect(values)
        self.assertEqual(e.bbox(), (50, 51, 70, 61))
        self.assertEqual(e.bbox(with_stroke=True), (
            50-(5./2.),
            51-(5./2.),
            70+(5./2.),
            61+(5./2.)
        ))
        e *= "translate(2)"
        self.assertEqual(e.bbox(), (52, 51, 72, 61))
        self.assertEqual(e.bbox(with_stroke=True), (
            52 - (5. / 2.),
            51 - (5. / 2.),
            72 + (5. / 2.),
            61 + (5. / 2.)
        ))
        e *= "scale(2)"
        self.assertEqual(e.bbox(), (52 * 2, 51 * 2, 72 * 2, 61 * 2))
        self.assertEqual(e.bbox(with_stroke=True), (
            52 * 2 - 5.,
            51 * 2 - 5.,
            72 * 2 + 5.,
            61 * 2 + 5.
        ))
        self.assertEqual(e.bbox(transformed=False), (50, 51, 70, 61))
        self.assertEqual(e.bbox(transformed=False, with_stroke=True), (
            50 - (5. / 2.),
            51 - (5. / 2.),
            70 + (5. / 2.),
            61 + (5. / 2.)
        ))

    def test_bbox_path(self):
        values = {
            'tag': 'rect',
            'rx': "4",
            'ry': "2",
            'x': "50",
            'y': "51",
            'width': "20",
            'height': "10"
        }
        e = Path(Rect(values))
        self.assertEqual(e.bbox(), (50,51,70,61))
        e *= "translate(2)"
        self.assertEqual(e.bbox(), (52, 51, 72, 61))

    def test_bbox_path_stroke(self):
        values = {
            'tag': 'rect',
            'rx': "4",
            'ry': "2",
            'x': "50",
            'y': "51",
            'width': "20",
            'height': "10",
            'stroke-width': "5",
            'stroke': 'red',
        }
        e = Path(Rect(values))
        self.assertEqual(e.bbox(), (50, 51, 70, 61))
        self.assertEqual(e.bbox(with_stroke=True), (
            50-(5./2.),
            51-(5./2.),
            70+(5./2.),
            61+(5./2.)
        ))
        e *= "translate(2)"
        self.assertEqual(e.bbox(), (52, 51, 72, 61))
        self.assertEqual(e.bbox(with_stroke=True), (
            52 - (5. / 2.),
            51 - (5. / 2.),
            72 + (5. / 2.),
            61 + (5. / 2.)
        ))
        e *= "scale(2)"
        self.assertEqual(e.bbox(), (52 * 2, 51 * 2, 72 * 2, 61 * 2))
        self.assertEqual(e.bbox(with_stroke=True), (
            52 * 2 - 5.,
            51 * 2 - 5.,
            72 * 2 + 5.,
            61 * 2 + 5.
        ))
        self.assertEqual(e.bbox(transformed=False), (50, 51, 70, 61))
        self.assertEqual(e.bbox(transformed=False, with_stroke=True), (
            50 - (5. / 2.),
            51 - (5. / 2.),
            70 + (5. / 2.),
            61 + (5. / 2.)
        ))

    def test_bbox_path_stroke_none(self):
        """
        Same as test_bbox_path_stroke but stroke is set to none, so the bbox should not change.
        """
        values = {
            'tag': 'rect',
            'rx': "4",
            'ry': "2",
            'x': "50",
            'y': "51",
            'width': "20",
            'height': "10",
            'stroke-width': "5",
            'stroke': "none",
        }
        e = Path(Rect(values))
        self.assertEqual(e.bbox(), (50, 51, 70, 61))
        self.assertEqual(e.bbox(with_stroke=True), (
            50,
            51,
            70,
            61
        ))
        e *= "translate(2)"
        self.assertEqual(e.bbox(), (52, 51, 72, 61))
        self.assertEqual(e.bbox(with_stroke=True), (
            52,
            51,
            72,
            61
        ))
        e *= "scale(2)"
        self.assertEqual(e.bbox(), (52 * 2, 51 * 2, 72 * 2, 61 * 2))
        self.assertEqual(e.bbox(with_stroke=True), (
            52 * 2,
            51 * 2,
            72 * 2,
            61 * 2
        ))
        self.assertEqual(e.bbox(transformed=False), (50, 51, 70, 61))
        self.assertEqual(e.bbox(transformed=False, with_stroke=True), (
            50,
            51,
            70,
            61
        ))

    def test_bbox_path_stroke_unset(self):
        """
        Same as test_bbox_path_stroke but the stroke is unset and thus shouldn't contribute to the bbox even if
        with_stroke is set.
        """
        values = {
            'tag': 'rect',
            'rx': "4",
            'ry': "2",
            'x': "50",
            'y': "51",
            'width': "20",
            'height': "10",
            'stroke-width': "5",
        }
        e = Path(Rect(values))
        self.assertEqual(e.bbox(), (50, 51, 70, 61))
        self.assertEqual(e.bbox(with_stroke=True), (
            50,
            51,
            70,
            61
        ))
        e *= "translate(2)"
        self.assertEqual(e.bbox(), (52, 51, 72, 61))
        self.assertEqual(e.bbox(with_stroke=True), (
            52,
            51,
            72,
            61
        ))
        e *= "scale(2)"
        self.assertEqual(e.bbox(), (52 * 2, 51 * 2, 72 * 2, 61 * 2))
        self.assertEqual(e.bbox(with_stroke=True), (
            52 * 2,
            51 * 2,
            72 * 2,
            61 * 2
        ))
        self.assertEqual(e.bbox(transformed=False), (50, 51, 70, 61))
        self.assertEqual(e.bbox(transformed=False, with_stroke=True), (
            50,
            51,
            70,
            61
        ))

    def test_bbox_subpath(self):
        p = Path("M 10,100 H 20 V 80 H 10 Z m 10,-90 H 60 V 70 H 20 Z")
        e = p.subpath(1)
        self.assertEqual(e.bbox(), (20, 10, 60, 70))
        e *= "translate(5)"
        self.assertEqual(e.bbox(), (25, 10, 65, 70))

    def test_bbox_move_subpath2(self):
        p = Path("M 0,0 Z m 100,100 h 20 v 20 h -20 Z")
        e = p.subpath(1)
        self.assertEqual(e.bbox(), (100, 100, 120, 120))

    def test_bbox_subpath_stroke(self):
        values = {
            'tag': 'rect',
            'rx': "4",
            'ry': "2",
            'x': "50",
            'y': "51",
            'width': "20",
            'height': "10",
            'stroke-width': "5",
            'stroke': 'red',
        }
        p = Path(Rect(values))
        e = p.subpath(0)
        self.assertEqual(e.bbox(), (50, 51, 70, 61))
        self.assertEqual(e.bbox(with_stroke=True), (
            50-(5./2.),
            51-(5./2.),
            70+(5./2.),
            61+(5./2.)
        ))
        p *= "translate(2)"
        self.assertEqual(e.bbox(), (52, 51, 72, 61))
        self.assertEqual(e.bbox(with_stroke=True), (
            52 - (5. / 2.),
            51 - (5. / 2.),
            72 + (5. / 2.),
            61 + (5. / 2.)
        ))
        p *= "scale(2)"
        self.assertEqual(e.bbox(), (52 * 2, 51 * 2, 72 * 2, 61 * 2))
        self.assertEqual(e.bbox(with_stroke=True), (
            52 * 2 - 5.,
            51 * 2 - 5.,
            72 * 2 + 5.,
            61 * 2 + 5.
        ))
        self.assertEqual(e.bbox(transformed=False), (50, 51, 70, 61))
        self.assertEqual(e.bbox(transformed=False, with_stroke=True), (
            50 - (5. / 2.),
            51 - (5. / 2.),
            70 + (5. / 2.),
            61 + (5. / 2.)
        ))

    def test_bbox_rotated_circle(self):
        # Rotation of circle must not affect it's bounding box
        c = Circle(cx=0, cy=0, r=1, transform="rotate(45)")
        (xmin, ymin, xmax, ymax) = c.bbox()
        self.assertAlmostEqual(-1, xmin)
        self.assertAlmostEqual(-1, ymin)
        self.assertAlmostEqual( 1, xmax)
        self.assertAlmostEqual( 1, ymax)

    def test_bbox_svg_with_rotated_circle(self):
        # Rotation of circle within group must not affect it's bounding box
        q = io.StringIO(
            u'''<?xml version="1.0" encoding="utf-8" ?>
            <svg>
              <circle cx="0" cy="0" r="1" transform="rotate(45)"/>
            </svg>
            '''
        )
        svg = SVG.parse(q)
        (xmin, ymin, xmax, ymax) = svg.bbox()
        self.assertAlmostEqual(-1, xmin)
        self.assertAlmostEqual(-1, ymin)
        self.assertAlmostEqual( 1, xmax)
        self.assertAlmostEqual( 1, ymax)

    def test_bbox_translated_circle(self):
        c = Circle(cx=0, cy=0, r=1, transform="translate(-1,-1)")
        (xmin, ymin, xmax, ymax) = c.bbox()
        self.assertAlmostEqual(-2, xmin)
        self.assertAlmostEqual(-2, ymin)
        self.assertAlmostEqual( 0, xmax)
        self.assertAlmostEqual( 0, ymax)

    def test_bbox_svg_with_translated_group_with_circle(self):
        # Translation of nested group must be applied correctly
        q = io.StringIO(
            u'''<?xml version="1.0" encoding="utf-8" ?>
            <svg>
              <g transform="translate(-1,-1)">
                <circle cx="0" cy="0" r="1"/>
              </g>
            </svg>
            '''
        )
        svg = SVG.parse(q)
        (xmin, ymin, xmax, ymax) = svg.bbox()
        self.assertAlmostEqual(-2, xmin)
        self.assertAlmostEqual(-2, ymin)
        self.assertAlmostEqual( 0, xmax)
        self.assertAlmostEqual( 0, ymax)


    def test_issue_104(self):
        """Testing Issue 104 rotated bbox"""
        rect = Rect(10,10,10,10)
        rect *= "rotate(45deg)"
        self.assertEqual(rect.bbox(), abs(rect).bbox())

        circ = Circle(5,5,10)
        circ *= "rotate(45deg)"
        self.assertEqual(circ.bbox(), abs(circ).bbox())

        path = Path("M0 0 100,100")
        path *= "rotate(45deg)"
        self.assertEqual(path.bbox(), abs(path).bbox())

        path = Path("M0 0q100,100 200,200z")
        path *= "rotate(45deg)"
        self.assertEqual(path.bbox(), abs(path).bbox())

        path = Path("M0 20c0,128 94,94 200,200z")
        path *= "rotate(45deg)"
        self.assertEqual(path.bbox(), abs(path).bbox())

        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg>
                        <path d="M0 36c0 128.082 96 214 251 214c153.639 0 293 -37 293 -264c0 -220 -158.05 -325.976 -254 -391c-121 -82 -200.248 -117.634 -339 -171c-5.93907 -2.28437 -11.3166 -3.27496 -15.9795 -3.27496c-11.9348 0 -19.1871 6.48977 -19.1871 14.3854 c0 7.04844 5.77949 15.2172 19.1666 20.8896c118 50 225 86 316 200c91 113 125 205.913 125 350c0 135 -33 224 -145 224c-46.615 0 -77.452 -12.593 -112 -44c-8.09234 -7.35667 -11.3121 -13.0296 -11.3121 -17.4022c0 -13.4585 30.5027 -14.5978 43.3121 -14.5978 c69 0 123 -64.8867 123 -136c0 -75 -48 -132 -139 -132c-79.1582 0 -135 74 -135 150zM572 128c0 35 29 64 64 64s63 -29 63 -64s-28 -63 -63 -63s-64 28 -64 63zM572 -131c0 35 29 64 64 64s63 -29 63 -64s-28 -63 -63 -63s-64 28 -64 63z" transform="rotate(45deg)"/>
                        </svg>''')
        m = SVG.parse(q, reify=False)
        p0 = m[0]
        p1 = abs(p0)
        self.assertEqual(p0, p1)
        self.assertEqual(p0.bbox(), p1.bbox())
