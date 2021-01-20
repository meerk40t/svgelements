from __future__ import print_function

import unittest
import io

from svgelements import *


class TestElementColor(unittest.TestCase):
    """These tests test the basic functions of the Color element."""

    def test_color_red(self):
        r0 = Color('red')
        self.assertEqual(r0, 'red')
        r1 = Color('#F00')
        self.assertEqual(r0, r1)
        r2 = Color('#FF0000')
        self.assertEqual(r0, r2)
        r3 = Color("rgb(255, 0, 0)")
        self.assertEqual(r0, r3)
        r4 = Color("rgb(100%, 0%, 0%)")
        self.assertEqual(r0, r4)
        r5 = Color("rgb(300, 0, 0)")
        self.assertEqual(r0, r5)
        r6 = Color("rgb(255, -10, 0)")
        self.assertEqual(r0, r6)
        r7 = Color("rgb(110%, 0%, 0%)")
        self.assertEqual(r0, r7)
        r8 = Color("rgba(255, 0, 0, 1)")
        self.assertEqual(r0, r8)
        r9 = Color("rgb(100%, 0%, 0%)")
        self.assertEqual(r0, r9)
        ra = Color("rgba(100%, 0%, 0%, 1)")
        self.assertEqual(r0, ra)
        rb = Color("hsl(0, 100%, 50%)")
        self.assertEqual(r0, rb)
        rc = Color("hsla(0, 100%, 50%, 1.0)")
        self.assertEqual(r0, rc)

        half_red = Color("rgba(100%, 0%, 0%, 0.5)")
        self.assertNotEqual(r0, half_red)

    def test_color_transparent(self):
        t0 = Color('transparent')
        t1 = Color('rgba(0,0,0,0)')
        self.assertEqual(t0, t1)
        self.assertNotEqual(t0, "black")

    def test_color_hsl(self):
        c0 = Color("hsl(0, 100%, 50%)")  # red
        self.assertEqual(c0, "red")
        c1 = Color("hsl(120, 100%, 50%)")  # lime
        self.assertEqual(c1, "lime")
        c2 = Color("hsl(120, 100%, 19.62%)")  # dark green
        self.assertEqual(c2, "dark green")
        c3 = Color("hsl(120, 73.4%, 75%)")  # light green
        self.assertEqual(c3, "light green")
        c4 = Color("hsl(120, 60%, 66.67%)")  # pastel green
        self.assertEqual(c4, "#77dd77")

    def test_color_hsla(self):
        c0 = Color.parse("hsl(120, 100%, 50%)")
        c1 = Color.parse("hsla(120, 100%, 50%, 1)")
        self.assertEqual(c0, c1)
        self.assertNotEqual(c0, "black")
        t1 = Color.parse("hsla(240, 100%, 50%, 0.5)")  # semi - transparent solid blue
        t2 = Color.parse("hsla(30, 100%, 50%, 0.1)")  # very transparent solid orange
        self.assertNotEqual(t1,t2)

    def test_parse_fill_opacity(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>\n
                        <svg>
                        <rect fill-opacity="0.5" x="0" y="0" width="100" height="100"/>
                        </svg>'''
                        )
        m = list(SVG.parse(q).elements())
        r = m[1]
        self.assertAlmostEqual(r.fill.opacity, 0.5, delta=1.0/255.0)

    def test_parse_stroke_opacity(self):
        q = io.StringIO(u'''<?xml version="1.0" encoding="utf-8" ?>
                        <svg>
                        <rect stroke-opacity="0.2" stroke="red" x="0" y="0" width="100" height="100"/>
                        </svg>
                        ''')
        m = list(SVG.parse(q).elements())
        r = m[1]
        self.assertAlmostEqual(r.stroke.opacity, 0.2, delta=1.0/255.0)

    def test_color_none(self):
        color = Color(None)
        self.assertEqual(color, SVG_VALUE_NONE)
        self.assertEqual(color.red, None)
        self.assertEqual(color.green, None)
        self.assertEqual(color.blue, None)
        self.assertEqual(color.alpha, None)
        self.assertEqual(color.opacity, None)
        self.assertEqual(color.hexa, None)
        self.assertEqual(color.hex, None)
        self.assertEqual(color.blackness, None)
        self.assertEqual(color.brightness, None)
        self.assertEqual(color.hsl, None)
        self.assertEqual(color.hue, None)
        self.assertEqual(color.saturation, None)
        self.assertEqual(color.lightness, None)
        self.assertEqual(color.luma, None)
        self.assertEqual(color.luminance, None)
        self.assertEqual(color.intensity, None)

        def set_red():
            color.red = 0
        self.assertRaises(ValueError, set_red)

        def set_green():
            color.green = 0
        self.assertRaises(ValueError, set_green)

        def set_blue():
            color.blue = 0
        self.assertRaises(ValueError, set_blue)

        def set_alpha():
            color.alpha = 0
        self.assertRaises(ValueError, set_alpha)

        def set_opacity():
            color.opacity = 1
        self.assertRaises(ValueError, set_opacity)