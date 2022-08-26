import unittest
import io

from svgelements import *


class TestSVGCSS(unittest.TestCase):

    def test_issue_103(self):
        """Testing Issue 103 css class parsing
        This test is based on an Illustrator file, where the styling relies more on CSS.
        """

        q = io.StringIO(u'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80">
        <defs>
        <style>.cls-1,.cls-2{fill:none;stroke-miterlimit:10;}.cls-1{stroke:blue;}.cls-2{stroke:red;}</style>
        </defs>
        <g id="Layer_2" data-name="Layer 2">
        <g id="Layer_1-2" data-name="Layer 1">
        <polygon points="56.59 67.4 39.86 57.28 23.01 67.22 26.34 45.99 12.83 30.88 31.62 27.88 40.12 8.6 48.41 27.97 67.17 31.17 53.5 46.14 56.59 67.4"/>
        <circle class="cls-1" cx="40" cy="40" r="35"/>
        <circle class="cls-2" cx="40" cy="40" r="39.5"/>
        </g>
        </g>
        </svg>''')
        m = SVG.parse(q)
        poly = m[0][0][0]
        circ1 = m[0][0][1]
        circ2 = m[0][0][2]

        self.assertEqual(poly.fill, "black")
        self.assertEqual(poly.stroke, "none")

        self.assertEqual(circ1.fill, "none")
        self.assertEqual(circ1.stroke, "blue")

        self.assertEqual(circ2.fill, "none")
        self.assertEqual(circ2.stroke, "red")

    def test_issue_178(self):
        """Testing Issue 178 css comment parsing
        """

        q = io.StringIO(u'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80">
        <defs>
        <style>
        //this is a comment.
        .cls-1,.cls-2{fill:none;stroke-miterlimit:10;}.cls-1{stroke:blue;}.cls-2{stroke:red;}
        //.cls-2{stroke:pink;}
        /* Testing this should be functional */
        </style>
        </defs>
        <g id="Layer_2" data-name="Layer 2">
        <g id="Layer_1-2" data-name="Layer 1">
        <polygon points="56.59 67.4 39.86 57.28 23.01 67.22 26.34 45.99 12.83 30.88 31.62 27.88 40.12 8.6 48.41 27.97 67.17 31.17 53.5 46.14 56.59 67.4"/>
        <circle class="cls-1" cx="40" cy="40" r="35"/>
        <circle class="cls-2" cx="40" cy="40" r="39.5"/>
        </g>
        </g>
        </svg>''')
        m = SVG.parse(q)
        poly = m[0][0][0]
        circ1 = m[0][0][1]
        circ2 = m[0][0][2]

        self.assertEqual(poly.fill, "black")
        self.assertEqual(poly.stroke, "none")

        self.assertEqual(circ1.fill, "none")
        self.assertEqual(circ1.stroke, "blue")

        self.assertEqual(circ2.fill, "none")
        self.assertEqual(circ2.stroke, "red")


    def test_issue_174b(self):
        """
        aliflux-omo noted a crash parsing https://upload.wikimedia.org/wikipedia/commons/5/58/Axis_Occupation_of_Europe_%281942%29.svg
        Which contained a pointless blank style comment.
        """

        q = io.StringIO(u'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 80">
        <style/>
        </svg>''')
        SVG.parse(q)
