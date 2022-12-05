
import unittest
import io

from svgelements import *


class TestElementColor(unittest.TestCase):
    """These tests test the basic functions of the Color element."""

    def test_color_red(self):
        reference = Color('red')
        self.assertEqual(reference, 'red')
        self.assertEqual(reference, Color('#F00'))
        self.assertEqual(reference, Color('#FF0000'))
        self.assertEqual(reference, Color("rgb(255, 0, 0)"))
        self.assertEqual(reference, Color("rgb(100%, 0%, 0%)"))
        self.assertEqual(reference, Color("rgb(300, 0, 0)"))
        self.assertEqual(reference, Color("rgb(255, -10, 0)"))
        self.assertEqual(reference, Color("rgb(110%, 0%, 0%)"))
        self.assertEqual(reference, Color("rgba(255, 0, 0, 1)"))
        self.assertEqual(reference, Color("rgba(100%, 0%, 0%, 1)"))
        self.assertEqual(reference, Color("hsl(0, 100%, 50%)"))
        self.assertEqual(reference, Color("hsla(0, 100%, 50%, 1.0)"))
        self.assertEqual(reference, Color(0xFF0000))
        color = Color()
        color.rgb = 0xFF0000
        self.assertEqual(reference, color)
        self.assertEqual(reference, Color(rgb=0xFF0000))
        self.assertEqual(reference, Color(bgr=0x0000FF))
        self.assertEqual(reference, Color(argb=0xFFFF0000))
        self.assertEqual(reference, Color(rgba=0xFF0000FF))
        self.assertEqual(reference, Color(0xFF0000, 1.0))

    def test_color_green(self):
        reference = Color('lime')  # Lime is 255 green, green is 128 green.
        self.assertEqual(reference, 'lime')
        self.assertEqual(reference, Color('#0F0'))
        self.assertEqual(reference, Color('#00FF00'))
        self.assertEqual(reference, Color("rgb(0, 255, 0)"))
        self.assertEqual(reference, Color("rgb(0%, 100%, 0%)"))
        self.assertEqual(reference, Color("rgb(0, 300, 0)"))
        self.assertEqual(reference, Color("rgb(-10, 255, 0)"))
        self.assertEqual(reference, Color("rgb(0%, 110%, 0%)"))
        self.assertEqual(reference, Color("rgba(0, 255, 0, 1)"))
        self.assertEqual(reference, Color("rgba(0%, 100%, 0%, 1)"))
        self.assertEqual(reference, Color("hsl(120, 100%, 50%)"))
        self.assertEqual(reference, Color("hsla(120, 100%, 50%, 1.0)"))
        self.assertEqual(reference, Color(0x00FF00))
        color = Color()
        color.rgb = 0x00FF00
        self.assertEqual(reference, color)
        self.assertEqual(reference, Color(rgb=0x00FF00))
        self.assertEqual(reference, Color(bgr=0x00FF00))
        self.assertEqual(reference, Color(argb=0xFF00FF00))
        self.assertEqual(reference, Color(rgba=0x00FF00FF))
        self.assertEqual(reference, Color(0x00FF00, 1.0))

    def test_color_blue(self):
        reference = Color('blue')
        self.assertEqual(reference, 'blue')
        self.assertEqual(reference, Color('#00F'))
        self.assertEqual(reference, Color('#0000FF'))
        self.assertEqual(reference, Color("rgb(0, 0, 255)"))
        self.assertEqual(reference, Color("rgb(0%, 0%, 100%)"))
        self.assertEqual(reference, Color("rgb(0, 0, 300)"))
        self.assertEqual(reference, Color("rgb(0, -10, 255)"))
        self.assertEqual(reference, Color("rgb(0%, 0%, 110%)"))
        self.assertEqual(reference, Color("rgba(0, 0, 255, 1)"))
        self.assertEqual(reference, Color("rgb(0%, 0%, 100%)"))
        self.assertEqual(reference, Color("rgba(0%, 0%, 100%, 1)"))
        self.assertEqual(reference, Color("hsl(240, 100%, 50%)"))
        self.assertEqual(reference, Color("hsla(240, 100%, 50%, 1.0)"))
        self.assertEqual(reference, Color(0x0000FF))
        color = Color()
        color.rgb = 0x0000FF
        self.assertEqual(reference, color)
        self.assertEqual(reference, Color(rgb=0x0000FF))
        self.assertEqual(reference, Color(bgr=0xFF0000))
        self.assertEqual(reference, Color(argb=0xFF0000FF))
        self.assertEqual(reference, Color(rgba=0x0000FFFF))
        self.assertEqual(reference, Color(0x0000FF, 1.0))

    def test_color_bgr(self):
        reference = Color("#26A")
        self.assertEqual(reference, Color(bgr=0xAA6622))
        reference.bgr = 0x2468AC
        self.assertEqual(reference, Color(rgb=0xAC6824))
        self.assertEqual(reference.alpha, 0xFF)

    def test_color_red_half(self):
        half_ref = Color("rgba(100%, 0%, 0%, 0.5)")
        self.assertNotEqual(half_ref, 'red')

        color = Color('red', opacity=0.5)
        self.assertEqual(color, half_ref)

    def test_color_transparent(self):
        t0 = Color('transparent')
        t1 = Color('rgba(0,0,0,0)')
        self.assertEqual(t0, t1)
        self.assertNotEqual(t0, "black")

    def test_color_hsl(self):
        c0 = Color("hsl(0, 100%, 50%)")  # red
        self.assertAlmostEqual(c0.hue, 0)
        self.assertAlmostEqual(c0.saturation, 1, places=2)
        self.assertAlmostEqual(c0.lightness, 0.5, places=2)
        self.assertEqual(c0, "red")
        c1 = Color("hsl(120, 100%, 50%)")  # lime
        self.assertAlmostEqual(c1.hue, 120)
        self.assertAlmostEqual(c1.saturation, 1, places=2)
        self.assertAlmostEqual(c1.lightness, 0.5, places=2)
        self.assertEqual(c1, "lime")
        c2 = Color("hsl(120, 100%, 19.62%)")  # dark green
        self.assertAlmostEqual(c2.hue, 120)
        self.assertAlmostEqual(c2.saturation, 1, places=2)
        self.assertAlmostEqual(c2.lightness, 0.1962, places=2)
        self.assertEqual(c2, "dark green")
        c3 = Color("hsl(120, 73.4%, 75%)")  # light green
        self.assertAlmostEqual(c3.hue, 120)
        self.assertAlmostEqual(c3.saturation, 0.734, places=2)
        self.assertAlmostEqual(c3.lightness, 0.75, places=2)
        self.assertEqual(c3, "light green")
        c4 = Color("hsl(120, 60%, 66.67%)")  # pastel green
        self.assertAlmostEqual(c4.hue, 120)
        self.assertAlmostEqual(c4.saturation, 0.6, places=2)
        self.assertAlmostEqual(c4.lightness, 0.6667, places=2)
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

    def test_color_hexa(self):
        for r in range(0,255,17):
            for g in range(0, 255, 17):
                for b in range(0, 255, 17):
                    for a in range(0, 255, 17):
                        c = Color()
                        c.red = r
                        c.green = g
                        c.blue = b
                        c.alpha = a
                        hexa = c.hexa
                        c2 = Color(hexa)
                        self.assertEqual(c,c2)

    def test_color_hex(self):
        for r in range(0,255,17):
            for g in range(0, 255, 17):
                for b in range(0, 255, 17):
                    c = Color()
                    c.red = r
                    c.green = g
                    c.blue = b
                    c.alpha = 255
                    hex = c.hex
                    c2 = Color(hex)
                    self.assertEqual(c,c2)

    def test_color_components(self):
        color = Color("#E9967A80")
        color2 = Color("darksalmon", .5)
        self.assertEqual(color, color2)
        self.assertEqual(color.red, 0xE9)
        self.assertEqual(color.green, 0x96)
        self.assertEqual(color.blue, 0x7A)
        self.assertEqual(color.alpha, 0x80)
        self.assertAlmostEqual(color.opacity, 0.50196078)
        self.assertEqual(color.hex, "#e9967a80")
        self.assertAlmostEqual(color.blackness, 0.0862745098)

        color.red = 0
        self.assertEqual(color.red, 0x0)
        color.green = 0
        self.assertEqual(color.green, 0x0)
        color.blue = 0
        self.assertEqual(color.blue, 0x0)
        color.alpha = 0
        self.assertEqual(color.alpha, 0x0)
        color.opacity = 1
        self.assertEqual(color.alpha, 0xFF)

        color.lightness = .5
        self.assertEqual(color.red, 0x7F)
        self.assertEqual(color.green, 0x7F)
        self.assertEqual(color.blue, 0x7F)
        self.assertEqual(color.alpha, 0xFF)

    def test_color_distinct(self):
        c0 = Color.distinct(0)
        self.assertEqual(c0, "white")
        c1 = Color.distinct(1)
        self.assertEqual(c1, "black")
        c2 = Color.distinct(2)
        self.assertEqual(c2, "red")
        c3 = Color.distinct(3)
        self.assertEqual(c3, "lime")
        c4 = Color.distinct(4)
        self.assertEqual(c4, "blue")
        c5 = Color.distinct(5)
        self.assertEqual(c5, "yellow")
        c6 = Color.distinct(6)
        self.assertEqual(c6, "cyan")
        c7 = Color.distinct(7)
        self.assertEqual(c7, "magenta")
        c8 = Color.distinct(6767890)
        self.assertEqual(c8, "#d85c3d")
