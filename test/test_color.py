from __future__ import print_function

import unittest

from svgelements import *


class TestElementColor(unittest.TestCase):

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
