import io
import unittest

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
        svg.write_xml("myfile.svg")

    def test_write_group(self):
        g = Group()
        self.assertEquals(g.string_xml(), "<g />")

