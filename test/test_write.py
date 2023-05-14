import io
import os
import pathlib
import unittest
from xml.etree.ElementTree import ParseError

from svgelements import *


class TestElementWrite(unittest.TestCase):

    def test_write(self):
        q = io.StringIO(
            u'''
            <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="360pt" height="360pt" viewBox="0 0 360 360" version="1.1">'
            <g id="mygroup">
            <path style="fill:none;stroke-width:0.004;stroke-linecap:butt;stroke-linejoin:miter;stroke:rgb(0%,0%,0%);stroke-opacity:1;stroke-miterlimit:10;" d="M 0.00199653 0 L 0.00199653 1 M 0.0220052 0 L 0.0220052 1 M 0.042003 0 L 0.042003 1 M 0.0620009 0 L 0.0620009 1 M 0.0819987 0 L 0.0819987 1 M 0.101997 0 L 0.101997 1 M 0.122005 0 L 0.122005 1 M 0.142003 0 L 0.142003 1 M 0.162001 0 L 0.162001 1 M 0.181999 0 L 0.181999 1 M 0.201997 0 L 0.201997 1 M 0.222005 0 L 0.222005 1 M 0.242003 0 L 0.242003 1 M 0.262001 0 L 0.262001 1 M 0.281999 0 L 0.281999 1 M 0.301997 0 L 0.301997 1 M 0.322005 0 L 0.322005 1 M 0.342003 0 L 0.342003 1 M 0.362001 0 L 0.362001 1 M 0.381999 0 L 0.381999 1 M 0.401997 0 L 0.401997 1 M 0.422005 0 L 0.422005 1 M 0.442003 0 L 0.442003 1 M 0.462001 0 L 0.462001 1 M 0.481999 0 L 0.481999 1 M 0.501997 0 L 0.501997 1 M 0.522005 0 L 0.522005 1 M 0.542003 0 L 0.542003 1 M 0.562001 0 L 0.562001 1 M 0.581999 0 L 0.581999 1 M 0.601997 0 L 0.601997 1 M 0.622005 0 L 0.622005 1 M 0.642003 0 L 0.642003 1 M 0.662001 0 L 0.662001 1 M 0.681999 0 L 0.681999 1 M 0.701997 0 L 0.701997 1 M 0.722005 0 L 0.722005 1 M 0.742003 0 L 0.742003 1 M 0.762001 0 L 0.762001 1 M 0.781999 0 L 0.781999 1 M 0.801997 0 L 0.801997 1 M 0.822005 0 L 0.822005 1 M 0.842003 0 L 0.842003 1 M 0.862001 0 L 0.862001 1 M 0.881999 0 L 0.881999 1 M 0.901997 0 L 0.901997 1 M 0.922005 0 L 0.922005 1 M 0.942003 0 L 0.942003 1 M 0.962001 0 L 0.962001 1 M 0.981999 0 L 0.981999 1 " transform="matrix(360,0,0,360,0,0)"/>
            </g>
            </svg>
            ''')
        svg = SVG.parse(q, reify=False)
        print(svg.string_xml())
        # svg.write_xml("myfile.svg")

    def test_write_group(self):
        g = Group()
        self.assertEquals(g.string_xml(), "<g />")

    def test_write_rect(self):
        r = Rect("1in", "1in", "3in", "3in", rx="5%")
        self.assertIn(
            r.string_xml(),
            (
                '<rect rx="0.15in" x="1in" y="1in" ry="0.15in" width="3in" height="3in" />',
                '<rect height="3in" rx="0.15in" ry="0.15in" width="3in" x="1in" y="1in" />',
            ),
        )
        r *= "scale(3)"
        self.assertIn(
            r.string_xml(),
            (
                '<rect rx="0.15in" x="1in" y="1in" ry="0.15in" width="3in" height="3in" transform="matrix(3.000000, 0.000000, 0.000000, 3.000000, 0.000000, 0.000000)" />',
                '<rect height="3in" rx="0.15in" ry="0.15in" transform="matrix(3.000000, 0.000000, 0.000000, 3.000000, 0.000000, 0.000000)" width="3in" x="1in" y="1in" />',
            ),
        )
        r.reify()
        self.assertIn(
            r.string_xml(),
            (
                '<rect rx="0.45in" x="3in" y="3in" ry="0.45in" width="9in" height="9in" />',
                '<rect height="9in" rx="0.45in" ry="0.45in" width="9in" x="3in" y="3in" />',
            ),
        )
        r = Path(r)
        self.assertIn(
            r.string_xml(),
            (
                '<path rx="5%" d="M 3.45,3 L 11.55,3 A 0.45,0.45 0 0,1 12,3.45 L 12,11.55 A 0.45,0.45 0 0,1 11.55,12 L 3.45,12 A 0.45,0.45 0 0,1 3,11.55 L 3,3.45 A 0.45,0.45 0 0,1 3.45,3 Z" />',
                '<path d="M 3.45,3 L 11.55,3 A 0.45,0.45 0 0,1 12,3.45 L 12,11.55 A 0.45,0.45 0 0,1 11.55,12 L 3.45,12 A 0.45,0.45 0 0,1 3,11.55 L 3,3.45 A 0.45,0.45 0 0,1 3.45,3 Z" rx="5%" />',
            ),
        )

    def test_write_path(self):
        r = Path("M0,0zzzz")
        r *= "translate(5,5)"
        self.assertEqual(
            r.string_xml(),
            '<path d="M 0,0 z z z z" transform="matrix(1.000000, 0.000000, 0.000000, 1.000000, 5.000000, 5.000000)" />',
        )
        r.reify()
        self.assertEqual(r.string_xml(), '<path d="M 5,5 z z z z" />')

    def test_write_circle(self):
        c = Circle(r=5, stroke="none", fill="yellow")
        q = SVG.parse(io.StringIO(c.string_xml()))
        self.assertEqual(c, q)

    def test_write_ellipse(self):
        c = Ellipse(rx=3, ry=2, fill="cornflower blue")
        q = SVG.parse(io.StringIO(c.string_xml()))
        self.assertEqual(c, q)

    def test_write_line(self):
        c = SimpleLine(x1=0, x2=10, y1=5, y2=6, id="line", fill="light grey")
        q = SVG.parse(io.StringIO(c.string_xml()))
        self.assertEqual(c, q)

    def test_write_pathlib_issue_227(self):
        """
        Tests pathlib.Path file saving. This is permitted by the xml writer but would crash see issue #227

        This also provides an example of pretty-print off and short_empty_elements off (an xml writer option).

        """
        file1 = "myfile.svg"
        self.addCleanup(os.remove, file1)
        file = pathlib.Path(file1)
        svg = SVG(viewport="0 0 1000 1000", height="10mm", width="10mm")
        svg.append(Rect("10%", "10%", "80%", "80%", fill="red"))
        svg.write_xml(file, pretty=False, short_empty_elements=False)

    def test_write_filename(self):
        """
        Tests filename file saving. This is permitted by the xml writer but would crash see issue #227

        This also provides an example short_empty_elements off, utf-8 encoding.

        """
        file1 = "myfile-f.svg"
        self.addCleanup(os.remove, file1)
        svg = SVG(viewport="0 0 1000 1000", height="10mm", width="10mm")
        svg.append(Rect("10%", "10%", "80%", "80%", fill="red"))
        svg.write_xml(file1, short_empty_elements=False, encoding="utf-8")

    def test_write_filename_svgz(self):
        """
        Tests pathlib.Path file saving. This is permitted by the xml writer but would crash see issue #227

        This also provides an example of xml_declaration=True.

        """
        file1 = "myfile-f.svgz"
        self.addCleanup(os.remove, file1)
        svg = SVG(viewport="0 0 1000 1000", height="10mm", width="10mm")
        svg.append(Rect("10%", "10%", "80%", "80%", fill="red"))
        svg.write_xml(file1, xml_declaration=True)


    # def test_read_write(self):
    #     import glob
    #     for g in glob.glob("*.svg"):
    #         if g.startswith("test-"):
    #             continue
    #         print(g)
    #         try:
    #             svg = SVG.parse(g, transform="translate(1,1)")
    #         except ParseError:
    #             print(f"{g} could not be parsed.")
    #             continue
    #         except ValueError:
    #             continue
    #         svg.write_xml(f"test-{g}.")
